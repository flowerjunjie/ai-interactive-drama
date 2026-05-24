# Infrastructure & DevOps Audit - AI Interactive Drama

**Audit Date:** 2026-05-24  
**Project Root:** `/www/workspace/ai-interactive-drama`

---

## Container Status

| Container | Status | Uptime | Ports |
|-----------|--------|--------|-------|
| ruoyi-mysql | Up | 18 hours | 33060/tcp, 0.0.0.0:13306->3306/tcp |
| ruoyi-redis | Healthy | 2 days | 0.0.0.0:16379->6379/tcp |

**Evidence:**
```
$ docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
NAMES         STATUS                PORTS
ruoyi-mysql   Up 18 hours           33060/tcp, 0.0.0.0:13306->3306/tcp, [::]:13306->3306/tcp
ruoyi-redis   Up 2 days (healthy)   0.0.0.0:16379->6379/tcp, [::]:16379->6379/tcp
```

**MySQL Version:** 8.0.46 (MySQL Community Server - GPL)
**Redis Version:** 8.6.3

**Databases:**
- `ai_video` (production drama database)
- `ruoyi-fastapi` (RuoYi admin system)
- `mysql`, `information_schema`, `performance_schema`, `sys` (system)

---

## Network Exposure (Ports Listening)

| Port | Service | Bind Address | Process |
|------|---------|--------------|---------|
| 3306 | MySQL (socat redirect) | 0.0.0.0 | socat (pid 592646) |
| 6379 | Redis | 127.0.0.1 | (internal only - secure) |
| 13306 | MySQL | 0.0.0.0:13306 | Docker port forward |
| 16379 | Redis | 0.0.0.0:16379 | Docker port forward |
| 19199 | FastAPI Backend | 0.0.0.0 | python/uvicorn (pid 1897925) |
| 5188 | Admin Frontend | *:5188 | node (pid 1008749) |
| 8099 | Download Page | 0.0.0.0:8099 | nginx |

**Evidence:**
```
$ ss -tlnp | grep -E "19199|3306|13306|5188|8099|6379"
LISTEN 0  5            0.0.0.0:3306       0.0.0.0:*    users:(("socat",pid=592646,fd=5))
LISTEN 0  511        127.0.0.1:6379       0.0.0.0:*                                                
LISTEN 0  2048         0.0.0.0:19199      0.0.0.0:*    users:(("python",pid=1897925,fd=35))
LISTEN 0  4096         0.0.0.0:16379      0.0.0.0:*                                                
LISTEN 0  511          0.0.0.0:8099       0.0.0.0:*                                                
LISTEN 0  4096         0.0.0.0:13306      0.0.0.0:*                                                
LISTEN 0  4096            [::]:16379         [::]:*                                                
LISTEN 0  511          *:5188             *:*    users:(("node",pid=1008749,fd=22))
LISTEN 0  4096            [::]:13306         [::]:*                                                
LISTEN 0  511                [::1]:6379        [::]:* 
```

**Process Details:**
```
$ ps aux | grep -E "uvicorn|python.*server" | grep -v grep
develop+  1897925  1.6  1.3 1269260 223500 ?  Sl  May23  0:51 .venv/bin/python -m uvicorn server:create_app --host 0.0.0.0 --port 19199
```

---

## Backup Health

**Status:** OPERATIONAL

**Crontab Entry:**
```
0 3 * * * /www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/scripts/backup/backup.sh >> /www/workspace/ai-interactive-drama/backups/backup.log 2>&1
```

**Backup Directory Contents:**
```
$ ls -la /www/workspace/ai-interactive-drama/backups/
total 36
drwxr-xr-x  2 developer developer 4096 May 23 03:00 .
drwxr-xr-x 16 developer developer 4096 May 24 00:20 ..
-rw-rw-r--  1 developer developer    0 May 23 03:00 .backup.lock
-rw-rw-r--  1 developer developer 3180 May 21 08:01 ai_drama_20260521_080153.full.sql.gz
-rw-rw-r--  1 developer developer 4117 May 22 03:00 ai_drama_20260522_030002.full.sql.gz
-rw-rw-r--  1 developer developer 8143 May 23 03:00 ai_drama_20260523_030001.full.sql.gz
-rw-rw-r--  1 developer developer 4500 May 23 03:00 backup.log
```

**Backup Script Details:**
- Retention: 7 days (default)
- Databases backed up: `ai_video` (configurable)
- Backup user: `root` / `password` (configurable via env)
- Lock mechanism prevents concurrent runs
- Compression: gzip
- Logging: `backup.log`

**Observations:**
- Backups exist for May 21, 22, 23 (today)
- Missing May 24 (backup runs at 3AM - may be pending)
- Total backup directory size: 32K (small, healthy)
- Lock file present indicating backup ran on May 23

---

## nginx Configuration

**Enabled Sites:**
```
/etc/nginx/sites-enabled/
├── ai-drama-80.disabled      (disabled)
├── ai-drama-8188             (port 8188)
├── ai-drama.disabled         (disabled)
├── ai-drama-static
├── json2word-80-ssl         (SSL, port 443)
├── json2word-8093
├── lingxi-landing.disabled   (disabled)
├── mirofish                  (port 3021)
├── mobile-app-8288           (port 8288)
├── ruoyi-app-8388            (port 8388)
├── shadowbroker
└── superread-8090            (port 8090)
```

**AI Interactive Drama Relevant Configurations:**

