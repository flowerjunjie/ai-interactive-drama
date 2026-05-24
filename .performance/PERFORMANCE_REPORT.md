# Performance Audit Report - AI Interactive Drama

**Audit Date:** 2026-05-24  
**Backend:** FastAPI on port 19199 (MySQL + Redis)  
**Mobile App:** Android APK (3.3MB release, 4.3MB debug)

---

## Benchmark Results (Actual Numbers)

| Endpoint | Response Time | Status |
|----------|--------------|--------|
| `GET /api/app/feed?page_num=1&page_size=10` | **113ms** | OK |
| `GET /api/app/dramas` | **228ms** | OK |

### Database Index Audit

| Table | Indexes Found | Notes |
|-------|---------------|-------|
| `drama_user_subscribe` | PRIMARY, uq_subscribe_user_drama (app_user_id, drama_id) | OK |
| `drama_user_watch_history` | PRIMARY, uq_drama_watch_user_drama (app_user_id, drama_id) | OK |
| `drama_video_node` | PRIMARY, idx_dvn_drama (drama_id) | OK - 21 rows, 6 cardinality |
| `drama` | PRIMARY only | **Missing** status index |
| `drama_ad` | PRIMARY only | **Missing** status/weight index |
| `drama_user_like` | PRIMARY, uq_drama_like_target (app_user_id, target_type, target_id) | OK |
| `drama_comment` | PRIMARY, idx_dc_drama (drama_id) | OK |

### Row Counts (small dataset)
- dramas: 6
- video_nodes: 21
- ads: 3

---

## Critical Performance Issues

### 1. **Missing Composite Index on `drama.status`**
- **Impact:** `feed()` and `list_dramas()` queries filter by `Drama.status == 'published'` but there is no index on `status`. With small data this is not critical, but as data grows this will cause full table scans.
- **Fix:** Add index on `(status)` or composite `(status, create_time)`.

### 2. **Missing Index on `DramaAd.status` + `DramaAd.weight`**
- **Impact:** `feed()` loads all ads with `WHERE DramaAd.status == '0' ORDER BY weight DESC`, but no index exists. Currently only 3 ads, but will bottleneck at scale.
- **Fix:** Add index `(status, weight DESC)`.

### 3. **Duplicate Async MySQL Drivers**
- **Impact:** Both `asyncmy==0.2.11` and `PyMySQL==1.1.2` are installed. `asyncmy` is the async driver; `PyMySQL` is sync. Using both increases dependency footprint and potential conflicts.
- **Fix:** Remove `PyMySQL` if not used (keep `asyncmy` for async operations).

---

## High Priority Optimizations

### 1. **Connection Pool Configuration Review**
```python
db_pool_size: int = 50   # Default 50
db_pool_recycle: int = 3600  # 1 hour
```
- **Current:** 50 connections with 1-hour recycle
- **Assessment:** `db_pool_size=50` is excessive for a single-worker uvicorn deployment. With `app_workers=1`, you typically need 5-15 connections. 50 can exhaust MySQL connections under load.
- **Recommendation:** Reduce to `db_pool_size=15` for single worker, or `25` if running multiple workers.

### 2. **`feed()` Ad Shuffling is Non-Random**
```python
ads_active[ad_idx % len(ads_active)]
```
- **Issue:** Uses simple round-robin (cycling through ads in order). First ad always shown first after every page load.
- **Impact:** Users on page 1 always see same first ad.
- **Fix:** Use random start offset: `ad_idx = random.randint(0, len(ads_active) - 1)`.

### 3. **`list_dramas()` Returns Unpaginated Results**
```python
async def list_dramas(cls, db, drama_type=None, keyword=None, sort=None) -> list[Drama]:
```
- **Issue:** Returns all matching dramas with no pagination. At 1000+ dramas, this will be slow and memory-intensive.
- **Fix:** Add `page_num` and `page_size` parameters with OFFSET/LIMIT.

---

