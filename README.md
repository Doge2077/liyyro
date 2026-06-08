# lys2021 个人博客

基于 [VitePress](https://vitepress.dev/) 构建的个人博客，部署在 https://blog.lys2021.com/

## 技术栈

- **框架**: VitePress 1.x
- **语言**: TypeScript + Vue 3
- **图床**: GitHub + jsDelivr CDN
- **容器化**: Docker + Nginx
- **反向代理**: Caddy（自动 HTTPS）

## 快速开始

### 本地开发

```bash
# 安装依赖
npm install --legacy-peer-deps

# 启动开发服务器（端口 8081）
npm run docs:dev

# 或使用脚本
bash dev.sh
```

### 构建

```bash
npm run docs:build
```

### 部署到本机 Docker

```bash
bash deploy.sh
```

## 目录结构

```
├── .vitepress/
│   ├── config/
│   │   ├── index.mts         # VitePress 主配置
│   │   ├── theme.ts          # 主题配置（调用 auto-nav）
│   │   └── auto-nav.ts       # 自动生成导航栏+侧边栏
│   └── theme/
│       ├── components/       # Vue 组件
│       ├── composables/      # 组合式函数
│       ├── index.ts          # 主题入口
│       └── style.css         # 全局样式
├── docs/
│   ├── public/               # 静态资源
│   ├── index.md              # 首页
│   ├── AI/                   # AI 板块
│   ├── Life/                 # 生活板块
│   └── History/              # 历史板块
│       ├── algorithm/        # 算法
│       ├── java/             # Java
│       ├── cpp/              # C/C++
│       ├── cs-fundamentals/  # 计算机基础
│       ├── database/         # 数据库
│       ├── python/           # Python
│       ├── linux/            # Linux
│       ├── tips/             # 技巧
│       └── other/            # 其他
├── scripts/                  # 工具脚本
├── order.json                # 目录排序配置
├── deploy.sh                 # 一键部署脚本
├── dev.sh                    # 本地开发脚本
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## 目录排序配置

编辑 `order.json` 控制侧边栏目录和文章的排序：

```json
{
  "topLevel": ["AI", "Life", "History"],
  "History": {
    "_order": ["algorithm", "java", "cpp", ...],
    "algorithm": {
      "_order": ["算法讲解", "算法题解", "竞赛题解"],
      "算法讲解": {
        "_order": ["1. 基础算法初识", "2. 基础数据结构初识", ...]
      }
    }
  }
}
```

- `topLevel`: 顶部导航栏排序
- `_order`: 子目录/文件的排序数组
- 目录和文件名需与实际一致

## 添加新文章

1. 在 `docs/` 对应目录下创建 `.md` 文件
2. 添加 frontmatter：

```yaml
---
title: "文章标题"
date: 2024-01-01
categories: [分类]
tags: [标签]
description: "描述"
---

# 文章标题

正文内容...
```

3. 如需控制排序，在 `order.json` 的 `_order` 数组中添加文件名

## 图片管理

图片存放在独立仓库 [Doge2077/liyyro-photo](https://github.com/Doge2077/liyyro-photo)，通过 jsDelivr CDN 加速：

```markdown
![描述](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/06/xxx.png)
```

## 自动部署

推送到 `main` 分支后，GitHub Actions 自动构建并部署到服务器。

需要在 GitHub 仓库 Settings > Secrets 中配置：
- `REMOTE_HOST`: 服务器地址
- `REMOTE_USER`: SSH 用户名
- `SSH_PRIVATE_KEY`: SSH 私钥

## License

MIT
