"""
TruthLens — Analytics API Endpoints.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/analytics/dashboard")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get combined dashboard summary data."""
    svc = AnalyticsService(db)
    return await svc.get_dashboard_summary()


@router.get("/analytics/fraud-trends")
async def get_fraud_trends(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get fraud case trends over time."""
    svc = AnalyticsService(db)
    return await svc.get_fraud_trends(days=days)


@router.get("/analytics/document-distribution")
async def get_document_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of documents by type."""
    svc = AnalyticsService(db)
    return await svc.get_document_distribution()


@router.get("/analytics/risk-distribution")
async def get_risk_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get case count by risk category."""
    svc = AnalyticsService(db)
    return await svc.get_risk_distribution()


@router.get("/analytics/processing-stats")
async def get_processing_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get processing time and fraud detection statistics."""
    svc = AnalyticsService(db)
    return await svc.get_processing_stats()
