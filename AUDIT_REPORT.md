# Full Technical Audit — AI Crypto Advisor

## 1) Requirements Checklist

### API Endpoints

| Requirement | Status | Notes |
|-------------|--------|-------|
| POST /api/auth/signup | **PASS** | Implemented, returns JWT. |
| POST /api/auth/login | **PASS** | Implemented, returns JWT. |
| GET /api/me | **PASS** | Implemented, returns user profile + onboarded. |
| POST /api/onboarding | **PASS** | Implemented, protected. |
| GET /api/preferences (optional) | **PASS** | Implemented at `/api/preferences` (audit fix). `/api/onboarding/preferences` kept as alias. |
| GET /api/dashboard/today | **PASS** | Returns date, news, prices, ai_insight, meme. |
| POST /api/votes | **PASS** | Body: section_type, content_id, vote_value. |
| GET /api/votes/today | **PASS** | Returns votes for today's snapshot. |
| GET /api/health | **PASS** | Returns { status: "ok" }. |

### Database Schema

| Table / Constraint | Status | Notes |
|--------------------|--------|-------|
| users: id, name, email(unique), password_hash, created_at | **PASS** | Matches. |
| user_preferences: id, user_id(FK unique), assets, investor_type, content_types, created_at | **PASS** | ARRAY(Text) used for assets/content_types (spec allows text[]). |
| daily_snapshots: id, user_id(FK), snapshot_date, created_at | **PASS** | Unique (user_id, snapshot_date) present. |
| snapshot_news_items | **PASS** | All columns + FK. |
| snapshot_prices (snapshot_id unique) | **PASS** | raw_json(jsonb). |
| snapshot_ai_insights (snapshot_id unique) | **PASS** | |
| snapshot_memes (snapshot_id unique) | **PASS** | |
| votes: user_id, section_type, content_id, vote_value, created_at | **PASS** | |
| Unique (user_id, section_type, content_id) on votes | **PASS** | uq_user_section_content in model and migration. |

### Auth & Security

| Item | Status | Notes |
|------|--------|-------|
| Password hashing bcrypt | **PASS** | passlib CryptContext(schemes=["bcrypt"]). |
| JWT creation + verification | **PASS** | jose, exp, sub. |
| Protected routes use Authorization: Bearer | **PASS** | get_current_user uses HTTPBearer. |
| GET /api/me protected | **PASS** | Depends(get_current_user). |
| POST /api/onboarding protected | **PASS** | |
| GET /api/dashboard/today protected | **PASS** | |
| POST /api/votes, GET /api/votes/today protected | **PASS** | |
| current_user dependency secure | **PASS** | Validates token, loads user from DB. |

### Daily Snapshot & Voting

| Item | Status | Notes |
|------|--------|-------|
| One snapshot per user per day | **PASS** | get_today_for_user by (user_id, snapshot_date); unique constraint. |
| Snapshot persisted (news, prices, ai_insight, meme) | **PASS** | All stored in DB; dashboard reads from snapshot. |
| Vote upsert by (user_id, section_type, content_id) | **PASS** | VoteRepository.upsert updates existing or inserts. |
| content_id references snapshot item ids | **PASS** | NEWS=news item id, PRICES=prices id, AI_INSIGHT=id, MEME=id. |

### External APIs & Fallbacks

| Item | Status | Notes |
|------|--------|-------|
| CryptoPanic with fallback | **PASS** | No key or error → FALLBACK_NEWS. |
| CoinGecko for prices | **PASS** | No key required. No explicit fallback on failure (empty list). |
| AI (OpenRouter/HuggingFace) with fallback | **PASS** | FALLBACK_AI_INSIGHT when no key or failure. |
| Meme (Reddit) with fallback | **PASS** | FALLBACK_MEME when fetch fails. |

### Frontend

| Item | Status | Notes |
|------|--------|-------|
| App load → token → /api/me → route | **PASS** | AuthProvider refreshProfile() on mount. |
| Not logged in → /login | **PASS** | ProtectedRoute redirects. |
| !onboarded → /onboarding | **PASS** | ProtectedRoute checks user.onboarded. |
| Onboarding save → redirect /dashboard | **PASS** | navigate('/dashboard') after submit. |
| Vote buttons show current state from backend | **PASS** | VoteButtons use votes from GET /api/votes/today. |
| "Thanks for feedback" after voting | **PASS** | VoteButtons show when value !== 0. |
| Axios interceptor 401 → logout | **PASS** | Clears token, dispatches auth:logout. |

### Docker & Infra

| Item | Status | Notes |
|------|--------|-------|
| docker-compose: postgres + backend | **PASS** | infra/docker-compose.yml. |
| Backend env: DATABASE_URL, JWT_*, API keys | **PASS** | In compose and .env.example. |
| Frontend env: VITE_API_BASE_URL | **PASS** | .env.example. |

### Alembic

| Item | Status | Notes |
|------|--------|-------|
| Migrations match models | **PASS** | 001_initial_schema aligns with SQLAlchemy models. |

---

**Applied fix:** Added `GET /api/preferences` via `routers/preferences.py`; kept `GET /api/onboarding/preferences` as alias.

---

## 2) Logical Issues

### Critical

- **None.**

### Medium

- **Snapshot creation race:** Two concurrent first-time requests for the same user can both see “no snapshot” and attempt insert. The unique constraint `(user_id, snapshot_date)` causes one to fail with IntegrityError. **Suggestion:** Catch IntegrityError in `get_or_create_today_snapshot`, re-query by (user_id, today), and return the existing snapshot (or use SELECT FOR UPDATE / advisory lock if you need stricter guarantees).
- **CoinGecko failure:** If CoinGecko API fails, `fetch_prices` returns `[]` and the snapshot stores empty prices. **Suggestion:** Optional: add a small static fallback (e.g. BTC/ETH placeholder) for consistency with other sections; not required by spec.

### Minor

- **Unused import (fixed):** Removed unused `OAuth2PasswordBearer` from `core/dependencies.py`.
- **Vote response id:** After optimistic vote update in Dashboard, the new vote is pushed with `id: 0`. UI still works; for consistency you could refetch GET /api/votes/today after vote or use the id returned by POST.

---

## 3) Code Quality Assessment

- **Architecture:** Repositories (DB only), services (business logic), routers (HTTP) are clearly separated. No controllers folder; spec allows “keep in routers if small” — **8/10**.
- **Backend quality:** Consistent async, correct use of dependencies, clear schemas. Minor: duplicate “preferences” logic could be one shared function. **8/10**.
- **Frontend quality:** Typed services and types, auth flow and route guards correct. **7/10**.
- **Maintainability:** Structure is easy to follow; README and env examples help. **8/10**.
- **Production readiness:** CORS and env-based config in place. JWT secret and DB URL must be set in production. **7/10**.

---

## 4) Non-Functional Verification

| Item | Status |
|------|--------|
| No TODOs in project code (except optional refresh token) | **PASS** (no TODOs in app code) |
| README: setup (local + docker) | **PASS** |
| README: API keys optional + fallbacks | **PASS** |
| README: deployment notes | **PASS** |
| README: “AI tools usage summary” placeholder | **PASS** |
| No unnecessary extra features | **PASS** |
| Scope matches spec | **PASS** (after adding GET /api/preferences) |

---

## 5) Final Verdict

**Interview-ready:** **Yes.**

GET /api/preferences and the unused import fix have been applied. All specification requirements are met. Optionally address the medium items (snapshot creation race, optional CoinGecko fallback) for extra polish.
