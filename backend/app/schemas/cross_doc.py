"""
TruthLens — Cross-Document Analysis Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class Mismatch(BaseModel):
    field: str
    type: str
    severity: str
    values: Optional[Dict[str, Any]] = None
    similarity_scores: Optional[Dict[str, Any]] = None
    deviation_percent: Optional[float] = None
    assessment: Optional[str] = None
    description: Optional[str] = None
    detail: Optional[str] = None

class CrossDocReportResponse(BaseModel):
    case_id: str
    consistency_score: float
    total_checks: int
    mismatches_found: int
    checks: Dict[str, List[Mismatch]]
    critical_findings: List[Mismatch]
    processing_time_ms: int
