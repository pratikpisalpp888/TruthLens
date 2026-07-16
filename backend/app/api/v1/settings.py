"""
TruthLens — Settings API (Admin only).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, require_role
from app.db.models.user import User
from app.core.config import settings as app_settings

router = APIRouter()

# In-memory risk thresholds (would live in DB in production)
_risk_thresholds = {
    "high_threshold": 50,
    "medium_threshold": 80,
    "weights": {
        "document_authenticity": 0.25,
        "cross_document_consistency": 0.25,
        "itr_validity": 0.25,
        "fraud_pattern_risk": 0.15,
        "compliance_risk": 0.10
    }
}


@router.get("/settings/risk-thresholds")
async def get_risk_thresholds(
    current_user: User = Depends(require_role(["admin"]))
):
    """Get current risk scoring thresholds (admin only)."""
    return _risk_thresholds


@router.put("/settings/risk-thresholds")
async def update_risk_thresholds(
    body: dict,
    current_user: User = Depends(require_role(["admin"]))
):
    """Update risk scoring thresholds (admin only)."""
    if "high_threshold" in body:
        _risk_thresholds["high_threshold"] = body["high_threshold"]
    if "medium_threshold" in body:
        _risk_thresholds["medium_threshold"] = body["medium_threshold"]
    if "weights" in body:
        _risk_thresholds["weights"].update(body["weights"])
    return {"message": "Thresholds updated", "current": _risk_thresholds}


@router.get("/settings/system-info")
async def get_system_info(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get system information: model versions, DB status, storage usage."""
    from app.rag.knowledge_loader import KnowledgeBaseLoader

    kb_loaded = False
    kb_count = 0
    try:
        loader = KnowledgeBaseLoader()
        kb_loaded = await loader.is_loaded()
        info = loader.qdrant.get_collection("knowledge_base")
        kb_count = info.points_count
    except Exception:
        pass

    fp_count = 0
    try:
        from app.services.fraud_dna_service import FraudDNAService
        svc = FraudDNAService()
        fp_info = svc.qdrant.get_collection("fraud_patterns")
        fp_count = fp_info.points_count
    except Exception:
        pass

    return {
        "platform": "TruthLens v1.0",
        "ollama_model": app_settings.OLLAMA_MODEL,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "ocr_engine": "PaddleOCR",
        "ner_model": "spaCy en_core_web_sm",
        "knowledge_base_indexed": kb_loaded,
        "knowledge_base_chunks": kb_count,
        "fraud_patterns_loaded": fp_count,
        "database": app_settings.DATABASE_URL.split("@")[-1],
        "minio_bucket": app_settings.MINIO_BUCKET,
    }
