import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Traefik + NGINX + App',
  description: 'Tài liệu hệ thống gateway Traefik → NGINX → App',
  lang: 'vi-VN',
  base: process.env.BASE_PATH || '/',
  ignoreDeadLinks: [
    /localhost/,
  ],

  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Kiến trúc', link: '/architecture' },
      { text: 'Hướng dẫn', link: '/guide/setup' },
    ],

    sidebar: [
      {
        text: 'Tổng quan',
        items: [
          { text: 'Giới thiệu', link: '/introduction' },
          { text: 'Kiến trúc hệ thống', link: '/architecture' },
        ]
      },
      {
        text: 'Hướng dẫn',
        items: [
          { text: 'Cài đặt & Chạy', link: '/guide/setup' },
          { text: 'Triển khai Production', link: '/guide/deployment' },
        ]
      },
      {
        text: 'Cấu hình',
        items: [
          { text: 'Traefik Gateway', link: '/config/traefik' },
          { text: 'NGINX Performance', link: '/config/nginx' },
          { text: 'Express App', link: '/config/app' },
        ]
      },
      {
        text: 'Testing',
        items: [
          { text: 'Test Suite', link: '/testing' },
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],

    outline: {
      level: [2, 3],
      label: 'Mục lục'
    },

    footer: {
      message: 'Traefik + NGINX + App Documentation',
    }
  }
})
