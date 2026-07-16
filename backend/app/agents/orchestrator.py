"""
TruthLens — LangGraph Orchestrator.
"""

import time
import datetime
import asyncio
from typing import Optional, Callable, Awaitable

from langgraph.graph import StateGraph, END

from app.agents.state import TruthLensState
from app.agents.classifier_agent import ClassifierAgent
from app.agents.forensic_agent import ForensicAgent
from app.agents.crossref_agent import CrossRefAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.decision_agent import DecisionAgent
from app.services.report_service import ReportService


class TruthLensOrchestrator:

    def __init__(self, db):
        self.db = db
        self.classifier = ClassifierAgent()
        self.forensic = ForensicAgent(db)
        self.crossref = CrossRefAgent(db)
        self.compliance = ComplianceAgent()
        self.decision = DecisionAgent()
        self.report_svc = ReportService()
        self._progress_cb: Optional[Callable] = None

    def set_progress_callback(self, cb: Callable):
        self._progress_cb = cb

    async def _notify(self, agent: str, status: str, data: dict = None):
        if self._progress_cb:
            try:
                await self._progress_cb(agent, status, data or {})
            except Exception:
                pass

    def build_graph(self) -> StateGraph:
        graph = StateGraph(TruthLensState)

        # Wrap each agent.run with notification
        async def run_classifier(state):
            await self._notify("classifier", "started")
            state = await self.classifier.run(state)
            await self._notify("classifier", "completed", state["classification_results"])
            return state

        async def run_forensic(state):
            await self._notify("forensic", "started")
            state = await self.forensic.run(state)
            
            # Count anomalies for the live UI
            total_anomalies = 0
            total_critical = 0
            for fr in state.get("forensic_results", {}).values():
                if isinstance(fr, dict):
                    anomalies = fr.get("anomalies", [])
                    total_anomalies += len(anomalies)
                    total_critical += sum(1 for a in anomalies if a.get("severity") == "critical")
            
            await self._notify("forensic", "completed", {
                "docs_analyzed": len(state.get("documents", [])),
                "anomalies": total_anomalies,
                "critical": total_critical
            })
            return state

        async def run_crossref(state):
            await self._notify("crossref", "started")
            state = await self.crossref.run(state)
            await self._notify("crossref", "completed", {"mismatches": state["cross_reference_results"].get("mismatches_found", 0)})
            return state

        async def run_compliance(state):
            await self._notify("compliance", "started")
            state = await self.compliance.run(state)
            await self._notify("compliance", "completed", {"violations": len(state["compliance_results"].get("regulatory_violations", []))})
            return state

        async def run_decision(state):
            await self._notify("decision", "started")
            state = await self.decision.run(state)
            # Generate report
            try:
                pdf_bytes = await self.report_svc.generate_pdf(state)
                md = await self.report_svc.generate_markdown(state)
                state["report"] = md
                state["_pdf_bytes"] = pdf_bytes
            except Exception as e:
                state["errors"] = state.get("errors", []) + [{"agent": "report", "error": str(e)}]
            await self._notify("decision", "completed", state["final_decision"])
            return state

        graph.add_node("classifier", run_classifier)
        graph.add_node("forensic", run_forensic)
        graph.add_node("crossref", run_crossref)
        graph.add_node("compliance", run_compliance)
        graph.add_node("decision", run_decision)

        # Edges — sequential flow to avoid LangGraph multiple-edge restrictions
        graph.set_entry_point("classifier")
        graph.add_edge("classifier", "forensic")
        graph.add_edge("forensic", "crossref")
        graph.add_edge("crossref", "compliance")
        graph.add_edge("compliance", "decision")
        graph.add_edge("decision", END)

        return graph.compile()

    async def analyze_case(self, case_id: str) -> TruthLensState:
        from app.repositories.document_repo import DocumentRepository
        from app.repositories.case_repo import CaseRepository

        doc_repo = DocumentRepository(self.db)
        case_repo = CaseRepository(self.db)

        documents = await doc_repo.get_by_case(case_id)

        initial_state = TruthLensState(
            case_id=case_id,
            documents=documents,
            classification_results={},
            forensic_results={},
            cross_reference_results={},
            itr_results={},
            fraud_dna_results={},
            compliance_results={},
            risk_scores={},
            final_decision={},
            report="",
            agent_logs=[],
            errors=[],
            current_agent="",
            start_time=time.time()
        )

        graph = self.build_graph()
        final_state = await graph.ainvoke(initial_state)

        # Save results and update case
        composite = final_state["risk_scores"].get("composite", 50)
        category = final_state["risk_scores"].get("category", "medium")

        try:
            await case_repo.update(case_id, {
                "status": "analyzed",
                "risk_score": composite,
                "risk_category": category,
                "analysis_completed_at": datetime.datetime.utcnow()
            })
            await self.db.commit()
        except Exception as e:
            pass  # Non-fatal

        return final_state
