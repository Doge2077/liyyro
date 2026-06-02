#!/bin/bash
# publish.sh - 发布文章到博客
# 用法: sh scripts/publish.sh AI/llm/my-article.md

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
    echo "用法: sh scripts/publish.sh <文章路径>"
    echo "示例: sh scripts/publish.sh AI/llm/my-article.md"
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
echo -e "${GREEN}发布文章: $ARTICLE_PATH${NC}"
echo -e "${GREEN}========================================${NC}"

# 读取文件内容
CONTENT=$(cat "$FULL_PATH")

# 获取文章 slug（文件名不含扩展名）
SLUG=$(basename "$ARTICLE_PATH" .md)

# 当前年月
YEAR=$(date +%Y)
MONTH=$(date +%m)

# 扫描并处理图片
echo -e "${YELLOW}扫描图片引用...${NC}"

# 处理绝对路径图片 (如 /home/user/photo.png 或 ./images/photo.png)
process_local_image() {
    local img_path="$1"
    
    # 如果是相对路径，转换为绝对路径
    if [[ "$img_path" == ./* ]] || [[ "$img_path" == ../* ]]; then
        img_path="$(dirname "$FULL_PATH")/$img_path"
    fi
    
    # 检查文件是否存在
    if [ ! -f "$img_path" ]; then
        echo -e "${RED}  警告: 图片不存在: $img_path${NC}"
        return
    fi
    
    # 计算文件哈希
    HASH=$(md5sum "$img_path" | cut -c1-8)
    EXT="${img_path##*.}"
    NEW_FILENAME="${SLUG}-${HASH}.${EXT}"
    
    # 复制到图床仓库
    TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
    mkdir -p "$TARGET_DIR"
    cp "$img_path" "$TARGET_DIR/$NEW_FILENAME"
    
    # 生成 CDN URL
    CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
    
    echo -e "${GREEN}  已上传: $(basename "$img_path") -> $CDN_URL${NC}"
    
    # 替换文件中的引用
    sed -i "s|$img_path|$CDN_URL|g" "$FULL_PATH"
}

# 处理 HTTP URL 图片（下载后上传）
process_http_image() {
    local url="$1"
    
    # 跳过已经是 jsDelivr 的 URL
    if [[ "$url" == *"cdn.jsdelivr.net"* ]]; then
        return
    fi
    
    # 下载图片
    TEMP_FILE="/tmp/publish_img_$"
    EXT="${url##*.}"
    EXT="${EXT%%\?*}"  # 移除查询参数
    
    if curl -sL "$url" -o "$TEMP_FILE.$EXT" 2>/dev/null; then
        # 计算哈希
        HASH=$(md5sum "$TEMP_FILE.$EXT" | cut -c1-8)
        NEW_FILENAME="${SLUG}-${HASH}.${EXT}"
        
        # 复制到图床仓库
        TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
        mkdir -p "$TARGET_DIR"
        mv "$TEMP_FILE.$EXT" "$TARGET_DIR/$NEW_FILENAME"
        
        # 生成 CDN URL
        CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
        
        echo -e "${GREEN}  已下载并上传: $url -> $CDN_URL${NC}"
        
        # 替换文件中的引用
        sed -i "s|$url|$CDN_URL|g" "$FULL_PATH"
    else
        echo -e "${RED}  警告: 无法下载: $url${NC}"
    fi
}

# 处理 Base64 图片
process_base64_image() {
    local data_url="$1"
    
    # 提取格式和数据
    FORMAT=$(echo "$data_url" | grep -oP 'data:image/\K[^;]+')
    BASE64_DATA=$(echo "$data_url" | grep -oP 'base64,\K[^"]+')
    
    if [ -z "$FORMAT" ] || [ -z "$BASE64_DATA" ]; then
        return
    fi
    
    # 解码
    TEMP_FILE="/tmp/publish_img_$.$FORMAT"
    echo "$BASE64_DATA" | base64 -d > "$TEMP_FILE"
    
    # 计算哈希
    HASH=$(md5sum "$TEMP_FILE" | cut -c1-8)
    NEW_FILENAME="${SLUG}-${HASH}.${FORMAT}"
    
    # 复制到图床仓库
    TARGET_DIR="$PHOTO_REPO/images/$YEAR/$MONTH"
    mkdir -p "$TARGET_DIR"
    mv "$TEMP_FILE" "$TARGET_DIR/$NEW_FILENAME"
    
    # 生成 CDN URL
    CDN_URL="$CDN_PREFIX/$YEAR/$MONTH/$NEW_FILENAME"
    
    echo -e "${GREEN}  已解码并上传: base64 image -> $CDN_URL${NC}"
    
    # 替换文件中的引用（需要转义特殊字符）
    ESCAPED_DATA_URL=$(echo "$data_url" | sed 's/[&/\]/\\&/g')
    sed -i "s|$ESCAPED_DATA_URL|$CDN_URL|g" "$FULL_PATH"
}

# 扫描 Markdown 中的图片引用
# 格式: ![alt](url) 或 <img src="url">
while IFS= read -r line; do
    # 提取 Markdown 图片 URL
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
    
    # 提取 HTML img 标签 URL
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

# 提交图床仓库
echo -e "${YELLOW}提交图床仓库...${NC}"
cd "$PHOTO_REPO"
git add .
git diff --cached --quiet || git commit -m "add images for $ARTICLE_PATH"
git push origin main

# 提交博客仓库
echo -e "${YELLOW}提交博客仓库...${NC}"
cd "$BLOG_REPO"
git add "docs/$ARTICLE_PATH"
git commit -m "publish: $ARTICLE_PATH"
git push origin main

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}发布成功!${NC}"
echo -e "${GREEN}文章: $ARTICLE_PATH${NC}"
echo -e "${GREEN}========================================${NC}"
