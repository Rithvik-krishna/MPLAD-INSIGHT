"""
NIDHI TRACE Sitewide Backend Audit & Verification Suite
Validates:
1. Live FastAPI Backend Routes on port 3000
2. SQLite Database Record Integrity & Anomaly Engine Coverage
3. Sitewide Frontend Integration with Backend Endpoints
4. Vercel Serverless Function Interfaces
"""

import sys
import os
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:3000"

def log_test(name, passed, detail=""):
    is_ok = bool(passed)
    mark = "PASS" if is_ok else "FAIL"
    print(f"[{mark}] {name} {('- ' + str(detail)) if detail else ''}")
    return is_ok

def run_sitewide_audit():
    print("=" * 70)
    print("   NIDHI TRACE GLOBAL BACKEND AUDIT & VERIFICATION REPORT")
    print("=" * 70)
    results = []

    # 1. Test Health
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/health", timeout=5)
        data = json.loads(req.read().decode())
        results.append(log_test("GET /health", req.status == 200 and data.get("status") == "ok", data))
    except Exception as e:
        results.append(log_test("GET /health", False, e))

    # 2. Test Anomaly Summary Breakdown
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/anomalies/summary/breakdown", timeout=5)
        data = json.loads(req.read().decode())
        has_metrics = data.get("total_works") == 198116 and data.get("flagged_count") == 25483
        results.append(log_test("GET /api/anomalies/summary/breakdown", req.status == 200 and has_metrics, f"Total Registered: {data.get('total_works')}, Flagged: {data.get('flagged_count')}, Critical: {data.get('critical_count')}"))
    except Exception as e:
        results.append(log_test("GET /api/anomalies/summary/breakdown", False, e))

    # 3. Test Anomaly Overview
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/anomalies/overview", timeout=5)
        data = json.loads(req.read().decode())
        has_kpis = data.get("totalRegisteredWorks") == 198116 and data.get("totalScannedWorks") == 171890
        results.append(log_test("GET /api/anomalies/overview", req.status == 200 and has_kpis, f"Coverage: {data.get('coveragePct')}%, Exposure: ₹{data.get('scrutinyExposureCr')} Cr"))
    except Exception as e:
        results.append(log_test("GET /api/anomalies/overview", False, e))

    # 4. Test Anomalies List
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/anomalies/?limit=10", timeout=5)
        data = json.loads(req.read().decode())
        results.append(log_test("GET /api/anomalies/ (General Flagged)", req.status == 200 and len(data) == 10, f"Fetched {len(data)} flagged works, top work: {data[0].get('work_id')}"))
    except Exception as e:
        results.append(log_test("GET /api/anomalies/", False, e))

    # 5. Test Anomaly Signals (Delay, Amount, MP Drift, Isolation Forest, High Severity)
    for signal in ["delay", "amount", "mp_drift", "isolation_forest", "high_severity"]:
        try:
            req = urllib.request.urlopen(f"{BASE_URL}/api/anomalies/?signal={signal}&limit=3", timeout=5)
            data = json.loads(req.read().decode())
            results.append(log_test(f"GET /api/anomalies/?signal={signal}", req.status == 200 and len(data) > 0, f"{len(data)} cases matching signal '{signal}'"))
        except Exception as e:
            results.append(log_test(f"GET /api/anomalies/?signal={signal}", False, e))

    # 6. Test Single Dossier Endpoint
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/anomalies/MPLAD-01515", timeout=5)
        data = json.loads(req.read().decode())
        has_dossier = data.get("work_id") == "MPLAD-01515" and data.get("explanation")
        results.append(log_test("GET /api/anomalies/MPLAD-01515", req.status == 200 and has_dossier, f"Score: {data.get('score')}, Explanation: {data.get('explanation')[:45]}..."))
    except Exception as e:
        results.append(log_test("GET /api/anomalies/MPLAD-01515", False, e))

    # 7. Test Works List Endpoint
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/works/?limit=10", timeout=5)
        data = json.loads(req.read().decode())
        results.append(log_test("GET /api/works/?limit=10", req.status == 200 and len(data) == 10, f"Returned {len(data)} works, first: {data[0].get('work_id')} ({data[0].get('title')[:30]}...)"))
    except Exception as e:
        results.append(log_test("GET /api/works/", False, e))

    # 8. Test Single Work Endpoint
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/works/MPLAD-01515", timeout=5)
        data = json.loads(req.read().decode())
        results.append(log_test("GET /api/works/MPLAD-01515", req.status == 200 and data.get("work_id") == "MPLAD-01515", f"Work: {data.get('work_id')}, State: {data.get('state')}, Sector: {data.get('sector') or data.get('work_category')}"))
    except Exception as e:
        results.append(log_test("GET /api/works/MPLAD-01515", False, e))

    # 9. Test Assistant Status & Chat
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/api/assistant/status", timeout=5)
        data = json.loads(req.read().decode())
        results.append(log_test("GET /api/assistant/status", req.status == 200 and data.get("status") in ("active", "online"), f"Status: {data.get('status')}, Mode: {data.get('mode')}, Model: {data.get('model')}"))
    except Exception as e:
        results.append(log_test("GET /api/assistant/status", False, e))

    # 10. Frontend Web Pages Verification
    pages = [
        "Overview_Dashboard.html",
        "index.html",
        "Flagged_Cases.html",
        "Data_Explorer.html",
        "Case_Details.html",
        "Analytics.html",
        "Geographic_Map.html",
        "screens/Overview_Dashboard.html",
        "screens/index.html",
        "screens/Flagged_Cases.html",
        "screens/Data_Explorer.html",
        "screens/Case_Details.html",
        "screens/Analytics.html",
        "screens/Geographic_Map.html"
    ]
    for page in pages:
        try:
            req = urllib.request.urlopen(f"{BASE_URL}/{page}", timeout=5)
            results.append(log_test(f"Serving {page}", req.status == 200))
        except Exception as e:
            results.append(log_test(f"Serving {page}", False, e))

    # 11. Vercel Serverless Handlers Verification
    vercel_handlers = [
        "api/works.py",
        "api/anomalies.py",
        "api/assistant/chat.py",
        "api/assistant/status.py"
    ]
    for h in vercel_handlers:
        results.append(log_test(f"Vercel handler exists: {h}", os.path.exists(h)))

    print("-" * 70)
    passed_count = sum(results)
    total_count = len(results)
    print(f"Audit Summary: {passed_count}/{total_count} verification checks passed ({passed_count/total_count*100:.1f}%).")
    print("=" * 70)
    return passed_count == total_count

if __name__ == "__main__":
    success = run_sitewide_audit()
    sys.exit(0 if success else 1)
