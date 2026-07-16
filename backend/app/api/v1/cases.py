"""
TruthLens — Complete Case Management API.
"""

import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_

from app.core.dependencies import get_db, get_current_user, require_role
from app.db.models.user import User
from app.db.models.case import Case
from app.repositories.case_repo import CaseRepository
from app.repositories.audit_log_repo import AuditLogRepository as AuditRepository
from app.core.exceptions import ResourceNotFoundError

router = APIRouter()


def _generate_case_number() -> str:
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    import random
    suffix = str(random.randint(1000, 9999))
    return f"TL-{today}-{suffix}"


@router.post("/cases", status_code=status.HTTP_201_CREATED)
async def create_case(
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new loan underwriting case."""
    case_repo = CaseRepository(db)
    audit_repo = AuditRepository(db)

    case_data = {
        "case_number": _generate_case_number(),
        "applicant_name": body.get("applicant_name", ""),
        "loan_type": body.get("loan_type", "home_loan"),
        "loan_amount": body.get("loan_amount", 0),
        "status": "created",
        "officer_id": str(current_user.id),
    }
    case = await case_repo.create(case_data)
    await audit_repo.log(
        user_id=str(current_user.id),
        action="case.created",
        resource_type="case",
        resource_id=str(case.id),
        details={"case_number": case.case_number}
    )
    await db.commit()
    return {"id": str(case.id), "case_number": case.case_number, "status": case.status}


@router.get("/cases")
async def list_cases(
    status_filter: Optional[str] = Query(None, alias="status"),
    risk_category: Optional[str] = None,
    officer_id: Optional[str] = None,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List cases with filters, search, and pagination."""
    query = select(Case)
    filters = []
    if status_filter:
        filters.append(Case.status == status_filter)
    if risk_category:
        filters.append(Case.risk_category == risk_category)
    if officer_id:
        filters.append(Case.officer_id == officer_id)
    if date_from:
        filters.append(Case.created_at >= datetime.datetime.combine(date_from, datetime.time.min))
    if date_to:
        filters.append(Case.created_at <= datetime.datetime.combine(date_to, datetime.time.max))
    if search:
        filters.append(or_(
            Case.applicant_name.ilike(f"%{search}%"),
            Case.case_number.ilike(f"%{search}%")
        ))
    if filters:
        query = query.where(and_(*filters))

    sort_col = getattr(Case, sort_by, Case.created_at)
    query = query.order_by(sort_col.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    cases = result.scalars().all()

    count_q = select(func.count()).select_from(Case)
    if filters:
        count_q = count_q.where(and_(*filters))
    total = (await db.execute(count_q)).scalar()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "cases": [
            {
                "id": str(c.id), "case_number": c.case_number,
                "applicant_name": c.applicant_name, "status": c.status,
                "risk_category": c.risk_category, "loan_amount": c.loan_amount,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in cases
        ]
    }


@router.get("/cases/{case_id}")
async def get_case(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get full case details with documents."""
    case_repo = CaseRepository(db)
    case = await case_repo.get_by_id(case_id)
    if not case:
        raise ResourceNotFoundError("Case not found")

    from app.repositories.document_repo import DocumentRepository
    doc_repo = DocumentRepository(db)
    docs = await doc_repo.get_by_case(case_id)

    return {
        "id": str(case.id),
        "case_number": case.case_number,
        "applicant_name": case.applicant_name,
        "loan_type": case.loan_type,
        "loan_amount": case.loan_amount,
        "status": case.status,
        "risk_score": case.risk_score,
        "risk_category": case.risk_category,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "documents": [
            {
                "id": str(d.id), "file_name": d.original_filename,
                "document_type": d.document_type, "status": d.processing_status
            }
            for d in docs
        ]
    }


@router.put("/cases/{case_id}")
async def update_case(
    case_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update case details."""
    case_repo = CaseRepository(db)
    case = await case_repo.update(case_id, body)
    if not case:
        raise ResourceNotFoundError("Case not found")
    await db.commit()
    return {"id": case_id, "message": "Updated"}


@router.post("/cases/{case_id}/decide")
async def decide_case(
    case_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Officer marks final decision on a case."""
    decision = body.get("decision")
    reason = body.get("reason", "")
    if decision not in ["approved", "flagged", "rejected"]:
        return {"error": "decision must be approved, flagged, or rejected"}

    case_repo = CaseRepository(db)
    audit_repo = AuditRepository(db)

    await case_repo.update(case_id, {
        "status": decision,
        "officer_decision": decision,
        "officer_notes": reason,
        "decided_by": str(current_user.id),
        "decided_at": datetime.datetime.utcnow()
    })
    await audit_repo.log(
        user_id=str(current_user.id),
        action="case.decided",
        resource_type="case",
        resource_id=case_id,
        details={"decision": decision, "reason": reason}
    )
    await db.commit()
    return {"message": "Decision recorded", "decision": decision}

@router.delete("/cases/{case_id}")
async def delete_case(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a case."""
    case_repo = CaseRepository(db)
    case = await case_repo.get_by_id(case_id)
    if not case:
        raise ResourceNotFoundError("Case not found")
        
    await db.delete(case)
    await db.commit()
    return {"message": "Case deleted successfully"}
