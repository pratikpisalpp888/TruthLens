"""
TruthLens — RAG __init__.
"""

# Lazy imports to avoid loading torch/sentence-transformers at startup
# (prevents Windows shm.dll crash on uvicorn startup)
def __getattr__(name):
    if name == "EmbeddingService":
        from app.rag.embeddings import EmbeddingService
        return EmbeddingService
    if name == "KnowledgeBaseLoader":
        from app.rag.knowledge_loader import KnowledgeBaseLoader
        return KnowledgeBaseLoader
    if name == "CRAGSystem":
        from app.rag.crag import CRAGSystem
        return CRAGSystem
    if name == "GraphRAGSystem":
        from app.rag.graph_rag import GraphRAGSystem
        return GraphRAGSystem
    raise AttributeError(f"module 'app.rag' has no attribute {name!r}")

__all__ = ["EmbeddingService", "KnowledgeBaseLoader", "CRAGSystem", "GraphRAGSystem"]
