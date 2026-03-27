# Traefik + NGINX + App

Hệ thống gateway sử dụng **Traefik** làm reverse proxy/gateway bên ngoài, **NGINX** làm performance layer (cache, buffering), và **Express app** phía sau.

## Kiến trúc

```
Client → Traefik (:80) → NGINX → App (:3000)
                ↑
          Dashboard (:8080)
```

- **Traefik**: Auto-discovery qua Docker labels, route traffic đến NGINX
- **NGINX**: Reverse proxy nội bộ, cache `/api/`, forward headers
- **App**: Express server, không expose ra ngoài → an toàn hơn

## Cấu trúc thư mục

```
├── docker-compose.yml
├── nginx.conf
├── app/
│   ├── package.json
│   └── index.js
└── docs/
    └── Idea.md
```

## Cách chạy

```bash
# Thêm vào /etc/hosts (hoặc C:\Windows\System32\drivers\etc\hosts trên Windows)
127.0.0.1 example.local

# Khởi chạy
docker compose up -d
```

Truy cập:
- http://example.local — App qua Traefik → NGINX
- http://localhost:8080 — Traefik Dashboard

## Scale app

```bash
docker compose up --scale app=3 -d
```

NGINX sẽ tự động load balance giữa các instance.

## Nâng cao

- **HTTPS**: Thêm entrypoint `websecure` và ACME resolver trong Traefik
- **Rate limit / Gzip / Buffering**: Cấu hình thêm trong `nginx.conf`
