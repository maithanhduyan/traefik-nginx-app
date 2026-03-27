# Traefik Gateway

Traefik là tầng đầu tiên nhận traffic, làm nhiệm vụ routing.

## Base config

File `docker-compose.yml` chứa config chung:

```yaml
traefik:
  image: traefik:v3.0
  command:
    - --api.insecure=true
    - --entrypoints.web.address=:80
  ports:
    - "80:80"      # Web traffic
    - "8080:8080"  # Dashboard
```

## Dev — File Provider

File `docker-compose.override.yml` (tự động load):

```yaml
traefik:
  command:
    - --api.insecure=true
    - --providers.file.filename=/etc/traefik/dynamic.yml
    - --entrypoints.web.address=:80
  volumes:
    - ./traefik-dynamic.yml:/etc/traefik/dynamic.yml:ro
```

Routing được định nghĩa trong `traefik-dynamic.yml`:

```yaml
http:
  routers:
    nginx-router:
      rule: "Host(`example.local`) || Host(`localhost`)"
      entryPoints:
        - web
      service: nginx-service

  services:
    nginx-service:
      loadBalancer:
        servers:
          - url: "http://nginx:80"
```

## Prod — Docker Provider

File `docker-compose.prod.yml` (chỉ định khi deploy):

```yaml
traefik:
  command:
    - --api.insecure=true
    - --providers.docker=true
    - --entrypoints.web.address=:80
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
```

Traefik tự đọc labels từ container `nginx`:

```yaml
nginx:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.nginx.rule=Host(`example.local`)"
    - "traefik.http.services.nginx.loadbalancer.server.port=80"
```

## Dashboard

Truy cập http://localhost:8080 để xem:

- **Entrypoints**: Port đang lắng nghe
- **HTTP Routers**: Routing rules
- **HTTP Services**: Backend services
- **Middlewares**: Middleware đang active