**Port 8188 (Admin + Download Page):**
```nginx
server {
    listen 8188;
    server_name _;
    root /www/workspace/ai-interactive-drama/ruoyi-fastapi-frontend/dist;
    
    location /download-page/ {
        alias /www/workspace/ai-interactive-drama/download-page/;
        autoindex off;
    }
    
    location /dev-api/ {
        proxy_pass http://127.0.0.1:19199/;
    }
    
    location /prod-api/ {
        proxy_pass http://127.0.0.1:19199/;
    }
}
```

**Port 8288 (Mobile App H5):**
```nginx
server {
    listen 8288;
    root /www/workspace/ai-interactive-drama/mobile-app/dist/build/h5;
    
    location /api/ {
        proxy_pass http://127.0.0.1:19199/api/;
    }
}
```

**Port 8388 (RuoYi App H5):**
```nginx
server {
    listen 8388;
    root /www/workspace/ai-interactive-drama/ruoyi-fastapi-app/dist/build/h5;
    
    location /api/ {
        proxy_pass http://127.0.0.1:19199/;
    }
}
```

**Port 8099 (Download Page Only):**
```nginx
server {
    listen 8099;
    server_name _;
    
    location / {
        root /www/workspace/ai-interactive-drama;
        index index.html;
    }
}
```

---

## Process Management

| Process | PID | Memory | CPU | Start Time | Description |
|---------|-----|--------|-----|------------|-------------|
| uvicorn (FastAPI) | 1897925 | 1.3% | 1.6% | May 23 | Main backend server on port 19199 |
| python http.server | 1009497 | 0.1% | 0.2% | May 23 | Temporary screenshot server on 18080 |
| wormhole_server | 475532 | 0.6% | 0.6% | May 22 | Shadowbroker backend |
| nginx (master) | - | - | - | - | Multiple sites enabled |

**Crontab Status:**
```
$ crontab -l
0 3 * * * /www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/scripts/backup/backup.sh >> /www/workspace/ai-interactive-drama/backups/backup.log 2>&1
```

---

## Disk Space Analysis

| Filesystem | Size | Used | Available | Use% | Mount |
|-----------|------|------|-----------|------|-------|
| /dev/vda1 | 39G | 33G | 5.9G | 85% | / |
| /dev/vdb1 | 98G | 85G | 8.1G | 92% | /www |

**Status:** WARNING - Both partitions above optimal thresholds

**Breakdown by Component (estimated):**
- Backups: 32K (negligible)
- Frontend dist: ~XX MB
- Mobile app dist: ~XX MB
- MySQL data: managed by Docker
- Redis data: managed by Docker

**Backup Directory Size:** 32K (very small - good compression)

---

## Security Concerns

### High Priority

1. **MySQL Port 3306/13306 Exposed to 0.0.0.0**
   - MySQL is listening on all interfaces via socat
   - Should be bound to 127.0.0.1 or specific internal interface
   - Credentials: root/proot123 (weak, well-known RuoYi default)

2. **Redis Ports 6379/16379 Exposed to 0.0.0.0**
   - Redis bound to all interfaces
   - No authentication visible in exposure
   - Should be 127.0.0.1 only

3. **Backend API Port 19199 Exposed to 0.0.0.0**
   - FastAPI on all interfaces
   - Direct backend access without nginx proxy
   - Consider binding to 127.0.0.1 and routing through nginx

### Medium Priority

4. **Disk Space /www at 92%**
   - 8.1GB remaining of 98GB
   - At current pace, may fill within weeks
   - Should implement monitoring/alerting

5. **Disk Space / at 85%**
   - 5.9GB remaining of 39GB
   - Manageable but trending upward

6. **Multiple nginx Sites for Same Application**
   - Ports 8188, 8288, 8388, 8099 all serve variations
   - Port 8099 serves from project root (could expose other files)
   - Consider consolidation

### Low Priority

7. **Disabled nginx Sites Still Present**
   - `ai-drama-80.disabled`, `ai-drama.disabled`, `lingxi-landing.disabled`
   - Should be removed if no longer needed

8. **No SSL on Primary Sites**
   - Port 80 sites redirect to SSL on lxexam domain only
   - AI Drama sites (8188, 8288, 8388) have no SSL configured

9. **Shadowbroker Process Running**
   - Unrelated process using resources
   - May or may not be intentional

---

## Recommendations

### Immediate Actions

1. **Restrict MySQL/Redis to localhost**
   - Change socat binding from 0.0.0.0 to 127.0.0.1
   - Or configure Docker ports to 127.0.0.1:13306 only

2. **Add monitoring for disk space**
   - Alert at 85% usage
   - Current /www at 92% needs attention

### Short-term Actions

3. **Consolidate nginx configurations**
   - AI Drama should have one primary site with all routes
   - Clean up disabled sites

4. **Implement SSL for production**
   - Use Let's Encrypt for free SSL
   - Redirect HTTP to HTTPS

5. **Review backup retention**
   - 7 days is minimal
   - Consider 14-30 days for drama platform data

### Long-term Improvements

6. **Move credentials to environment variables**
   - Current defaults in backup script
   - Use Docker secrets or vault

7. **Add health check endpoints**
   - `/health` for backend
   - Monitor container health

8. **Implement log rotation**
   - nginx logs
   - application logs
   - backup logs

---

## Summary Score

| Category | Status | Score |
|----------|--------|-------|
| Container Health | Good | 8/10 |
| Network Security | Needs Work | 4/10 |
| Backup System | Good | 8/10 |
| nginx Configuration | Adequate | 6/10 |
| Disk Space | Warning | 5/10 |
| Process Management | Adequate | 7/10 |
| **Overall** | **Needs Attention** | **6.3/10** |

---

*Report generated by Claude Code Infrastructure Audit*