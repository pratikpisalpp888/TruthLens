"""
TruthLens — Compliance Agent (CRAG-powered).
"""

import datetime
from typing import List, Dict, Any
from app.agents.state import TruthLensState
from app.services.rag_service import RAGService


class ComplianceAgent:

    async def run(self, state: TruthLensState) -> TruthLensState:
        logs = state.get("agent_logs", [])
        errors = state.get("errors", [])
        state["current_agent"] = "compliance"

        rag = RAGService()
        violations = []
        required_actions = []
        citations = []

        # Collect critical findings from prior agents
        findings: List[Dict[str, Any]] = []

        # From forensics
        for doc_id, fr in state.get("forensic_results", {}).items():
            if isinstance(fr, dict) and fr.get("authenticity_score", 100) < 50:
                findings.append({
                    "type": "forensic",
                    "detail": f"Document {doc_id} has low authenticity score ({fr.get('authenticity_score')})",
                    "severity": "critical"
                })

        # From cross-doc
        cross = state.get("cross_reference_results", {})
        for m in cross.get("critical_findings", []):
            finding_detail = m.get("assessment") or m.get("detail") or "Critical mismatch"
            findings.append({
                "type": "cross_doc",
                "detail": finding_detail,
                "severity": "critical"
            })

        # From ITR
        itr = state.get("itr_results", {})
        for issue in itr.get("critical_issues", []):
            findings.append({
                "type": "itr",
                "detail": issue,
                "severity": "critical"
            })

        # For each critical/high finding, query CRAG for regulatory reference
        for finding in findings[:5]:  # Limit to 5 CRAG calls to avoid latency
            try:
                question = f"What RBI regulation or banking guideline applies to: {finding['detail']}?"
                crag_resp = await rag.answer_question(question)
                violations.append({
                    "finding": finding["detail"],
                    "severity": finding["severity"],
                    "regulation": crag_resp.answer
                })
                required_actions.append(f"Investigate: {finding['detail']}")
                for src in crag_resp.sources:
                    citations.append(src.file)
            except Exception as e:
                errors.append({"agent": "compliance_crag", "error": str(e)})

        logs.append({
            "agent": "compliance",
            "status": "completed",
            "violations_found": len(violations),
            "crag_citations": len(set(citations)),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

        state["compliance_results"] = {
            "regulatory_violations": violations,
            "required_actions": list(set(required_actions)),
            "citations": list(set(citations))
        }
        state["agent_logs"] = logs
        state["errors"] = errors
        return state
