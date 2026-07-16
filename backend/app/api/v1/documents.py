"""
TruthLens — Documents API Endpoints.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, require_role
from app.db.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.repositories.document_repo import DocumentRepository
from app.utils.masking import apply_masking
from app.core.exceptions import ResourceNotFoundError

router = APIRouter()

@router.post("/cases/{case_id}/documents", response_model=List[DocumentResponse], status_code=status.HTTP_201_CREATED)
async def upload_documents(
    case_id: str,
    bg_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload multiple documents to a case."""
    service = DocumentService(db)
    docs = await service.upload_multiple(case_id, files, current_user.id, bg_tasks)
    return docs

@router.get("/cases/{case_id}/documents", response_model=List[DocumentResponse])
async def list_documents(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all documents for a case."""
    repo = DocumentRepository(db)
    docs = await repo.get_by_case(case_id)
    return docs

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document_metadata(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document metadata + extracted data (masked if officer)."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
        
    doc_dict = {
        "id": doc.id,
        "case_id": doc.case_id,
        "original_filename": doc.original_filename,
        "file_size": doc.file_size,
        "mime_type": doc.mime_type,
        "document_type": doc.document_type,
        "processing_status": doc.processing_status,
        "created_at": doc.created_at,
        "extracted_entities": doc.extracted_entities,
        "extracted_fields": doc.extracted_fields,
        "error_message": doc.error_message
    }
    
    masked_doc = apply_masking(doc_dict, current_user.role)
    return masked_doc

@router.get("/documents/{document_id}/download")
async def download_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Stream original document (decrypted)."""
    service = DocumentService(db)
    return await service.get_document_file(document_id, current_user.id)

@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "officer"]))
):
    """Soft delete document and remove from MinIO."""
    service = DocumentService(db)
    await service.delete_document(document_id, current_user.id)
    return None

@router.get("/documents/{document_id}/ocr-result")
async def get_ocr_result(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get raw OCR text."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
    return {"ocr_text": doc.ocr_text, "language_detected": doc.language_detected}

@router.get("/documents/{document_id}/entities")
async def get_entities(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get extracted NER entities."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
    
    entities = apply_masking(doc.extracted_entities or {}, current_user.role)
    return {"entities": entities}

@router.get("/documents/{document_id}/extracted-fields")
async def get_extracted_fields(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get structured fields specific to the document type."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
    
    fields = apply_masking(doc.extracted_fields or {}, current_user.role)
    return {"extracted_fields": fields}

@router.post("/documents/{document_id}/reprocess")
async def reprocess_document(
    document_id: str,
    bg_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Re-run the OCR/Classification/NER pipeline."""
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(document_id)
    if not doc:
        raise ResourceNotFoundError("Document not found")
        
    await repo.update(document_id, {"processing_status": "uploaded", "error_message": None})
    await db.commit()
    
    service = DocumentService(db)
    bg_tasks.add_task(service.process_pipeline_bg, doc.id, doc.file_path, doc.mime_type)
    
    return {"message": "Document queued for reprocessing"}
