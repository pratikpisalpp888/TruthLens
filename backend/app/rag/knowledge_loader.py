"""
TruthLens — Knowledge Base Loader.
"""

import os
import uuid
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.core.config import settings

class KnowledgeBaseLoader:
    def __init__(self):
        self.qdrant = QdrantClient(path=settings.QDRANT_PATH)
        try:
            from app.rag.embeddings import EmbeddingService
            self.embedder = EmbeddingService()
        except Exception as e:
            import structlog
            structlog.get_logger().warning(f"EmbeddingService unavailable in KnowledgeLoader: {e}")
            self.embedder = None
        self.collection_name = "knowledge_base"
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.qdrant.get_collection(self.collection_name)
        except Exception:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> list:
        """Simple recursive character text splitter approximation."""
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += (chunk_size - overlap)
            if i >= len(words):
                break
        return chunks

    async def load_and_index(self):
        """Read all markdown files from data/knowledge_base and index to Qdrant."""
        base_dir = "data/knowledge_base"
        if not os.path.exists(base_dir):
            return
            
        points = []
        for root, _, files in os.walk(base_dir):
            category = os.path.basename(root)
            for file in files:
                if not file.endswith(".md"):
                    continue
                    
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                chunks = self._chunk_text(content)
                title = file.replace(".md", "")
                
                # Encode chunks
                embeddings = self.embedder.encode_batch(chunks)
                
                for idx, (chunk_text, vector) in enumerate(zip(chunks, embeddings)):
                    points.append(
                        PointStruct(
                            id=str(uuid.uuid4()),
                            vector=vector,
                            payload={
                                "source_file": file,
                                "category": category,
                                "chunk_index": idx,
                                "full_document_title": title,
                                "text": chunk_text
                            }
                        )
                    )
                    
        # Upsert in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=batch
            )

    async def is_loaded(self) -> bool:
        """Check if Qdrant collection has expected count."""
        try:
            count = self.qdrant.count(collection_name=self.collection_name)
            return count.count > 0
        except Exception:
            return False
