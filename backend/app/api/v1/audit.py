"""
TruthLens — Audit Log API (Admin only).
"""

import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.dependencies import get_db, get_current_user, require_role
from app.db.models.audit_log import AuditLog
from app.db.models.user import User

router = APIRouter()


@router.get("/audit-logs")
async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get audit logs with optional filters (admin only)."""
    filters = []
    if user_id:
        filters.append(AuditLog.user_id == user_id)
    if action:
        filters.append(AuditLog.action == action)
    if resource_type:
        filters.append(AuditLog.resource_type == resource_type)
    if date_from:
        filters.append(AuditLog.created_at >= datetime.datetime.combine(date_from, datetime.time.min))
    if date_to:
        filters.append(AuditLog.created_at <= datetime.datetime.combine(date_to, datetime.time.max))

    q = select(AuditLog)
    if filters:
        q = q.where(and_(*filters))
    q = q.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(q)
    logs = result.scalars().all()

    return {
        "skip": skip,
        "limit": limit,
        "logs": [
            {
                "id": str(l.id),
                "user_id": str(l.user_id),
                "action": l.action,
                "resource_type": l.resource_type,
                "resource_id": str(l.resource_id) if l.resource_id else None,
                "details": l.details,
                "ip_address": l.ip_address,
                "created_at": l.created_at.isoformat() if l.created_at else None
            }
            for l in logs
        ]
    }
