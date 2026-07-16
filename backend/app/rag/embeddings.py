"""
TruthLens — Embedding Service.

Uses FastEmbed (BAAI/bge-small-en-v1.5) for robust, highly accurate, and extremely fast
in-process embeddings via ONNX. Outputs 384-dimensional dense vectors to match Qdrant schema.
No external APIs or heavy PyTorch dependencies required.
"""

import asyncio
from typing import List
import structlog
from fastembed import TextEmbedding

log = structlog.get_logger()

_embedder_instance = None


class EmbeddingService:
    """
    Embedding service utilizing FastEmbed for robust, dependency-light neural embeddings.
    """

    def __init__(self):
        global _embedder_instance
        if _embedder_instance is not None:
            self._model = _embedder_instance
            return

        # Initialize FastEmbed (downloads model weights on first run, caches locally)
        # BAAI/bge-small-en-v1.5 is standard, high quality, and 384-dimensional.
        try:
            log.info("Initializing FastEmbed (BAAI/bge-small-en-v1.5) ...")
            self._model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            _embedder_instance = self._model
            log.info("FastEmbed initialized successfully.")
        except Exception as e:
            log.error(f"Failed to initialize FastEmbed: {e}")
            raise RuntimeError("Embeddings pipeline failed to initialize. FastEmbed is required.") from e

    def encode(self, text: str) -> List[float]:
        """Encode a single string into a 384-dim embedding vector."""
        # FastEmbed's embed() returns a generator of numpy arrays.
        # We need a single list of floats for Qdrant.
        embeddings = list(self._model.embed([text]))
        return embeddings[0].tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode a batch of strings into embeddings."""
        embeddings = list(self._model.embed(texts))
        return [vec.tolist() for vec in embeddings]

    async def encode_async(self, text: str) -> List[float]:
        """Async-safe encode — runs CPU work in executor so it doesn't block event loop."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.encode, text)
