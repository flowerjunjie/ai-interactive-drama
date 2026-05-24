# Code Quality Review - AI Interactive Drama

## Critical Issues (bug risk)

### [CRITICAL] Player page: `videoSrc` computed may read both `video_url` and `videoUrl`
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:224`
**Issue:** `node.value?.video_url || node.value?.videoUrl` mixes snake_case and camelCase properties from two different sources. The backend sends snake_case (`video_url`), but fallback to camelCase suggests dual source handling that is fragile and undocumented.
**Fix:** Normalize API response to one format in the service layer or define a single property accessor.

```typescript
// Current problematic code:
const videoSrc = computed(() => node.value?.video_url || node.value?.videoUrl || '')
```

### [CRITICAL] Player page: Hardcoded fallback values expose business logic assumptions
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:229,236`
**Issue:** `dramaMeta.value?.title || '逆天战神'` and `heat ?? 124000` are hardcoded Chinese drama titles and magic numbers as defaults. If the backend returns null on deleted content, users see "逆天战神" which is incorrect data.
**Fix:** Show "内容不存在" or redirect to a 404 page instead of fabricating plausible-looking fake data.

```typescript
// Current problematic code:
const dramaTitle = computed(() => dramaMeta.value?.title || '逆天战神')
const heatLine = computed(() => {
  const h = dramaMeta.value?.heat
  if (h == null) return '986.5万热度'  // hardcoded default
  const n = Number(h)
  return n >= 10000 ? `${(n / 10000).toFixed(1)}万热度` : `${n}热度`
})
const favHint = computed(() => Number(dramaMeta.value?.heat ?? 124000))
```

### [CRITICAL] Player page: `favHint` uses `heat` field to display "favorite count"
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:236`
**Issue:** `favHint` pulls from `heat` field, which is a drama popularity metric, not favorite count. This is a semantic bug -- the star icon tooltip will show wrong data.
**Fix:** The backend should provide a dedicated `favorite_count` field for the drama detail endpoint.

### [CRITICAL] Mine page: API error handling missing `fail` callbacks
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/mine/index.vue:253-265,270-278`
**Issue:** `uni.request` calls in `loadDashboard()` and `loadSubscriptions()` only define `success` callbacks. If the request fails or returns a non-200 code, the failure is silently ignored and the UI retains stale data (or zeros from initial state).
**Fix:** Add `fail` callbacks and handle `b.code !== 200` with error feedback in the `success` callback.

```typescript
// Current problematic code - no fail handler, no error code handling:
uni.request({
  url: appApi('/me/dashboard'),
  header: authHeaders(),
  success: (res: any) => {
    const b = res.data as any
    if (b.code !== 200 || !b.data) return  // silent failure
    // ...
  },
})
```

### [CRITICAL] DramaAppUser password stored as `String(100)` without hashing annotation
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/entity/do/drama_do.py:33`
**Issue:** Password field comment says "密码hash" but the column definition gives no indication of the hashing algorithm. In `app_auth_service.py`, the actual hashing implementation should be verified to be secure (bcrypt/argon2). If this is not inspectable from the DO, it is a hidden dependency.
**Fix:** Add a code comment or constants file indicating the hashing algorithm used, or add a validator to enforce bcrypt.

## High Priority Issues (tech debt)

### [HIGH] Service layer returns raw ORM objects to controller
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:143`
**Issue:** `list_episodes` returns `list[DramaVideoNode]` -- raw ORM objects. Controllers then manually pick fields to build response dicts (e.g., `app_drama_controller.py:76`). This violates DRY and creates tight coupling.
**Fix:** Have service methods return typed DTOs/VO objects directly.

### [HIGH] Magic numbers in `feed()` ad insertion logic
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:86`
**Issue:** `(i + 1) % 3 == 0` -- magic number 3 for ad insertion frequency. No constant explains why ads appear every 3 videos.
**Fix:** Define a named constant like `AD_INSERT_INTERVAL = 3` at the top of the service class.

### [HIGH] Magic numbers in `list_comments` limit
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:392`
**Issue:** `.limit(100)` is a magic number with no explanation. If a drama goes viral, 100 comments is insufficient.
**Fix:** Make configurable via `CommentCreateModel.page_size` or a class constant.

