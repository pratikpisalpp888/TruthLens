"""
TruthLens — Document Viewer & Annotations API.

Enhanced: Now also returns text-based rule signals as annotatable regions
so the viewer can show ALL fraud findings, not just pixel-level ones.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.db.models.document import Document
from app.db.models.analysis import AnalysisResult
from app.services.storage_service import StorageService
from app.utils.encryption import decrypt_file
from app.core.config import settings

router = APIRouter()
storage = StorageService()


@router.get("/documents/{document_id}/annotations")
async def get_document_annotations(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns visual anomaly bounding boxes for the document viewer.
    Combines:
      1. Pixel-level ELA anomaly regions (from ForensicsService)
      2. Text-based rule signals (from ForensicAgent) converted to approximate regions
    """
    stmt = select(AnalysisResult).where(
        AnalysisResult.document_id == document_id,
        AnalysisResult.analysis_type == "forensics"
    )
    result = await db.execute(stmt)
    analysis = result.scalar_one_or_none()

    if not analysis:
        return {"anomaly_regions": []}

    evidence = analysis.evidence_paths or {}
    regions = list(evidence.get("anomaly_regions", []))

    # Also include text-based rule signals as page-level highlighted regions
    # These don't have pixel coords but we can create banner-style annotations
    # placed at the top of page 1 as visual indicators
    findings = analysis.findings or {}
    rule_signals = []

    # Try to pull from the forensic findings stored in the DB
    for key, val in findings.items():
        if key == "rule_signals" and isinstance(val, list):
            rule_signals = val
            break

    # Convert rule signals to visible annotation regions (stacked at top of page)
    Y_OFFSET = 20  # Start Y position
    for i, sig in enumerate(rule_signals[:8]):  # Max 8 text signals shown
        regions.append({
            "page": 1,
            "x": 20,
            "y": Y_OFFSET + (i * 60),
            "width": 555,
            "height": 50,
            "severity": sig.get("severity", "medium"),
            "label": sig.get("type", "fraud_signal").replace("_", " ").title(),
            "reason": sig.get("description", "Fraud signal detected"),
        })

    return {"anomaly_regions": regions}


@router.get("/documents/{document_id}/preview")
async def get_document_preview(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the raw decrypted document bytes (PDF or Image) for the React viewer.
    """
    doc = await db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        encrypted_bytes = await storage.download(doc.file_path)
        decrypted_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)

        return StreamingResponse(
            io.BytesIO(decrypted_bytes),
            media_type=doc.mime_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
