"""
TruthLens — Case Chat API (AI Interrogator).

Officers can ask natural language questions about any case.
Answers are powered by CRAG + Ollama llama3.1:8b with full case context.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.db.models.case import Case
from app.db.models.analysis import AnalysisResult

router = APIRouter()

# Pull analysis state from the orchestration module's in-memory store
def _get_analysis_state(case_id: str) -> dict:
    try:
        from app.api.v1.orchestration import _analysis_results
        return _analysis_results.get(case_id, {})
    except Exception:
        return {}


async def _build_case_context(case_id: str, db: AsyncSession) -> dict:
    """Build a rich context dict from DB + in-memory analysis state."""
    context = _get_analysis_state(case_id)

    # Supplement with DB data if not in memory
    case = await db.get(Case, case_id)
    if case:
        context["case_info"] = {
            "case_number": case.case_number,
            "applicant_name": case.applicant_name,
            "loan_type": case.loan_type,
            "loan_amount": float(case.loan_amount) if case.loan_amount else 0,
            "status": case.status,
            "risk_score": float(case.risk_score) if case.risk_score else 0,
            "risk_category": case.risk_category,
            "decision": case.decision,
        }

    # Pull analysis results from DB
    stmt = select(AnalysisResult).where(AnalysisResult.case_id == case_id)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    if rows and "agent_logs" not in context:
        context["agent_logs"] = [
            {
                "agent": r.agent_name,
                "type": r.analysis_type,
                "score": float(r.score or 0),
                "severity": r.severity,
                "findings": r.findings,
            }
            for r in rows
        ]

    return context


def _build_system_prompt(context: dict) -> str:
    """Build a rich system prompt from case context."""
    case_info = context.get("case_info", {})
    risk = context.get("risk_scores", {})
    decision = context.get("final_decision", {})
    forensic = context.get("forensic_results", {})
    compliance = context.get("compliance_results", {})
    crossref = context.get("cross_reference_results", {})
    mismatches = context.get("mismatches", [])
    dna = context.get("fraud_dna_results", {})

    prompt_parts = [
        "You are TruthLens, an expert AI forensic analyst for Indian bank loan fraud detection.",
        "Answer questions about this specific case concisely and accurately.",
        "If you don't have exact data, give guidance based on Indian banking regulations and fraud patterns.",
        "",
        "=== CASE CONTEXT ===",
    ]

    if case_info:
        prompt_parts += [
            f"Case Number: {case_info.get('case_number', 'Unknown')}",
            f"Applicant: {case_info.get('applicant_name', 'Unknown')}",
            f"Loan Type: {case_info.get('loan_type', 'Unknown')}",
            f"Loan Amount: ₹{case_info.get('loan_amount', 0):,.0f}",
            f"Risk Score: {case_info.get('risk_score', risk.get('composite', 0))}/100",
            f"Risk Category: {case_info.get('risk_category', risk.get('category', 'Unknown'))}",
            f"AI Decision: {case_info.get('decision', decision.get('decision', 'Pending'))}",
        ]

    reasoning = decision.get("reasoning", [])
    if reasoning:
        prompt_parts.append(f"Decision Reasoning: {'; '.join(reasoning[:3])}")

    if mismatches:
        prompt_parts.append(f"Document Mismatches Found: {len(mismatches)}")
        for m in mismatches[:3]:
            prompt_parts.append(f"  - {m.get('field', 'Field')}: {m.get('doc1', '')} vs {m.get('doc2', '')}")

    doc_count = len([k for k in forensic.keys() if not k.startswith("_")])
    if doc_count:
        prompt_parts.append(f"Documents Analyzed: {doc_count}")

    compliance_violations = compliance.get("regulatory_violations", [])
    if compliance_violations:
        prompt_parts.append(f"Compliance Violations: {len(compliance_violations)}")

    fraud_matches = sum(
        v.get("match_count", 0) for v in dna.values() if isinstance(v, dict)
    )
    if fraud_matches:
        prompt_parts.append(f"Fraud DNA Pattern Matches: {fraud_matches}")

    prompt_parts += ["", "Answer the officer's question based on this case data:"]
    return "\n".join(prompt_parts)


@router.post("/cases/{case_id}/chat")
async def case_chat(
    case_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    AI Interrogator — ask any question about a case in natural language.
    Powered by CRAG retrieval + Ollama llama3.1:8b generation.
    """
    question = body.get("question", "").strip()
    chat_history = body.get("history", [])  # list of {role, content}

    if not question:
        return {"error": "Question is required"}

    # Build full case context
    context = await _build_case_context(case_id, db)

    # Try CRAG-enhanced answer first
    crag_answer = None
    sources = []
    retrieval_quality = "general"

    try:
        from app.rag.crag import CRAGSystem
        crag = CRAGSystem()
        crag_response = await crag.query(question, context=context)
        crag_answer = crag_response.answer
        sources = [{"file": s.file, "relevance": s.relevance} for s in crag_response.sources]
        retrieval_quality = crag_response.retrieval_quality
    except Exception:
        pass

    # If CRAG gave a good answer, use it. Otherwise fall back to direct Ollama with case context.
    if crag_answer and len(crag_answer) > 30:
        answer = crag_answer
    else:
        # Direct Ollama call with full case context
        try:
            import httpx
            from app.core.config import settings

            system = _build_system_prompt(context)

            # Build conversation history string
            history_str = ""
            for turn in chat_history[-4:]:  # Last 4 turns for context
                role = "Officer" if turn.get("role") == "user" else "TruthLens AI"
                history_str += f"{role}: {turn.get('content', '')}\n"

            full_prompt = f"{system}\n\n{history_str}Officer: {question}\nTruthLens AI:"

            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    f"{settings.OLLAMA_HOST}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": full_prompt,
                        "stream": False,
                        "options": {"temperature": 0.3, "num_predict": 300}
                    }
                )
                answer = resp.json().get("response", "").strip()
        except Exception as e:
            answer = f"I'm having trouble connecting to the AI engine. Based on the case data: Risk score is {context.get('case_info', {}).get('risk_score', 'unknown')}/100 with decision: {context.get('case_info', {}).get('decision', 'pending')}."

    # Detect special query types for structured responses
    question_lower = question.lower()
    structured_data = None

    if any(w in question_lower for w in ["risk score", "score breakdown", "how risky"]):
        structured_data = {
            "type": "risk_breakdown",
            "scores": context.get("risk_scores", {}),
        }
    elif any(w in question_lower for w in ["mismatch", "inconsistency", "different"]):
        structured_data = {
            "type": "mismatches",
            "items": context.get("mismatches", [])[:5],
        }
    elif any(w in question_lower for w in ["compliance", "violation", "regulation", "rbi"]):
        structured_data = {
            "type": "compliance",
            "violations": context.get("compliance_results", {}).get("regulatory_violations", [])[:5],
        }
    elif any(w in question_lower for w in ["decision", "recommend", "approve", "reject"]):
        structured_data = {
            "type": "decision",
            "decision": context.get("final_decision", {}),
        }

    return {
        "answer": answer,
        "sources": sources,
        "retrieval_quality": retrieval_quality,
        "structured_data": structured_data,
        "case_id": case_id,
    }
