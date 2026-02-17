# AI Crypto Advisor

A personalized crypto investor dashboard. Users sign up, complete a short onboarding quiz, and see a daily dashboard with AI-curated content (market news, coin prices, AI insight, meme). Each section supports thumbs up/down feedback stored in the database.

## Live Demo

- **Frontend (Vercel):** https://ai-crypto-advisor-tawny.vercel.app
- **Backend (Render):** https://ai-crypto-advisor-backend-eu2.onrender.com
- **API Docs:** https://ai-crypto-advisor-backend-eu2.onrender.com/docs

## Tech Stack

- **Frontend:** React + Vite (TypeScript), React Context + custom hooks, Axios
- **Backend:** Python FastAPI, JWT (bcrypt), Routers / Services / Repositories
- **DB:** PostgreSQL, SQLAlchemy (async), Alembic migrations
- **Local dev:** Docker + docker-compose

## Project Structure (Monorepo)

```
/frontend     # React + Vite app
/backend      # FastAPI app
/infra        # docker-compose for Postgres + backend
```

## Setup

### Run entire app with Docker (no manual steps)

From the repo root:

```bash
cd infra
docker compose up -d --build
```

This starts:

- **Postgres** (internal)
- **Backend** (runs Alembic migrations, then uvicorn; internal, exposed on http://localhost:8000)
- **Frontend** (Vite dev server on http://localhost:5173)

**App:** http://localhost:5173  
No local venv or `npm run dev` required — Docker Compose runs the dev stack for you.

---

### Local development (optional)

**Prerequisites:** Node.js 18+, npm, Python 3.11+, Docker & Docker Compose (or PostgreSQL 15).

### 1. Database (Docker)

From repo root:

```bash
cd infra
docker-compose up -d postgres
```

This starts Postgres on `localhost:5432` (user: `moveo`, password: `moveo_secret`, db: `moveo_crypto`).

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # edit .env if needed
```

Run migrations (use sync URL for Alembic; same as `.env` but with `postgresql://` instead of `postgresql+asyncpg://`):

```bash
# Ensure DATABASE_URL in .env uses postgresql+asyncpg for the app.
# Alembic will use a sync URL internally (see app/db/migrations/env.py).
alembic -c alembic.ini upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173  
Vite proxy forwards `/api` to `http://localhost:8000`, so leave `VITE_API_BASE_URL` unset for local dev.

For local development with hot reload, use the steps below: run Postgres (and optionally backend) in Docker, then run the frontend with `npm run dev` and the backend with uvicorn as needed.

## API Keys and Fallbacks

All external APIs are **optional**. If keys are missing, the app uses fallbacks:

| Feature      | API / Key              | Fallback                          |
|-------------|------------------------|-----------------------------------|
| Market News | CryptoPanic API key   | Static list of 5 sample headlines |
| Coin Prices | CoinGecko (no key)    | N/A (always live)                  |
| AI Insight  | OpenRouter or HuggingFace | Static template insight text  |
| Meme        | Reddit JSON           | Placeholder image + link          |

Configure in backend `.env`:

- `CRYPTOPANIC_API_KEY` — [CryptoPanic](https://cryptopanic.com/developers/api/)
- `OPENROUTER_API_KEY` — [OpenRouter](https://openrouter.ai/)
- `HUGGINGFACE_API_KEY` — [Hugging Face](https://huggingface.co/settings/tokens)

## API Endpoints

- `POST /api/auth/signup` — Register (name, email, password)
- `POST /api/auth/login` — Login (email, password) → JWT
- `GET /api/me` — Current user profile + `onboarded` flag
- `POST /api/onboarding` — Save preferences (assets, investor_type, content_types)
- `GET /api/preferences` — Get saved preferences (optional)
- `GET /api/onboarding/preferences` — Same as above (alias)
- `GET /api/dashboard/today` — Today’s snapshot (news, prices, AI insight, meme)
- `POST /api/votes` — Submit vote (section_type, content_id, vote_value ±1)
- `GET /api/votes/today` — Votes for today’s snapshot
- `GET /api/health` — Health check

## Deployment Notes

- **Frontend:** Build with `npm run build`; deploy the `dist/` folder to Vercel, Netlify, or any static host. Set `VITE_API_BASE_URL` to your backend URL.
- **Backend:** Run with gunicorn/uvicorn behind a reverse proxy (e.g. Nginx). Set `DATABASE_URL`, `JWT_SECRET`, and optional API keys in the environment.
- **Database:** Use a managed PostgreSQL (e.g. Render, Railway, Supabase) and run Alembic migrations in CI or manually after deploy.

## Bonus: Using Feedback for Future Model Improvements

*(No implementation; suggestion only.)*

- **Labels:** Store thumbs up/down as binary (or ordinal) labels per (user, section_type, content_id, snapshot_date).
- **Features:** Use user preferences (assets, investor_type, content_types), content metadata (source, asset ids), and optionally content embeddings (e.g. from a small encoder) as features.
- **Training:** Train a re-ranking model or a classifier to predict “positive feedback” and use it to re-rank or filter items; or use the labels to select among prompt templates / models in an A/B setup.
- **Privacy:** Anonymize or aggregate before training; avoid storing or feeding PII into models; consider differential privacy or on-device learning if needed.

---

## Deliverable: Folder Tree & Commands

### Folder tree

```
moveo/
├── frontend/
│   ├── src/
│   │   ├── api/axios.ts, services/*.ts
│   │   ├── auth/AuthContext.tsx, useAuth.ts, ProtectedRoute.tsx
│   │   ├── components/dashboard/*.tsx
│   │   ├── pages/*.tsx
│   │   ├── types/index.ts
│   │   ├── App.tsx, main.tsx
│   │   └── vite-env.d.ts
│   ├── index.html, package.json, vite.config.ts, tsconfig*.json
│   └── .env.example
├── backend/
│   ├── app/
│   │   ├── core/config.py, security.py, dependencies.py
│   │   ├── db/session.py, base.py, migrations/
│   │   ├── models/, schemas/, repositories/, services/
│   │   ├── routers/, integrations/, utils/
│   │   └── main.py
│   ├── Dockerfile, requirements.txt, alembic.ini
│   └── .env.example
├── infra/
│   └── docker-compose.yml
└── README.md
```

### Commands (local dev)

```bash
# 1. Start Postgres
cd infra && docker-compose up -d postgres && cd ..

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+asyncpg://moveo:moveo_secret@localhost:5432/moveo_crypto"
alembic -c alembic.ini upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Frontend (new terminal)
cd frontend && npm install && npm run dev
```

Then open http://localhost:5173 — sign up, complete onboarding, and use the dashboard.

---

## AI tools usage summary

**Cursor** was used during development for:

- **Code generation and scaffolding:** FastAPI routers, services, repositories, React components, and API client code.
- **Refactoring and fixes:** Aligning types and schemas across frontend/backend, fixing integration code (e.g. CryptoPanic v2, OpenRouter/HuggingFace fallbacks), and resolving linter/type errors.
- **Documentation and config:** README setup instructions, API keys table, folder tree,

AI was used only as an assistant for implementation and documentation.
