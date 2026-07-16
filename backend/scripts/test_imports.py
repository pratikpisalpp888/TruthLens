import sys
print("Importing OCRService...")
try:
    from app.services.ocr_service import OCRService
    print("OCRService imported successfully")
except Exception as e:
    print(f"OCRService failed: {type(e).__name__}: {e}")

print("\nImporting NERService...")
try:
    from app.services.ner_service import NERService
    print("NERService imported successfully")
except Exception as e:
    print(f"NERService failed: {type(e).__name__}: {e}")

print("\nImporting FraudDNAService...")
try:
    from app.services.fraud_dna_service import FraudDNAService
    print("FraudDNAService imported successfully")
except Exception as e:
    print(f"FraudDNAService failed: {type(e).__name__}: {e}")
