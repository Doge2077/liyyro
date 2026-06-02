#!/usr/bin/env python3
"""
外部图片迁移脚本
将非 jsDelivr CDN 的图片下载并上传到 liyyro-photo 仓库
"""

import os
import re
import json
import hashlib
import shutil
import subprocess
import urllib.parse
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
PHOTO_REPO = "/root/liyyro-photo"
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"
REPORT_FILE = "/root/liyyro/scripts/image-migration-report.md"

# 需要迁移的图片来源域名
EXTERNAL_DOMAINS = [
    "cdn.acwing.com",
    "img-blog.csdnimg.cn",
    "image.itbaima.net",
    "image.itbaima.cn",
    "acwing.com",
    "csdnimg.cn",
]

def is_external_image(url):
    """判断是否为外部图片"""
    # 排除 jsDelivr CDN
    if "cdn.jsdelivr.net" in url:
        return False
    # 排除 data URL
    if url.startswith("data:"):
        return False
    # 检查是否为外部域名
    for domain in EXTERNAL_DOMAINS:
        if domain in url:
            return True
    # 检查是否为 HTTP(S) URL
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False

def download_image(url, timeout=30):
    """下载图片"""
    try:
        # 使用 curl 下载
        result = subprocess.run(
            ["curl", "-sL", "-o", "-", "--max-time", str(timeout), url],
            capture_output=True,
            timeout=timeout + 5
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            return result.stdout
        return None
    except Exception as e:
        return None

def get_file_hash(data):
    """计算文件哈希"""
    return hashlib.md5(data).hexdigest()[:8]

def get_extension_from_url(url):
    """从 URL 获取文件扩展名"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    # 移除查询参数
    path = path.split("?")[0]
    # 获取扩展名
    _, ext = os.path.splitext(path)
    if ext.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"]:
        return ext.lower()
    return ".png"  # 默认

def get_extension_from_content(data):
    """从内容判断文件类型"""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return ".png"
    elif data[:3] == b'\xff\xd8\xff':
        return ".jpg"
    elif data[:4] == b'GIF8':
        return ".gif"
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return ".webp"
    return ".png"

def upload_to_repo(image_data, original_url, year, month):
    """上传图片到 liyyro-photo 仓库"""
    # 计算哈希
    file_hash = get_file_hash(image_data)
    
    # 获取扩展名
    ext = get_extension_from_content(image_data)
    
    # 生成文件名
    filename = f"external-{file_hash}{ext}"
    
    # 创建目录
    target_dir = os.path.join(PHOTO_REPO, "images", year, month)
    os.makedirs(target_dir, exist_ok=True)
    
    # 保存文件
    target_path = os.path.join(target_dir, filename)
    with open(target_path, "wb") as f:
        f.write(image_data)
    
    # 生成 CDN URL
    cdn_url = f"{CDN_PREFIX}/{year}/{month}/{filename}"
    
    return cdn_url

def process_markdown_file(filepath):
    """处理单个 markdown 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    migrations = []
    
    # 匹配图片 URL
    # Markdown: ![alt](url)
    # HTML: <img src="url">
    patterns = [
        (r'!\[([^\]]*)\]\(([^)]+)\)', "markdown"),  # ![alt](url)
        (r'<img[^>]+src="([^"]+)"[^>]*>', "html"),   # <img src="url">
    ]
    
    for pattern, ptype in patterns:
        for match in re.finditer(pattern, content):
            if ptype == "markdown":
                alt = match.group(1)
                url = match.group(2)
            else:
                url = match.group(1)
            
            # 清理 URL
            url = url.strip()
            
            # 检查是否为外部图片
            if not is_external_image(url):
                continue
            
            # 跳过格式错误的 URL
            if url.startswith("<") or ">" in url:
                continue
            
            # 下载图片
            print(f"    下载: {url[:80]}...")
            image_data = download_image(url)
            
            if image_data is None:
                print(f"    ✗ 下载失败")
                migrations.append({"url": url, "status": "failed", "reason": "download_failed"})
                continue
            
            # 确定年月
            now = datetime.now()
            year = str(now.year)
            month = f"{now.month:02d}"
            
            # 上传到仓库
            try:
                cdn_url = upload_to_repo(image_data, url, year, month)
                print(f"    ✓ 上传成功: {cdn_url[:80]}...")
                
                # 替换 URL
                content = content.replace(url, cdn_url)
                migrations.append({"url": url, "status": "success", "new_url": cdn_url})
            except Exception as e:
                print(f"    ✗ 上传失败: {e}")
                migrations.append({"url": url, "status": "failed", "reason": str(e)})
    
    # 保存修改后的文件
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    return migrations

def main():
    print("=" * 60)
    print("外部图片迁移工具")
    print("=" * 60)
    
    # 统计
    total_files = 0
    total_images = 0
    success_count = 0
    failed_count = 0
    all_migrations = []
    
    # 遍历所有 markdown 文件
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, DOCS_DIR)
            
            # 检查文件是否包含外部图片
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            has_external = False
            for domain in EXTERNAL_DOMAINS:
                if domain in content:
                    has_external = True
                    break
            
            if not has_external:
                continue
            
            print(f"\n[{total_files + 1}] 处理: {rel_path}")
            total_files += 1
            
            migrations = process_markdown_file(filepath)
            
            for m in migrations:
                total_images += 1
                if m["status"] == "success":
                    success_count += 1
                else:
                    failed_count += 1
            
            all_migrations.append({
                "file": rel_path,
                "migrations": migrations
            })
    
    # 提交图床仓库
    if success_count > 0:
        print(f"\n提交图床仓库...")
        os.chdir(PHOTO_REPO)
        subprocess.run(["git", "add", "."])
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if result.returncode != 0:
            subprocess.run(["git", "commit", "-m", f"migrate: {success_count} external images"])
            subprocess.run(["git", "push", "origin", "main"])
            print("✓ 图床仓库已提交")
    
    # 生成报告
    report = f"""# 外部图片迁移报告

**迁移时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 统计

| 项目 | 数量 |
|------|------|
| 处理文件数 | {total_files} |
| 总图片数 | {total_images} |
| 成功迁移 | {success_count} |
| 迁移失败 | {failed_count} |

## 详情

"""
    
    for item in all_migrations:
        report += f"### {item['file']}\n\n"
        for m in item["migrations"]:
            if m["status"] == "success":
                report += f"- ✅ `{m['url'][:60]}...` → `{m['new_url'][:60]}...`\n"
            else:
                report += f"- ❌ `{m['url'][:60]}...` - {m.get('reason', 'unknown')}\n"
        report += "\n"
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n{'=' * 60}")
    print(f"迁移完成!")
    print(f"  处理文件: {total_files}")
    print(f"  总图片数: {total_images}")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")
    print(f"  报告: {REPORT_FILE}")

if __name__ == "__main__":
    main()
