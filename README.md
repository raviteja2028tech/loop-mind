# LOOP-MIND

**AI Recruitment Agent and Closed-Loop Campus Recruitment Intelligence Platform** — Hack in Hills '26, Round 2A prototype.

Team (PES University): Bhuvan Kumar P, Chiranthan B S Raj, A Raviteja.  
Built for Hack in Hills '26, Round 2A (prototype).

## The problem

Students prepare without knowing what each company expects, and when a candidate is not selected the process simply ends — the reasons (skill gaps, missing evidence) are never carried forward. Recruiters screen candidates without a shared evidence trail.

LOOP-MIND connects **student preparation** with **campus recruitment outcomes** in one loop, and keeps a **human recruiter** at the final decision. The authoritative specification is [`spec.md`](spec.md); the build order is in [`phase.md`](phase.md).

## What works in the prototype

Verified end to end on the real app:

| Student portal | Recruiter portal |
| --- | --- |
| Mobile + OTP login / account creation | Mobile + OTP login |
| Dashboard (profile completion, skills, projects, readiness) | Dashboard (jobs, applications, pipeline) |
| Skill-gap analysis for a chosen company + role: readiness %, missing skills, priority areas | Job management |
| Year-aware preparation plan | Candidates table with AI score and matching factors |
| Browse and apply to published jobs (starts the AI workflow) | AI workflow view: Resume Parser, Embedding, Matching, Shortlisting, **Human Approval**, Interview, Email |
| | Approve / Disapprove; approval triggers interview-question generation and the invitation email |
| | Interviews page; recruitment analytics |

Implemented but **not exercised in this round**: resume upload/parsing from the UI, What-If analysis, the Disapprove path, interview outcome recording, LinkedIn import, the React Native client in `mobile/`.

What the readiness score is: a comparison of the student's recorded skills and evidence against the selected company/role requirements (`backend/services/skill_gap_page_service.py`, agents in `AI services/agents/`). It is **not** a probability of being hired.

## Architecture

```text
React + TypeScript (Vite, Tailwind, React Flow, Recharts)      mobile/ (React Native)
                          |  REST /api  (proxied by Vite)
                 FastAPI + Pydantic + SQLAlchemy  (JWT + OTP auth)
        |-------------------|--------------------------|
   SQLite (primary)   AI services (LangChain agents,     ML and DL (scikit-learn
   Qdrant local        Gemini 2.5 Flash, RAG,             outcome pipeline, separate
   (vectors)           Sentence-Transformers)             from the agents)
```

AI recruitment flow: application + PDF resume -> Resume Parser -> Embedding -> Matching -> Shortlisting -> **Human Approval** -> Interview Agent -> Email Agent. A non-approved outcome is recorded with a reason.

| Directory | Purpose |
| --- | --- |
| `frontend/` | React web app (student, recruiter, public site) |
| `backend/` | FastAPI API, models, services, tests |
| `AI services/` | 12 LangChain agents, 2 multi-agent pipelines, RAG over Qdrant |
| `ML and DL/` | Dataset generation, preprocessing, training, evaluation gate, model store |
| `databases/` | SQLite file and local Qdrant store (git-ignored runtime data) |
| `specs/` | Recruitment rules and thresholds |
| `mobile/` | React Native client calling the same backend |

## Setup

Prerequisites: Python 3.12, Node.js 20+, Chrome (only for the demo recorder).

```bash
python -m venv .venv
.venv/Scripts/activate            # source .venv/bin/activate on macOS/Linux
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
pip install -r "AI services/requirements.txt"
pip install -r "ML and DL/requirements.txt" --extra-index-url https://download.pytorch.org/whl/cpu
cd frontend && npm install
```

### Environment

Copy `backend/.env.example` to **`.env` at the repo root**. Defaults work for a local demo; the optional values are:

- `GOOGLE_API_KEY` — Gemini key. Without it the agents run their deterministic fallback.
- `EMAIL_*` — SMTP mailbox for interview invitations. Empty means the Email Agent reports "not configured" and never fakes a send.
- `JWT_SECRET_KEY` — set a random value of 32+ bytes.

Never commit `.env`; it is git-ignored.

### Database

No manual step. On startup (`backend/main.py`) the tables are created and, outside `ENVIRONMENT=production`, the demo recruiter, demo student, 10 seed companies, seed jobs and the Qdrant company index are created. Company history is **seed data**.

## Run

```bash
# backend (from repo root)  ->  http://localhost:8011
.venv/Scripts/python.exe -m uvicorn backend.main:app --port 8011
# frontend                  ->  http://localhost:5180   (proxies /api to :8011)
cd frontend && npm run dev
```

Demo logins (development only; the OTP is fixed to `1111`):

| Role | Mobile |
| --- | --- |
| Student | `8888888888` |
| Recruiter | `9999999999` |
| New account | any unused 10-digit number |

## Tests

```bash
.venv/Scripts/python.exe -m pytest -q         # run with the backend STOPPED (Qdrant local lock)
.venv/Scripts/python.exe -m ruff check backend
cd frontend && npx tsc -b && npm run lint && npm run build
```

Last observed results: 139 backend tests passed; type-check, lint (0 errors) and build passed.

## Demo video

The prototype demonstration video is shared separately with the hackathon submission.

## Known limitations

- Company recruitment history is seed data, not real campus data.
- No outcome model is trained or validated: `ML and DL/models/ML/` is empty and training needs at least 10 concluded hires and 10 rejections. The deep-learning layer is intentionally unused.
- The seed jobs contain duplicate Nexora "Backend Engineer" postings.
- Retrieval uses embedded (local) Qdrant, so only one process can open it at a time.
- Bundled frontend chunks are larger than 500 kB; there are no frontend unit or e2e tests.
- The local `.env` JWT secret is shorter than the recommended 32 bytes.

## Planned future work

Train and validate the outcome model once enough concluded outcomes exist; replace seed company history with real recruitment data; consent-based placed-student knowledge sharing; a deep-learning layer only if the data justifies it.

## Contributors

- Chiranthan B S Raj
- Bhuvan Kumar P
- A Raviteja

## License

MIT, see [LICENSE](LICENSE).
