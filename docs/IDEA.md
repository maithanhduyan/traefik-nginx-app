Dưới đây là một mẫu **Docker Compose hoàn chỉnh** cho mô hình:

👉 Traefik (gateway)
👉 NGINX (performance layer)
👉 App phía sau

---

## 🧱 `docker-compose.yml`

```yaml
version: "3.9"

services:
  traefik:
    image: traefik:v3.0
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
    ports:
      - "80:80"
      - "8080:8080" # dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - web

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`example.local`)"
      - "traefik.http.services.nginx.loadbalancer.server.port=80"
    networks:
      - web
      - internal

  app:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./app:/app
    command: sh -c "npm install && npm start"
    networks:
      - internal

networks:
  web:
  internal:
```

---

## ⚙️ `nginx.conf`

```nginx
events {}

http {
  upstream backend {
    server app:3000;
  }

  server {
    listen 80;

    location / {
      proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    # cache example
    proxy_cache_path /tmp/cache levels=1:2 keys_zone=my_cache:10m max_size=100m;

    location /api/ {
      proxy_cache my_cache;
      proxy_pass http://backend;
    }
  }
}
```

---

## 📁 Cấu trúc thư mục

```
project/
├── docker-compose.yml
├── nginx.conf
└── app/
    ├── package.json
    └── index.js
```

---

## 🧪 Ví dụ `app/index.js`

```js
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Hello from app");
});

app.get("/api", (req, res) => {
  res.json({ time: new Date() });
});

app.listen(3000, () => console.log("App running on 3000"));
```

---

## 🚀 Cách chạy

```bash
docker compose up -d
```

Truy cập:

* [http://example.local](http://example.local)  (cần add vào `/etc/hosts`)
* [http://localhost:8080](http://localhost:8080) (Traefik dashboard)

---

## 🧠 Giải thích nhanh

* **Traefik**

  * Nhìn label → tự route đến NGINX
  * Không cần config file riêng

* **NGINX**

  * Làm reverse proxy nội bộ
  * Có thể thêm:

    * cache
    * rate limit
    * gzip
    * buffering

* **App**

  * Không expose ra ngoài → an toàn hơn

---

## 💡 Tips nâng cao

* Thêm HTTPS:

  ```yaml
  - --entrypoints.websecure.address=:443
  - --certificatesresolvers.le.acme.tlschallenge=true
  ```

* Scale app:

  ```bash
  docker compose up --scale app=3
  ```

* NGINX sẽ load balance nội bộ

---

Nếu bạn muốn, mình có thể nâng cấp config này lên:

* Production-ready (HTTPS + domain thật)
* Kubernetes version
* Hoặc benchmark so sánh trực tiếp Traefik vs NGINX setup này
