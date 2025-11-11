## ExegesisAI – Intelligent Bible Study Companion

Version: 1.0

Authors: [Olabode Ebiniyi]

Purpose:

To empower users to study the Bible deeply and personally using the methodology of Living by the Book — combining sound hermeneutics with Machine Learning–powered contextual analysis and application generation.


### 1. Overview

#### 1.1 Mission
ExegesisAI helps users:

- Deconstruct Bible verses intelligently using the Observation–Interpretation–Application (OIA) method.
- Access historical, linguistic, and theological insights.
- Generate personalized reflections and study notes.
- Store and retrieve journaling insights, themes, and cross-references dynamically.

#### 1.2 Key Features

- Verse expansion using transformer-based language models (BERT, T5, GPT-NeoX)
- Auto-context generation (historical, linguistic, and theological)
- Semantic cross-referencing and keyword linking
- Journaling and personal study tracking
- Multi-translation and lexicon integration (Greek/Hebrew roots)
- Daily devotional generation and recommendation engine


### 2. System Architecture

High-Level Diagram

 ┌───────────────────────────┐
 │        Frontend           │
 │ React / Next.js Dashboard │
 │  - Verse input UI         │
 │  - Study Journal          │
 │  - Crossrefs & Context    │
 └────────────┬──────────────┘
              │ REST API (JWT)
              ▼
 ┌───────────────────────────┐
 │        API Gateway        │
 │  FastAPI / Flask Backend  │
 │  - Auth & Routing         │
 │  - Study Orchestrator     │
 │  - Logging / Metrics      │
 └────────────┬──────────────┘
              │
   ┌──────────┴──────────┐
   ▼                     ▼
[ML Services]         [Data Layer]
 - Observation ML       - PostgreSQL (user data)
 - Interpretation ML     - Vector DB (embeddings)
 - Application ML        - Redis cache
 - RAG (Commentaries)    - S3 (exports)


### 3. Core Methodology (OIA)

| Step | Description | ML / Logic |
| --- | --- | --- |
| Observation | “What does it say?” – Grammar, structure, key terms. | NER, syntax tree parsing, POS tagging |
| Interpretation | “What does it mean?” – Context, cultural background, cross-references. | Semantic similarity, RAG, summarization |
| Application | “How does it apply?” – Personal relevance, questions, transformation. | LLM reflection generation, sentiment analysis |


### 4. Project Structure

```
exegesisai/
├─ backend/
│  ├─ app/
│  │  ├─ main.py                # FastAPI entry
│  │  ├─ api/                   # Routers (auth, verses, study, notes, exports, admin)
│  │  ├─ core/                  # settings, security (JWT), logging
│  │  ├─ services/              # orchestrator + integrations (Bible API, RAG, embeddings)
│  │  ├─ models/                # SQLAlchemy models
│  │  ├─ schemas/               # Pydantic DTOs
│  │  ├─ workers/               # Celery/RQ tasks (stub)
│  │  └─ utils/
│  ├─ migrations/               # Alembic (placeholder)
│  ├─ tests/
│  ├─ requirements.txt
│  └─ .env.example
├─ ml/                          # Optional: service containers or notebooks
│  ├─ observation/              # spaCy pipeline
│  ├─ interpretation/           # RAG service
│  └─ application/              # LLM prompt templates
├─ vector/                      # pgvector init or adapters
├─ frontend/
│  ├─ src/                      # Next.js app (minimal stub)
│  ├─ public/
│  └─ .env.example
├─ ops/
│  ├─ docker/                   # Dockerfiles
│  ├─ compose/                  # docker-compose.yml
│  └─ k8s/                      # manifests (placeholder)
├─ Makefile
├─ .env.example                 # root env passed into compose
└─ README.md
```


### 5. Quick Start (TL;DR)

With Docker (recommended)

