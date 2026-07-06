# 🛠 scripts

> 仓库维护 / 运维脚本。所有脚本幂等、可独立运行。

## 目录

| 脚本 | 用途 | 用法 |
| --- | --- | --- |
| `setup-dev.sh` | 一键启动开发环境（后端 + 前台 + 移动端） | `./scripts/setup-dev.sh [backend\|frontend\|mobile\|doctor\|stop\|all]` |

## 使用约定

- 所有脚本使用 `set -euo pipefail`（fail-fast）
- 日志统一输出到 `/tmp/ai-drama-*.log`
- PID 统一记录到 `/tmp/ai-drama-*.pid`
- 后台进程用 `nohup ... &`，方便 stop / restart
- 颜色：🟢 OK / 🟡 Warn / 🔴 Error

## 常用命令

```bash
# 全套启动
./scripts/setup-dev.sh

# 只看健康状态
./scripts/setup-dev.sh doctor

# 全部停止
./scripts/setup-dev.sh stop

# 重启某个组件
./scripts/setup-dev.sh stop && ./scripts/setup-dev.sh backend
```

## 添加新脚本

按以下模板：

```bash
#!/usr/bin/env bash
set -euo pipefail

# 标题：简短说明
# 前提：依赖工具 / 环境变量
# 用法：./scripts/your-script.sh [args]

main() {
  # 你的逻辑
}

main "$@"
```

加完后 `chmod +x scripts/your-script.sh`，更新本 README 目录。