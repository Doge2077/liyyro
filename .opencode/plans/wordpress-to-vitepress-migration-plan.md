# WordPress 迁移至 VitePress 个人博客 —— 技术方案

## 一、项目概述

### 1.1 目标

将现有 WordPress 博客（`/var/www/html`）迁移至基于 VitePress 的静态博客，参考 [haue-cs-wiki](https://github.com/haueosc/haue-cs-wiki) 项目架构，部署在自有服务器上，使用现有域名 `lys2021.com`。

### 1.2 现状分析

| 项目 | 详情 |
|------|------|
| WordPress 路径 | `/var/www/html` |
| 文章总数 | **200 篇** |
| 图片附件 | **349 张**（含缩略图共 1544 文件，约 360MB） |
| 主要分类 | Q&A(90), ALGORITHM(71), ARTICLES(19), Software Architect(14), Poems(12), Java(10) 等 |
| 数据库 | MySQL 8.0，库名 `lys2021_com` |
| 最新文章 | 服务指标、大模型基础、BERT模型训练实践、JDK源码系列等 |

### 1.3 haue-cs-wiki 项目结构分析

```
haue-cs-wiki/
├── .github/workflows/depoly.yml    # GitHub Actions 自动部署
├── .vitepress/
│   ├── config/
│   │   ├── index.mts               # VitePress 主配置（站点级）
│   │   └── zh.ts                   # 中文本地化配置（导航栏+侧边栏）
│   └── theme/
│       ├── components/             # 自定义 Vue 组件
│       │   ├── Footer.vue
│       │   ├── HeroImage.vue
│       │   ├── TypedInfo.vue
│       │   └── Wall.vue
│       ├── fonts/                  # 自定义字体
│       ├── icons/                  # SVG 图标
│       ├── index.ts                # 主题入口（扩展默认主题）
│       └── style.css               # 全局样式
├── docs/
│   ├── public/                     # 静态资源（图片等）
│   │   ├── images/
│   │   └── logo/
│   ├── index.md                    # 首页（frontmatter hero 布局）
│   ├── main.md                     # 导航页
│   └── [分类目录]/[文章].md        # 文章内容
├── package.json
└── tsconfig.json
```

**核心技术栈**：
- VitePress `^1.3.2`
- `@nolebase/vitepress-plugin-enhanced-readabilities` —— 阅读增强
- `@nolebase/vitepress-plugin-git-changelog` —— Git 变更日志
- `vitepress-plugin-codeblocks-fold` —— 代码折叠
- `markdown-it-footnote` —— 脚注支持
- `typed.js` —— 打字机动画

**haue-cs-wiki 配置要点**：
- `outDir: 'dist'`，`srcDir: 'docs'`
- 使用 `locales.root` 配置中文
- 侧边栏采用多级嵌套结构（前言、新手入门、竞赛经验、开发工具、学科课程、后端开发、前端开发、人工智能、考研经验、工作经验、考公留学）
- 主题通过 `extends: DefaultTheme` 扩展，使用插槽注入自定义组件
- 部署到 GitHub Pages，使用 `actions/deploy-pages@v4`

---

## 二、图床架构方案：GitHub + jsDelivr CDN

### 2.1 方案概述

| 层级 | 服务 | 说明 |
|------|------|------|
| 存储 | GitHub Repository | 图片以 Git 仓库存储，永久免费，无容量上限（建议 < 1GB） |
| 分发 | jsDelivr CDN | 全球 CDN 加速，中国境内可访问，免费 |
| 备份 | 本地 `docs/public/images/` | 构建时随项目一起部署到服务器 |

### 2.2 仓库结构

创建独立的图床仓库 `blog-assets`：

```
blog-assets/                    # 独立图床仓库
├── images/
│   ├── 2022/
│   │   └── ...
│   ├── 2023/
│   │   └── ...
│   ├── 2024/
│   │   ├── 06/
│   │   │   ├── image1.png
│   │   │   └── image2.jpg
│   │   └── 08/
│   ├── 2025/
│   │   └── ...
│   └── 2026/
│       └── ...
└── README.md
```

### 2.3 URL 格式

```
原始 GitHub URL:
https://raw.githubusercontent.com/<username>/blog-assets/main/images/2024/06/image.png

jsDelivr CDN URL（推荐）:
https://cdn.jsdelivr.net/gh/<username>/blog-assets@main/images/2024/06/image.png

带版本号（更稳定）:
https://cdn.jsdelivr.net/gh/<username>/blog-assets@v1.0/images/2024/06/image.png
```

### 2.4 jsDelivr 在中国的优势

- 在中国有 **ICP 备案**，使用阿里云 CDN 节点
- `cdn.jsdelivr.net` 在国内有 CDN 回源，访问速度快
- 完全免费，无流量限制
- GitHub 原始链接（`raw.githubusercontent.com`）在国内不稳定，jsDelivr 是最佳免费替代方案

### 2.5 图床迁移流程

```
1. 遍历 /var/www/html/wp-content/uploads/ 下所有图片文件
2. 过滤掉缩略图（文件名含 -150x150, -300x212 等尺寸后缀）
3. 按 年/月 目录结构复制到 blog-assets/images/
4. 生成图片映射表（旧URL → 新jsDelivr URL）
5. git push 到图床仓库
```

**WordPress 缩略图过滤规则**：
- 原始图片：`image-20240625142529340.png`
- 缩略图：`image-20240625142529340-150x150.png`、`image-20240625142529340-300x200.png`
- 规则：文件名中含 `-[数字]x[数字]` 后缀的为缩略图，跳过

---

## 三、项目架构设计

### 3.1 目录结构

```
blog/                              # 主项目仓库
├── .github/
│   └── workflows/
│       └── deploy.yml              # 自动构建 + 部署到服务器
├── .vitepress/
│   ├── config/
│   │   ├── index.mts               # 主配置
│   │   └── theme.ts                # 主题/导航/侧边栏配置
│   └── theme/
│       ├── components/
│       │   ├── BlogHome.vue        # 自定义首页（多 Tab 切换）
│       │   ├── PostList.vue        # 文章列表组件
│       │   └── Footer.vue          # 页脚
│       ├── composables/
│       │   └── usePosts.ts         # 文章数据获取逻辑
│       ├── index.ts                # 主题入口
│       └── style.css               # 全局样式
├── docs/
│   ├── public/
│   │   └── logo/
│   │       └── favicon.png
│   ├── index.md                    # 首页 frontmatter
│   ├── tech/                       # 技术板块（默认展示）
│   │   ├── index.md
│   │   ├── java/
│   │   │   ├── jdk-source-1.md
│   │   │   ├── jdk-source-2.md
│   │   │   └── ...
│   │   ├── algorithm/
│   │   │   ├── leetcode-hot100.md
│   │   │   └── ...
│   │   ├── spring/
│   │   ├── ai/
│   │   ├── linux/
│   │   ├── database/
│   │   └── cs-fundamentals/
│   ├── articles/                   # 文章/随笔板块
│   │   ├── index.md
│   │   └── ...
│   ├── qa/                         # Q&A 板块
│   │   ├── index.md
│   │   └── ...
│   ├── poems/                      # 诗歌板块
│   │   ├── index.md
│   │   └── ...
│   └── about/                      # 关于页面
│       └── index.md
├── scripts/
│   ├── wp-export.py                # WordPress 文章导出脚本
│   ├── migrate-images.py           # 图片迁移脚本
│   └── replace-urls.py             # URL 替换脚本
├── package.json
└── tsconfig.json
```

### 3.2 多 Tab 板块设计

首页采用自定义 Vue 组件实现 Tab 切换，默认展示技术板块：

```
┌──────────────────────────────────────────────────┐
│                  lys2021.com                      │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │  [ 技术 ]  [ 文章 ]  [ Q&A ]  [ 诗歌 ]  [关于] │ │  ← Tab 栏
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │                                             │ │
│  │  ● JDK源码系列（五）               2024-10-29 │ │
│  │  ● JDK源码系列（四）               2024-10-29 │ │
│  │  ● BERT模型训练实践                2025-04-21 │ │
│  │  ● Spring Validation 详解         2024-08-14 │ │
│  │  ● 线程池原理（一）                2024-08-09 │ │
│  │  ● 双 Token 三验证解决方案         2024-08-01 │ │
│  │  ...                                        │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  [← 1 2 3 ... →]                                 │
└──────────────────────────────────────────────────┘
```

**技术实现**：
- 使用 VitePress 的 `Markdown Section` 插槽注入 Vue 组件 `BlogHome.vue`
- 文章元数据通过 VitePress 的 `createContentLoader` API 获取
- 每个板块对应 `docs/` 下的一个子目录
- Tab 切换通过 Vue 响应式数据 `ref` 实现，无需页面跳转
- 支持分页、搜索、标签筛选

### 3.3 分类映射方案

WordPress 分类 → VitePress 目录映射：

| WordPress 分类 | 数量 | VitePress 目录 | 说明 |
|----------------|------|----------------|------|
| Java, Software Architect | 24 | `docs/tech/java/` | Java 技术栈 |
| ALGORITHM, Basic Algorithm, Intermediate Algorithm | 81 | `docs/tech/algorithm/` | 算法相关 |
| AI | 2 | `docs/tech/ai/` | 人工智能 |
| Linux | 9 | `docs/tech/linux/` | Linux 技术 |
| DataBase System | 8 | `docs/tech/database/` | 数据库 |
| Computer Network, CompOrg, Compilation, DataStructure | 15 | `docs/tech/cs-fundamentals/` | 计算机基础 |
| Python, Django, C/C++ | 10 | `docs/tech/python/`, `docs/tech/cpp/` | 其他语言 |
| Tips | 7 | `docs/tech/tips/` | 技巧 |
| ARTICLES, Essays | 25 | `docs/articles/` | 文章/随笔 |
| Q&A | 90 | `docs/qa/` | 问答 |
| Poems, Novels | 15 | `docs/poems/` | 诗歌/小说 |
| University 相关 | 12 | `docs/campus/` | 校园相关 |

---

## 四、WordPress 文章迁移方案

### 4.1 迁移流程

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  导出 WP 文章 │ →  │ HTML→Markdown │ →  │  图片迁移    │ →  │ URL 替换     │
│  (Python脚本) │    │  (转换工具)   │    │ (Git+jsDelivr)│    │ (自动化)     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### 4.2 导出脚本核心逻辑

```python
# scripts/wp-export.py
import mysql.connector
import html2text
import os
import json
from datetime import datetime

# 1. 连接数据库
db = mysql.connector.connect(
    host="127.0.0.1",
    user="lys2021_com",
    password="FZ4GHdHfFpX384FG",
    database="lys2021_com"
)

# 2. 查询所有已发布文章（含分类信息）
QUERY = """
SELECT p.ID, p.post_title, p.post_date, p.post_content, p.post_name,
       p.post_excerpt, GROUP_CONCAT(t.name) as categories
FROM wp_posts p
LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
LEFT JOIN wp_terms t ON tt.term_id = t.term_id
WHERE p.post_type='post' AND p.post_status='publish'
GROUP BY p.ID
ORDER BY p.post_date DESC
"""

# 3. HTML → Markdown 转换
converter = html2text.HTML2Text()
converter.body_width = 0  # 不自动换行
converter.protect_links = True
converter.unicode_snob = True

# 4. 分类映射（见上方分类映射表）
CATEGORY_MAP = {
    "Java": "tech/java",
    "Software Architect": "tech/java",
    "ALGORITHM": "tech/algorithm",
    # ... 完整映射
}

# 5. 生成 Markdown 文件（带 frontmatter）
# ---
# title: "文章标题"
# date: 2024-10-29
# categories: [Java]
# tags: [JDK, 源码]
# description: "文章摘要"
# ---
```

### 4.3 图片迁移脚本

```python
# scripts/migrate-images.py
import os
import re
import json
import shutil

WP_UPLOADS = "/var/www/html/wp-content/uploads"
BLOG_ASSETS = "/path/to/blog-assets/images"
URL_MAPPING = {}

# 1. 缩略图过滤规则
def is_thumbnail(filename):
    """判断是否为 WordPress 缩略图"""
    # 匹配 -数字x数字.扩展名 的模式
    return bool(re.search(r'-\d+x\d+\.\w+$', filename))

# 2. 扫描并复制原始图片
for year_dir in os.listdir(WP_UPLOADS):
    year_path = os.path.join(WP_UPLOADS, year_dir)
    if not os.path.isdir(year_path) or not year_dir.isdigit():
        continue
    for month_dir in os.listdir(year_path):
        month_path = os.path.join(year_path, month_dir)
        if not os.path.isdir(month_path):
            continue
        target_dir = os.path.join(BLOG_ASSETS, year_dir, month_dir)
        os.makedirs(target_dir, exist_ok=True)
        for filename in os.listdir(month_path):
            if is_thumbnail(filename):
                continue  # 跳过缩略图
            src = os.path.join(month_path, filename)
            dst = os.path.join(target_dir, filename)
            shutil.copy2(src, dst)
            # 记录 URL 映射
            old_url = f"https://lys2021.com/wp-content/uploads/{year_dir}/{month_dir}/{filename}"
            new_url = f"https://cdn.jsdelivr.net/gh/<user>/blog-assets@main/images/{year_dir}/{month_dir}/{filename}"
            URL_MAPPING[old_url] = new_url

# 3. 保存 URL 映射表
with open("url-mapping.json", "w") as f:
    json.dump(URL_MAPPING, f, indent=2, ensure_ascii=False)
```

### 4.4 URL 替换脚本

```python
# scripts/replace-urls.py
import json
import os
import re

# 加载映射表
with open("url-mapping.json") as f:
    url_mapping = json.load(f)

# 批量替换所有 Markdown 文件
docs_dir = "docs"
for root, dirs, files in os.walk(docs_dir):
    for filename in files:
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(root, filename)
        with open(filepath, "r") as f:
            content = f.read()
        
        modified = False
        for old_url, new_url in url_mapping.items():
            if old_url in content:
                content = content.replace(old_url, new_url)
                modified = True
        
        if modified:
            with open(filepath, "w") as f:
                f.write(content)
            print(f"Updated: {filepath}")
```

### 4.5 frontmatter 格式

每篇文章的 Markdown 文件头部：

```yaml
---
title: "JDK源码系列（五）"
date: 2024-10-29
categories:
  - Java
tags:
  - JDK
  - 源码
description: "深入分析JDK核心类库源码"
---
```

---

## 五、部署方案

### 5.1 服务器部署架构

```
┌─────────────────────────────────────────┐
│              你的服务器（当前机器）        │
│                                         │
│  ┌─────────┐    ┌──────────────────┐   │
│  │  Nginx   │    │  VitePress 构建   │   │
│  │  反向代理 │ ←  │  输出目录 (dist/) │   │
│  │          │    └──────────────────┘   │
│  │  80/443  │                           │
│  └─────────┘                            │
│                                         │
│  域名: lys2021.com                      │
│  SSL: Let's Encrypt                     │
└─────────────────────────────────────────┘
```

### 5.2 GitHub Actions 自动部署

```yaml
# .github/workflows/deploy.yml
name: Deploy Blog

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build with VitePress
        run: npm run docs:build

      - name: Deploy to Server via rsync
        uses: Burnett01/rsync-deployments@7.0.1
        with:
          switches: -avzr --delete
          path: dist/
          remote_path: /var/www/blog/
          remote_host: ${{ secrets.REMOTE_HOST }}
          remote_user: ${{ secrets.REMOTE_USER }}
          remote_key: ${{ secrets.SSH_PRIVATE_KEY }}
```

### 5.3 Nginx 配置

```nginx
# /etc/nginx/sites-available/lys2021-blog
server {
    listen 80;
    server_name lys2021.com www.lys2021.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lys2021.com www.lys2021.com;

    ssl_certificate /etc/letsencrypt/live/lys2021.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lys2021.com/privkey.pem;

    root /var/www/blog;
    index index.html;

    # VitePress 静态资源缓存
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback（VitePress 需要）
    location / {
        try_files $uri $uri.html $uri/ /index.html;
    }

    # 旧 WordPress URL 301 重定向（SEO 友好）
    # 示例: /2024/10/post-name/ → /tech/java/post-name
    location ~ "^/\d{4}/\d{2}/(.+)/$" {
        # 需要根据实际 URL 映射表配置
        return 301 /tech/$1;
    }

    # WordPress 短链接重定向
    location ~ "^/\?p=(\d+)$" {
        # 需要根据 ID 映射表配置
        return 301 /;
    }
}
```

### 5.4 旧 URL 重定向策略

为保持 SEO 和外部链接可用，需要配置重定向：

| 旧 WordPress URL | 新 VitePress URL |
|------------------|-------------------|
| `lys2021.com/2024/10/jdk-source-1/` | `lys2021.com/tech/java/jdk-source-1` |
| `lys2021.com/category/java/` | `lys2021.com/tech/java/` |
| `lys2021.com/?p=123` | 通过 ID 映射表重定向 |

建议在迁移脚本中同时生成 `redirects.json`，然后用 Nginx 的 `map` 或 `rewrite` 规则实现。

---

## 六、依赖清单

### 6.1 package.json

```json
{
  "name": "lys2021-blog",
  "private": true,
  "scripts": {
    "docs:dev": "vitepress dev --port 8080",
    "docs:build": "vitepress build",
    "docs:preview": "vitepress preview"
  },
  "dependencies": {
    "vitepress": "^1.3.2",
    "@nolebase/vitepress-plugin-enhanced-readabilities": "^2.4.0",
    "@nolebase/vitepress-plugin-git-changelog": "^2.4.0",
    "@nolebase/vitepress-plugin-highlight-targeted-heading": "^2.4.0",
    "vitepress-plugin-codeblocks-fold": "^1.2.28",
    "markdown-it-footnote": "^4.0.0",
    "typed.js": "^2.1.0"
  },
  "devDependencies": {
    "markdown-it-mathjax3": "^4.3.2"
  }
}
```

### 6.2 迁移脚本 Python 依赖

```bash
pip install mysql-connector-python html2text python-frontmatter beautifulsoup4 requests
```

---

## 七、实施步骤与时间估算

### 阶段一：项目初始化（1天）

- [ ] 创建 Git 仓库 `blog`
- [ ] 初始化 VitePress 项目（参考 haue-cs-wiki 的 package.json）
- [ ] 复制并适配 haue-cs-wiki 的主题配置
- [ ] 创建自定义首页 Tab 组件 `BlogHome.vue`
- [ ] 配置导航栏和侧边栏（按板块分类）
- [ ] 本地测试 `npm run docs:dev`

### 阶段二：图床搭建（1天）

- [ ] 创建图床仓库 `blog-assets`
- [ ] 编写图片迁移脚本 `scripts/migrate-images.py`
- [ ] 从 WordPress 上传目录提取原始图片（跳过缩略图）
- [ ] 按 `images/年/月/` 结构推送到图床仓库
- [ ] 生成 URL 映射表 `url-mapping.json`
- [ ] 验证 jsDelivr URL 可访问

### 阶段三：文章迁移（2-3天）

- [ ] 编写 WordPress 导出脚本 `scripts/wp-export.py`
- [ ] HTML → Markdown 转换（处理代码块、表格、图片、脚注等）
- [ ] 生成 frontmatter 元数据（title, date, categories, tags）
- [ ] 使用 URL 映射表替换文章中的图片链接
- [ ] 按分类整理到对应目录
- [ ] 生成 URL 重定向映射表 `redirects.json`
- [ ] 人工校验关键文章（代码块、复杂排版）

### 阶段四：部署配置（1天）

- [ ] 配置 Nginx 反向代理
- [ ] 配置 SSL 证书（Let's Encrypt）
- [ ] 设置 GitHub Actions 自动部署
- [ ] 配置旧 URL 重定向规则
- [ ] DNS 切换（lys2021.com → 新博客）

### 阶段五：验证与优化（1天）

- [ ] 检查所有文章渲染正确
- [ ] 验证图片加载正常（jsDelivr CDN）
- [ ] 测试旧链接重定向
- [ ] 检查移动端适配
- [ ] SEO 基础配置（sitemap.xml、robots.txt）
- [ ] 性能测试（Lighthouse）

**总计：约 6-7 天**

---

## 八、风险与应对

| 风险 | 影响 | 应对方案 |
|------|------|----------|
| jsDelivr 在中国偶尔波动 | 图片短暂不可用 | 同时将图片放在 `docs/public/images/` 作为本地备份 |
| HTML→Markdown 转换不完美 | 部分格式丢失 | 对重要文章进行人工校验和修正 |
| GitHub 仓库超过 1GB | 推送变慢 | 定期清理历史版本，使用 `git filter-repo` 压缩 |
| 旧 URL SEO 流失 | 搜索排名下降 | 配置 301 重定向 + 提交 sitemap 到搜索引擎 |
| WordPress 数据库连接问题 | 导出失败 | 已确认 MySQL 服务正常运行，需要临时修改 mysql 配置文件 |

---

## 九、备选图床对比

| 方案 | 免费额度 | 中国访问 | 稳定性 | 复杂度 |
|------|----------|----------|--------|--------|
| **GitHub + jsDelivr（推荐）** | 无限 | ✅ 有 ICP | ⭐⭐⭐⭐⭐ | 低 |
| Cloudflare R2 | 10GB | ⚠️ 需自定义域名 | ⭐⭐⭐⭐ | 中 |
| SM.MS | 5GB | ✅ | ⭐⭐⭐ | 低 |
| 阿里云 OSS | 5GB/月 | ✅ | ⭐⭐⭐⭐⭐ | 中 |
| 自建 MinIO | 无限 | ✅ | ⭐⭐⭐ | 高 |

---

## 十、总结

本方案采用 **VitePress + GitHub/jsDelivr 图床 + 自有服务器部署** 的架构：

1. **免费**：VitePress 开源，jsDelivr CDN 免费，GitHub 存储免费
2. **稳定**：纯静态文件，无数据库依赖，无 PHP 运行时
3. **中国可访问**：jsDelivr 在中国有 ICDN 节点，服务器在境内
4. **永久托管**：Git 仓库 + 静态文件，不依赖第三方 SaaS
5. **易于维护**：Markdown 写作，Git 版本控制，CI/CD 自动部署
6. **多板块**：通过 Tab 组件实现技术/文章/Q&A/诗歌等板块切换，默认展示技术板块
