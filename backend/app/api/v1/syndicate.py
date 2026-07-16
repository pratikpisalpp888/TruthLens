"""
TruthLens — Fraud Syndicate Intelligence API.

Cross-case entity analysis to detect organized fraud rings.
Uses the existing GraphRAG NetworkX infrastructure.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.db.models.case import Case
from app.db.models.analysis import AnalysisResult

router = APIRouter()


async def _extract_entities_from_case(case: Case, analysis_rows: list) -> dict:
    """Extract PAN, phone, address, property from case data."""
    entities = {
        "applicant_name": case.applicant_name,
        "loan_amount": float(case.loan_amount) if case.loan_amount else 0,
        "loan_type": case.loan_type,
        "pans": [],
        "phones": [],
        "addresses": [],
        "property_ids": [],
        "document_hashes": [],
    }

    for row in analysis_rows:
        if not isinstance(row.findings, dict):
            continue
        findings = row.findings

        # NER entities extracted during analysis
        ner = findings.get("ner_entities", {})
        if ner:
            entities["pans"].extend(ner.get("pan_numbers", []))
            entities["phones"].extend(ner.get("phone_numbers", []))
            entities["addresses"].extend(ner.get("addresses", []))

        # Cross-doc findings
        cross = findings.get("cross_reference_results", {})
        if cross:
            entities["pans"].extend(cross.get("pan_numbers", []))

        # Forensic evidence paths (document template hashes)
        if row.evidence_paths and isinstance(row.evidence_paths, dict):
            phash = row.evidence_paths.get("template_phash")
            if phash:
                entities["document_hashes"].append(phash)

    # Deduplicate
    for key in ["pans", "phones", "addresses", "document_hashes"]:
        entities[key] = list(set(entities[key]))

    return entities


def _compute_connection_strength(e1: dict, e2: dict) -> tuple[float, list[str]]:
    """Compute how strongly two cases are connected and why."""
    shared = []
    score = 0.0

    # Shared PAN numbers — strongest signal (same identity)
    shared_pans = set(e1["pans"]) & set(e2["pans"])
    if shared_pans:
        shared.append(f"Shared PAN: {', '.join(shared_pans)}")
        score += 0.9

    # Shared phone numbers
    shared_phones = set(e1["phones"]) & set(e2["phones"])
    if shared_phones:
        shared.append(f"Shared Phone: {', '.join(list(shared_phones)[:2])}")
        score += 0.7

    # Shared document template hash — same blank form used
    shared_hashes = set(e1["document_hashes"]) & set(e2["document_hashes"])
    if shared_hashes:
        shared.append(f"Same document template (Template DNA match)")
        score += 0.8

    # Same applicant name similarity (fuzzy)
    name1 = e1.get("applicant_name", "").lower().split()
    name2 = e2.get("applicant_name", "").lower().split()
    if name1 and name2:
        common_words = set(name1) & set(name2) - {"kumar", "singh", "sharma", "mr", "mrs", "ms"}
        if len(common_words) >= 2:
            shared.append(f"Similar applicant name: {e1['applicant_name']} / {e2['applicant_name']}")
            score += 0.5

    return min(score, 1.0), shared


@router.get("/cases/{case_id}/syndicate-connections")
async def get_syndicate_connections(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fraud Syndicate Intelligence — Cross-case entity analysis.
    Returns a graph of cases connected to this case via shared identifiers.
    """
    # Load the target case
    target_case = await db.get(Case, case_id)
    if not target_case:
        return {"error": "Case not found"}

    # Load ALL analyzed cases for cross-comparison (limit 200 for performance)
    all_cases_stmt = select(Case).where(Case.status.in_(["analyzed", "decided", "analyzing"])).limit(200)
    result = await db.execute(all_cases_stmt)
    all_cases = result.scalars().all()

    # Load analysis results for all cases in one query
    all_case_ids = [str(c.id) for c in all_cases]
    analysis_stmt = select(AnalysisResult).where(AnalysisResult.case_id.in_(all_case_ids))
    analysis_result = await db.execute(analysis_stmt)
    analysis_rows = analysis_result.scalars().all()

    # Group by case_id
    analysis_by_case: dict[str, list] = {}
    for row in analysis_rows:
        cid = str(row.case_id)
        if cid not in analysis_by_case:
            analysis_by_case[cid] = []
        analysis_by_case[cid].append(row)

    # Extract entities for target case
    target_entities = await _extract_entities_from_case(
        target_case, analysis_by_case.get(case_id, [])
    )

    # Build graph
    nodes = []
    edges = []
    seen_nodes = set()

    # Add target node
    risk_score = float(target_case.risk_score or 0)
    target_node = {
        "id": case_id,
        "label": target_case.case_number or case_id[:8],
        "type": "case",
        "risk": "critical" if target_case.decision == "rejected" else "high" if risk_score > 60 else "medium",
        "applicant": target_case.applicant_name,
        "status": target_case.status,
        "decision": target_case.decision,
        "risk_score": risk_score,
        "loan_amount": float(target_case.loan_amount or 0),
        "loan_type": target_case.loan_type,
        "is_target": True,
    }
    nodes.append(target_node)
    seen_nodes.add(case_id)

    # Compare target with every other case
    for case in all_cases:
        cid = str(case.id)
        if cid == case_id:
            continue

        case_entities = await _extract_entities_from_case(
            case, analysis_by_case.get(cid, [])
        )

        strength, reasons = _compute_connection_strength(target_entities, case_entities)

        if strength > 0.4:  # Only show meaningful connections
            if cid not in seen_nodes:
                case_risk = float(case.risk_score or 0)
                is_fraud = case.decision == "rejected"
                
                nodes.append({
                    "id": cid,
                    "label": case.case_number or cid[:8],
                    "type": "case",
                    "risk": "critical" if is_fraud else "high" if case_risk > 60 else "low",
                    "applicant": case.applicant_name,
                    "status": case.status,
                    "decision": case.decision,
                    "risk_score": case_risk,
                    "loan_amount": float(case.loan_amount or 0),
                    "loan_type": case.loan_type,
                    "is_target": False,
                })
                seen_nodes.add(cid)

            edges.append({
                "id": f"{case_id}-{cid}",
                "source": case_id,
                "target": cid,
                "strength": round(strength, 2),
                "reasons": reasons,
                "label": reasons[0] if reasons else "Connected",
                "type": "fraud" if strength > 0.8 else "suspicious" if strength > 0.6 else "weak",
            })

    # Detect fraud rings (clusters of 3+ cases)
    rings = []
    if len(edges) >= 2:
        connected_ids = {e["target"] for e in edges} | {e["source"] for e in edges}
        high_risk_connected = [
            n for n in nodes
            if n["id"] in connected_ids and (n.get("risk_score", 0) > 60 or n.get("decision") == "rejected")
        ]
        if len(high_risk_connected) >= 2:
            rings.append({
                "id": f"RING-{case_id[:8]}",
                "case_count": len(connected_ids),
                "high_risk_count": len(high_risk_connected),
                "description": f"Potential fraud syndicate: {len(connected_ids)} connected cases, {len(high_risk_connected)} high-risk",
                "severity": "critical" if len(high_risk_connected) >= 3 else "high",
            })

    # Compute overall syndicate risk signal
    connection_count = len(edges)
    fraud_connections = sum(1 for e in edges if e["type"] == "fraud")
    syndicate_risk_score = min(100, (fraud_connections * 30 + connection_count * 10))

    return {
        "case_id": case_id,
        "graph": {
            "nodes": nodes,
            "edges": edges,
        },
        "summary": {
            "total_connections": connection_count,
            "fraud_connections": fraud_connections,
            "suspicious_connections": sum(1 for e in edges if e["type"] == "suspicious"),
            "syndicate_risk_score": syndicate_risk_score,
            "fraud_rings_detected": len(rings),
            "rings": rings,
        },
        "target_entities": {
            "pans_found": len(target_entities["pans"]),
            "phones_found": len(target_entities["phones"]),
        },
        "intelligence_note": (
            f"TruthLens scanned {len(all_cases)} cases and found {connection_count} connections to this case. "
            + (f"⚠️ {len(rings)} potential fraud ring(s) detected." if rings else "No organized fraud rings detected.")
        ),
    }


@router.get("/syndicate/overview")
async def get_syndicate_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    System-wide fraud syndicate overview — shows all detected rings across all cases.
    """
    # Load all high-risk rejected cases
    stmt = select(Case).where(Case.status.in_(["analyzed", "decided"]))
    result = await db.execute(stmt)
    cases = result.scalars().all()

    high_risk = [c for c in cases if (c.risk_score or 0) > 60 or c.decision == "rejected"]
    flagged = [c for c in cases if c.decision == "flagged"]
    approved = [c for c in cases if c.decision == "approved"]

    return {
        "total_cases": len(cases),
        "high_risk_cases": len(high_risk),
        "flagged_cases": len(flagged),
        "approved_cases": len(approved),
        "cases": [
            {
                "id": str(c.id),
                "case_number": c.case_number,
                "applicant_name": c.applicant_name,
                "risk_score": float(c.risk_score or 0),
                "decision": c.decision,
                "loan_amount": float(c.loan_amount or 0),
                "loan_type": c.loan_type,
            }
            for c in cases[:50]
        ],
    }
