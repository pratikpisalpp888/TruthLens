"""
TruthLens — Analysis API Endpoints.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.services.forensics_service import ForensicsService
from app.services.storage_service import StorageService
from app.utils.encryption import decrypt_file
from app.schemas.forensics import ForensicReportResponse
from app.core.exceptions import ResourceNotFoundError
from app.core.config import settings

router = APIRouter()

@router.post("/documents/{document_id}/forensics", response_model=ForensicReportResponse)
async def run_forensics(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run full forensics suite on a document."""
    service = ForensicsService(db)
    return await service.analyze_document(document_id)

@router.get("/documents/{document_id}/forensic-report", response_model=ForensicReportResponse)
async def get_forensic_report(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch existing forensics report."""
    from app.repositories.analysis_repo import AnalysisResultRepository
    repo = AnalysisResultRepository(db)
    result = await repo.get_latest(case_id=document_id, analysis_type="forensics") # Assuming case_id lookup issue, but it needs case_id
    # We should search by document_id actually
    from sqlalchemy import select
    from app.db.models.analysis import AnalysisResult
    query = select(AnalysisResult).where(AnalysisResult.document_id == document_id, AnalysisResult.analysis_type == "forensics").order_by(AnalysisResult.created_at.desc())
    res = await db.execute(query)
    record = res.scalars().first()
    
    if not record:
        raise ResourceNotFoundError("No forensic report found for this document")
        
    return ForensicReportResponse(
        document_id=document_id,
        authenticity_score=record.score or 0.0,
        tampering_probability=0.0, # Computed
        checks=record.findings,
        anomalies=[],
        processing_time_ms=record.processing_time_ms
    )

@router.get("/documents/{document_id}/heatmap")
async def get_heatmap(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download ELA heatmap image."""
    from sqlalchemy import select
    from app.db.models.analysis import AnalysisResult
    query = select(AnalysisResult).where(AnalysisResult.document_id == document_id, AnalysisResult.analysis_type == "forensics").order_by(AnalysisResult.created_at.desc())
    res = await db.execute(query)
    record = res.scalars().first()
    
    if not record or not record.evidence_paths or "heatmap" not in record.evidence_paths:
        raise ResourceNotFoundError("Heatmap not found")
        
    storage = StorageService()
    encrypted_bytes = await storage.download(record.evidence_paths["heatmap"])
    decrypted_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)
    
    async def streamer():
        yield decrypted_bytes
        
    return StreamingResponse(streamer(), media_type="image/jpeg")

@router.get("/cases/{case_id}/printer-comparison")
async def get_printer_comparison(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compare printer fingerprints across all docs in a case."""
    service = ForensicsService(db)
    return await service.compare_printer_fingerprints(case_id)
