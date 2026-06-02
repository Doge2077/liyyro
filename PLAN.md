# WordPress 迁移至 VitePress 个人博客 —— 技术方案

## 一、项目概述

### 1.1 目标

将现有 WordPress 博客（`/var/www/html`）迁移至基于 VitePress 的静态博客，参考 [haue-cs-wiki](https://github.com/haueosc/haue-cs-wiki) 项目架构，部署在自有服务器上，使用子域名 `blog.lys2021.com`。WordPress 原站保持不动。

### 1.2 现状分析

| 项目 | 详情 |
|------|------|
| WordPress 路径 | `/var/www/html`（保留不动） |
| 文章总数 | **200 篇**（全量迁移） |
| 图片附件 | **349 张**（含缩略图共 1544 文件，约 360MB） |
| 主要分类 | Q&A(90), ALGORITHM(71), ARTICLES(19), Software Architect(14), Poems(12), Java(10) 等 |
| 数据库 | MySQL 8.0，库名 `lys2021_com` |
| 博客域名 | `blog.lys2021.com`（新） |

### 1.3 haue-cs-wiki 项目结构分析

```
haue-cs-wiki/
├── .github/workflows/depoly.yml    # GitHub Actions 自动部署
├── .vitepress/
│   ├── config/
│   │   ├── index.mts               # 主配置（outDir/srcDir/插件/head）
│   │   └── zh.ts                   # 中文配置（nav/sidebar/翻译）
│   └── theme/
│       ├── components/             # Vue 组件（Footer/Wall/TypedInfo/HeroImage）
│       ├── fonts/                  # 自定义字体
│       ├── icons/                  # SVG 图标
│       ├── index.ts                # 主题入口（扩展 DefaultTheme + 插件注册）
│       └── style.css               # 全局样式
├── docs/
│   ├── public/images/              # 静态图片资源
│   ├── index.md                    # 首页 frontmatter hero 布局
│   └── [分类]/[文章].md            # 文章内容
├── package.json
└── tsconfig.json
```

核心技术栈：VitePress ^1.3.2 + @nolebase 插件 + codeblocks-fold + markdown-it-footnote

---

## 二、图床架构：GitHub + jsDelivr CDN

### 2.1 仓库信息

| 项目 | 详情 |
|------|------|
| 图床仓库 | `Doge2077/liyyro-photo`（公开） |
| CDN 地址 | `https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/` |
| 访问速度 | 中国有 ICDN 节点，免费无流量限制 |

### 2.2 仓库结构

```
liyyro-photo/
├── images/
│   ├── 2022/
│   ├── 2023/
│   ├── 2024/
│   │   ├── 06/
│   │   │   ├── image1.png
│   │   │   └── image2.jpg
│   │   └── 08/
│   ├── 2025/
│   └── 2026/
│       └── 06/
│           └── {文章slug}-{hash}.png   # 新上传图片命名规则
└── README.md
```

### 2.3 URL 映射示例

```
旧 URL（WordPress）:
https://lys2021.com/wp-content/uploads/2024/06/image.png

新 URL（jsDelivr CDN）:
https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/06/image.png
```

### 2.4 图片迁移规则

- 跳过缩略图（文件名含 `-数字x数字` 后缀，如 `-150x150.png`）
- 只保留原始尺寸图片
- 按 `images/年/月/` 目录结构组织

---

## 三、项目架构设计

### 3.1 目录结构

```
blog/
├── .github/workflows/deploy.yml
├── .vitepress/
│   ├── config/
│   │   ├── index.mts               # 主配置
│   │   ├── theme.ts                # 主题配置（调用 auto-nav）
│   │   └── auto-nav.ts             # ★ 自动生成导航栏+侧边栏
│   └── theme/
│       ├── components/
│       │   ├── BlogHome.vue        # 多 Tab 切换首页
│       │   ├── PostList.vue        # 文章列表
│       │   └── Footer.vue
│       ├── composables/
│       │   └── usePosts.ts         # 文章数据获取
│       ├── index.ts
│       └── style.css
├── docs/                           # ★ 用户只需维护这个目录下的 .md 文件
│   ├── public/logo/favicon.png
│   ├── index.md                    # 首页
│   ├── AI/                         # AI 板块（一级目录 = nav 标签）
│   │   ├── llm/                    # 二级目录 = 侧边栏分组
│   │   │   └── xxx.md              # 文章
│   │   ├── bert/
│   │   │   └── xxx.md
│   │   └── ...
│   ├── Life/                       # 生活板块
│   │   ├── poems/
│   │   │   └── xxx.md
│   │   ├── essays/
│   │   │   └── xxx.md
│   │   └── ...
│   └── History/                    # 历史文章
│       ├── java/
│       │   └── xxx.md
│       ├── algorithm/
│       │   └── xxx.md
│       └── ...
├── scripts/
│   ├── publish.sh                  # 发布文章
│   ├── update.sh                   # 更新文章
│   ├── delete.sh                   # 删除文章
│   ├── wp-export.py                # WordPress 导出
│   ├── migrate-images.py           # 图片迁移
│   └── replace-urls.py             # URL 替换
├── package.json
└── tsconfig.json
```

### 3.2 自动目录生成机制

**核心原则**：用户只需维护 `docs/` 下的 `.md` 文件和目录结构，导航栏和侧边栏在构建时自动生成。

**规则**：
- `docs/` 下的一级目录（AI、Life、History）→ 自动生成 **顶部导航栏** Tab
- 每个一级目录下的二级目录 → 自动生成该板块的 **侧边栏分组**
- 二级目录下的 `.md` 文件 → 自动生成侧边栏 **文章链接**
- 文章标题优先取 frontmatter 中的 `title`，没有则取文件名
- 排序：按 frontmatter 中的 `date` 降序（最新在前），无 date 的按文件名字母序

**auto-nav.ts 核心逻辑**：

```ts
// .vitepress/config/auto-nav.ts
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

const docsDir = path.resolve(__dirname, '../../docs')

// 扫描一级目录 → 生成 nav
function generateNav() {
  const dirs = fs.readdirSync(docsDir)
    .filter(d => fs.statSync(path.join(docsDir, d)).isDirectory() && d !== 'public' && d !== '.vitepress')
  return dirs.map(dir => ({
    text: dir,  // 或者用映射表：{ AI: 'AI', Life: '生活', History: '历史' }
    link: `/${dir}/`
  }))
}

// 扫描二级目录 → 生成 sidebar
function generateSidebar() {
  const sidebar = {}
  const firstLevelDirs = fs.readdirSync(docsDir)
    .filter(d => fs.statSync(path.join(docsDir, d)).isDirectory() && d !== 'public' && d !== '.vitepress')

  for (const firstDir of firstLevelDirs) {
    const firstPath = path.join(docsDir, firstDir)
    const secondLevelDirs = fs.readdirSync(firstPath)
      .filter(d => fs.statSync(path.join(firstPath, d)).isDirectory())

    sidebar[`/${firstDir}/`] = secondLevelDirs.map(secondDir => ({
      text: secondDir,
      collapsed: false,
      items: getMarkdownFiles(path.join(firstPath, secondDir))
        .sort((a, b) => b.date - a.date)  // 按日期降序
        .map(f => ({ text: f.title, link: `/${firstDir}/${secondDir}/${f.name}` }))
    }))
  }
  return sidebar
}

// 递归获取 .md 文件（排除 index.md）
function getMarkdownFiles(dir) {
  const files = []
  for (const f of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, f)
    if (fs.statSync(fullPath).isDirectory()) {
      files.push(...getMarkdownFiles(fullPath))
    } else if (f.endsWith('.md') && f !== 'index.md') {
      const content = fs.readFileSync(fullPath, 'utf-8')
      const { data } = matter(content)
      files.push({
        name: f.replace('.md', ''),
        title: data.title || f.replace('.md', ''),
        date: data.date ? new Date(data.date) : new Date(0)
      })
    }
  }
  return files
}
```

**theme.ts 调用方式**：

```ts
// .vitepress/config/theme.ts
import { generateNav, generateSidebar } from './auto-nav'

export const zh = defineConfig({
  themeConfig: {
    nav: generateNav(),
    sidebar: generateSidebar(),
    // ...
  }
})
```

**用户操作流程**：
```
1. 在 docs/AI/llm/ 下新建 my-article.md
2. 写好内容，添加 frontmatter（title, date, categories, tags）
3. 运行 sh scripts/publish.sh AI/llm/my-article.md
4. 自动处理图片 + git push
5. GitHub Actions 自动构建部署
6. 导航栏和侧边栏自动更新，无需手动维护
```

### 3.3 板块设计

三个板块：**AI**（默认展示）、**Life**、**History**

```
┌──────────────────────────────────────────────────┐
│                blog.lys2021.com                   │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │          [ AI ]  [ Life ]  [ History ]        │ │  ← 顶部导航（自动生成）
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────┐  ┌───────────────────────────────┐ │
│  │ llm/     │  │                               │ │
│  │  - xxx   │  │  ● 大模型基础（一）   2025-04-22 │ │
│  │  - xxx   │  │  ● BERT模型训练实践  2025-04-21 │ │
│  │ bert/    │  │  ...                          │ │
│  │  - xxx   │  │                               │ │
│  └──────────┘  └───────────────────────────────┘ │
│  侧边栏（自动生成）    文章列表                    │
└──────────────────────────────────────────────────┘
```

### 3.4 WordPress 分类映射

| WordPress 分类 | 数量 | 新板块目录 | 说明 |
|----------------|------|------------|------|
| AI | 2 | `AI/` | AI 相关文章 |
| Poems, Novels | 15 | `Life/poems/` | 生活-诗歌 |
| ARTICLES, Essays | 25 | `Life/essays/` | 生活-随笔 |
| University 相关 | 12 | `Life/campus/` | 生活-校园 |
| Java, Software Architect | 24 | `History/java/` | 历史-Java |
| ALGORITHM, Basic/Intermediate Algorithm | 81 | `History/algorithm/` | 历史-算法 |
| Q&A | 90 | `History/qa/` | 历史-问答 |
| Linux | 9 | `History/linux/` | 历史-Linux |
| DataBase System | 8 | `History/database/` | 历史-数据库 |
| Computer Network 等 | 15 | `History/cs-fundamentals/` | 历史-计算机基础 |
| Python, Django, C/C++ | 10 | `History/python/` | 历史-其他语言 |
| Tips | 7 | `History/tips/` | 历史-技巧 |

---

## 四、Markdown 扩展语法支持

### 4.1 需要支持的语法

| 语法 | 说明 | 实现方式 |
|------|------|----------|
| 内联数学公式 | `$E=mc^2$` | `markdown-it-mathjax3` 或 `markdown-it-katex` |
| 块级数学公式 | `$$E=mc^2$$` | 同上 |
| `\( \)` 数学公式 | `\(E=mc^2\)` | 同上 |
| `\[ \]` 数学公式 | `\[E=mc^2\]` | 同上 |
| Mermaid 图表 | ` ```mermaid ` | `vitepress-plugin-mermaid` |
| GraphTD | ` ```mermaid graph TD ` | 同上（Mermaid 子集） |
| HTML 表格 | `<table>...</table>` | VitePress 原生支持 |

### 4.2 package.json 依赖更新

```json
{
  "dependencies": {
    "vitepress": "^1.3.2",
    "@nolebase/vitepress-plugin-enhanced-readabilities": "^2.4.0",
    "@nolebase/vitepress-plugin-git-changelog": "^2.4.0",
    "@nolebase/vitepress-plugin-highlight-targeted-heading": "^2.4.0",
    "vitepress-plugin-codeblocks-fold": "^1.2.28",
    "vitepress-plugin-mermaid": "^2.0.16",
    "markdown-it-footnote": "^4.0.0",
    "typed.js": "^2.1.0"
  },
  "devDependencies": {
    "markdown-it-mathjax3": "^4.3.2"
  }
}
```

### 4.3 VitePress 配置（数学公式 + Mermaid）

```ts
// .vitepress/config/index.mts
import markdownItMathjax3 from 'markdown-it-mathjax3'

export default defineConfig({
  markdown: {
    math: true,
    config: (md) => {
      md.use(markdownItMathjax3)
    }
  },
  // Mermaid 通过 vitepress-plugin-mermaid 注入
})
```

---

## 五、内置脚本设计

### 5.1 publish.sh —— 发布文章

**功能**：将写好的 `.md` 文件发布到博客，自动处理图片。

**用法**：`sh scripts/publish.sh AI/llm/my-article.md`

**流程**：
```
1. 检查文件是否存在
2. 读取 Markdown 文件内容
3. 扫描所有图片引用：
   - 绝对路径：/home/user/photo.png → 上传到图床仓库
   - 相对路径：./images/photo.png → 上传到图床仓库
   - HTTP URL：https://xxx.com/photo.png → 下载后上传到图床仓库
   - Base64：data:image/png;base64,... → 解码后上传到图床仓库
4. 将图片上传到 liyyro-photo 仓库的 images/年/月/ 目录
5. 替换 Markdown 中的图片链接为 jsDelivr URL
6. git add + commit + push 到博客仓库
7. 输出发布成功信息
```

**图片命名规则**：`{文章slug}-{hash}.{ext}`，避免冲突。

### 5.2 update.sh —— 更新文章

**功能**：更新已发布的文章，扫描新图片，已有的图片不重复上传。

**用法**：`sh scripts/update.sh AI/llm/my-article.md`

**流程**：
```
1. 检查文件是否存在
2. 读取 Markdown 文件内容
3. 扫描所有图片引用
4. 对比已有图片 URL：
   - 已是 jsDelivr URL → 跳过
   - 新图片（绝对路径/URL/base64）→ 上传到图床
5. 替换新图片链接为 jsDelivr URL
6. git add + commit + push
7. 输出更新成功信息
```

### 5.3 delete.sh —— 删除文章

**功能**：删除文章，同时删除远端图床仓库中的对应图片。

**用法**：`sh scripts/delete.sh AI/llm/my-article.md`

**流程**：
```
1. 检查文件是否存在
2. 读取 Markdown 文件内容
3. 提取所有 jsDelivr 图片 URL
4. 从 liyyro-photo 仓库中删除对应图片文件
5. git add + commit + push 图床仓库
6. 删除博客仓库中的 Markdown 文件
7. git add + commit + push 博客仓库
8. 输出删除成功信息
```

### 5.4 脚本依赖

```bash
# 系统依赖
apt install git curl jq

# 图床仓库需要提前 clone 到本地
git clone https://github.com/Doge2077/liyyro-photo.git /path/to/liyyro-photo
```

### 5.5 脚本配置文件（scripts/config.sh）

```bash
#!/bin/bash
# 图床仓库本地路径
PHOTO_REPO="/path/to/liyyro-photo"
# 图床仓库 GitHub 地址
PHOTO_GITHUB="Doge2077/liyyro-photo"
# jsDelivr CDN 前缀
CDN_PREFIX="https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"
# 博客仓库本地路径
BLOG_REPO="/root/liyyro"
# 当前年月
CURRENT_YEAR=$(date +%Y)
CURRENT_MONTH=$(date +%m)
```

---

## 六、迁移方案

### 6.1 迁移流程

```
导出 WP 文章 → HTML→Markdown → 图片迁移 → URL 替换 → 逐篇审查
```

### 6.2 导出脚本（wp-export.py）

```python
import mysql.connector
import html2text
import os

db = mysql.connector.connect(
    host="127.0.0.1", user="lys2021_com",
    password="FZ4GHdHfFpX384FG", database="lys2021_com"
)

QUERY = """
SELECT p.ID, p.post_title, p.post_date, p.post_content, p.post_name,
       p.post_excerpt, GROUP_CONCAT(t.name) as categories
FROM wp_posts p
LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
LEFT JOIN wp_terms t ON tt.term_id = t.term_id
WHERE p.post_type='post' AND p.post_status='publish'
GROUP BY p.ID ORDER BY p.post_date DESC
"""

converter = html2text.HTML2Text()
converter.body_width = 0
```

### 6.3 图片迁移脚本（migrate-images.py）

```python
import os, re, json, shutil

WP_UPLOADS = "/var/www/html/wp-content/uploads"
BLOG_ASSETS = "/path/to/liyyro-photo/images"

def is_thumbnail(filename):
    return bool(re.search(r'-\d+x\d+\.\w+$', filename))

# 遍历 → 过滤缩略图 → 复制 → 生成 URL 映射表
```

### 6.4 frontmatter 格式

```yaml
---
title: "JDK源码系列（五）"
date: 2024-10-29
categories: [Java]
tags: [JDK, 源码]
description: "深入分析JDK核心类库源码"
---
```

### 6.5 逐篇审查清单

每篇迁移的文章需要检查：
- [ ] frontmatter 格式正确（title/date/categories/tags）
- [ ] 图片链接已替换为 jsDelivr URL
- [ ] 代码块语法正确（语言标记、缩进）
- [ ] 数学公式语法正确（`$...$`、`$$...$$`、`\( ... \)`、`\[ ... \]`）
- [ ] HTML 表格渲染正确
- [ ] 链接可访问
- [ ] 特殊字符转义正确

---

## 七、部署方案

### 7.1 架构

```
GitHub Actions 构建 → rsync 部署到服务器 → Nginx 反向代理（blog.lys2021.com）
```

### 7.2 GitHub Actions（deploy.yml）

```yaml
name: Deploy Blog
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run docs:build
      - name: Deploy via rsync
        uses: Burnett01/rsync-deployments@7.0.1
        with:
          switches: -avzr --delete
          path: dist/
          remote_path: /var/www/blog/
          remote_host: ${{ secrets.REMOTE_HOST }}
          remote_user: ${{ secrets.REMOTE_USER }}
          remote_key: ${{ secrets.SSH_PRIVATE_KEY }}
```

### 7.3 Nginx 配置

```nginx
# blog.lys2021.com
server {
    listen 80;
    server_name blog.lys2021.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name blog.lys2021.com;

    ssl_certificate /etc/letsencrypt/live/blog.lys2021.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/blog.lys2021.com/privkey.pem;

    root /var/www/blog;
    index index.html;

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri.html $uri/ /index.html;
    }
}
```

### 7.4 SSL 证书

```bash
# 申请证书
certbot certonly --nginx -d blog.lys2021.com

# 自动续期（已由 certbot 自动配置）
# crontab: 0 0 1 * * certbot renew --quiet
```

---

## 八、实施步骤

| 阶段 | 耗时 | 内容 |
|------|------|------|
| 项目初始化 | 1天 | VitePress 项目 + 主题 + Tab 组件 + 数学公式/Mermaid 支持 |
| 图床搭建 | 1天 | 图片迁移 + URL 映射表 + liyyro-photo 仓库初始化 |
| 文章迁移 | 3-4天 | 导出 + 转换 + 替换 + **逐篇审查**（200篇） |
| 脚本开发 | 1天 | publish.sh + update.sh + delete.sh |
| 部署配置 | 1天 | Nginx + SSL + GitHub Actions + DNS |
| 验证优化 | 1天 | 测试 + SEO + 性能 |

**总计：约 8-9 天**

---

## 九、风险与应对

| 风险 | 应对 |
|------|------|
| jsDelivr 波动 | 图片同时放 `docs/public/images/` 本地备份 |
| HTML→Markdown 不完美 | 200 篇文章逐篇审查修正 |
| 数学公式渲染问题 | 测试各种公式语法，确保 MathJax3 配置正确 |
| Mermaid 渲染问题 | 测试各类图表语法 |
| MySQL 配置问题 | 临时修改 `/etc/mysql/my.cnf` 中的 `performance_schema=off` |

---

## 十、待确认事项

- [x] 域名：使用 `blog.lys2021.com` 子域名
- [x] WordPress：保留不动
- [x] 全量迁移：200 篇文章全部迁移
- [x] SSH：已配置
- [x] 图床仓库：`Doge2077/liyyro-photo`
