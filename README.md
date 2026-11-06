# ASR LABS AI Content Operating System

Multi-channel AI content studio for planning, producing, approving, and publishing educational content across independent brands — orchestrated by five coordinated agents and operated from a central founder dashboard.

> **Status:** Foundation + channel configs. App implementation proceeds phase by phase (see blueprint §11).

**Live brands**

| Channel | Educates on | Instagram | YouTube |
| --- | --- | --- | --- |
| **ASR LABS** | AI, science, emerging tech, women innovators (English) | `@asrlabs.co` (live) | Create from scratch |
| **MANTHAN** | धर्म • कर्म • आत्मबोध — contemplative wisdom (Hindi) | MANTHAN (live, early) | Create from scratch |

Configs: `config/channels/`. Strategy: `docs/CHANNELS.md`. Ops blueprint: `docs/ASR_LABS_Professional_Operating_Blueprint_v2.pdf`.

---

## Vision

Run a content operation like a product team:

| Layer | Responsibility |
| --- | --- |
| **Founder Dashboard** | Strategy overview, approvals, calendar, analytics |
| **Agent Layer** | CEO → Manager → Researcher → Production & QA → Publishing Manager |
| **Channel Layer** | Per-channel brand, voice, formats, and publishing targets |
| **Pipeline** | Topic → Research → Script → Voice → Visuals → Video → QA → Approve → Publish |
| **Data & Media** | Supabase/PostgreSQL for state; local/object storage for assets |

**Publishing targets (IST):** ASR LABS 08:00 + 20:00 daily; MANTHAN 19:00 daily (scale after buffer).

---

## Current Folder Structure

```text
ASR-LABS-AI-STUDIO/
├── backend/                 # FastAPI application
│   ├── agents/              # Five AI agents (roles + orchestration)
│   ├── api/                 # HTTP routes (dashboard, channels, pipeline)
│   ├── services/            # Business logic (LLM, media, FFmpeg, publish)
│   ├── database/            # Models, migrations, Supabase clients
│   └── workflows/           # Multi-step pipeline / job orchestration
├── frontend/                # Next.js + TypeScript + Tailwind dashboard
├── config/
│   └── channels/            # Per-channel brand & pipeline configs (YAML/JSON)
├── prompts/                 # Versioned prompt templates per agent/task
├── storage/                 # Generated media artifacts (gitignored content)
│   ├── scripts/
│   ├── voiceovers/
│   ├── visuals/
│   ├── videos/
│   └── thumbnails/
├── logs/                    # Runtime / agent logs (gitignored)
├── docs/                    # Architecture notes, runbooks, ADRs
├── .env.example             # Placeholder env var names only
├── .gitignore
└── README.md
```

---

## Proposed Architecture

