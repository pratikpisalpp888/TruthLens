"""
TruthLens — Document Service.
"""

import uuid
from typing import List, AsyncGenerator
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from app.db.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.services.storage_service import StorageService
from app.services.audit_service import AuditService
from app.services.classification_service import DocumentClassifier
from app.utils.encryption import encrypt_file, decrypt_file, generate_file_hash
from app.utils.file_utils import validate_file, get_mime_type, get_page_count
from app.core.exceptions import ValidationException, ResourceNotFoundError
from app.core.config import settings

class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DocumentRepository(db)
        self.storage = StorageService()
        self.audit = AuditService(db)
    async def process_pipeline_bg(self, document_id: str, file_path: str, mime_type: str):
        """Background task chain: OCR -> Classify -> NER -> Extract."""
        print(f"DEBUG: Starting background task for {document_id}")
        import asyncio
        from app.db.session import async_session_maker
        from app.repositories.document_repo import DocumentRepository
        
        try:
            async with async_session_maker() as db:
                print("DEBUG: DB Session created")
                repo = DocumentRepository(db)
                try:
                    from app.services.ocr_service import OCRService
                    from app.services.ner_service import NERService
                    from app.extractors import get_extractor
                    
                    # 1. OCR
                    ocr_svc = OCRService()
                    ocr_res = await ocr_svc.extract_text(document_id, file_path, mime_type)
                    ocr_text = ocr_res["full_text"]
                    
                    await repo.update(document_id, {
                        "ocr_text": ocr_text,
                        "language_detected": ocr_res["language"],
                        "processing_status": "ocr_done"
                    })
                    await db.commit()
                    
                    # 2. Classify
                    doc_type, conf = DocumentClassifier.classify(text=ocr_text)
                    
                    await repo.update(document_id, {
                        "document_type": doc_type,
                        "classification_confidence": conf,
                        "processing_status": "classified"
                    })
                    await db.commit()
                    
                    # 3. NER (with timeout so it can't block forever)
                    try:
                        ner_svc = NERService()
                        ner_res = await asyncio.wait_for(
                            ner_svc.extract_entities(document_id, ocr_text),
                            timeout=60.0
                        )
                        entities = ner_res["entities"]
                    except (asyncio.TimeoutError, Exception) as ner_err:
                        import structlog
                        structlog.get_logger().warning(f"NER step failed/timed-out: {ner_err}")
                        entities = {}  # Continue pipeline with empty entities
                    
                    await repo.update(document_id, {
                        "extracted_entities": entities,
                    })
                    await db.commit()
                    
                    # 4. Extract specific fields
                    extractor = get_extractor(doc_type)
                    if extractor:
                        extracted_fields = await extractor.extract(document_id, ocr_text, entities)
                        await repo.update(document_id, {
                            "extracted_fields": extracted_fields,
                            "processing_status": "extracted"
                        })
                    else:
                        await repo.update(document_id, {
                            "processing_status": "extracted"
                        })
                    await db.commit()
                        
                except Exception as e:
                    await repo.update_processing_status(document_id, "error", str(e))
                    await db.commit()
        except Exception as outer_e:
            print(f"DEBUG: Background task crashed completely: {outer_e}")

    async def upload_document(self, case_id: str, file: UploadFile, user_id: str, bg_tasks: BackgroundTasks) -> Document:
        file_bytes = await file.read()
        
        if not validate_file(file, file_bytes):
            raise ValidationException("Invalid file type or size exceeded (10MB max).")
            
        file_hash = generate_file_hash(file_bytes)
        
        existing = await self.repo.get_all(filters={"file_hash": file_hash, "case_id": case_id})
        if existing:
            raise ValidationException("Duplicate document found in this case.")

        encrypted_bytes = encrypt_file(file_bytes, settings.ENCRYPTION_KEY)
        
        doc_uuid = str(uuid.uuid4())
        ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
        storage_path = f"documents/{case_id}/{doc_uuid}.{ext}"
        
        await self.storage.ensure_bucket()
        await self.storage.upload(storage_path, encrypted_bytes)
        
        mime = get_mime_type(file_bytes)
        
        doc = await self.repo.create({
            "id": doc_uuid,
            "case_id": case_id,
            "original_filename": file.filename,
            "stored_filename": f"{doc_uuid}.{ext}",
            "file_path": storage_path,
            "file_hash": file_hash,
            "file_size": len(file_bytes),
            "mime_type": mime,
            "page_count": get_page_count(file_bytes, mime),
            "processing_status": "uploaded"
        })
        
        await self.audit.log(user_id, "document.uploaded", "document", doc.id, {"case_id": case_id})
        
        # Trigger background processing pipeline
        bg_tasks.add_task(self.process_pipeline_bg, doc.id, storage_path, mime)
        
        return doc

    async def upload_multiple(self, case_id: str, files: List[UploadFile], user_id: str, bg_tasks: BackgroundTasks) -> List[Document]:
        uploaded_docs = []
        for file in files:
            doc = await self.upload_document(case_id, file, user_id, bg_tasks)
            uploaded_docs.append(doc)
        return uploaded_docs

    async def get_document_file(self, document_id: str, user_id: str) -> StreamingResponse:
        doc = await self.repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundError("Document not found")
            
        encrypted_bytes = await self.storage.download(doc.file_path)
        decrypted_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)
        
        await self.audit.log(user_id, "document.accessed", "document", document_id)
        
        async def file_streamer() -> AsyncGenerator[bytes, None]:
            chunk_size = 8192
            for i in range(0, len(decrypted_bytes), chunk_size):
                yield decrypted_bytes[i:i + chunk_size]
                
        return StreamingResponse(
            file_streamer(), 
            media_type=doc.mime_type,
            headers={"Content-Disposition": f"inline; filename={doc.original_filename}"}
        )

    async def delete_document(self, document_id: str, user_id: str) -> bool:
        doc = await self.repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundError("Document not found")
            
        await self.storage.delete(doc.file_path)
        deleted = await self.repo.delete(document_id)
        
        if deleted:
            await self.audit.log(user_id, "document.deleted", "document", document_id)
        return deleted
