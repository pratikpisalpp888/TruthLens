"""
TruthLens — RAG Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CRAGSource(BaseModel):
    file: str
    relevance: float

class CRAGResponse(BaseModel):
    answer: str
    sources: List[CRAGSource]
    retrieval_quality: str
    was_corrected: bool
    confidence: float

class FraudRing(BaseModel):
    ring_id: str
    connected_cases: List[str]
    shared_elements: Dict[str, str]
    suspicion_score: float

class RAGQuery(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None
