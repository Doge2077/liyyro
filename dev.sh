#!/bin/bash
# ============================================================
# dev.sh - 本地开发启动脚本
# 用法: bash dev.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  本地开发服务器${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装依赖...${NC}"
    npm install --legacy-peer-deps
fi

echo -e "${GREEN}启动开发服务器: http://localhost:8081${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止${NC}"
echo ""

npm run docs:dev