```bash
# 1) Clone & enter
git clone https://github.com/your-org/exegesisai.git
cd exegesisai

# 2) Create environment
cp .env.example .env

# 3) Launch full stack (API + Postgres + Redis + Workers + Frontend)
docker compose -f ops/compose/docker-compose.yml up --build
```

Without Docker (local Python + Node)

```bash
# Backend
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
uvicorn app.main:app --reload

# Frontend
cd frontend
pnpm i || npm i
cp .env.example .env.local
pnpm dev || npm run dev
```


### 6. Environment Variables

Create a file from each example:

- Root: `.env` → used by Docker Compose to wire services
- Backend: `backend/.env`
- Frontend: `frontend/.env.local`

Root `.env.example`

```bash
# Postgres
POSTGRES_USER=exegesis
POSTGRES_PASSWORD=exegesis
POSTGRES_DB=exegesis

# Redis
REDIS_URL=redis://redis:6379/0

# Vector DB (pgvector)
VECTOR_DATABASE_URL=postgresql+psycopg://exegesis:exegesis@db:5432/exegesis

# Backend
API_PORT=8000
API_URL=http://localhost:8000

# Frontend
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

Backend `backend/.env.example`

```bash
ENV=dev
API_BASE_URL=http://0.0.0.0:8000
JWT_SECRET=change-me
JWT_EXPIRES_MIN=60
REFRESH_EXPIRES_MIN=43200

# Datastores
DATABASE_URL=postgresql+psycopg://exegesis:exegesis@db:5432/exegesis
REDIS_URL=redis://redis:6379/0
VECTOR_DATABASE_URL=postgresql+psycopg://exegesis:exegesis@db:5432/exegesis

# Integrations
BIBLE_API_PROVIDER=esv
BIBLE_API_KEY=your-esv-key
OPENAI_API_KEY=your-openai-key
EMBEDDINGS_PROVIDER=openai
S3_ENDPOINT=http://minio:9000
S3_BUCKET=exegesis-exports
S3_ACCESS_KEY=change-me
S3_SECRET_KEY=change-me
S3_REGION=auto
```

Frontend `frontend/.env.example`

```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
NEXT_PUBLIC_DEFAULT_TRANSLATION=ESV
```


### 7. Running Services

Docker Compose

```bash
docker compose -f ops/compose/docker-compose.yml up --build
```

Services:

- api        : http://localhost:8000 (Swagger at /docs)
- db         : Postgres + pgvector
- redis      : cache + queue
- worker     : Celery/RQ worker (stub)
- frontend   : http://localhost:3000


### 8. API Usage (cURL / HTTPie)

Health

```bash
curl -s http://localhost:8000/health
```

Sign up + Login

```bash
http POST :8000/api/v1/auth/signup email=you@ex.com password=secret displayName=You
http POST :8000/api/v1/auth/login  email=you@ex.com password=secret
```

Lookup a verse

```bash
http GET :8000/api/v1/verses/lookup ref=="Romans 12:2" translation==ESV "Authorization: Bearer $JWT"
```

Run full OIA study

```bash
http POST :8000/api/v1/study/run \
  reference="Romans 12:2" translation="ESV" \
  include:='["observation","interpretation","application"]' \
  return_sources:=true "Authorization: Bearer $JWT"
```


### 9. Makefile (selected targets)

```
.PHONY: dev lint test fmt migrate seed

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	python -m pip install --quiet ruff || true
	ruff check backend

fmt:
	python -m pip install --quiet black isort || true
	black backend && isort backend

test:
	pytest -q

migrate:
	alembic upgrade head

seed:
	python -m app.scripts.seed_minimal
```


### 10. Notes

- This repository includes a functional FastAPI scaffold and minimal Next.js stub focused on demonstrating the OIA workflow and API surface. Individual ML services and heavy model weights are intentionally stubbed to keep the starter lightweight.
- Swap in your preferred Bible API provider and embeddings provider by adjusting `app/services` and environment variables.


