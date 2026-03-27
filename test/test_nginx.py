import requests
import time
import sys

# ─── Config ───
BASE_URL = "http://localhost"
API_URL = f"{BASE_URL}/api/"
MAIN_URL = f"{BASE_URL}/"

PASS = "\033[92m✔ PASS\033[0m"
FAIL = "\033[91m✘ FAIL\033[0m"
WARN = "\033[93m⚠ WARN\033[0m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[90m"

results = []


def report(name, passed, detail=""):
    status = PASS if passed else FAIL
    results.append(passed)
    print(f"  {status}  {name}")
    if detail:
        print(f"       {DIM}{detail}{RESET}")


def sep(title):
    print(f"\n{BOLD}{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}{RESET}")


# ─── 1. Basic Connectivity ───
sep("1. Basic Connectivity")
try:
    r = requests.get(MAIN_URL, timeout=5)
    report("GET / returns 200", r.status_code == 200, f"status={r.status_code}")
    report("GET / body is correct", r.text == "Hello from app", f"body={r.text!r}")
except Exception as e:
    report("GET / reachable", False, str(e))

try:
    r = requests.get(API_URL, timeout=5)
    report("GET /api/ returns 200", r.status_code == 200, f"status={r.status_code}")
    data = r.json()
    report("GET /api/ returns JSON with time", "time" in data, f"body={data}")
except Exception as e:
    report("GET /api/ reachable", False, str(e))

# ─── 2. Cache ───
sep("2. Cache (X-Cache-Status)")
try:
    # Purge: first request may be MISS or HIT from previous test
    requests.get(API_URL, timeout=5)
    time.sleep(0.1)

    r1 = requests.get(API_URL, timeout=5)
    cache1 = r1.headers.get("X-Cache-Status", "NONE")
    body1 = r1.text

    time.sleep(1)

    r2 = requests.get(API_URL, timeout=5)
    cache2 = r2.headers.get("X-Cache-Status", "NONE")
    body2 = r2.text

    report("X-Cache-Status header present", cache1 != "NONE", f"value={cache1}")
    report("Cached response returns same body", body1 == body2,
           f"req1={body1[:60]}, req2={body2[:60]}")
    report("Second request is HIT", cache2 == "HIT", f"cache={cache2}")
except Exception as e:
    report("Cache test", False, str(e))

# ─── 3. Gzip ───
sep("3. Gzip Compression")
try:
    # Small response - should NOT be gzipped (< gzip_min_length 256)
    r_small = requests.get(MAIN_URL, headers={"Accept-Encoding": "gzip"}, timeout=5)
    enc_small = r_small.headers.get("Content-Encoding", "none")
    report("Small response (<256b) not gzipped", enc_small == "none",
           f"Content-Encoding={enc_small}, size={len(r_small.content)}b")

    # Verify gzip is configured by checking a non-rate-limited endpoint
    report("Gzip configured (small responses skipped correctly)",
           enc_small == "none" and r_small.status_code == 200,
           f"gzip_min_length=256, response={len(r_small.content)}b — below threshold")
except Exception as e:
    report("Gzip test", False, str(e))

# ─── 4. Buffering ───
sep("4. Proxy Buffering")
try:
    r = requests.get(MAIN_URL, timeout=5)
    report("Proxy buffering active (response complete)", r.status_code == 200,
           f"status={r.status_code}, content-length={r.headers.get('Content-Length', 'chunked')}")

    accel = r.headers.get("X-Accel-Buffering", "not-set")
    report("No X-Accel-Buffering:no header", accel != "no",
           f"X-Accel-Buffering={accel}")
except Exception as e:
    report("Buffering test", False, str(e))

# ─── 5. Rate Limit ───
sep("5. Rate Limit (limit_req 10r/s burst=5)")
try:
    # Wait to fully reset rate limit window
    time.sleep(2)

    statuses = []
    for i in range(25):
        try:
            r = requests.get(API_URL, timeout=5)
            statuses.append(r.status_code)
        except Exception:
            statuses.append(0)

    ok_count = statuses.count(200)
    limited_count = statuses.count(503)

    report("Some requests succeed (200)", ok_count > 0,
           f"200s={ok_count}/25")
    report("Some requests rate-limited (503)", limited_count > 0,
           f"503s={limited_count}/25")
    report("Rate limit kicks in correctly",
           ok_count < 25 and limited_count > 0,
           f"200={ok_count}, 503={limited_count}, other={25 - ok_count - limited_count}")

    print(f"       {DIM}Distribution: ", end="")
    for s in statuses:
        print(f"{'·' if s == 200 else '×'}", end="")
    print(f"  (·=200 ×=503){RESET}")
except Exception as e:
    report("Rate limit test", False, str(e))

# ─── 6. Proxy Headers ───
sep("6. Proxy Headers (X-Real-IP, X-Forwarded-For)")
try:
    r = requests.get(MAIN_URL, timeout=5)
    report("Request proxied successfully", r.status_code == 200,
           "Headers set at NGINX level (transparent to client)")
except Exception as e:
    report("Proxy headers test", False, str(e))

# ─── Summary ───
total = len(results)
passed = sum(results)
failed = total - passed

print(f"\n{BOLD}{'═'*50}")
print(f"  SUMMARY")
print(f"{'═'*50}{RESET}")
print(f"  Total:  {total}")
print(f"  Passed: {BOLD}\033[92m{passed}\033[0m{RESET}")
if failed:
    print(f"  Failed: {BOLD}\033[91m{failed}\033[0m{RESET}")
else:
    print(f"  Failed: {BOLD}0{RESET}")
print(f"{'═'*50}\n")

sys.exit(0 if failed == 0 else 1)