### High-level flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    Founder Dashboard (Next.js)              │
│   Channels · Topics · Approvals · Calendar · Analytics      │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS (auth'd)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                        │
│  api/  →  workflows/  →  agents/  →  services/  →  database/│
└───────┬───────────────┬──────────────────┬──────────────────┘
        │               │                  │
        ▼               ▼                  ▼
   config/channels   prompts/         storage/ + Supabase
   (brand identity)  (LLM templates)  (Postgres + media)
```

### Agent responsibilities

| Agent | Owns | Inputs | Outputs |
| --- | --- | --- | --- |
| **CEO** | Strategy, channel goals, content pillars, KPIs | Founder prefs, analytics | Daily/weekly briefs, priorities |
| **Manager** | Scheduling, assignment, SLA, queue health | CEO briefs, channel capacity | Topic plan, job tickets |
| **Researcher** | Facts, angles, sources, competitive hooks | Topic ticket, channel niche | Research pack + outline |
| **Production & QA** | Script, VO, visuals, render, quality gates | Research pack, brand config | Draft assets + QA report |
| **Publishing Manager** | Calendar, captions, platform publish, metrics | Approved assets | Scheduled/published posts + analytics |

Agents never call each other ad hoc from the UI. The **workflow engine** advances a content job through typed stages and invokes the right agent at each stage.

### Backend layers

1. **`api/`** — Thin FastAPI routers. Auth, validation, serialization. No LLM or FFmpeg logic.
2. **`workflows/`** — State machine for a content job (`draft → research → produce → qa → approval → schedule → published`). Idempotent steps, retries, human gates.
3. **`agents/`** — Role prompts + structured I/O schemas. Each agent is a pure orchestration unit over `services/`.
4. **`services/`** — Reusable capabilities: LLM client, TTS, image/video gen, FFmpeg render, platform adapters, analytics ingest.
5. **`database/`** — SQLAlchemy/Supabase models, repositories, migrations. Secrets stay server-side.

### Frontend

- Next.js App Router + TypeScript + Tailwind.
- Talks **only** to the FastAPI backend (never to LLM/provider APIs directly).
- Surfaces: overview, channel settings, topic board, asset review, approval queue, publishing calendar, analytics.

### Data & secrets

- **Supabase PostgreSQL** — channels, jobs, agents runs, approvals, calendar, metrics.
- **Storage** — local `storage/` in early phases; migrate to object storage (e.g. Supabase Storage / S3) when needed.
- **Secrets** — backend `.env` only. Frontend gets public URLs / anon keys if required for auth UX; **no provider API keys in client code**.

### Channel model

Each channel under `config/channels/` defines:

- Brand voice, visual identity, forbidden topics
- Formats (short, long, carousel, etc.)
- Target platforms and posting windows
- Default agents overrides / prompt packs

---

## Module Guide

### `backend/agents/`

Implements the five agents as discrete modules with shared base types (`AgentContext`, `AgentResult`). CEO sets strategy; Manager creates jobs; Researcher fills evidence; Production & QA generates and scores assets; Publishing Manager ships and reports. Prompt text lives in `prompts/`, not hard-coded in agent classes when possible.

### `backend/api/`

REST (and later optional SSE/WebSocket) endpoints for the dashboard: channels CRUD, job lifecycle, approvals, calendar, analytics queries. Guarantees that all mutations go through workflows so agent side-effects stay auditable.

### `backend/services/`

Provider adapters and utilities: LLM, research tools, TTS, image generation, FFmpeg wrappers, thumbnail composition, YouTube/TikTok/etc. publishers. Services are the only place that reads secret env vars for third parties.

### `backend/database/`

Schema for users/founders, channels, content jobs, assets, agent runs, approvals, publish events, and metrics. Supabase client + migration strategy (e.g. Alembic or Supabase migrations).

### `backend/workflows/`

Orchestrates the daily/ops pipeline. Persists job stage, handles retries, pauses on **human approval**, and emits events the dashboard consumes.

### `frontend/`

Founder-facing UI. Channel switcher, Kanban/calendar for jobs, asset players/preview, approve/reject actions, analytics charts. Uses typed API client generated or hand-maintained against FastAPI OpenAPI.

### `config/channels/`

Source-of-truth configs for each independent channel (YAML/JSON). Loaded by backend at runtime; editable via dashboard later with DB override layer.

### `prompts/`

Versioned prompt templates (`ceo/daily_brief.md`, `researcher/outline.md`, etc.). Enables iteration without redeploying agent code when only wording changes.

### `storage/`

Filesystem buckets for intermediate and final media. Paths recorded in the database. Not committed to git.

### `logs/`

Structured application and agent-run logs for debugging production pipelines.

### `docs/`

Living architecture decisions, channel onboarding, ops runbooks.

---

## Tech Stack

| Concern | Choice |
| --- | --- |
| API | Python 3.11+ · FastAPI · Uvicorn |
| UI | Next.js · TypeScript · Tailwind CSS |
| Data | Supabase · PostgreSQL |
| Media | FFmpeg |
| Auth (planned) | Supabase Auth or equivalent server-verified sessions |
| Config | Env vars + channel YAML/JSON |

---

## Security Principles

1. **Never** put API keys or provider secrets in frontend code or client bundles.
2. All LLM / TTS / publish credentials live in backend environment variables.
3. Human approval is a hard gate before public publishing.
4. Audit agent runs and publish actions in the database.

---

## Implementation roadmap (from blueprint)

| Phase | Build | Exit criteria |
| --- | --- | --- |
| **0. Foundation** | Repo, brand configs, env template | ✅ Done |
| **1. App shell** | FastAPI + Next.js dashboard, brand tokens, schema, login | Founder can log in and create a content item |
| **2. Workflow** | Task lifecycle, five agents, audit log | Sample video moves through states |
| **3. Research** | Topic backlog, sources, claim checks | Dossier with traceable sources |
| **4. Production + QA** | Script, storyboard, assets, independent QA | Full package passes QA |
| **5. Approval UI** | Exact-version preview, pause switch | Nothing publishes without founder approval |
| **6. YouTube** | Official API upload + schedule | One approved test video live |
| **7. Instagram** | Graph API Reel publish | One approved test Reel live |
| **8. Analytics** | Metrics by slot/pillar | Weekly performance review |

Content states:  
`IDEA → RESEARCH → RESEARCH_APPROVED → BRIEF_READY → IN_PRODUCTION → QA_REVIEW → REVISION_REQUIRED → AWAITING_FOUNDER → APPROVED → SCHEDULED → PUBLISHED`

---

## Environment

Copy `.env.example` to `.env` and fill values locally. Never commit `.env`.

---

## License

Proprietary — ASR LABS. All rights reserved unless otherwise stated.
