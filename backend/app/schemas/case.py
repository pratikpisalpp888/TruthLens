"""
TruthLens — Case Pydantic Schemas.

Request/response models for case management.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

class CaseBase(BaseModel):
    applicant_name: str = Field(min_length=2, max_length=255)
    loan_type: str
    loan_amount: float
    status: str = Field(default="created")
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    decision: Optional[str] = None
    decision_reason: Optional[str] = None

class CaseCreate(BaseModel):
    applicant_name: str
    loan_type: str
    loan_amount: float

class CaseUpdate(BaseModel):
    status: Optional[str] = None
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    decision: Optional[str] = None
    decision_reason: Optional[str] = None

class CaseResponse(CaseBase):
    id: str
    case_number: str
    officer_id: Optional[str] = None
    analysis_started_at: Optional[datetime] = None
    analysis_completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseSummary(BaseModel):
    id: str
    case_number: str
    applicant_name: str
    loan_type: str
    loan_amount: float
    status: str
    risk_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
