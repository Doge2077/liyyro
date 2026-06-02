#!/bin/bash
# update.sh - 更新已发布的文章
# 用法: sh scripts/update.sh AI/llm/my-article.md

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
    echo "用法: sh scripts/update.sh <文章路径>"
    echo "示例: sh scripts/update.sh AI/llm/my-article.md"
    exit 1
fi

ARTICLE_PATH="$1"
FULL_PATH="$BLOG_REPO/docs/$ARTICLE_PATH"

# 检查文件是否存在
if [ ! -f "$FULL_PATH" ]; then
    echo -e "${RED}错误: 文件不存在: $FULL_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}更新文章: $ARTICLE_PATH${NC}"
echo -e "${GREEN}========================================${NC}"

# 读取文件内容
CONTENT=$(cat "$FULL_PATH")

# 获取文章 slug
SLUG=$(basename "$ARTICLE_PATH" .md)

# 当前年月
YEAR=$(date +%Y)
MONTH=$(date +%m)

# 扫描并处理新图片（跳过已是 jsDelivr 的）
echo -e "${YELLOW}扫描新图片引用...${NC}"

NEW_IMAGE_COUNT=0

process_local_image() {
    local img_path="$1"
    
    if [[ "$img_path" == ./* ]] || [[ "$img_path" == ../* ]]; then
        img_path="$(dirname "$FULL_PATH")/$img_path"
    fi
    
    if [ ! -f "$img_path" ]; then
        echo -e "${RED}  警告: 图片不存在: $img_path${NC}"
        return
    fi
    
    HASH=$(md5sum "$img_path" | cut -c1-8)
    EXT="${img_path##*.}"
    NEW_FILENAME="${SLUG}-${HASH}.${EXT}"
    
    TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
    mkdir -p "$TARGET_DIR"
    cp "$img_path" "$TARGET_DIR/$NEW_FILENAME"
    
    CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
    echo -e "${GREEN}  已上传: $(basename "$img_path") -> $CDN_URL${NC}"
    
    sed -i "s|$img_path|$CDN_URL|g" "$FULL_PATH"
    NEW_IMAGE_COUNT=$((NEW_IMAGE_COUNT + 1))
}

process_http_image() {
    local url="$1"
    
    if [[ "$url" == *"cdn.jsdelivr.net"* ]]; then
        return
    fi
    
    TEMP_FILE="/tmp/update_img_$"
    EXT="${url##*.}"
    EXT="${EXT%%\?*}"
    
    if curl -sL "$url" -o "$TEMP_FILE.$EXT" 2>/dev/null; then
        HASH=$(md5sum "$TEMP_FILE.$EXT" | cut -c1-8)
        NEW_FILENAME="${SLUG}-${HASH}.${EXT}"
        
        TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
        mkdir -p "$TARGET_DIR"
        mv "$TEMP_FILE.$EXT" "$TARGET_DIR/$NEW_FILENAME"
        
        CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
        echo -e "${GREEN}  已下载并上传: $url -> $CDN_URL${NC}"
        
        sed -i "s|$url|$CDN_URL|g" "$FULL_PATH"
        NEW_IMAGE_COUNT=$((NEW_IMAGE_COUNT + 1))
    else
        echo -e "${RED}  警告: 无法下载: $url${NC}"
    fi
}

process_base64_image() {
    local data_url="$1"
    
    FORMAT=$(echo "$data_url" | grep -oP 'data:image/\K[^;]+')
    BASE64_DATA=$(echo "$data_url" | grep -oP 'base64,\K[^"]+')
    
    if [ -z "$FORMAT" ] || [ -z "$BASE64_DATA" ]; then
        return
    fi
    
    TEMP_FILE="/tmp/update_img_$.$FORMAT"
    echo "$BASE64_DATA" | base64 -d > "$TEMP_FILE"
    
    HASH=$(md5sum "$TEMP_FILE" | cut -c1-8)
    NEW_FILENAME="${SLUG}-${HASH}.${FORMAT}"
    
    TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
    mkdir -p "$TARGET_DIR"
    mv "$TEMP_FILE" "$TARGET_DIR/$NEW_FILENAME"
    
    CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
    echo -e "${GREEN}  已解码并上传: base64 image -> $CDN_URL${NC}"
    
    ESCAPED_DATA_URL=$(echo "$data_url" | sed 's/[&/\]/\\&/g')
    sed -i "s|$ESCAPED_DATA_URL|$CDN_URL|g" "$FULL_PATH"
    NEW_IMAGE_COUNT=$((NEW_IMAGE_COUNT + 1))
}

while IFS= read -r line; do
    if echo "$line" | grep -qP '!\[.*?\]\(.*?\)'; then
        IMG_URL=$(echo "$line" | grep -oP '!\[.*?\]\(\K[^)]+')
        if [ -n "$IMG_URL" ]; then
            if [[ "$IMG_URL" == http* ]]; then
                process_http_image "$IMG_URL"
            elif [[ "$IMG_URL" == data:* ]]; then
                process_base64_image "$IMG_URL"
            elif [[ "$IMG_URL" != *"cdn.jsdelivr.net"* ]]; then
                process_local_image "$IMG_URL"
            fi
        fi
    fi
    
    if echo "$line" | grep -qP '<img.*?src=".*?"'; then
        IMG_URL=$(echo "$line" | grep -oP 'src="\K[^"]+')
        if [ -n "$IMG_URL" ]; then
            if [[ "$IMG_URL" == http* ]]; then
                process_http_image "$IMG_URL"
            elif [[ "$IMG_URL" == data:* ]]; then
                process_base64_image "$IMG_URL"
            elif [[ "$IMG_URL" != *"cdn.jsdelivr.net"* ]]; then
                process_local_image "$IMG_URL"
            fi
        fi
    fi
done < "$FULL_PATH"

echo -e "${YELLOW}发现 $NEW_IMAGE_COUNT 张新图片${NC}"

# 提交图床仓库（如果有新图片）
if [ $NEW_IMAGE_COUNT -gt 0 ]; then
    echo -e "${YELLOW}提交图床仓库...${NC}"
    cd "$PHOTO_REPO"
    git add .
    git commit -m "update images for $ARTICLE_PATH"
    git push origin main
fi

# 提交博客仓库
echo -e "${YELLOW}提交博客仓库...${NC}"
cd "$BLOG_REPO"
git add "docs/$ARTICLE_PATH"
git commit -m "update: $ARTICLE_PATH"
git push origin main

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}更新成功!${NC}"
echo -e "${GREEN}文章: $ARTICLE_PATH${NC}"
echo -e "${GREEN}新增图片: $NEW_IMAGE_COUNT${NC}"
echo -e "${GREEN}========================================${NC}"
