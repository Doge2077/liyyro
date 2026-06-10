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
RED='\033[0;31m'
NC='\033[0m'

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8081}"
URL="http://${HOST}:${PORT}/"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  本地开发服务器${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

if ! command -v node >/dev/null 2>&1; then
    echo -e "${RED}错误: node 未安装${NC}"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo -e "${RED}错误: npm 未安装${NC}"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装依赖...${NC}"
    npm install --legacy-peer-deps
fi

echo -e "${YELLOW}启动开发服务器，等待服务就绪...${NC}"
npx vitepress dev --host "$HOST" --port "$PORT" &
SERVER_PID=$!

cleanup() {
    if kill -0 "$SERVER_PID" >/dev/null 2>&1; then
        kill "$SERVER_PID" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT INT TERM

for i in $(seq 1 60); do
    if curl -fsS "$URL" >/dev/null 2>&1; then
        echo ""
        echo -e "${GREEN}服务已就绪: ${URL}${NC}"
        echo -e "${YELLOW}按 Ctrl+C 停止${NC}"
        wait "$SERVER_PID"
        exit $?
    fi

    if ! kill -0 "$SERVER_PID" >/dev/null 2>&1; then
        echo -e "${RED}开发服务器启动失败${NC}"
        wait "$SERVER_PID"
        exit $?
    fi

    sleep 1
done

echo -e "${RED}开发服务器启动超时: ${URL}${NC}"
exit 1
