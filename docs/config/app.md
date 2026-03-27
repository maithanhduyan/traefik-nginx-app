# Express App

Backend đơn giản chạy Express trên Node.js 18.

## Source code

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

## Endpoints

| Method | Path | Response | Mô tả |
|--------|------|----------|-------|
| GET | `/` | `Hello from app` | Health check, HTML |
| GET | `/api` | `{"time":"..."}` | API endpoint, JSON |

## Docker config

```yaml
app:
  image: node:18-alpine
  working_dir: /app
  volumes:
    - ./app:/app
  command: sh -c "npm install && npm start"
  networks:
    - internal     # Chỉ internal network
```

::: info Bảo mật
App **chỉ nằm trên network `internal`** — không thể truy cập trực tiếp từ bên ngoài. Chỉ NGINX (cùng network `internal`) mới gọi được `app:3000`.
:::

## Dependencies

```json
{
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

## Scale

Khi scale app (`--scale app=3`), Docker DNS tự trả về nhiều IP cho hostname `app`. NGINX upstream sẽ round-robin giữa các instance.