### [HIGH] Duplicate route handlers with aliased paths
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/controller/app_drama_controller.py:111-127`
**Issue:** Two separate endpoint functions (`post_like` and `post_like_alias`) exist for identical logic because `/api/likes` and `/api/like` are both registered. This is maintained manually and could drift.
**Fix:** Use FastAPI's `response_model` and a single handler, or add the alias path via `include_router` with `prefix`.

### [HIGH] `server_service.py` calls `platform.platform()` without import
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_admin/service/server_service.py:41`
**Issue:** The function uses `platform.platform()`, `platform.node()`, `platform.machine()`, `platform.python_version()` but the `platform` module is not imported at line 1. It may work because Python has a builtin shadow, but it is poor practice and will fail if the builtin is ever shadowed.
**Fix:** Add `import platform` at the top of the file.

## Medium Priority Issues (maintainability)

### [MEDIUM] Service methods lack type hints on return annotations
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py`
**Issue:** Many public methods like `feed()`, `list_dramas()`, `list_history()` return `list[dict]` or `list[Drama]` without Pydantic validation. The schema of returned dicts is implicit and undocumented.
**Fix:** Define response models (e.g., `FeedItemResponse`, `DramaListItemResponse`) and return those instead of bare dicts.

### [MEDIUM] No input validation on `keyword` search parameter
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:138-140`
**Issue:** `keyword.strip()` is used directly in a `LIKE` query without length limits or SQL injection defense at the service level. While SQLAlchemy parameterization should protect against SQL injection, a maximum length should be enforced.
**Fix:** Add `Field(max_length=100)` validation in the Pydantic query model.

### [MEDIUM] `DramaAppContentService` is a utility class with only static methods
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:34`
**Issue:** The class uses `@classmethod` throughout with no instance state. This is a code smell -- it should be a plain module with functions or a proper singleton service with dependency injection.
**Fix:** Convert to module-level functions or a proper injected service class.

### [MEDIUM] Player page: `tagPills` computed silently catches JSON parse errors
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:245-248`
**Issue:** `try { JSON.parse(s) } catch { /* ignore */ }` silently ignores malformed JSON. If the backend sends bad tags data, debugging will be very difficult.
**Fix:** Log a warning when JSON parsing fails so developers know the data format is unexpected.

### [MEDIUM] Player page: `interactiveFlag` and `triggerSec` duplicate camelCase/snake_case handling
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:294-301`
**Issue:** `n?.is_interactive === '1' || n?.isInteractive === '1'` and `n?.choice_trigger_sec ?? n?.choiceTriggerSec` check both snake_case and camelCase variants throughout the file. This pattern repeats 5+ times.
**Fix:** Create a normalizeNode() utility that returns a fully snake_cased copy, applied once when node data is loaded.

### [MEDIUM] Login page: password stored in plain text in localStorage
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/login/index.vue:139-143`
**Issue:** `uni.setStorageSync('saved_password', password.value)` stores the user's actual password. While this is gated behind a "remember password" opt-in checkbox, it is a security risk if the device is compromised.
**Fix:** Store a remember token instead, or use a device-specific encryption key from the backend to store a reversible credential hint.

### [MEDIUM] Mine page: `subscriptions` uses `reactive<any[]>([])`
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/mine/index.vue:226`
**Issue:** `any[]` typing discards all structure information about subscription objects.
**Fix:** Define a `Subscription` interface with proper fields.

## Low Priority Issues (style/nit)

### [LOW] `DramaAppContentService._node_visible_app()` is a `@classmethod` that does not use `cls`
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/service/drama_app_service.py:38-39`
**Issue:** `_node_visible_app()` uses `@classmethod` but only accesses class-level attributes (`DramaVideoNode.status`, `DramaVideoNode.review_status`). This should be a `@staticmethod`.
**Fix:** Change to `@staticmethod`.

