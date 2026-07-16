"""
TruthLens — Report Service (ReportLab PDF + Markdown).
"""

import io
import datetime
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from app.agents.state import TruthLensState


class ReportService:

    def _get_styles(self):
        styles = getSampleStyleSheet()
        heading1 = ParagraphStyle(
            "CustomH1", parent=styles["Heading1"],
            textColor=colors.HexColor("#1a237e"), fontSize=18, spaceAfter=12
        )
        heading2 = ParagraphStyle(
            "CustomH2", parent=styles["Heading2"],
            textColor=colors.HexColor("#283593"), fontSize=13, spaceAfter=8
        )
        body = ParagraphStyle(
            "CustomBody", parent=styles["Normal"],
            fontSize=10, leading=14, spaceAfter=6
        )
        label = ParagraphStyle(
            "Label", parent=styles["Normal"],
            fontSize=9, textColor=colors.HexColor("#616161"), spaceAfter=4
        )
        return {"h1": heading1, "h2": heading2, "body": body, "label": label}

    def _risk_color(self, category: str):
        return {
            "low": colors.HexColor("#2e7d32"),
            "medium": colors.HexColor("#f57f17"),
            "high": colors.HexColor("#c62828"),
        }.get(category, colors.black)

    async def generate_pdf(self, state: TruthLensState) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = self._get_styles()
        elements = []

        risk_scores = state.get("risk_scores", {})
        final_decision = state.get("final_decision", {})
        case_id = state.get("case_id", "N/A")
        docs = state.get("documents", [])
        cross = state.get("cross_reference_results", {})
        itr = state.get("itr_results", {})
        compliance = state.get("compliance_results", {})
        agent_logs = state.get("agent_logs", [])
        composite = risk_scores.get("composite", 0)
        category = risk_scores.get("category", "unknown")
        decision = final_decision.get("decision", "N/A")

        # ── Header ────────────────────────────────────────────────────────
        elements.append(Paragraph("🔍 TruthLens — Document Forensics Report", styles["h1"]))
        elements.append(Paragraph(f"<b>Canara Bank | Loan Underwriting Fraud Detection Platform</b>", styles["label"]))
        elements.append(Paragraph(f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["label"]))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a237e")))
        elements.append(Spacer(1, 0.3*cm))

        # ── Case Info ─────────────────────────────────────────────────────
        elements.append(Paragraph("Case Information", styles["h2"]))
        case_data = [
            ["Case ID", case_id],
            ["Total Documents", str(len(docs))],
            ["Analysis Date", datetime.datetime.utcnow().strftime('%Y-%m-%d')],
        ]
        case_table = Table(case_data, colWidths=[5*cm, 12*cm])
        case_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#e8eaf6")),
            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bdbdbd")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("PADDING", (0,0), (-1,-1), 6),
        ]))
        elements.append(case_table)
        elements.append(Spacer(1, 0.4*cm))

        # ── Risk Score Dashboard ──────────────────────────────────────────
        elements.append(Paragraph("Risk Score Dashboard", styles["h2"]))
        score_data = [["Metric", "Score", "Weight"]]
        weight_map = {
            "document_authenticity": "25%",
            "cross_document_consistency": "25%",
            "itr_validity": "25%",
            "fraud_pattern_risk": "15%",
            "compliance_risk": "10%"
        }
        for k, w in weight_map.items():
            v = risk_scores.get(k, 0)
            score_data.append([k.replace("_", " ").title(), f"{v}/100", w])
        score_data.append(["COMPOSITE RISK SCORE", f"{composite}/100", ""])

        score_table = Table(score_data, colWidths=[8*cm, 4*cm, 3*cm])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a237e")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("BACKGROUND", (0,-1), (-1,-1), self._risk_color(category)),
            ("TEXTCOLOR", (0,-1), (-1,-1), colors.white),
            ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bdbdbd")),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("PADDING", (0,0), (-1,-1), 6),
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 0.4*cm))

        # ── Final Decision ────────────────────────────────────────────────
        elements.append(Paragraph("Final Decision", styles["h2"]))
        dec_color = {"APPROVE": colors.HexColor("#2e7d32"),
                     "FLAG_FOR_REVIEW": colors.HexColor("#f57f17"),
                     "REJECT": colors.HexColor("#c62828")}.get(decision, colors.black)
        elements.append(Paragraph(
            f"<font color='#{dec_color.hexval()[1:]}' size='14'><b>{decision}</b></font> "
            f"(Confidence: {final_decision.get('confidence', 0)}%)",
            styles["body"]
        ))
        elements.append(Paragraph(f"<b>Summary:</b> {final_decision.get('summary', '')}", styles["body"]))
        actions = final_decision.get("recommended_actions", "")
        if actions:
            elements.append(Paragraph(f"<b>Recommended Actions:</b> {actions}", styles["body"]))
        elements.append(Spacer(1, 0.4*cm))

        # ── Cross-Document Findings ───────────────────────────────────────
        if cross:
            elements.append(Paragraph("Cross-Document Consistency", styles["h2"]))
            elements.append(Paragraph(
                f"Consistency Score: {cross.get('consistency_score', 0)}/100 | "
                f"Mismatches Found: {cross.get('mismatches_found', 0)}", styles["body"]
            ))
        elements.append(Spacer(1, 0.3*cm))

        # ── ITR Findings ──────────────────────────────────────────────────
        if itr:
            elements.append(Paragraph("ITR Validation", styles["h2"]))
            elements.append(Paragraph(
                f"Validity Score: {itr.get('validity_score', 0)}/100 | "
                f"Form: {itr.get('form_type', 'N/A')} | AY: {itr.get('assessment_year', 'N/A')}",
                styles["body"]
            ))
            for issue in itr.get("critical_issues", []):
                elements.append(Paragraph(f"⚠️ {issue}", styles["body"]))
        elements.append(Spacer(1, 0.3*cm))

        # ── Compliance Violations ─────────────────────────────────────────
        if compliance.get("regulatory_violations"):
            elements.append(Paragraph("Compliance & Regulatory Violations", styles["h2"]))
            for v in compliance["regulatory_violations"]:
                elements.append(Paragraph(f"• [{v.get('severity', '').upper()}] {v.get('finding', '')}", styles["body"]))
                elements.append(Paragraph(f"  Regulation: {v.get('regulation', '')}", styles["label"]))
        elements.append(Spacer(1, 0.3*cm))

        # ── Agent Execution Log ───────────────────────────────────────────
        elements.append(Paragraph("Agent Execution Log", styles["h2"]))
        log_data = [["Agent", "Status", "Timestamp"]]
        for log in agent_logs:
            log_data.append([
                log.get("agent", ""), log.get("status", ""), log.get("timestamp", "")
            ])
        log_table = Table(log_data, colWidths=[5*cm, 4*cm, 8*cm])
        log_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#283593")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bdbdbd")),
            ("PADDING", (0,0), (-1,-1), 5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
        ]))
        elements.append(log_table)
        elements.append(Spacer(1, 0.4*cm))

        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        elements.append(Paragraph(
            "This report is auto-generated by TruthLens AI Forensics Platform. "
            "All analysis is performed offline using local AI models. "
            "For official use only — Canara Bank Internal.",
            styles["label"]
        ))

        doc.build(elements)
        return buf.getvalue()

    async def generate_markdown(self, state: TruthLensState) -> str:
        risk_scores = state.get("risk_scores", {})
        decision = state.get("final_decision", {})
        case_id = state.get("case_id", "N/A")
        docs = state.get("documents", [])
        cross = state.get("cross_reference_results", {})
        itr = state.get("itr_results", {})

        md = f"""# TruthLens Forensic Report

**Case ID:** `{case_id}`
**Documents:** {len(docs)}
**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

## Risk Score Dashboard

| Metric | Score |
|--------|-------|
| Document Authenticity | {risk_scores.get("document_authenticity", 0)}/100 |
| Cross-Document Consistency | {risk_scores.get("cross_document_consistency", 0)}/100 |
| ITR Validity | {risk_scores.get("itr_validity", 0)}/100 |
| Fraud Pattern Risk | {risk_scores.get("fraud_pattern_risk", 0)}/100 |
| Compliance Risk | {risk_scores.get("compliance_risk", 0)}/100 |
| **Composite Score** | **{risk_scores.get("composite", 0)}/100** |

**Risk Category:** {risk_scores.get("category", "unknown").upper()}

---

## Final Decision

**Decision:** {decision.get("decision", "N/A")}
**Confidence:** {decision.get("confidence", 0)}%
**Summary:** {decision.get("summary", "")}

---

## Cross-Document Consistency

Consistency Score: {cross.get("consistency_score", "N/A")} | Mismatches: {cross.get("mismatches_found", 0)}

## ITR Validation

Validity Score: {itr.get("validity_score", "N/A")} | Form: {itr.get("form_type", "N/A")} | AY: {itr.get("assessment_year", "N/A")}

---
*Generated by TruthLens AI — Canara Bank Internal Use Only*
"""
        return md
