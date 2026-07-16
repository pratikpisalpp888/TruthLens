"""
TruthLens — Analysis Pydantic Schemas.

Request/response models for forensic analysis operations.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

class AnalysisTriggerRequest(BaseModel):
    analysis_type: str = Field(default="forensics")
    document_ids: Optional[list[str]] = None
    force_rerun: bool = False

class RiskScoreBreakdown(BaseModel):
    forensic_score: Optional[float] = None
    cross_doc_score: Optional[float] = None
    itr_score: Optional[float] = None
    compliance_score: Optional[float] = None
    fraud_dna_score: Optional[float] = None

class AnalysisResponse(BaseModel):
    id: str
    case_id: str
    document_id: Optional[str] = None
    analysis_type: str
    status: str
    overall_risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    confidence_score: Optional[float] = None
    score_breakdown: Optional[RiskScoreBreakdown] = None
    anomalies: Optional[dict[str, Any]] = None
    flags: Optional[list[str]] = None
    recommendations: Optional[list[str]] = None
    matched_fraud_patterns: Optional[list[dict[str, Any]]] = None
    summary: Optional[str] = None
    report_url: Optional[str] = None
    report_generated: bool = False
    duration_seconds: Optional[float] = None
    agent_iterations: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class AnalysisSummary(BaseModel):
    id: str
    analysis_type: str
    status: str
    overall_risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    report_generated: bool
    created_at: datetime

class RAGQueryRequest(BaseModel):
    query: str = Field(min_length=5, max_length=1000)
    case_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    sources: list[dict[str, Any]]
    confidence: Optional[float] = None
    case_id: Optional[str] = None

