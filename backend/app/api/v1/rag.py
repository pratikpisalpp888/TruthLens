"""
TruthLens — RAG API Endpoints.
"""

from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, require_role
from app.db.models.user import User
from app.schemas.rag import CRAGResponse, RAGQuery
from app.services.rag_service import RAGService
from app.rag.knowledge_loader import KnowledgeBaseLoader

router = APIRouter()

@router.post("/rag/query", response_model=CRAGResponse)
async def query_rag(
    body: RAGQuery,
    current_user: User = Depends(get_current_user)
):
    """Ask a compliance or fraud question using the CRAG pipeline."""
    service = RAGService()
    return await service.answer_question(body.question, body.context)

@router.get("/rag/knowledge-base/status")
async def knowledge_base_status(
    current_user: User = Depends(require_role(["admin"]))
):
    """Check whether the knowledge base has been loaded into Qdrant."""
    loader = KnowledgeBaseLoader()
    loaded = await loader.is_loaded()
    return {"loaded": loaded}

@router.post("/rag/knowledge-base/reload", status_code=status.HTTP_202_ACCEPTED)
async def reload_knowledge_base(
    bg_tasks: BackgroundTasks,
    current_user: User = Depends(require_role(["admin"]))
):
    """Trigger a full reload of the knowledge base into Qdrant."""
    loader = KnowledgeBaseLoader()
    bg_tasks.add_task(loader.load_and_index)
    return {"message": "Knowledge base reload queued."}

@router.get("/rag/fraud-network/{case_id}")
async def get_fraud_network(
    case_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get the GraphRAG fraud network around a specific case."""
    service = RAGService()
    return await service.get_fraud_network_context(case_id)
