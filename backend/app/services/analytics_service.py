"""
TruthLens — Analytics Service.
"""

import datetime
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from app.db.models.case import Case
from app.db.models.document import Document
from app.db.models.analysis import AnalysisResult


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_fraud_trends(self, days: int = 30) -> Dict[str, Any]:
        """Case counts grouped by risk_category over last N days."""
        since = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        q = select(
            func.date(Case.created_at).label("date"),
            Case.risk_category,
            func.count().label("count")
        ).where(Case.created_at >= since).group_by(
            func.date(Case.created_at), Case.risk_category
        ).order_by(func.date(Case.created_at))

        result = await self.db.execute(q)
        rows = result.fetchall()

        dates_set = sorted(set(str(r.date) for r in rows))
        data = {d: {"low": 0, "medium": 0, "high": 0} for d in dates_set}
        for r in rows:
            cat = r.risk_category or "medium"
            data[str(r.date)][cat] = data[str(r.date)].get(cat, 0) + r.count

        return {
            "dates": dates_set,
            "low": [data[d]["low"] for d in dates_set],
            "medium": [data[d]["medium"] for d in dates_set],
            "high": [data[d]["high"] for d in dates_set],
        }

    async def get_document_distribution(self) -> Dict[str, int]:
        """Count documents by document_type."""
        q = select(Document.document_type, func.count().label("count")).group_by(Document.document_type)
        result = await self.db.execute(q)
        return {row.document_type or "unknown": row.count for row in result.fetchall()}

    async def get_risk_distribution(self) -> Dict[str, int]:
        """Count cases by risk_category."""
        q = select(Case.risk_category, func.count().label("count")).group_by(Case.risk_category)
        result = await self.db.execute(q)
        return {row.risk_category or "unanalyzed": row.count for row in result.fetchall()}

    async def get_processing_stats(self) -> Dict[str, Any]:
        """Average analysis time, total cases, frauds detected."""
        total_cases = (await self.db.execute(select(func.count()).select_from(Case))).scalar() or 0
        fraud_cases = (await self.db.execute(
            select(func.count()).select_from(Case).where(Case.risk_category == "high")
        )).scalar() or 0
        avg_time = (await self.db.execute(
            select(func.avg(AnalysisResult.processing_time_ms)).select_from(AnalysisResult)
        )).scalar() or 0
        return {
            "total_cases": total_cases,
            "frauds_detected": fraud_cases,
            "avg_analysis_time_ms": round(avg_time, 0),
            "avg_analysis_time_seconds": round(avg_time / 1000, 1) if avg_time else 0,
            "fraud_rate_percent": round((fraud_cases / total_cases * 100), 1) if total_cases else 0
        }

    async def get_officer_stats(self, officer_id: str) -> Dict[str, Any]:
        """Cases handled by a specific officer."""
        total = (await self.db.execute(
            select(func.count()).select_from(Case).where(Case.officer_id == officer_id)
        )).scalar() or 0
        decided = (await self.db.execute(
            select(func.count()).select_from(Case).where(
                Case.officer_id == officer_id,
                Case.decided_by == officer_id
            )
        )).scalar() or 0
        return {
            "officer_id": officer_id,
            "total_cases": total,
            "decisions_made": decided,
        }

    async def get_dashboard_summary(self) -> Dict[str, Any]:
        """Combined dashboard data."""
        risk_dist = await self.get_risk_distribution()
        doc_dist = await self.get_document_distribution()
        proc_stats = await self.get_processing_stats()
        trends = await self.get_fraud_trends(days=7)
        return {
            "risk_distribution": risk_dist,
            "document_distribution": doc_dist,
            "processing_stats": proc_stats,
            "weekly_trends": trends,
        }
