#!/usr/bin/env bash
# scripts/setup-dev.sh — 一键启动开发环境
#
# 作用：5 分钟内把后端 + 管理后台 + 移动端都跑起来
# 适用：Linux / macOS（Windows 需 WSL 或 Git Bash）
# 前提：Python 3.10+ / Node 18+ / pnpm 8+ / MySQL / Redis 已装
#
# 用法：
#   chmod +x scripts/setup-dev.sh
#   ./scripts/setup-dev.sh           # 全跑
#   ./scripts/setup-dev.sh backend   # 只跑后端
#   ./scripts/setup-dev.sh frontend  # 只跑管理后台
#   ./scripts/setup-dev.sh mobile    # 只跑移动端
#   ./scripts/setup-dev.sh doctor    # 只跑健康检查

set -euo pipefail

# ───────────────────────────────────────────
# 工具函数
# ───────────────────────────────────────────
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_BLUE='\033[0;34m'
COLOR_OFF='\033[0m'

log()   { echo -e "${COLOR_BLUE}[setup]${COLOR_OFF} $*"; }
ok()    { echo -e "${COLOR_GREEN}[ ✓ ]${COLOR_OFF} $*"; }
warn()  { echo -e "${COLOR_YELLOW}[!]${COLOR_OFF} $*" >&2; }
err()   { echo -e "${COLOR_RED}[✗]${COLOR_OFF} $*" >&2; }

need() {
  command -v "$1" >/dev/null 2>&1 || {
    err "缺少依赖: $1"
    exit 1
  }
}

