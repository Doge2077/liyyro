#!/bin/bash
# ============================================================
# delete.sh - 删除文章
# 用法: bash scripts/delete.sh <文件路径>
# 示例: bash scripts/delete.sh docs/AI/要删除的文章.md
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_REPO="$(dirname "$SCRIPT_DIR")"
PHOTO_REPO="/root/liyyro-photo"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}用法: bash scripts/delete.sh <文件路径>${NC}"
    echo -e "示例: bash scripts/delete.sh docs/AI/要删除的文章.md"
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

echo -e "${YELLOW}删除文章: $FILE_PATH${NC}"
read -p "确认删除？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消${NC}"
    exit 0
fi

# 删除文件
rm "$FILE_PATH"
echo -e "${GREEN}文件已删除${NC}"

# 提交并推送
echo -e "${YELLOW}提交到 Git...${NC}"
cd "$BLOG_REPO"
git add .
git commit -m "delete: $(basename "$FILE_PATH" .md)"
git push origin main

echo -e "${GREEN}删除完成！${NC}"
