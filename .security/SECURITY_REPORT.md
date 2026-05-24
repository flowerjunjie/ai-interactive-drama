# Security Audit Report - AI Interactive Drama

**Audit Date:** 2026-05-24
**Auditor:** Security Reviewer Agent
**Environment:** Production (Docker)
**Backend Port:** 19199 | **Frontend Port:** 5188

---

## Critical Findings (Must Fix Immediately)

### 1. [CRITICAL] MySQL Root Password Weak - Already Exploited

**Description:** MySQL root password is `root123`, a common weak password that was exploited in a recent ransomware attack (0.016 BTC demand).

**Evidence:**
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
user    host    plugin
root    localhost    mysql_native_password
root    172.18.0.1    mysql_native_password
```

**Remediation:**
1. Immediately change MySQL root password to a strong random string (32+ characters)
2. Update backend configuration in `.env.prod` with new credentials
3. Consider using a password manager or secrets management system
4. Add the new credentials to Docker secrets or environment variables

```bash
# Change MySQL root password (execute inside container)
docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'NEW_STRONG_PASSWORD_HERE';"
docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "ALTER USER 'root'@'172.18.0.1' IDENTIFIED BY 'NEW_STRONG_PASSWORD_HERE';"
FLUSH PRIVILEGES;
```

---

### 2. [CRITICAL] MySQL Binding to All Interfaces

**Description:** MySQL `bind_address = *` allows connections from any network interface. Combined with weak passwords and remote access users, this creates a critical exposure vector.

**Evidence:**
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SHOW VARIABLES LIKE 'bind_address';"
Variable_name    Value
bind_address    *
```

**Remediation:**
1. Change MySQL bind_address to `127.0.0.1` only (localhost)
2. Ensure all application connections go through the Docker internal network
3. Add firewall rules to block external access to port 13306

```bash
# Update my.cnf or docker compose to bind to 127.0.0.1 only
```

---

### 3. [CRITICAL] MySQL Remote Access User Exists

**Description:** User `appuser` has remote access from any host (`%`), creating an additional attack vector.

**Evidence:**
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SELECT user, host FROM mysql.user WHERE host='%';"
user    host
appuser    %
```

**Remediation:**
1. If remote access is not required, revoke `appuser@%` privileges
2. If remote access is needed, restrict to specific IP ranges (e.g., `172.18.0.0/16`)
3. Use strong authentication for any remote users

---

### 4. [CRITICAL] Redis Has No Authentication

**Description:** Redis is running without a password (`requirepass` is empty), allowing unauthorized access to all cached data including sessions and JWT tokens.

**Evidence:**
```
$ docker exec ruoyi-redis redis-cli -p 6379 CONFIG GET requirepass
requirepass
(empty)
```

**Remediation:**
1. Enable Redis authentication with a strong password
2. Update `RedisSettings` in `config/env.py` to set `redis_password`
3. Restart Redis container after configuration change

---

### 5. [CRITICAL] JWT Secret Hardcoded in Source Code

**Description:** JWT secret key is hardcoded in `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/config/env.py:39`. This secret is committed to version control and is discoverable in all environments.

**Evidence:**
```python
# /www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/config/env.py:39
jwt_secret_key: str = 'b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55'
```

**Impact:** Attackers with access to source code can forge valid JWT tokens, bypassing authentication entirely.

**Remediation:**
1. Remove the hardcoded default value
2. Require `JWT_SECRET_KEY` to be set via environment variable
3. Generate a new secret key immediately: `openssl rand -hex 32`
4. Ensure `.env.prod` contains a unique, strong secret not used elsewhere

---

### 6. [CRITICAL] Unencrypted Database Backups

**Description:** Database backups in `/www/workspace/ai-interactive-drama/backups/` are gzip compressed but NOT encrypted. These backups contain sensitive data including user password hashes.

**Evidence:**
```
$ ls -la /www/workspace/ai-interactive-drama/backups/
-rw-rw-r-- 1 developer developer 8143 May 23 03:00 ai_drama_20260523_030001.full.sql.gz

