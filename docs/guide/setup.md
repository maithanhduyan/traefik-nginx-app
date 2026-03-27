# Cài đặt & Chạy

## Yêu cầu

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) hoặc Docker Engine (Linux)
- Docker Compose v2+
- Python 3.x (để chạy test)

## Dev — Windows

```bash
# Clone project
cd traefik-nginx-app

# Khởi chạy (tự động load docker-compose.override.yml)
docker compose up -d
```

Docker Compose sẽ tự merge `docker-compose.yml` + `docker-compose.override.yml`:
- Traefik dùng **file provider** (đọc `traefik-dynamic.yml`)
- Không cần mount Docker socket

### Truy cập

| URL | Mô tả |
|-----|-------|
| http://localhost | App qua Traefik → NGINX |
| http://localhost/api/ | API endpoint (có cache) |
| http://localhost:8080 | Traefik Dashboard |

### Kiểm tra

```bash
# Test nhanh
curl http://localhost/
# → Hello from app

curl http://localhost/api/
# → {"time":"2026-03-27T..."}

# Test suite đầy đủ
python test/test_nginx.py
```

## Dừng services

```bash
docker compose down
```

## Xem logs

```bash
# Tất cả services
docker compose logs -f

# Chỉ 1 service
docker compose logs traefik --tail 20
docker compose logs nginx --tail 20
docker compose logs app --tail 20
```

## Scale app

```bash
docker compose up --scale app=3 -d
```

NGINX sẽ tự động load balance giữa các instance qua upstream `backend`.
