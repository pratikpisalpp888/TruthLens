import asyncio
import uuid
from app.db.session import async_session_maker
from app.services.document_service import DocumentService

async def main():
    async with async_session_maker() as db:
        svc = DocumentService(db)
        doc_id = "a9bdb7d5-a948-4c32-bf7d-95a831860ad0" # From the last test
        # We don't have the file path easily, but it will fail before or at ocr_service
        # Let's see what happens
        await svc.process_pipeline_bg(doc_id, "documents/test_case/test_doc.pdf", "application/pdf")

if __name__ == "__main__":
    asyncio.run(main())