$ zcat ai_drama_20260523_030001.full.sql.gz | head -50
-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
-- Host: 127.0.0.1    Database: ai_video
```

**Remediation:**
1. Implement encrypted backups using GPG or openssl
2. Store backup encryption keys separately from backups
3. Rotate encryption keys regularly
4. Set restricted permissions on backup files (chmod 600)

---

## High Findings

### 7. [HIGH] API Documentation Publicly Exposed

**Description:** OpenAPI documentation is accessible at `http://127.0.0.1:19199/openapi.json` without authentication, exposing all API endpoints, request/response schemas, and operation IDs.

**Evidence:**
```
$ curl -s http://127.0.0.1:19199/openapi.json | head -50
{"openapi":"3.1.0","info":{"title":"RuoYi-FastAPI","description":"RuoYi-FastAPI接口文档","version":"1.9.0"},"paths":{...}}
```

**Remediation:**
1. Disable OpenAPI documentation in production by setting `app_disable_swagger: bool = True` in `.env.prod`
2. Alternatively, restrict access to documentation endpoints via reverse proxy rules
3. Ensure documentation is only accessible in non-production environments

---

### 8. [HIGH] Default Database Credentials in Configuration

**Description:** Database configuration in `config/env.py` contains weak default credentials (`root`/`root`).

**Evidence:**
```python
# /www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/config/env.py:50-55
db_username: str = 'root'
db_password: str = 'root'
db_database: str = 'ruoyi-fastapi'
```

**Remediation:**
1. Remove default credentials from source code
2. Require all database credentials to be provided via environment variables
3. Use unique database name, username, and strong password per environment

---

### 9. [HIGH] MySQL Using Weak Authentication Plugin

**Description:** MySQL is using `mysql_native_password` instead of the more secure `caching_sha2_password`. While `mysql_native_password` is not inherently insecure, `caching_sha2_password` provides better performance and security for repeated connections.

