"""
TruthLens — Fraud DNA Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class FeatureVector(BaseModel):
    structural: Dict[str, float]
    content: Dict[str, float]
    behavioral: Dict[str, float]

class DNASignature(BaseModel):
    vector: List[float]
    hash: str
    feature_summary: Dict[str, Any]
    document_id: str

class PatternMatch(BaseModel):
    matched_pattern_id: str
    similarity: float
    matched_case_id: str
    pattern_type: str
    description: str
    matched_features: List[str]

class VelocityResult(BaseModel):
    time_spread_hours: float
    suspicious: bool
    detail: str
    severity: str

class NetworkAnalysis(BaseModel):
    case_id: str
    connected_cases: int
    fraud_rings_detected: int
    shared_elements: List[str]
    network_risk_score: float
    graph_data: Dict[str, Any]
