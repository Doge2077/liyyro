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

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  博客部署脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查依赖
echo -e "${YELLOW}[1/5] 检查依赖...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: node 未安装${NC}"
    exit 1
fi
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: docker 未安装${NC}"
    exit 1
fi
if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null; then
    echo -e "${RED}错误: docker compose 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ 依赖检查通过${NC}"

# 安装依赖
echo -e "${YELLOW}[2/5] 安装 npm 依赖...${NC}"
npm ci --legacy-peer-deps 2>/dev/null || npm install --legacy-peer-deps
echo -e "${GREEN}  ✓ 依赖安装完成${NC}"

# 构建
echo -e "${YELLOW}[3/5] 构建 VitePress...${NC}"
export NODE_OPTIONS="--max-old-space-size=8192"
npm run docs:build
echo -e "${GREEN}  ✓ 构建完成${NC}"

# 停止旧容器
echo -e "${YELLOW}[4/5] 停止旧容器...${NC}"
docker compose down 2>/dev/null || true
echo -e "${GREEN}  ✓ 旧容器已停止${NC}"

# 构建并启动新容器
echo -e "${YELLOW}[5/5] 构建并启动新容器...${NC}"
docker compose up -d --build
echo -e "${GREEN}  ✓ 容器已启动${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 验证
echo -e "${YELLOW}验证服务状态...${NC}"
docker compose ps
echo ""
echo -e "${GREEN}访问地址: https://blog.lys2021.com/${NC}"
