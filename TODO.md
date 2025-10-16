# Jobcopilot — 60-day plan

Day 1 = 2026-11-06.

## Phase 1 — Foundations (day 1–14)
- [ ] D1  uv project, ruff + pytest, CI green
- [x] D2  SQLAlchemy models: Posting, Score, Letter, Digest (Posting done)
- [ ] D3  Postgres via docker-compose
- [ ] D4  Fetcher: RSS ingestion (feedparser), normalization
- [ ] D5  Fetcher: public job API source
- [ ] D6  CLI: `fetch` command
- [ ] D7  Profile model (your resume as YAML/JSON)
- [ ] D8  FastAPI skeleton: health + list postings
- [ ] D9  Storage layer tests
- [ ] D10 README: pipeline diagram, setup
- [ ] D11 Dockerfile
- [ ] D12 Alembic migrations
- [ ] D13 Config via pydantic-settings
- [ ] D14 Phase 1 retro

## Phase 2 — Depth (day 15–40) — the agentic core
- [ ] D15 LLM client abstraction (provider-agnostic)
- [ ] D16 Scoring agent: prompt + structured output (score + reasons)
- [ ] D17 Scoring agent: retry / validation loop on malformed output
- [ ] D18 Agent trace: log each reasoning step to DB (traceable "agentic" evidence)
- [ ] D19 CLI: `score` command
- [ ] D20 Letter agent: draft generation from profile + posting
- [ ] D21 Letter agent: tone/style rules + regeneration
- [ ] D22 CLI: `letter <posting-id>`
- [ ] D23 Dedup: near-duplicate detection (title+company hash)
- [ ] D24 Filters: location, remote, keywords, salary hints
- [ ] D25 Scheduler: daily fetch+score run (APScheduler)
- [ ] D26 Digest builder: top N matches
- [ ] D27 Digest render: markdown + JSON
- [ ] D28 API endpoints: postings, scores, letters
- [ ] D29 API endpoint: trigger fetch/score
- [ ] D30 Prompt eval suite: fixture postings with expected score bands
- [ ] D31 Cost tracking: token usage per run
- [ ] D32 Rate limiting + retries on LLM calls
- [ ] D33 Tests: agent flows with mocked LLM
- [ ] D34 README: agent architecture + trace screenshots
- [ ] D35 Structured logging
- [ ] D36 Refactor: pipeline as explicit steps (fetch→filter→score→draft→digest)
- [ ] D37 Multi-provider support (second LLM backend)
- [ ] D38 Error handling: dead-letter table for failed postings
- [ ] D39 Demo seed data
- [ ] D40 Phase 2 retro

## Phase 3 — Polish (day 41–60)
- [ ] D41 Test coverage push (>80%)
- [ ] D42 Docker compose: api + worker + db
- [ ] D43 GitHub Actions: ruff format check
- [ ] D44 CHANGELOG.md
- [ ] D45 Docs: prompt design notes
- [ ] D46 Eval report in README (accuracy on fixture set)
- [ ] D47 Demo GIF in README
- [ ] D48 Tag v0.1 release
- [ ] D49 Cross-link jobcopilot-ui
- [ ] D50–D60 Buffer / stretch: email digest, more sources, salary parsing
