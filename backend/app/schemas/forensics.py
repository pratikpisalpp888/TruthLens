"""
TruthLens — Forensics Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class Anomaly(BaseModel):
    check_type: str
    severity: str
    description: str
    confidence: float
    evidence_path: Optional[str] = None

class ForensicReportResponse(BaseModel):
    document_id: str
    authenticity_score: float
    tampering_probability: float
    checks: Dict[str, Any]
    anomalies: List[Anomaly]
    heatmap_path: Optional[str] = None
    annotated_path: Optional[str] = None
    processing_time_ms: int
