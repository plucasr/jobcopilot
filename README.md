![Jobcopilot](docs/banner.svg)

# Jobcopilot

[![CI](https://github.com/plucasr/jobcopilot/actions/workflows/ci.yml/badge.svg)](https://github.com/plucasr/jobcopilot/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Agentic job-hunt copilot. Watches job sources, scores postings against your profile with an LLM agent, and drafts tailored cover letters.

## Features
- **Find** — RSS / public API ingestion
- **Score** — LLM agent with traceable reasoning steps, persisted to `agent_traces`
- **Draft** — tailored cover letters (planned)
- **Digest** — daily best matches (planned)

## Agent trace

Every step the scoring agent takes (prompt built, LLM response, parse attempts,
persistence) is recorded in the `agent_traces` table, making each score
fully traceable.

```bash
export LLM_API_KEY=...
jobcopilot score --profile profile.json --db sqlite:///jobcopilot.db
```

## Stack
Python · FastAPI · Typer · SQLAlchemy · PostgreSQL

## Related
UI: [jobcopilot-ui](https://github.com/plucasr/jobcopilot-ui)

## Status
Actively built over 60 days — see [TODO.md](TODO.md) for the traceable plan.
