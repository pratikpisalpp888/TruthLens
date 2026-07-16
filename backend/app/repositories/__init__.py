"""TruthLens Repositories."""

from app.repositories.user_repo import UserRepository
from app.repositories.case_repo import CaseRepository
from app.repositories.document_repo import DocumentRepository
from app.repositories.analysis_repo import AnalysisResultRepository
from app.repositories.fraud_pattern_repo import FraudPatternRepository
from app.repositories.audit_log_repo import AuditLogRepository

__all__ = [
    "UserRepository",
    "CaseRepository",
    "DocumentRepository",
    "AnalysisResultRepository",
    "FraudPatternRepository",
    "AuditLogRepository"
]
