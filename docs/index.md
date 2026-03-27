---
layout: home

hero:
  name: Traefik + NGINX + App
  text: Gateway & Performance Layer
  tagline: Hệ thống reverse proxy đa tầng với Traefik làm gateway, NGINX làm performance layer, và Express app phía sau.
  actions:
    - theme: brand
      text: Bắt đầu →
      link: /guide/setup
    - theme: alt
      text: Kiến trúc
      link: /architecture

features:
  - icon: 🔀
    title: Traefik Gateway
    details: Auto-discovery, routing thông minh, dashboard giám sát. Hỗ trợ Docker provider (Linux) và file provider (Windows).
  - icon: ⚡
    title: NGINX Performance
    details: Cache, rate limit, gzip compression, proxy buffering — tối ưu hoá hiệu suất trước khi request đến app.
  - icon: 🔒
    title: Network Isolation
    details: App không expose trực tiếp ra ngoài. Tách biệt mạng web (public) và internal (private).
  - icon: 🚀
    title: Scale Ready
    details: Hỗ trợ scale app với docker compose --scale. NGINX tự load balance nội bộ.
---