## Medium Priority Optimizations

### 1. **SQLAlchemy Version Upgrade**
- **Current:** `SQLAlchemy[asyncio]==2.0.46`
- **Latest:** 2.0.x is current LTS, but 2.0.46 is from March 2024. Consider upgrading to latest 2.0.x for bug fixes and performance improvements.

### 2. **`ad_impression()` and `ad_click()` Double Commit**
```python
await db.execute(update...)
await db.commit()  # explicit commit after execute
```
- **Issue:** Both methods call `commit()` explicitly. This is fine but inconsistent with other methods that rely on auto-commit from the session context.
- **Fix:** Remove explicit `await db.commit()` if using session with `autocommit=True`, or standardize to always use explicit commits.

### 3. **`entry_node()` Issues Two Queries**
```python
node = r.scalars().first()
if node:
    return node
# Falls through to second query
```
- **Issue:** Could be combined with `ORDER BY is_entry DESC, episode_no...` and `LIMIT 1`.
- **Fix:** Combine into single query with `ORDER BY (is_entry='1') DESC` trick.

### 4. **Missing Composite Index for `list_history`**
```python
select(DramaUserWatchHistory, Drama)
.join(Drama, Drama.drama_id == DramaUserWatchHistory.drama_id)
.where(DramaUserWatchHistory.app_user_id == user_id)
.order_by(DramaUserWatchHistory.update_time.desc())
```
- **Issue:** No index on `(app_user_id, update_time)` for the watch history query.
- **Fix:** Add composite index on `(app_user_id, update_time DESC)`.

---

## Low Priority / Nice-to-Have

### 1. **Batch API Response Time Logging**
Currently no middleware logs per-request timing. Consider adding optional timing header `X-Response-Time-ms`.

### 2. **Redis Connection Pool Settings**
No Redis pool configuration visible. Check if `redis==7.1.0` connection pool is sized appropriately.

### 3. **`db_echo: bool = True` in Production**
The `db_echo: True` setting logs all SQL. Should be `False` in `.env.prod`.

### 4. **Drama Tags Column**
`drama.tags` is stored as text but searched with `LIKE`. Consider full-text index if tags search becomes more complex.

---

## Recommendations Summary

| Priority | Issue | Estimated Impact | Effort |
|----------|-------|------------------|--------|
| High | Reduce `db_pool_size` from 50 to 15-25 | Prevents connection exhaustion | 5 min |
| High | Add index on `drama(status)` | Faster feed/list queries at scale | 10 min |
| High | Add pagination to `list_dramas()` | Prevents OOM with large datasets | 30 min |
| Medium | Add index on `drama_ad(status, weight)` | Faster ad selection | 10 min |
| Medium | Randomize ad start index in `feed()` | Fairer ad distribution | 5 min |
| Medium | Combine `entry_node()` queries | Reduces DB round-trips | 15 min |
| Low | Remove unused `PyMySQL` | Smaller dependency footprint | 5 min |
| Low | Disable `db_echo` in prod | Reduces I/O overhead | 5 min |

---

## Verified Issues in Code

### `feed()` method - Ads loaded on every request
```python
ads = (
    await db.execute(
        select(DramaAd).where(DramaAd.status == '0').order_by(DramaAd.weight.desc()).limit(50)
    )
).scalars().all()
```
- Ads loaded from DB on every feed call. Consider caching ads in Redis with 5-minute TTL.

### `list_dramas()` - No pagination
```python
async def list_dramas(cls, db, drama_type=None, keyword=None, sort=None) -> list[Drama]:
    q = select(Drama).where(Drama.status == 'published')
    # ... no pagination ...
    r = await db.execute(q)
    return list(r.scalars().all())
```
- Returns all results. Should support `page_num`/`page_size`.

### `entry_node()` - Two queries when one could suffice
```python
node = r.scalars().first()
if node:
    return node
# Falls through to second query
```
- Two round-trips to DB when one sorted query would work.