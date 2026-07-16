import asyncio
import httpx
import os
import time

BASE_URL = "http://localhost:8000/api/v1"

async def test_pipeline():
    print("Testing TruthLens Backend Pipeline...")
    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Login
        print("Logging in...")
        resp = await client.post(f"{BASE_URL}/auth/login", data={
            "username": "admin@truthlens.ai",
            "password": "admin123"
        })
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return
        
        token = resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create a Case
        print("Creating a new case...")
        resp = await client.post(f"{BASE_URL}/cases", json={
            "applicant_name": "John Doe Test",
            "loan_type": "home_loan",
            "loan_amount": 5000000
        }, headers=headers)
        
        if resp.status_code != 201:
            print(f"Failed to create case: {resp.status_code} {resp.text}")
            return
            
        case = resp.json()
        case_id = case["id"]
        print(f"Created case ID: {case_id} (Number: {case.get('case_number')})")
        
        # 3. Create a dummy test file
        test_file_path = "test_doc.pdf"
        with open(test_file_path, "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<< /Title (Test Document) >>\nendobj\n")
            
        # 4. Upload Document
        print("Uploading document...")
        with open(test_file_path, "rb") as f:
            files = {"files": ("test_doc.pdf", f, "application/pdf")}
            resp = await client.post(f"{BASE_URL}/cases/{case_id}/documents", files=files, headers=headers)
            
        if resp.status_code != 201:
            print(f"Failed to upload document: {resp.status_code} {resp.text}")
            return
            
        docs = resp.json()
        doc_id = docs[0]["id"]
        # 5. Poll for processing completion (resilient to server restarts)
        print(f"Uploaded document ID: {doc_id}. Waiting for processing...")
        final_status = None
        for attempt in range(15):
            await asyncio.sleep(2)
            try:
                resp = await client.get(f"{BASE_URL}/documents/{doc_id}", headers=headers)
                if resp.status_code == 200:
                    doc_status = resp.json()
                    status_val = doc_status.get("processing_status")
                    print(f"  [{attempt+1}] Status: {status_val}")
                    final_status = status_val
                    if status_val in ["completed", "extracted", "failed", "error", "ner_done"]:
                        break
                else:
                    print(f"  [{attempt+1}] HTTP {resp.status_code}, retrying...")
            except Exception as e:
                print(f"  [{attempt+1}] Connection error (server restarting?): {e}")
                await asyncio.sleep(3)  # wait extra for server to come back

        print(f"\n{'='*50}")
        print(f"Pipeline Test Result: {final_status or 'timeout'}")
        if final_status in ["completed", "extracted"]:
            print("[PASS] Pipeline completed SUCCESSFULLY!")
        elif final_status == "error":
            # Get error details
            try:
                resp = await client.get(f"{BASE_URL}/documents/{doc_id}", headers=headers)
                err = resp.json().get("error_message", "unknown error")
                print(f"[FAIL] Pipeline FAILED with error: {err}")
            except Exception as e2:
                print(f"[FAIL] Pipeline FAILED (could not fetch details): {e2}")
        else:
            print(f"[WARN] Pipeline ended with status: {final_status}")
        print(f"{'='*50}")
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    asyncio.run(test_pipeline())
