#!/bin/bash
# ============================================================
# update.sh - 更新已发布的文章
# 用法: bash scripts/update.sh <文件路径>
# 示例: bash scripts/update.sh docs/AI/已发布的文章.md
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_REPO="$(dirname "$SCRIPT_DIR")"
PHOTO_REPO="/root/liyyro-photo"
CDN_PREFIX="https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}用法: bash scripts/update.sh <文件路径>${NC}"
    echo -e "示例: bash scripts/update.sh docs/AI/已发布的文章.md"
    exit 1
fi

FILE_PATH="$1"

# 如果是相对路径，相对于 blog 仓库
if [[ ! "$FILE_PATH" = /* ]]; then
    FILE_PATH="$BLOG_REPO/$FILE_PATH"
fi

if [ ! -f "$FILE_PATH" ]; then
    echo -e "${RED}错误: 文件不存在: $FILE_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}更新文章: $FILE_PATH${NC}"

# 扫描图片并上传到图床（同 publish.sh）
echo -e "${YELLOW}扫描图片...${NC}"
python3 -c "
import re
import os
import hashlib
import shutil
from datetime import datetime

filepath = '$FILE_PATH'
photo_repo = '$PHOTO_REPO'
cdn_prefix = '$CDN_PREFIX'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
matches = re.findall(img_pattern, content)

changed = False
for alt, url in matches:
    url = url.strip()
    if 'cdn.jsdelivr.net' in url:
        continue
    if url.startswith('http://') or url.startswith('https://'):
        continue
    if url.startswith('./') or url.startswith('../'):
        img_path = os.path.join(os.path.dirname(filepath), url)
    else:
        img_path = os.path.join(os.path.dirname(filepath), url)
    
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]
        ext = os.path.splitext(img_path)[1]
        new_filename = f'{file_hash}{ext}'
        
        year = datetime.now().strftime('%Y')
        month = datetime.now().strftime('%m')
        target_dir = os.path.join(photo_repo, 'images', year, month)
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, new_filename)
        shutil.copy2(img_path, target_path)
        
        cdn_url = f'{cdn_prefix}/{year}/{month}/{new_filename}'
        content = content.replace(url, cdn_url)
        changed = True
        print(f'  上传: {url} -> {cdn_url}')

if changed:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('图片处理完成')
else:
    print('无新图片需要上传')
" 2>&1

echo -e "${YELLOW}提交到 Git...${NC}"
cd "$BLOG_REPO"
git add .
git commit -m "update: $(basename "$FILE_PATH" .md)"
git push origin main

echo -e "${GREEN}更新完成！${NC}"
