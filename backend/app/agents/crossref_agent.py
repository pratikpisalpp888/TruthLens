"""
TruthLens — Cross-Reference Agent.
"""

import datetime
from app.agents.state import TruthLensState
from app.services.cross_doc_service import CrossDocumentService
from app.services.itr_service import ITRValidationService


class CrossRefAgent:

    def __init__(self, db):
        self.db = db

    async def run(self, state: TruthLensState) -> TruthLensState:
        logs = state.get("agent_logs", [])
        errors = state.get("errors", [])
        state["current_agent"] = "crossref"

        case_id = state["case_id"]
        docs = state.get("documents", [])

        cross_doc_report = {}
        itr_report = {}

        try:
            cross_svc = CrossDocumentService(self.db)
            report = await cross_svc.analyze_case(case_id)
            cross_doc_report = report.dict()
        except Exception as e:
            errors.append({"agent": "crossref", "error": str(e)})

        # If ITR document exists, run ITR validation
        itr_docs = [d for d in docs if d.document_type == "itr"]
        if itr_docs:
            try:
                itr_svc = ITRValidationService(self.db)
                itr_res = await itr_svc.validate(str(itr_docs[0].id), case_id)
                itr_report = itr_res.dict()
            except Exception as e:
                errors.append({"agent": "itr_validation", "error": str(e)})

        logs.append({
            "agent": "crossref",
            "status": "completed",
            "mismatches_found": cross_doc_report.get("mismatches_found", 0),
            "itr_validated": bool(itr_docs),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

        state["cross_reference_results"] = cross_doc_report
        state["itr_results"] = itr_report
        state["agent_logs"] = logs
        state["errors"] = errors
        return state
