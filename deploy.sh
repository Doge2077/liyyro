#!/bin/bash
# ============================================================
# deploy.sh - 一键构建并部署博客到本机 Docker
# 用法: bash deploy.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PORT="${PORT:-8081}"
URL="${URL:-http://127.0.0.1:${PORT}/}"
BUILD_SCRIPT="${BUILD_SCRIPT:-docs:build}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  博客部署脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${YELLOW}[1/5] 检查依赖...${NC}"
for cmd in node npm docker; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo -e "${RED}错误: ${cmd} 未安装${NC}"
        exit 1
    fi
done

if ! docker compose version >/dev/null 2>&1; then
    echo -e "${RED}错误: docker compose 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}  依赖检查通过${NC}"

echo -e "${YELLOW}[2/5] 安装 npm 依赖...${NC}"
if [ -f package-lock.json ]; then
    npm ci --legacy-peer-deps
else
    npm install --legacy-peer-deps
fi
echo -e "${GREEN}  依赖安装完成${NC}"

echo -e "${YELLOW}[3/5] 构建 VitePress (${BUILD_SCRIPT})...${NC}"
export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=1024}"
npm run "$BUILD_SCRIPT"
echo -e "${GREEN}  构建完成${NC}"

echo -e "${YELLOW}[4/5] 重启容器...${NC}"
docker compose down --remove-orphans 2>/dev/null || true
docker compose up -d --build
echo -e "${GREEN}  容器已启动${NC}"

echo -e "${YELLOW}[5/5] 验证服务状态...${NC}"
for i in $(seq 1 60); do
    if curl -fsS "$URL" >/dev/null 2>&1; then
        echo -e "${GREEN}  服务验证通过${NC}"
        echo ""
        docker compose ps
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  部署完成${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${GREEN}访问地址: ${URL}${NC}"
        exit 0
    fi
    sleep 1
done

echo -e "${RED}服务验证超时: ${URL}${NC}"
docker compose ps
exit 1
