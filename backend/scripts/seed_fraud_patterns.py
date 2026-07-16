"""
TruthLens — Seed Fraud Patterns.
"""

import asyncio
import sys
import os
import uuid

# Ensure imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.fraud_dna_service import FraudDNAService
from app.schemas.fraud_dna import FeatureVector

def seed_fraud_patterns():
    service = FraudDNAService()
    
    categories = [
        "income_inflation", 
        "property_forgery", 
        "identity_manipulation", 
        "coordinated_fraud", 
        "bank_statement_fraud", 
        "velocity_fraud"
    ]
    
    print("Seeding 30 fraud patterns into Qdrant...")
    
    total = 0
    for category in categories:
        for i in range(5):
            # Generate slight variations in vectors for each pattern
            struct = {
                "ela_max_intensity": 0.7 + (i * 0.05),
                "metadata_suspicious_software": 1.0 if i % 2 == 0 else 0.0,
            }
            content = {
                "numeric_density": 0.6 + (i * 0.02)
            }
            behav = {
                "document_creation_hour": 0.9 if category == "velocity_fraud" else 0.5
            }
            
            features = FeatureVector(
                structural=struct,
                content=content,
                behavioral=behav
            )
            
            doc_id = str(uuid.uuid4())
            case_id = str(uuid.uuid4())
            
            sig = service.generate_dna_signature(features, doc_id)
            service.store_pattern(sig, case_id, is_fraud=True, pattern_type=category)
            total += 1
            
    print(f"Successfully seeded {total} fraud patterns.")

if __name__ == "__main__":
    seed_fraud_patterns()
