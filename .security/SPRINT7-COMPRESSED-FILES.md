# SECURITY: 压缩文件格式风险评估与缓解

**发现日期**: 2026-05-25
**审计方**: Sprint 7 Security Audit
**状态**: 部分缓解（code-layer 已移除 rar/html/htm；zip/gz/bz2 待专项评估）

---

## 1. 风险概览

| 风险项 | 文件类型 | 风险等级 | 现状 |
|--------|----------|----------|------|
| 存储型 XSS | `html`, `htm` | **高** | ✅ 已移除（e08eae3） |
| 可执行文件投放 | `rar` | **高** | ✅ 已移除（32758ce） |
| 恶意压缩包 | `zip`, `gz`, `bz2` | **中** | ⚠️ 待专项评估 |
| TOS 路径遍历 | `tos_key` | **高** | ✅ 已防护（e08eae3） |

---

## 2. `html`/`htm` 风险（已修复）

**问题**：用户上传 `.html`/`.htm` 文件并通过 CDN 访问时，可执行存储型 XSS 攻击。

**修复**：从 `DEFAULT_ALLOWED_EXTENSION` 中移除 `html`/`htm`。

**commit**: `e08eae3 fix(security): drama VO模型补齐file_id正整数校验+移除危险扩展名`

---

## 3. `rar` 风险（已修复）

**问题**：
- RAR 格式支持跨平台压缩二进制可执行文件（Windows `.exe`、Linux ELF、macOS Mach-O）
- RAR 压缩包可在不同平台解压，可能释放可执行文件到系统路径
- 历史上 RAR 格式存在多个解析漏洞（CVE-2023-31146 等）

**修复**：从 `DEFAULT_ALLOWED_EXTENSION` 中移除 `rar`。

**commit**: `32758ce fix(security): DEFAULT_ALLOWED_EXTENSION 移除 rar 格式`

---

## 4. `zip`/`gz`/`bz2` 风险（待专项评估）

**问题**：仍保留在白名单中，存在以下风险：

| 格式 | 风险 | 说明 |
|------|------|------|
| `zip` | 中 | 可包含 `..` 路径遍历文件名；解压覆盖攻击 |
| `gz` | 低-中 | 单文件压缩，风险较低 |
| `bz2` | 低 | 同上 |

**建议**：
1. 评估是否业务确实需要这些压缩格式上传
2. 如不需要，从白名单移除
3. 如需要，实施以下防护：
   - 解压后检查文件名不含 `..`（路径穿越）
   - 检查解压后文件大小不超过阈值（zip 炸弹防护）
   - 验证文件头魔数（magic bytes）匹配声明的扩展名

---

## 5. TOS 路径遍历（已防护）

**问题**：`UploadCompleteIn.tos_key` 可包含 `..` 路径遍历，导致文件写入到预期目录外。

**修复**：添加校验逻辑：
```python
@field_validator('tos_key')
@classmethod
def _validate_tos_key(cls, v: str | None) -> str | None:
    if v is None:
        return v
    if '..' in v or v.startswith('/') or v.startswith('\\'):
        raise ValueError('Invalid tos_key path')
    return v
```

**commit**: `e08eae3`

---

## 6. 病毒扫描（架构层，待接入）

当前系统无运行时文件扫描。`complete_upload` 写入 TOS 后即无法追责。

**建议接入方案**：ClamAV 集成

```python
# 伪代码示例（接入点：complete_upload 写入前）
async def scan_file_before_upload(filepath: str) -> bool:
    """调用 ClamAV 扫描文件，返回 True 表示安全"""
    # 建议使用 clamd 或 python-clamd 客户端
    # 扫描结果写入 DB 记录，供审计溯源
```

**注意事项**：
- 扫描应在文件写入 TOS 后、标记 `complete` 前异步执行
- 扫描结果写入 `drama_upload_file` 表或独立 `file_scan_results` 表
- 发现恶意文件应触发：`status=_UPP（待处理）` + 告警 + 保留原始文件供取证

---

## 7. IDOR 漏洞（DB 层，需 DBA）

**问题**：`admin_app_user_watch` 和 `admin_app_user_favs` 无用户归属校验，任何 admin 可查询任意用户数据。

**修复**：需 DBA 执行 ALTER TABLE 添加 `tenant_id` 列，并修改 service 层校验逻辑。

**状态**：⚠️ 已记录，待排期