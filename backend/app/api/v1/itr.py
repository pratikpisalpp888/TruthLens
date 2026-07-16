"""
TruthLens — ITR API Endpoints.
"""

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.services.itr_service import ITRValidationService
from app.schemas.itr import ITRReportResponse
from app.core.exceptions import ResourceNotFoundError
from app.repositories.document_repo import DocumentRepository

router = APIRouter()

@router.post("/standalone-scan", response_model=ITRReportResponse)
async def standalone_itr_scan(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Standalone ITR scan for the dedicated ITR Intelligence page.
    Reads the PDF/image bytes, runs OCR inline, then executes the full 7-layer 
    validation without creating any case/document DB records.
    """
    file_bytes = await file.read()

    # Step 1: OCR inline directly from bytes (no decryption or temp files)
    from app.services.ocr_service import OCRService
    
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "pdf"
    mime = "application/pdf" if ext == "pdf" else f"image/{ext}"
    
    ocr_svc = OCRService()
    ocr_result = await ocr_svc.extract_text_from_bytes(file_bytes, mime)
    ocr_text = ocr_result.get("full_text", "")

    # Step 2: Run 7-layer analysis directly on OCR text (no DB writes needed)
    itr_service = ITRValidationService(db)
    return await itr_service.validate_from_text(ocr_text)


@router.post("/documents/{document_id}/itr-validate", response_model=ITRReportResponse)
async def validate_itr(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run full ITR validation suite against an existing DB document."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
        
    service = ITRValidationService(db)
    return await service.validate(document_id, doc.case_id)

@router.get("/documents/{document_id}/itr-report", response_model=ITRReportResponse)
async def get_itr_report(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch existing ITR validation report."""
    from sqlalchemy import select
    from app.db.models.analysis import AnalysisResult
    
    query = select(AnalysisResult).where(
        AnalysisResult.document_id == document_id, 
        AnalysisResult.analysis_type.in_(["itr_verification", "itr_verification_7_layer"])
    ).order_by(AnalysisResult.created_at.desc())
    
    res = await db.execute(query)
    record = res.scalars().first()
    
    if not record:
        raise ResourceNotFoundError("No ITR validation report found for this document")
        
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    
    return ITRReportResponse(
        document_id=document_id,
        validity_score=record.score or 0.0,
        form_type=doc.extracted_fields.get("form_type") if doc and doc.extracted_fields else None,
        assessment_year=doc.extracted_fields.get("assessment_year") if doc and doc.extracted_fields else None,
        sub_reports=record.findings,
        critical_issues=[],
        processing_time_ms=record.processing_time_ms
    )
