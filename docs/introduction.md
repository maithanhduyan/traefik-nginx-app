# Giới thiệu

Dự án này triển khai mô hình **reverse proxy đa tầng** sử dụng Docker Compose:

| Tầng | Công nghệ | Vai trò |
|------|-----------|---------|
| Gateway | **Traefik v3** | Routing, service discovery, dashboard |
| Performance | **NGINX** | Cache, rate limit, gzip, buffering |
| Application | **Express (Node.js)** | Business logic, API |

## Tại sao cần 2 tầng proxy?

**Traefik** giỏi ở việc:
- Tự động phát hiện service qua Docker labels
- Dashboard giám sát real-time
- Quản lý TLS/HTTPS tự động (ACME)

**NGINX** giỏi ở việc:
- Cache response với hiệu suất cao
- Rate limiting chi tiết
- Gzip compression
- Proxy buffering tối ưu

Kết hợp cả hai → lấy được ưu điểm tốt nhất của mỗi công cụ.

## Cấu trúc dự án

```
traefik-nginx-app/
├── docker-compose.yml            # Base (services chung)
├── docker-compose.override.yml   # Dev / Windows (file provider)
├── docker-compose.prod.yml       # Production / Linux (Docker provider)
├── traefik-dynamic.yml           # Traefik routing (dev mode)
├── nginx.conf                    # NGINX performance config
├── .env                          # Biến môi trường
├── app/
│   ├── package.json
│   └── index.js                  # Express server
├── test/
│   └── test_nginx.py             # Test suite (Python)
└── docs/                         # Tài liệu (VitePress)
```
