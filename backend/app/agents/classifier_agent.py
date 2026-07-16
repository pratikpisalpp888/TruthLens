"""
TruthLens — Classifier Agent.
"""

import datetime
from app.agents.state import TruthLensState


class ClassifierAgent:

    async def run(self, state: TruthLensState) -> TruthLensState:
        logs = state.get("agent_logs", [])
        errors = state.get("errors", [])
        state["current_agent"] = "classifier"

        classification_results = {}
        docs = state.get("documents", [])

        for doc in docs:
            doc_id = str(doc.id)
            doc_type = doc.document_type or "unknown"
            confidence = 0.95 if doc_type != "unknown" else 0.40

            # If low confidence, fall back to LLM classification (Phi-3 via Ollama)
            if confidence < 0.60:
                try:
                    import httpx
                    from app.core.config import settings
                    prompt = (
                        f"Classify this document type from these options: "
                        f"[itr, bank_statement, sale_deed, land_record, identity, other]. "
                        f"Document text excerpt: '{(doc.ocr_text or '')[:500]}'. "
                        f"Respond with only the document type."
                    )
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        resp = await client.post(
                            f"{settings.OLLAMA_HOST}/api/generate",
                            json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False}
                        )
                        resp_json = resp.json()
                        llm_type = resp_json.get("response", "other").strip().lower()
                        doc_type = llm_type if llm_type in [
                            "itr", "bank_statement", "sale_deed", "land_record", "identity", "other"
                        ] else "other"
                        confidence = 0.70
                except Exception as e:
                    errors.append({"agent": "classifier", "error": str(e)})

            classification_results[doc_id] = {
                "type": doc_type,
                "confidence": confidence
            }

        logs.append({
            "agent": "classifier",
            "status": "completed",
            "documents_classified": len(docs),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

        state["classification_results"] = classification_results
        state["agent_logs"] = logs
        state["errors"] = errors
        return state
