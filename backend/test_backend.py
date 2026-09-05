"""
Quick smoke test — hits every key endpoint once, prints pass/fail.
Run this while `uvicorn app.main:app --reload` is running in another terminal.
"""
import urllib.request
import json
import sys

BASE = "http://127.0.0.1:8000"

def check(path, label):
    try:
        with urllib.request.urlopen(BASE + path, timeout=8) as r:
            data = json.loads(r.read())
            print(f"[PASS] {label}: {path}")
            print(f"   {json.dumps(data)[:140]}...")
            return True
    except Exception as e:
        print(f"[FAIL] {label}: {path}")
        print(f"   ERROR: {e}")
        return False

def check_post(path, payload, label):
    try:
        req = urllib.request.Request(
            BASE + path,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read())
            print(f"[PASS] {label}: {path}")
            print(f"   {json.dumps(data)[:140]}...")
            return True
    except Exception as e:
        print(f"[FAIL] {label}: {path}")
        print(f"   ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE = sys.argv[1].rstrip("/")

    print(f"Testing NidhiTrace backend at: {BASE}\n")
    results = []
    results.append(check("/health", "Health check"))
    results.append(check("/api/anomalies/summary/breakdown", "Breakdown"))
    results.append(check("/api/anomalies/?signal=high_severity&limit=3", "High severity list"))
    results.append(check("/api/anomalies/?signal=delay&limit=3", "Delay list"))
    results.append(check("/api/anomalies/?signal=amount&limit=3", "Amount list"))
    results.append(check("/api/anomalies/?signal=mp_drift&limit=3", "MP-drift list"))
    results.append(check("/api/works/?limit=3", "Works list"))
    results.append(check("/api/assistant/status", "Assistant Status"))
    results.append(check_post("/api/assistant/chat", {"message": "help", "pageContext": {"page": "overview"}}, "Assistant Chat"))

    print(f"\n{sum(results)}/{len(results)} passed")
    if sum(results) < len(results):
        sys.exit(1)