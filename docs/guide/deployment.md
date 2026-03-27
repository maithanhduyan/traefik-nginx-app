# Triển khai Production

## Linux Production

Trên Linux, Traefik có thể truy cập Docker socket trực tiếp → dùng **Docker provider** thay vì file provider.

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Khác biệt so với Dev

| | Dev (Windows) | Prod (Linux) |
|--|---------------|--------------|
| Traefik provider | File (`traefik-dynamic.yml`) | Docker (labels) |
| Docker socket | Không mount | `/var/run/docker.sock` |
| Routing config | `traefik-dynamic.yml` | Labels trên nginx service |

### Cấu hình domain

Thêm DNS record hoặc sửa `/etc/hosts`:

```bash
echo "127.0.0.1 example.local" >> /etc/hosts
```

Hoặc thay `example.local` trong `docker-compose.prod.yml` bằng domain thật.

## HTTPS (TLS)

Thêm vào command của Traefik trong `docker-compose.prod.yml`:

```yaml
services:
  traefik:
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.le.acme.tlschallenge=true
      - --certificatesresolvers.le.acme.email=your@email.com
      - --certificatesresolvers.le.acme.storage=/letsencrypt/acme.json
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt

  nginx:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`yourdomain.com`)"
      - "traefik.http.routers.nginx.entrypoints=websecure"
      - "traefik.http.routers.nginx.tls.certresolver=le"
      - "traefik.http.services.nginx.loadbalancer.server.port=80"

volumes:
  letsencrypt:
```

::: warning Lưu ý
- `--api.insecure=true` nên tắt trên production hoặc đặt sau firewall
- Đảm bảo port 80/443 mở trên firewall cho ACME challenge
:::

## Scale & Load Balancing

```bash
# Scale app lên 3 instances
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --scale app=3 -d
```

NGINX upstream `backend` tự phân phối traffic qua DNS round-robin nội bộ Docker.

## Health Check (nâng cao)

Thêm healthcheck cho từng service:

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/"]
      interval: 30s
      timeout: 5s
      retries: 3
```
