"""
TruthLens — ITR Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class FormatResult(BaseModel):
    valid: bool
    checks: Dict[str, Any]
    issues: List[str]

class ComputationDeviation(BaseModel):
    field: str
    declared: float
    max_allowed: Optional[float] = None
    computed: Optional[float] = None
    excess: Optional[float] = None
    severity: str
    description: str

class ComputationResult(BaseModel):
    valid: bool
    computed_values: Dict[str, Any]
    declared_values: Dict[str, Any]
    deviations: List[ComputationDeviation]

class BankCrossResult(BaseModel):
    income_deviation_percent: float
    itr_income: float
    bank_credits: float
    unexplained_deposits: List[Any]
    tds_match: bool
    severity: str

class BehaviorResult(BaseModel):
    income_trend: str
    yoy_change_percent: float
    deduction_ratio: float
    risk_indicators: List[str]

class ITRReportResponse(BaseModel):
    document_id: str
    validity_score: float
    form_type: Optional[str] = None
    assessment_year: Optional[str] = None
    sub_reports: Dict[str, Any]
    critical_issues: List[str]
    processing_time_ms: int
