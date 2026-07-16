"""
TruthLens — Performance Benchmark Script.
"""

import asyncio
import time
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def run_benchmark():
    print("=" * 60)
    print(" TruthLens — Performance Benchmark")
    print("=" * 60)

    import httpx

    base = "http://localhost:8000/api/v1"
    results = {}

    # ── Login ────────────────────────────────────────────────────
    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{base}/auth/login",
                              data={"username": "admin@canara.bank", "password": "Admin@TruthLens123"})
        if r.status_code != 200:
            print(f"❌ Login failed: {r.text}")
            return
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    results["login_ms"] = round((time.time() - t0) * 1000)
    print(f"\n[1] Login:          {results['login_ms']} ms ✅")

    # ── Create Case ──────────────────────────────────────────────
    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{base}/cases", headers=headers, json={
            "applicant_name": "Benchmark Test User",
            "loan_type": "home_loan",
            "loan_amount": 5000000
        })
        if r.status_code not in (200, 201):
            print(f"❌ Create case failed: {r.text}")
            return
        case_id = r.json()["id"]
    results["create_case_ms"] = round((time.time() - t0) * 1000)
    print(f"[2] Create case:    {results['create_case_ms']} ms ✅  ID={case_id}")

    # ── Trigger Analysis ─────────────────────────────────────────
    t0 = time.time()
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{base}/cases/{case_id}/analyze", headers=headers)
        if r.status_code not in (200, 202):
            print(f"❌ Analysis trigger failed: {r.text}")
        else:
            # Poll for completion
            for _ in range(20):
                await asyncio.sleep(3)
                status_r = await client.get(f"{base}/cases/{case_id}/analysis-status", headers=headers)
                if status_r.json().get("status") == "completed":
                    break
    results["full_analysis_ms"] = round((time.time() - t0) * 1000)
    print(f"[3] Full analysis:  {results['full_analysis_ms']} ms")

    # ── Get Report ───────────────────────────────────────────────
    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{base}/cases/{case_id}/full-report", headers=headers)
    results["get_report_ms"] = round((time.time() - t0) * 1000)
    print(f"[4] Get report:     {results['get_report_ms']} ms")

    # ── Download PDF ─────────────────────────────────────────────
    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{base}/cases/{case_id}/report/pdf", headers=headers)
    results["pdf_download_ms"] = round((time.time() - t0) * 1000)
    print(f"[5] PDF download:   {results['pdf_download_ms']} ms  (size={len(r.content)} bytes)")

    total = sum(results.values())
    results["total_ms"] = total

    print("\n" + "=" * 60)
    print(f" TOTAL TIME: {total} ms  ({total/1000:.1f} seconds)")
    target = 90_000
    if total < target:
        print(f" ✅ PASS — Under {target/1000}s target")
    else:
        print(f" ⚠️  SLOW — Exceeds {target/1000}s target by {(total - target)/1000:.1f}s")
    print("=" * 60)

    # Save benchmark results
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to benchmark_results.json")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
