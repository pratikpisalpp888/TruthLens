"""TruthLens Extractors."""

from app.extractors.base_extractor import BaseExtractor
from app.extractors.itr_extractor import ITRExtractor
from app.extractors.sale_deed_extractor import SaleDeedExtractor
from app.extractors.bank_statement_extractor import BankStatementExtractor
from app.extractors.land_record_extractor import LandRecordExtractor

def get_extractor(document_type: str) -> BaseExtractor:
    if document_type == "itr":
        return ITRExtractor()
    elif document_type == "sale_deed":
        return SaleDeedExtractor()
    elif document_type == "bank_statement":
        return BankStatementExtractor()
    elif document_type == "land_record":
        return LandRecordExtractor()
    return None

__all__ = [
    "BaseExtractor",
    "ITRExtractor",
    "SaleDeedExtractor",
    "BankStatementExtractor",
    "LandRecordExtractor",
    "get_extractor"
]
