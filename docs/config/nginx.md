# NGINX Performance Layer

NGINX đứng giữa Traefik và App, cung cấp 4 tính năng performance chính.

## Tổng quan `nginx.conf`

```nginx
events {}

http {
  upstream backend {
    server app:3000;
  }

  # Cache, Rate Limit, Gzip config ở đây...

  server {
    listen 80;
    # Buffering, Proxy headers ở đây...

    location / { ... }
    location /api/ { ... }
  }
}
```

## 1. Cache

Cache response từ backend để giảm tải.

```nginx
proxy_cache_path /tmp/cache levels=1:2 keys_zone=my_cache:10m max_size=100m inactive=60m;

location /api/ {
  proxy_cache my_cache;
  proxy_cache_valid 200 10m;      # Cache 200 OK trong 10 phút
  proxy_cache_valid 404 1m;       # Cache 404 trong 1 phút
  proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
  add_header X-Cache-Status $upstream_cache_status;
}
```

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `keys_zone` | `my_cache:10m` | 10MB metadata cho cache keys |
| `max_size` | `100m` | Tối đa 100MB cache trên disk |
| `inactive` | `60m` | Xoá cache không dùng sau 60 phút |
| `proxy_cache_valid 200` | `10m` | Response 200 cache 10 phút |

Header `X-Cache-Status` cho biết:
- `MISS` — Chưa có cache, request gửi đến backend
- `HIT` — Trả từ cache, không gọi backend
- `EXPIRED` — Cache hết hạn
- `STALE` — Trả cache cũ khi backend lỗi

## 2. Rate Limit

Giới hạn số request/giây theo IP.

```nginx
# Định nghĩa zone
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=30r/s;

# Áp dụng
location / {
  limit_req zone=general_limit burst=20 nodelay;
}

location /api/ {
  limit_req zone=api_limit burst=5 nodelay;
}
```

| Zone | Rate | Burst | Áp dụng |
|------|------|-------|---------|
| `general_limit` | 30 req/s | 20 | Tất cả `/` |
| `api_limit` | 10 req/s | 5 | Chỉ `/api/` |

- **`rate=10r/s`**: Trung bình 10 request/giây
- **`burst=5`**: Cho phép burst thêm 5 request
- **`nodelay`**: Xử lý burst ngay, không delay
- Vượt quá → trả **503 Service Temporarily Unavailable**

## 3. Gzip Compression

Nén response để giảm bandwidth.

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_min_length 256;
gzip_comp_level 5;
gzip_types
  text/plain
  text/css
  application/json
  application/javascript
  text/xml
  application/xml
  application/xml+rss
  text/javascript;
```

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `gzip_min_length` | `256` | Chỉ nén response > 256 bytes |
| `gzip_comp_level` | `5` | Cân bằng CPU vs compression ratio |
| `gzip_vary` | `on` | Thêm `Vary: Accept-Encoding` header |
| `gzip_proxied` | `any` | Nén cả response từ proxy |

::: tip
`gzip_comp_level 5` là sweet spot — level cao hơn tốn CPU nhưng nén không nhiều hơn đáng kể.
:::

## 4. Proxy Buffering

Buffer response từ upstream để giải phóng backend sớm hơn.

```nginx
proxy_buffering on;
proxy_buffer_size 8k;
proxy_buffers 8 16k;
proxy_busy_buffers_size 32k;
proxy_temp_file_write_size 64k;
```

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `proxy_buffer_size` | `8k` | Buffer cho response header |
| `proxy_buffers` | `8 × 16k` | 8 buffer, mỗi cái 16KB |
| `proxy_busy_buffers_size` | `32k` | Max gửi client trong khi đọc upstream |
| `proxy_temp_file_write_size` | `64k` | Max ghi temp file mỗi lần |

**Tại sao cần buffering?**

Không có buffering: NGINX giữ kết nối đến backend **cho đến khi client nhận hết** → lãng phí resource backend.

Có buffering: NGINX **đọc hết response từ backend** rồi tự gửi dần cho client → backend được giải phóng ngay.

## Proxy Headers

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Đảm bảo app nhận được thông tin client gốc (IP, protocol) dù request đi qua nhiều proxy.
