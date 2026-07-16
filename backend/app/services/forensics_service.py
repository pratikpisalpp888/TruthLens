"""
TruthLens — Forensics Service Orchestrator.
"""

import time
import asyncio
import cv2
import numpy as np
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repo import DocumentRepository
from app.repositories.analysis_repo import AnalysisResultRepository
from app.services.storage_service import StorageService
from app.utils.encryption import decrypt_file, encrypt_file
from app.core.exceptions import ResourceNotFoundError
from app.core.config import settings

from app.forensics.ela import ErrorLevelAnalysis
from app.forensics.metadata import MetadataAnalyzer
from app.forensics.font_analysis import FontAnalyzer
from app.forensics.compression import CompressionAnalyzer
from app.forensics.printer_fingerprint import PrinterFingerprint
from app.forensics.signature_check import SignatureChecker
from app.forensics.itr_validator import validate_itr_data
from app.schemas.forensics import ForensicReportResponse, Anomaly

class ForensicsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.analysis_repo = AnalysisResultRepository(db)
        self.storage = StorageService()

    def _extract_text_regions(self, pdf_bytes: bytes) -> list:
        """Extract exact text bounding boxes using PyMuPDF (fitz)."""
        import fitz
        regions = []
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Extract words: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
                words = page.get_text("words")
                for w in words:
                    regions.append({
                        "page": page_num + 1,
                        "x": w[0],
                        "y": w[1],
                        "width": w[2] - w[0],
                        "height": w[3] - w[1],
                        "text": w[4]
                    })
            doc.close()
        except Exception as e:
            pass
        return regions

    async def analyze_document(self, document_id: str) -> ForensicReportResponse:
        start_time = time.time()
        
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundError("Document not found")
            
        encrypted_bytes = await self.storage.download(doc.file_path)
        decrypted_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)
        
        # Determine if it's PDF or Image
        is_pdf = doc.mime_type == "application/pdf"
        
        # Prepare image for CV analysis
        images = []
        if is_pdf:
            from app.utils.file_utils import pdf_to_images
            loop = asyncio.get_event_loop()
            pil_images = await loop.run_in_executor(None, pdf_to_images, decrypted_bytes)
            for pimg in pil_images:
                cv_img = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
                images.append(cv_img)
        else:
            nparr = np.frombuffer(decrypted_bytes, np.uint8)
            cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            images.append(cv_img)
            
        first_image = images[0] if images else None
        
        ela = ErrorLevelAnalysis()
        meta = MetadataAnalyzer()
        font = FontAnalyzer()
        comp = CompressionAnalyzer()
        printer = PrinterFingerprint()
        sig = SignatureChecker()
        
        # In a real app we'd use asyncio.gather for these CPU bound tasks wrapped in run_in_executor
        # Here we run sequentially for simplicity in the mockup structure
        
        ela_res = ela.analyze(first_image) if first_image is not None else {}
        
        if is_pdf:
            meta_res = meta.analyze_pdf(decrypted_bytes)
        else:
            meta_res = meta.analyze_image(decrypted_bytes)
            
        font_res = font.analyze(first_image, []) if first_image is not None else {}
        comp_res = comp.analyze(decrypted_bytes)
        print_res = printer.extract(first_image) if first_image is not None else {}
        
        if is_pdf:
            sig_res = sig.check_digital_signature(decrypted_bytes)
        else:
            sig_res = sig.detect_visual_signature(first_image) if first_image is not None else {}
            
        # Composite score
        # Base starts at 100
        score = 100.0
        
        # Penalties
        ela_prob = ela_res.get("tampering_probability", 0)
        score -= (ela_prob * 30.0) # ELA weight 0.30
        
        meta_anomalies = meta_res.get("anomalies", [])
        score -= (len(meta_anomalies) * 10.0) # Metadata penalty
        
        comp_score = comp_res.get("anomaly_score", 0)
        score -= (comp_score * 15.0) # Compression weight 0.15
        
        authenticity_score = max(0.0, score)
        tampering_prob = 1.0 - (authenticity_score / 100.0)
        
        # Compile anomalies
        anomalies = []
        for a in meta_anomalies:
            anomalies.append(Anomaly(
                check_type="metadata",
                severity=a["severity"],
                description=a["detail"],
                confidence=a["confidence"]
            ))
            
        if ela_prob > 0.5:
            anomalies.append(Anomaly(
                check_type="ela",
                severity="high",
                description="High ELA intensity variance detected.",
                confidence=ela_prob
            ))

        # ── Visual Anomaly Regions ──
        anomaly_regions = []
        
        if is_pdf:
            text_regions = self._extract_text_regions(decrypted_bytes)
            
            # Simple heuristic extraction for ITR fields just to feed validator
            # In production, we'd use the NER service output here.
            extracted_fields = {}
            full_text = " ".join([r["text"] for r in text_regions])
            import re
            ack_match = re.search(r'\b\d{15}\b|\b\d{10}\b', full_text)
            if ack_match: extracted_fields["ack_number"] = ack_match.group(0)
            
            pan_match = re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', full_text)
            if pan_match: extracted_fields["pan_number"] = pan_match.group(0)
            
            ay_match = re.search(r'\b20\d{2}-\d{2}\b', full_text)
            if ay_match: extracted_fields["assessment_year"] = ay_match.group(0)

            # Validate against our ITR rules engine
            itr_findings = validate_itr_data(extracted_fields)
            
            # For each finding, find its bounding box in the PDF to highlight it
            for finding in itr_findings:
                val = str(finding["value"])
                for r in text_regions:
                    if val in r["text"]:
                        anomaly_regions.append({
                            "page": r["page"],
                            "x": r["x"],
                            "y": r["y"],
                            "width": r["width"],
                            "height": r["height"],
                            "severity": finding["severity"],
                            "label": finding["label"],
                            "reason": finding["reason"]
                        })
                        break # Only highlight the first instance
            
        # Save images
        heatmap_path = f"forensics/{doc.case_id}/{document_id}_heatmap.jpg"
        annotated_path = f"forensics/{doc.case_id}/{document_id}_annotated.jpg"
        
        if first_image is not None and "heatmap" in ela_res:
            heatmap_bytes = cv2.imencode('.jpg', ela_res["heatmap"])[1].tobytes()
            await self.storage.upload(heatmap_path, encrypt_file(heatmap_bytes, settings.ENCRYPTION_KEY))
            
            annotated_bytes = cv2.imencode('.jpg', ela_res["analysis_image"])[1].tobytes()
            await self.storage.upload(annotated_path, encrypt_file(annotated_bytes, settings.ENCRYPTION_KEY))
            
            # Clean up the large numpy arrays from the dict before saving to DB
            del ela_res["heatmap"]
            del ela_res["analysis_image"]
            
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Save to DB
        checks = {
            "ela": ela_res,
            "metadata": meta_res,
            "font": font_res,
            "compression": comp_res,
            "printer": print_res,
            "signature": sig_res
        }
        
        # Merge anomaly regions into evidence paths
        evidence_paths = {"heatmap": heatmap_path, "annotated": annotated_path, "anomaly_regions": anomaly_regions}
        
        await self.analysis_repo.create({
            "case_id": doc.case_id,
            "document_id": document_id,
            "analysis_type": "forensics",
            "findings": checks,
            "score": authenticity_score,
            "severity": "high" if tampering_prob > 0.6 else "low",
            "confidence": 0.9,
            "evidence_paths": evidence_paths,
            "processing_time_ms": processing_time_ms
        })
        await self.db.commit()
        
        return ForensicReportResponse(
            document_id=document_id,
            authenticity_score=authenticity_score,
            tampering_probability=tampering_prob,
            checks=checks,
            anomalies=anomalies,
            heatmap_path=heatmap_path,
            annotated_path=annotated_path,
            processing_time_ms=processing_time_ms
        )

    async def compare_printer_fingerprints(self, case_id: str) -> Dict[str, Any]:
        docs = await self.doc_repo.get_by_case(case_id)
        if not docs:
            return {"status": "no_documents"}
            
        fingerprints = []
        for doc in docs:
            # We would fetch from analysis results normally
            result = await self.analysis_repo.get_latest(doc.case_id, "forensics")
            if result and "printer" in result.findings:
                fp = result.findings["printer"].get("fingerprint_hash")
                if fp:
                    fingerprints.append({"document_id": doc.id, "hash": fp})
                    
        return {"fingerprints": fingerprints}
