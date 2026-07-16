"""
TruthLens — Fraud DNA API Endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.services.fraud_dna_service import FraudDNAService
from app.schemas.fraud_dna import DNASignature, PatternMatch, VelocityResult, NetworkAnalysis

router = APIRouter()

@router.post("/documents/{document_id}/fraud-dna", response_model=DNASignature)
async def generate_fraud_dna(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Extract forensic features and generate a Fraud DNA signature."""
    service = FraudDNAService(db)
    features = await service.extract_forensic_features(document_id)
    sig = service.generate_dna_signature(features, document_id)
    # Store it for future pattern matching
    service.store_pattern(sig, case_id="unknown_case", is_fraud=False, pattern_type="unclassified")
    return sig

@router.get("/documents/{document_id}/fraud-dna-matches", response_model=List[PatternMatch])
async def get_fraud_dna_matches(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Find historical fraud patterns similar to this document."""
    service = FraudDNAService(db)
    features = await service.extract_forensic_features(document_id)
    sig = service.generate_dna_signature(features, document_id)
    matches = service.match_patterns(sig)
    return matches

@router.post("/cases/{case_id}/velocity-check", response_model=VelocityResult)
async def check_velocity(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check for suspicious document creation velocity in a case."""
    service = FraudDNAService(db)
    return await service.detect_document_velocity(case_id)

@router.get("/cases/{case_id}/fraud-network", response_model=NetworkAnalysis)
async def get_fraud_network(
    case_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze historical graph connections for a case."""
    service = FraudDNAService(db)
    return await service.analyze_fraud_network(case_id)

@router.get("/fraud-patterns")
async def list_fraud_patterns(
    current_user: User = Depends(get_current_user)
):
    """List all known fraud patterns from the vector database."""
    service = FraudDNAService()
    try:
        # Retrieve random samples (Qdrant doesn't have a simple select * without a vector, 
        # so we fetch via scroll)
        records, _ = service.qdrant.scroll(
            collection_name=service.collection_name,
            limit=50
        )
        return {"patterns": [r.payload for r in records]}
    except Exception:
        return {"patterns": []}
