import asyncio
import httpx
import sys
import json
import os
import time

BASE_URL = "http://localhost:8000/api/v1"

async def test_full_pipeline():
    print("--- TRUTHLENS BRUTAL END-TO-END TEST ---")
    
    # We need a dummy pdf file
    with open("dummy_test.pdf", "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Title (Dummy)\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>\n%%EOF")
        
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 0. Authenticate
        print("0. Authenticating...")
        auth_payload = {"username": "officer@truthlens.ai", "password": "officer123"}
        res = await client.post(f"{BASE_URL}/auth/login", data=auth_payload)
        if res.status_code >= 400:
            print(f"FAILED to authenticate: {res.text}")
            sys.exit(1)
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Authenticated")
        
        # 1. Create Case
        print("\n1. Creating Case...")
        case_payload = {
            "applicant_name": "Brutal Test Applicant",
            "loan_type": "Personal Loan",
            "loan_amount": 500000.0,
            "description": "Automated E2E Test"
        }
        res = await client.post(f"{BASE_URL}/cases", json=case_payload, headers=headers)
        if res.status_code >= 400:
            print(f"FAILED to create case: {res.text}")
            sys.exit(1)
            
        case_id = res.json()["id"]
        print(f"✅ Case Created: {case_id}")
        
        # 2. Upload Document
        print("\n2. Uploading Document...")
        with open("dummy_test.pdf", "rb") as f:
            files = {"files": ("dummy_test.pdf", f, "application/pdf")}
            res = await client.post(f"{BASE_URL}/cases/{case_id}/documents", files=files, headers=headers)
            if res.status_code >= 400:
                print(f"FAILED to upload doc: {res.text}")
                sys.exit(1)
        
        doc_id = res.json()[0]["id"]
        print(f"✅ Document Uploaded: {doc_id}")
        
        # 3. Trigger Analysis
        print("\n3. Triggering Full Orchestration Analysis...")
        res = await client.post(f"{BASE_URL}/cases/{case_id}/analyze", headers=headers)
        if res.status_code >= 400:
            print(f"FAILED to start analysis: {res.text}")
            sys.exit(1)
        
        print("✅ Analysis triggered. Waiting for completion...")
        
        # Poll for completion
        max_retries = 30
        for i in range(max_retries):
            res = await client.get(f"{BASE_URL}/cases/{case_id}", headers=headers)
            case_data = res.json()
            status = case_data.get("status")
            print(f"  ...status: {status} ({i+1}/{max_retries})")
            if status == "analyzed":
                break
            elif status == "failed":
                print("FAILED: Case analysis marked as failed.")
                sys.exit(1)
            await asyncio.sleep(2)
        else:
            print("FAILED: Analysis timed out.")
            sys.exit(1)
            
        print("✅ Analysis Completed successfully.")
        
        # 4. Check Annotations
        print("\n4. Checking Document Annotations API...")
        res = await client.get(f"{BASE_URL}/documents/{doc_id}/annotations", headers=headers)
        if res.status_code >= 400:
            print(f"FAILED Annotations API: {res.text}")
            sys.exit(1)
        print("✅ Annotations API successful")
        
        # 5. Check AI Report
        print("\n5. Checking CRAG AI Report API...")
        res = await client.get(f"{BASE_URL}/cases/{case_id}/ai-report", headers=headers)
        if res.status_code >= 400:
            print(f"FAILED AI Report API: {res.text}")
            sys.exit(1)
        print("✅ AI Report API successful")
        
        # 6. Check Syndicate
        print("\n6. Checking Syndicate Intelligence API...")
        res = await client.get(f"{BASE_URL}/cases/{case_id}/syndicate-connections", headers=headers)
        if res.status_code >= 400:
            print(f"FAILED Syndicate API: {res.text}")
            sys.exit(1)
        print("✅ Syndicate API successful")
        
        # 7. Check Case Chat
        print("\n7. Checking Case Chat API (Interrogator)...")
        chat_payload = {"message": "Why is this case flagged?"}
        res = await client.post(f"{BASE_URL}/cases/{case_id}/chat", json=chat_payload, headers=headers)
        if res.status_code >= 400:
            print(f"FAILED Chat API: {res.text}")
            sys.exit(1)
        print("✅ Chat API successful")
        
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! The pipeline is brutal-proof.")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