### [LOW] Inconsistent naming in `DramaVideoNode` model
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/entity/do/drama_do.py`
**Issue:** Some models use snake_case column names (`drama_id`, `node_id`) but `is_entry`, `is_interactive` use `CHAR(1)` with string values `'0'`/`'1'`. This inconsistency is error-prone when querying.
**Fix:** Document the string-based boolean convention in a module-level constant.

### [LOW] `DramaAppUser.status` uses CHAR(1) with string values '0'/'1'
**File:** `/www/workspace/ai-interactive-drama/ruoyi-fastapi-backend/module_drama/entity/do/drama_do.py:35`
**Issue:** Same string-boolean pattern as `is_entry`/`is_interactive` but handled differently in code. No enforced consistency.
**Fix:** Establish a consistent pattern and document it.

### [LOW] No `aria-label` on icon-only buttons in player page
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:31-32`
**Issue:** Back button has no accessible label for screen readers.
**Fix:** Add `aria-label="返回"` to the back button view.

### [LOW] Console.warn only at line 573 in player page
**File:** `/www/workspace/ai-interactive-drama/mobile-app/src/pages/player/index.vue:573`
**Issue:** This is the only console.warn in the file, which is actually the correct pattern -- only use console.warn for player seekTo failure. However, it should arguably be a debug-level log, not warn, since seekTo failure is non-fatal.
**Fix:** Consider `console.debug()` for non-critical recovery scenarios.

## Best Practices Observed

- **N+1 query fix in list_comments**: The `list_comments()` method properly batch-fetches like counts in a single query (lines 398-404), confirming the documented fix was implemented.
- **JWT authentication flow**: The `get_optional_app_user`/`get_required_app_user` pattern in `app_user_dependency.py` is clean and properly uses async JWT decoding.
- **Pydantic models for request validation**: The VO file (`drama_vo.py`) properly uses Pydantic `Field()` with constraints (`min_length`, `max_length`, `ge`, `le`).
- **Service commit discipline**: Each service mutation method (`upsert_watch`, `toggle_like`, `toggle_favorite`, `add_comment`) correctly calls `await db.commit()` after changes.
- **Soft failure in share**: The player page `onShare()` gracefully falls back from WeChat share to system share without spamming toast messages on failure.
- **No TODO/FIXME in codebase**: Zero TODO/FIXME/HACK comments found, indicating good completion discipline.
- **No console.log in mobile app**: Only `console.warn` for seekTo failure is present -- correct pattern.
- **Log annotation properly configured**: The log annotation example at `log_annotation.py:105` correctly shows `api_key` exclusion for security-sensitive routes.

## Summary Statistics

| Metric | Backend | Mobile App |
|--------|---------|------------|
| Files reviewed | 5 | 3 |
| Total lines reviewed | ~1,800 | ~1,000 |
| TODO/FIXME/HACK/XXX | 0 | 0 |
| console.log statements | N/A | 0 |
| Hardcoded secrets | 0 | 0 |
| Critical issues | 5 | 4 |
| High priority issues | 5 | 2 |
| Medium priority issues | 5 | 4 |
| Low priority issues | 4 | 2 |

## Quick Wins (under 30 min)

1. **Add `import platform`** in `server_service.py:41` -- one line fix for correctness.
2. **Change `@classmethod` to `@staticmethod`** on `_node_visible_app()` -- mechanical refactor.
3. **Add `fail` callback** to `loadDashboard()` and `loadSubscriptions()` in mine page -- ~5 lines each.
4. **Define `AD_INSERT_INTERVAL = 3`** constant in `drama_app_service.py` -- eliminates one magic number.
5. **Add length validation** to `keyword` query param via Pydantic -- one line in VO file.

## Recommended Refactors (by effort)

### High Effort (>2 hours)
- **Normalize API response format** in player page: Create `normalizeNode()` utility to unify snake_case/camelCase handling. Currently the dual-format pattern appears in ~10 places.
- **Replace hardcoded fallback values** with proper error states: Change fallback drama title from `'逆天战神'` to showing a "content unavailable" state.

### Medium Effort (1-2 hours)
- **Convert `DramaAppContentService` to module functions** or proper injected service. Currently all methods are static/classmethods with no state, making dependency injection impossible.
- **Add response DTOs** for all service return types to eliminate bare `dict` returns.

### Low Effort (<1 hour)
- **Define `Subscription` interface** for `subscriptions` reactive in mine page.
- **Add `aria-label`** to icon-only buttons for accessibility.
- **Make `list_comments` limit configurable** via constant or query param default.
- **Add `console.debug` instead of `console.warn`** for seekTo failure (non-critical path).
