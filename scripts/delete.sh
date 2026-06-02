#!/bin/bash
# delete.sh - 删除文章及其图片
# 用法: sh scripts/delete.sh AI/llm/my-article.md

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_REPO="$(dirname "$SCRIPT_DIR")"
PHOTO_REPO="/root/liyyro-photo"
CDN_PREFIX="https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查参数
if [ -z "$1" ]; then
    echo -e "${RED}错误: 请提供文章路径${NC}"
    echo "用法: sh scripts/delete.sh <文章路径>"
    echo "示例: sh scripts/delete.sh AI/llm/my-article.md"
    exit 1
fi

ARTICLE_PATH="$1"
FULL_PATH="$BLOG_REPO/docs/$ARTICLE_PATH"

# 检查文件是否存在
if [ ! -f "$FULL_PATH" ]; then
    echo -e "${RED}错误: 文件不存在: $FULL_PATH${NC}"
    exit 1
fi

echo -e "${RED}========================================${NC}"
echo -e "${RED}删除文章: $ARTICLE_PATH${NC}"
echo -e "${RED}========================================${NC}"

# 确认删除
read -p "确定要删除这篇文章吗？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消删除${NC}"
    exit 0
fi

# 提取文章中的 jsDelivr 图片 URL
echo -e "${YELLOW}提取图片引用...${NC}"

IMAGE_URLS=()
while IFS= read -r line; do
    # 提取 Markdown 图片 URL
    if echo "$line" | grep -qP '!\[.*?\]\(.*?\)'; then
        IMG_URL=$(echo "$line" | grep -oP '!\[.*?\]\(\K[^)]+')
        if [[ "$IMG_URL" == *"cdn.jsdelivr.net"* ]]; then
            IMAGE_URLS+=("$IMG_URL")
        fi
    fi
    
    # 提取 HTML img 标签 URL
    if echo "$line" | grep -qP '<img.*?src=".*?"'; then
        IMG_URL=$(echo "$line" | grep -oP 'src="\K[^"]+')
        if [[ "$IMG_URL" == *"cdn.jsdelivr.net"* ]]; then
            IMAGE_URLS+=("$IMG_URL")
        fi
    fi
done < "$FULL_PATH"

echo -e "${YELLOW}找到 ${#IMAGE_URLS[@]} 张图片${NC}"

# 从图床仓库删除图片
if [ ${#IMAGE_URLS[@]} -gt 0 ]; then
    echo -e "${YELLOW}从图床仓库删除图片...${NC}"
    
    cd "$PHOTO_REPO"
    
    for url in "${IMAGE_URLS[@]}"; do
        # 从 URL 提取文件路径
        # URL 格式: https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/06/file.png
        FILE_PATH=$(echo "$url" | grep -oP 'images/.*$')
        
        if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
            rm -f "$FILE_PATH"
            echo -e "${GREEN}  已删除: $FILE_PATH${NC}"
        fi
    done
    
    # 提交图床仓库
    git add .
    if ! git diff --cached --quiet; then
        git commit -m "delete images for $ARTICLE_PATH"
        git push origin main
        echo -e "${GREEN}图床仓库已更新${NC}"
    fi
fi

# 删除文章文件
echo -e "${YELLOW}删除文章文件...${NC}"
rm -f "$FULL_PATH"
echo -e "${GREEN}已删除: $FULL_PATH${NC}"

# 检查目录是否为空，如果为空则删除
DIR_PATH=$(dirname "$FULL_PATH")
if [ "$DIR_PATH" != "$BLOG_REPO/docs" ] && [ -z "$(ls -A "$DIR_PATH" 2>/dev/null)" ]; then
    rmdir "$DIR_PATH"
    echo -e "${GREEN}已删除空目录: $DIR_PATH${NC}"
fi

# 提交博客仓库
echo -e "${YELLOW}提交博客仓库...${NC}"
cd "$BLOG_REPO"
git add -A
git commit -m "delete: $ARTICLE_PATH"
git push origin main

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}删除成功!${NC}"
echo -e "${GREEN}文章: $ARTICLE_PATH${NC}"
echo -e "${GREEN}删除图片: ${#IMAGE_URLS[@]} 张${NC}"
echo -e "${GREEN}========================================${NC}"
