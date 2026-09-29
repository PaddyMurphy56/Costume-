# Costume: deep resale-shopping system

A multi-session build of a system that finds deep-cut items across a very wide range of shopping sites. Tags generated from an item's text and photo guide the search. The first job is the Patrick Bateman costume brief in `config/brief.yaml`: a briefcase, a fake axe and fake blood for **$75 total including shipping and tax**, bought by **2026-10-15**. The system should also recommend add-ons that would make the costume look tough.

Read `docs/ROADMAP.md` before doing anything. It holds the build order, the session briefs, the contracts and the environment facts.

## Session model
- **There are two phases.** First, five build sessions, one per system. Then the finished system runs end to end **20–30 times** before the buy-by date (ROADMAP §6).
- **Each run makes the system smarter.** The user rates listings and hashtags. Those ratings drive a hashtag popularity board, a taste/vibe profile, site yield, and advanced ranking and tag generation.
- Build every system to be run repeatedly: run logs, stable IDs, idempotent steps, and a known cost per run.
- Each system is built in its own new session:
  - S1 Site Atlas
  - S2 Tagger
  - S3 Hunter
  - S4 Integration
  - S5 Audit & Hardening
- The kickoff prompt for each session is in `docs/sessions/`.
- **Every session starts with Method Discovery.** Work out the best way to build that part before building it (ROADMAP §5). Keep the record in `research/<session>/method-discovery.md`.
- Create agents in `.claude/agents/` whenever that would make the system better.
- Stay inside your session's scope. Finish by writing a handoff note (`docs/handoffs/`) and the next session's kickoff prompt (`docs/sessions/`).

## Where things live
| Path | What |
|---|---|
| `config/brief.yaml` | The costume brief. Every system reads its constraints from here. |
| `schemas/` | JSON Schema contracts between systems, plus examples |
| `registry/` | The Site Atlas output (`sites.yaml`) |
| `research/<session>/` | Each session's working notes, bake-offs and data |
| `docs/decisions/` | Decision records, numbered `0001-...` |
| `docs/handoffs/` | End-of-session handoff notes |
| `docs/sessions/` | Kickoff prompts for each session |
| `docs/templates/` | Templates for the three doc types above |
| `src/costume/` | Shared Python code |
| `tests/` | pytest |

## Commands
```bash
uv sync                                   # install (the SessionStart hook does this on the web)
uv run pytest                             # tests
uv run ruff check . && uv run ruff format --check .   # lint and format check
uv run costume-validate <file> <schema> [--def Name] [--each]   # validate data against a contract
```

## Environment constraints
- The container's proxy blocks retailer sites and their image CDNs (403). Do web research through the Firecrawl connector or WebSearch/WebFetch, not `curl`.
- PyPI and npm are reachable.
- Artifact pages can't load external images. Product photos have to be uploaded to the artifact.

## Rules
- Never bypass logins, captchas or bot protection, and never scrape against a site's terms. Record these as blockers.
- Cite sources for facts about sites and tools. Mark anything unconfirmed as unverified.
- Contracts change only with a schema version bump, a passing `uv run pytest`, and a note in the handoff.
