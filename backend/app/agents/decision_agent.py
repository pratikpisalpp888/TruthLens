"""
TruthLens — Decision Agent (LLM-powered final arbiter).
"""

import datetime
import httpx
from typing import Dict, Any
from app.agents.state import TruthLensState
from app.core.config import settings


class DecisionAgent:

    async def run(self, state: TruthLensState) -> TruthLensState:
        logs = state.get("agent_logs", [])
        errors = state.get("errors", [])
        state["current_agent"] = "decision"

        # ─── A. Calculate Risk Scores ───────────────────────────────────────────
        forensic_results = state.get("forensic_results", {})
        cross_ref = state.get("cross_reference_results", {})
        itr_res = state.get("itr_results", {})
        dna_res = state.get("fraud_dna_results", {})
        compliance_res = state.get("compliance_results", {})

        # Document authenticity — average of all forensic scores
        auth_scores = [
            v.get("authenticity_score", 50)
            for v in forensic_results.values()
            if isinstance(v, dict) and "authenticity_score" in v
        ]
        doc_authenticity = (sum(auth_scores) / len(auth_scores)) if auth_scores else 50.0

        # Cross-document consistency
        consistency_score = cross_ref.get("consistency_score", 50.0)

        # ITR validity
        itr_score = itr_res.get("validity_score", 50.0) if itr_res else 50.0

        # Fraud DNA — max similarity * 100
        max_sim = 0.0
        for doc_dna in dna_res.values():
            if isinstance(doc_dna, dict):
                for match in doc_dna.get("matches", []):
                    max_sim = max(max_sim, match.get("similarity", 0.0))
        fraud_pattern_risk = max_sim * 100.0  # Higher = more risky

        # Compliance risk — based on violation count
        violation_count = len(compliance_res.get("regulatory_violations", []))
        compliance_risk_score = max(0.0, 100.0 - (violation_count * 15))

        risk_scores: Dict[str, Any] = {
            "document_authenticity": round(100.0 - doc_authenticity, 2),  # 100 = full forgery
            "cross_document_consistency": round(100.0 - consistency_score, 2),  # 100 = completely inconsistent
            "itr_validity": round(100.0 - itr_score, 2),  # 100 = completely invalid
            "fraud_pattern_risk": round(fraud_pattern_risk, 2),  # 100 = exact match with known fraud
            "compliance_risk": round(min(100.0, violation_count * 25.0), 2),  # 100 = 4+ violations
        }

        weights = {
            "document_authenticity": 0.25,
            "cross_document_consistency": 0.25,
            "itr_validity": 0.25,
            "fraud_pattern_risk": 0.15,
            "compliance_risk": 0.10,
        }

        composite = sum(risk_scores[k] * weights[k] for k in weights)
        composite = round(composite, 2)
        risk_scores["composite"] = composite

        if composite >= 70:
            category = "high"
        elif composite >= 40:
            category = "medium"
        else:
            category = "low"

        risk_scores["category"] = category

        # ─── B. Generate Decision via Phi-3 ────────────────────────────────────
        forensic_summary = f"Authenticity avg: {doc_authenticity:.1f}/100. Velocity suspicious: {forensic_results.get('_velocity', {}).get('suspicious', False)}"
        cross_summary = f"Consistency score: {consistency_score}/100, Mismatches: {cross_ref.get('mismatches_found', 0)}"
        itr_summary = f"ITR validity: {itr_score}/100, Critical issues: {len(itr_res.get('critical_issues', []))}"
        dna_summary = f"Max fraud pattern match similarity: {round(max_sim * 100, 1)}%"
        compliance_summary = f"Regulatory violations: {violation_count}, Required actions: {len(compliance_res.get('required_actions', []))}"

        prompt = (
            "You are a senior bank fraud investigator at Canara Bank.\n"
            "Based on the following analysis findings, provide your recommendation.\n\n"
            f"Forensic findings: {forensic_summary}\n"
            f"Cross-document findings: {cross_summary}\n"
            f"ITR validation: {itr_summary}\n"
            f"Fraud pattern matches: {dna_summary}\n"
            f"Compliance issues: {compliance_summary}\n"
            f"Overall risk score: {composite}/100 (Category: {category.upper()})\n\n"
            "Provide EXACTLY in this format:\n"
            "DECISION: APPROVE or FLAG_FOR_REVIEW or REJECT\n"
            "CONFIDENCE: [0-100]%\n"
            "KEY_REASONS: 1) ... 2) ... 3) ...\n"
            "RECOMMENDED_ACTIONS: ...\n"
            "SUMMARY: [2-3 sentence executive summary]"
        )

        decision = {
            "decision": "flagged",
            "confidence": 75,
            "key_reasons": ["Insufficient forensic data", "Cross-doc check incomplete", "Manual review needed"],
            "recommended_actions": "Officer should manually verify all submitted documents.",
            "summary": f"Based on a composite risk score of {composite}/100 ({category} risk), this case requires careful review.",
            "risk_category": category,
            "composite_score": composite
        }

        # Determine rule-based decision immediately (no LLM dependency)
        total_anomalies = sum(
            len(fr.get("anomalies", []))
            for fr in forensic_results.values()
            if isinstance(fr, dict)
        )
        rule_signals = sum(
            len(fr.get("rule_signals", []))
            for fr in forensic_results.values()
            if isinstance(fr, dict)
        )
        critical_signals = sum(
            1 for fr in forensic_results.values()
            if isinstance(fr, dict)
            for sig in fr.get("rule_signals", [])
            if sig.get("severity") == "critical"
        )

        if composite >= 70 or critical_signals > 0 or total_anomalies > 5:
            base_decision = "rejected"
        elif composite >= 40 or total_anomalies > 2 or violation_count > 0:
            base_decision = "flagged"
        else:
            base_decision = "approved"

        decision["decision"] = base_decision
        decision["key_reasons"] = [
            f"Composite risk score: {composite}/100",
            f"Forensic anomalies detected: {total_anomalies}",
            f"Fraud signals: {rule_signals} rule-based indicators",
            f"Regulatory violations: {violation_count}",
        ]
        decision["summary"] = (
            f"AI analysis detected {total_anomalies} forensic anomalies and {rule_signals} fraud signals "
            f"with a composite risk score of {composite}/100. "
            f"Decision: {base_decision.upper()}."
        )
        # ─── B. Generate Decision (Pure Rule-Based / Deterministic) ──────────────────
        # Bypassing slow LLM calls entirely for maximum performance as requested.
        pass

        logs.append({
            "agent": "decision",
            "status": "completed",
            "composite_risk": composite,
            "category": category,
            "decision": decision["decision"],
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

        state["risk_scores"] = risk_scores
        state["final_decision"] = decision
        state["agent_logs"] = logs
        state["errors"] = errors
        return state
