# Kiến trúc hệ thống

## Luồng traffic

```
Internet
   │
   ▼
┌──────────────┐
│   Traefik    │  :80 (web) / :8080 (dashboard)
│   Gateway    │  Routing theo Host header
└──────┬───────┘
       │  network: web
       ▼
┌──────────────┐
│    NGINX     │  :80 (internal)
│  Performance │  Cache, Rate Limit, Gzip, Buffering
└──────┬───────┘
       │  network: internal
       ▼
┌──────────────┐
│  Express App │  :3000 (internal only)
│   Backend    │  Không expose ra ngoài
└──────────────┘
```

## Network topology

Hệ thống sử dụng **2 Docker networks** để tách biệt:

| Network | Services | Mục đích |
|---------|----------|----------|
| `web` | Traefik, NGINX | Public-facing, nhận traffic từ ngoài |
| `internal` | NGINX, App | Private, chỉ NGINX mới gọi được App |

::: tip Bảo mật
App **không nằm trên network `web`** → không thể truy cập trực tiếp từ bên ngoài. Mọi request buộc phải đi qua Traefik → NGINX.
:::

## Vai trò từng thành phần

### Traefik — Gateway Layer

- **Entrypoints**: Lắng nghe port `80` (web) và `8080` (dashboard)
- **Routing**: Dựa vào `Host` header để route traffic đến NGINX
- **Provider**:
  - **Linux (prod)**: Docker provider — tự đọc labels từ container
  - **Windows (dev)**: File provider — đọc từ `traefik-dynamic.yml`

### NGINX — Performance Layer

NGINX đứng giữa Traefik và App, xử lý 4 tính năng chính:

| Tính năng | Cấu hình | Mô tả |
|-----------|----------|-------|
| **Cache** | `proxy_cache my_cache` | Cache `/api/` response, giảm tải backend |
| **Rate Limit** | `limit_req 10r/s burst=5` | Chống abuse, bảo vệ API |
| **Gzip** | `gzip on; level=5` | Nén response > 256 bytes |
| **Buffering** | `proxy_buffering on; 8×16k` | Buffer response từ upstream |

### Express App — Application Layer

- Server đơn giản chạy port `3000`
- Endpoint `/` → HTML response
- Endpoint `/api` → JSON response `{ time: ... }`
- **Không expose port ra ngoài** → an toàn

## Compose file strategy

Dự án dùng **Docker Compose override pattern** để hỗ trợ đa môi trường:

```
docker-compose.yml              ← Base (luôn load)
docker-compose.override.yml     ← Dev (tự động load)
docker-compose.prod.yml         ← Prod (chỉ định thủ công)
```

| Môi trường | Compose files | Traefik provider |
|------------|---------------|------------------|
| **Dev (Windows)** | `yml` + `override.yml` | File provider |
| **Prod (Linux)** | `yml` + `prod.yml` | Docker provider |