**Evidence:**
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SELECT user, host, plugin FROM mysql.user;"
root    localhost    mysql_native_password
root    172.18.0.1    mysql_native_password
```

**Remediation:**
1. Migrate to `caching_sha2_password` for all users
2. This requires updating MySQL user authentication strings

---

## Medium Findings

### 10. [MEDIUM] No Visible Rate Limiting on API Endpoints

**Description:** No rate limiting is observed on API endpoints. This could allow brute force attacks on authentication endpoints.

**Evidence:**
```
$ curl -s http://127.0.0.1:19199/openapi.json | grep -c paths
(OpenAPI shows multiple auth-related endpoints without rate limit headers)
```

**Remediation:**
1. Implement rate limiting on all public endpoints (e.g., 100 requests/minute per IP)
2. Add stricter limits on authentication-related endpoints (e.g., 10 requests/minute)
3. Consider using Redis-based rate limiting for distributed deployments

---

### 11. [MEDIUM] Admin Backend Port Exposed

**Description:** Admin frontend runs on port 5188 and may be accessible externally. Check firewall rules to ensure only authorized networks can access admin interfaces.

**Evidence:**
```
$ docker ps
ruoyi-mysql   Up 18 hours    33060/tcp, 0.0.0.0:13306->3306/tcp, [::]:13306->3306/tcp
ruoyi-redis   Up 2 days      0.0.0.0:16379->6379/tcp, [::]:16379->6379/tcp
```

**Remediation:**
1. Ensure firewall restricts access to port 5188 (admin) and 19199 (API) to internal networks only
2. Consider using VPN or bastion host for admin access
3. Implement additional authentication (e.g., VPN, IP whitelist) for admin interfaces

---

## Low Findings

### 12. [LOW] No HTTPS Enforcement Visible

**Description:** API accepts HTTP connections on port 19199. While this may be intentional for local development, production deployments should enforce HTTPS.

**Evidence:**
```
$ curl -s http://127.0.0.1:19199/openapi.json
(Returns successful response over HTTP)
```

**Remediation:**
1. Configure uvicorn/uvicorn to redirect HTTP to HTTPS
2. Set HSTS headers for all responses
3. Use a reverse proxy (nginx) to handle TLS termination

---

### 13. [LOW] Application Running as Root in Docker

**Description:** Docker containers may be running as root by default.

**Remediation:**
1. Create a dedicated user for application processes
2. Use `USER` directive in Dockerfile
3. Run containers with `--user` flag in docker-compose

---

## Recommendations (Prioritized)

### Immediate Actions (Within 24 Hours)

1. **Change MySQL root password** - Use `openssl rand -base64 32` to generate a strong password
2. **Enable Redis authentication** - Set `redis_password` in environment configuration
3. **Rotate JWT secret** - Generate new secret key and invalidate all existing tokens
4. **Restrict MySQL bind address** - Change from `*` to `127.0.0.1`
5. **Review and remove remote MySQL users** - Remove or restrict `appuser@%`

### Short-term (Within 1 Week)

6. **Disable public API documentation** - Set `app_disable_swagger: true` in production
7. **Implement encrypted backups** - Use GPG encryption for all database backups
8. **Add rate limiting** - Implement request throttling on all endpoints
9. **Remove hardcoded defaults** - Ensure no credentials exist in source code

### Medium-term (Within 1 Month)

10. **Implement secrets management** - Consider using HashiCorp Vault, AWS Secrets Manager, or similar
11. **Add network segmentation** - Isolate database and Redis in private network
12. **Implement monitoring/alerting** - Set up alerts for failed login attempts, unusual queries
13. **Regular security audits** - Schedule monthly vulnerability scans

---

## Verification Evidence

### Docker Container Status
```
$ docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
NAMES         STATUS                PORTS
ruoyi-mysql   Up 18 hours           33060/tcp, 0.0.0.0:13306->3306/tcp, [::]:13306->3306/tcp
ruoyi-redis   Up 2 days (healthy)   0.0.0.0:16379->6379/tcp, [::]:16379->6379/tcp
```

### MySQL Authentication Configuration
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
user    host    plugin
root    localhost    mysql_native_password
root    172.18.0.1    mysql_native_password
```

### MySQL Remote Users
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SELECT user, host FROM mysql.user WHERE host='%';"
user    host
appuser    %
```

### MySQL Bind Address
```
$ docker exec ruoyi-mysql mysql -S /var/run/mysqld/mysqld.sock -uroot -proot123 -e "SHOW VARIABLES LIKE 'bind_address';"
Variable_name    Value
bind_address    *
```

### Redis Authentication
```
$ docker exec ruoyi-redis redis-cli -p 6379 CONFIG GET requirepass
requirepass
(empty)
```

### OpenAPI Documentation Exposure
```
$ curl -s http://127.0.0.1:19199/openapi.json | head -50
{"openapi":"3.1.0","info":{"title":"RuoYi-FastAPI","description":"RuoYi-FastAPI接口文档","version":"1.9.0"},"paths":{...}}
```

### JWT Secret Hardcoded
```python
# /www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/config/env.py:39
jwt_secret_key: str = 'b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55'
```

### Backup Files
```
$ ls -la /www/workspace/ai-interactive-drama/backups/
-rw-rw-r-- 1 developer developer 8143 May 23 03:00 ai_drama_20260523_030001.full.sql.gz
```

---

## Security Checklist

- [ ] MySQL root password changed to strong random string
- [ ] MySQL bind_address restricted to localhost only
- [ ] Remote MySQL users removed or restricted
- [ ] Redis password enabled
- [ ] JWT secret rotated
- [ ] API documentation disabled in production
- [ ] Hardcoded credentials removed from source code
- [ ] Database backups encrypted
- [ ] Rate limiting implemented
- [ ] Firewall rules configured
- [ ] Admin port access restricted
- [ ] HTTPS enforced (production)

---

**Report Generated:** 2026-05-24
**Risk Level:** CRITICAL
**Next Review:** 2026-05-31 (weekly until issues resolved)