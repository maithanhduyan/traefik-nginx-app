# Test Suite

Dự án sử dụng Python script để kiểm tra toàn bộ tính năng NGINX.

## Chạy test

```bash
# Yêu cầu: requests library
pip install requests

# Chạy (đảm bảo docker compose đang up)
python test/test_nginx.py
```

## Các test case

### 1. Basic Connectivity

| Test | Mô tả |
|------|-------|
| GET `/` returns 200 | Traefik → NGINX → App hoạt động |
| GET `/` body correct | Response đúng `"Hello from app"` |
| GET `/api/` returns 200 | API endpoint hoạt động |
| GET `/api/` returns JSON | Response có field `time` |

### 2. Cache

| Test | Mô tả |
|------|-------|
| X-Cache-Status present | NGINX trả header cache status |
| Same body on cache HIT | Response giống nhau khi cache |
| Second request is HIT | Request thứ 2 lấy từ cache |

### 3. Gzip

| Test | Mô tả |
|------|-------|
| Small response not gzipped | Response < 256 bytes không nén |
| Gzip config active | Cấu hình gzip hoạt động đúng |

### 4. Buffering

| Test | Mô tả |
|------|-------|
| Response complete | Proxy buffering trả response đầy đủ |
| No X-Accel-Buffering:no | Buffering không bị disable |

### 5. Rate Limit

| Test | Mô tả |
|------|-------|
| Some requests 200 | Một số request được phép |
| Some requests 503 | Vượt limit → bị chặn |
| Distribution correct | Tỉ lệ pass/block hợp lý |

### 6. Proxy Headers

| Test | Mô tả |
|------|-------|
| Request proxied | Headers được set đúng ở NGINX |

## Output mẫu

```
──────────────────────────────────────────────────
  1. Basic Connectivity
──────────────────────────────────────────────────
  ✔ PASS  GET / returns 200
  ✔ PASS  GET / body is correct
  ✔ PASS  GET /api/ returns 200
  ✔ PASS  GET /api/ returns JSON with time

──────────────────────────────────────────────────
  2. Cache (X-Cache-Status)
──────────────────────────────────────────────────
  ✔ PASS  X-Cache-Status header present
  ✔ PASS  Cached response returns same body
  ✔ PASS  Second request is HIT

──────────────────────────────────────────────────
  3. Gzip Compression
──────────────────────────────────────────────────
  ✔ PASS  Small response (<256b) not gzipped
  ✔ PASS  Gzip configured (small responses skipped correctly)

──────────────────────────────────────────────────
  4. Proxy Buffering
──────────────────────────────────────────────────
  ✔ PASS  Proxy buffering active (response complete)
  ✔ PASS  No X-Accel-Buffering:no header

──────────────────────────────────────────────────
  5. Rate Limit (limit_req 10r/s burst=5)
──────────────────────────────────────────────────
  ✔ PASS  Some requests succeed (200)
  ✔ PASS  Some requests rate-limited (503)
  ✔ PASS  Rate limit kicks in correctly
       Distribution: ······××·×××××××××·×××××·×

──────────────────────────────────────────────────
  6. Proxy Headers (X-Real-IP, X-Forwarded-For)
──────────────────────────────────────────────────
  ✔ PASS  Request proxied successfully

══════════════════════════════════════════════════
  SUMMARY: 15/15 PASSED
══════════════════════════════════════════════════
```