# ───────────────────────────────────────────
# 前置检查
# ───────────────────────────────────────────
preflight() {
  log "前置依赖检查 ..."
  need python3
  need node
  need npm
  command -v pnpm >/dev/null 2>&1 || warn "pnpm 未装（移动端需要）"
  command -v mysql >/dev/null 2>&1 || warn "mysql CLI 未装（可选）"
  command -v redis-cli >/dev/null 2>&1 || warn "redis-cli 未装（可选）"

  PY_VER=$(python3 -c 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  [[ "$PY_VER" < "3.10" ]] && { err "Python ≥ 3.10，当前 $PY_VER"; exit 1; }
  ok "Python $PY_VER"

  NODE_VER=$(node -v | sed 's/v//')
  ok "Node $NODE_VER"

  ok "前置检查通过"
}

# ───────────────────────────────────────────
# 后端
# ───────────────────────────────────────────
setup_backend() {
  log "配置后端 ..."
  cd ruoyi-fastapi-backend

  # 1. 装依赖
  if [[ ! -d ".venv" ]]; then
    log "创建虚拟环境 .venv"
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install --upgrade pip -q
  pip install -r requirements.txt -q
  ok "Python 依赖装好"

  # 2. env 模板
  if [[ ! -f ".env.dev" ]]; then
    cp .env.example .env.dev
    warn ".env.dev 已生成 —— 请按需修改数据库 / Redis 配置"
  else
    ok ".env.dev 已存在"
  fi

  # 3. 默认密码警示
  if grep -q "admin123" .env.dev 2>/dev/null; then
    warn "默认 admin 密码 admin123 —— 生产前必须改"
  fi

  cd ..
}

start_backend() {
  log "启动后端 (后台进程，端口 19199) ..."
  cd ruoyi-fastapi-backend
  # shellcheck disable=SC1091
  source .venv/bin/activate
  nohup ruoyi app run --env=dev > /tmp/ai-drama-backend.log 2>&1 &
  echo $! > /tmp/ai-drama-backend.pid
  cd ..
  ok "后端 PID=$(cat /tmp/ai-drama-backend.pid) · 日志 /tmp/ai-drama-backend.log"
}

# ───────────────────────────────────────────
# 管理后台
# ───────────────────────────────────────────
setup_frontend() {
  log "配置管理后台 ..."
  cd ruoyi-fastapi-frontend
  npm install --registry=https://registry.npmmirror.com --silent
  ok "管理后台依赖装好"
  cd ..
}

start_frontend() {
  log "启动管理后台 (后台进程，端口 5188) ..."
  cd ruoyi-fastapi-frontend
  nohup npm run dev > /tmp/ai-drama-frontend.log 2>&1 &
  echo $! > /tmp/ai-drama-frontend.pid
  cd ..
  ok "前端 PID=$(cat /tmp/ai-drama-frontend.pid) · 日志 /tmp/ai-drama-frontend.log"
}

# ───────────────────────────────────────────
# 移动端
# ───────────────────────────────────────────
setup_mobile() {
  log "配置移动端 ..."
  command -v pnpm >/dev/null 2>&1 || {
    warn "pnpm 未装，跳过移动端。安装：npm install -g pnpm"
    return
  }
  cd mobile-app
  pnpm config set registry https://registry.npmmirror.com
  pnpm install --silent
  ok "移动端依赖装好"
  cd ..
}

start_mobile() {
  log "启动移动端 H5 (后台进程，默认端口 uni 自动) ..."
  cd mobile-app
  nohup pnpm dev:h5 > /tmp/ai-drama-mobile.log 2>&1 &
  echo $! > /tmp/ai-drama-mobile.pid
  cd ..
  ok "移动端 PID=$(cat /tmp/ai-drama-mobile.pid) · 日志 /tmp/ai-drama-mobile.log"
}

# ───────────────────────────────────────────
# 健康检查
# ───────────────────────────────────────────
doctor() {
  log "健康检查 ..."
  sleep 2

  echo ""
  echo "┌──────────────────────────────┬──────────┐"
  echo "│ 检查项                        │ 状态      │"
  echo "├──────────────────────────────┼──────────┤"
  check_proc() {
    local name=$1 pidfile=$2 port=$3
    if [[ -f "$pidfile" ]] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
      printf "│ %-30s │ ${COLOR_GREEN}✓ 运行中${COLOR_OFF}  │\n" "$name (port $port)"
    else
      printf "│ %-30s │ ${COLOR_RED}✗ 未运行${COLOR_OFF}  │\n" "$name (port $port)"
    fi
  }
  check_proc "Backend"  /tmp/ai-drama-backend.pid  19199
  check_proc "Frontend" /tmp/ai-drama-frontend.pid 5188
  check_proc "Mobile"   /tmp/ai-drama-mobile.pid   auto

  echo "└──────────────────────────────┴──────────┘"
  echo ""
  echo "日志："
  echo "  tail -f /tmp/ai-drama-backend.log"
  echo "  tail -f /tmp/ai-drama-frontend.log"
  echo "  tail -f /tmp/ai-drama-mobile.log"
  echo ""
  echo "访问："
  echo "  后端 OpenAPI: http://localhost:19199/docs"
  echo "  管理后台:     http://localhost:5188  (admin / admin123)"
  echo "  移动端 H5:    http://localhost:8080  (uni 默认端口)"
}

stop_all() {
  log "停止所有进程 ..."
  for pidfile in /tmp/ai-drama-backend.pid /tmp/ai-drama-frontend.pid /tmp/ai-drama-mobile.pid; do
    [[ -f "$pidfile" ]] && kill "$(cat "$pidfile")" 2>/dev/null && rm "$pidfile"
  done
  ok "全部停止"
}

# ───────────────────────────────────────────
# 入口
# ───────────────────────────────────────────
usage() {
  cat <<EOF
用法：$0 <command>

command:
  preflight  仅前置检查
  backend    装 + 启后端
  frontend   装 + 启管理后台
  mobile     装 + 启移动端
  doctor     健康检查
  stop       停止所有
  all        装 + 启全部（默认）
EOF
}

main() {
  local cmd="${1:-all}"
  case "$cmd" in
    preflight) preflight ;;
    backend)   preflight; setup_backend;   start_backend ;;
    frontend)  preflight; setup_frontend;  start_frontend ;;
    mobile)    preflight; setup_mobile;    start_mobile ;;
    doctor)    doctor ;;
    stop)      stop_all ;;
    all)
      preflight
      setup_backend;   start_backend
      setup_frontend;  start_frontend
      setup_mobile;    start_mobile
      doctor
      ;;
    -h|--help|help) usage ;;
    *) err "未知命令: $cmd"; usage; exit 1 ;;
  esac
}

main "$@"