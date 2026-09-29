# Costume: deep resale-shopping system

A multi-session build of a system that finds deep-cut items across a very wide range of shopping sites. Tags generated from an item's text and photo guide the search. The first job is the Patrick Bateman costume brief in `config/brief.yaml`: a briefcase, a fake axe and fake blood for **$75 total including shipping and tax**, bought by **2026-10-15**. The system should also recommend add-ons that would make the costume look tough.

Read `docs/ROADMAP.md` before doing anything. It holds the build order, the session briefs, the contracts and the environment facts.

## Session model
- **There are two phases.** First, five build sessions, one per system. Then the finished system runs end to end **20–30 times** before the buy-by date (ROADMAP §6).
- **Each run adds items to a gallery; the system never assembles a costume.** The user puts the costume together from the gallery later.
- **Each run makes the system smarter.** The user gives feedback in four ways:
  - scores **every item** from 1 to 10, with a distribution chart to judge against;
  - changes rankings easily (reorder, pin, bury, factor sliders);
  - optionally boosts hashtags with ★/★★/★★★ or mutes them;
  - adds notes to items and hashtags.

  Hashtags never need individual ratings: their scores are learned from the scores of the items they describe. The Hunter runs the Tagger on every listing it finds, adds the best new hashtags to the hashtag pool, and follows them to find new things. All of this feedback is read against its distribution: a lone ★★★ hashtag is very valuable, and a 7 from a tough scorer is a strong score. It drives the hashtag popularity board, the taste/vibe profile, site yield, and advanced ranking and tag generation. The Tagger and Hunter read the notes on every run.
- Build every system to be run repeatedly: run logs, stable IDs, idempotent steps, and a known cost per run.
- Each system is built in its own new session:
  - S1 Site Atlas
  - S2 Tagger
  - S3 Hunter
  - S4 Integration
  - S5 Audit & Hardening
- The kickoff prompt for each session is in `docs/sessions/`.
- **Every session starts with Method Discovery.** Work out the best way to build that part before building it (ROADMAP §5). Keep the record in `research/<session>/method-discovery.md`.
- **Every session asks and suggests.** During creation, ask the user **5–10 questions** about how the system should work, and **suggest 1–5 things to implement**. Wait for the answers before locking the design. Record the questions, the answers and the accepted suggestions in the handoff.
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
uv run costume-netcheck [group]           # which hosts in config/network.yaml are reachable
```

## Environment constraints
- **No default tools.** Every session researches tools, plugins, skills, MCP servers, connectors, APIs and libraries, and picks the **most efficient way** to do each step. That includes the web scraper and search tooling. The Firecrawl connector and WebSearch/WebFetch are available today, but they are candidates, not defaults.
- The container's proxy blocks retailer sites and their image CDNs (403) unless a host is added to the environment's allowed domains. Retailer images are approved (`config/network.yaml`). Check reachability with `uv run costume-netcheck`.
- The user is in Houston, TX (Spring Branch / Memorial). Local pickup counts.
- PyPI and npm are reachable.
- Artifact pages can't load external images. Product photos have to be uploaded to the artifact.

## Rules
- Never bypass logins, captchas or bot protection, and never scrape against a site's terms. Record these as blockers.
- Cite sources for facts about sites and tools. Mark anything unconfirmed as unverified.
- Contracts change only with a schema version bump, a passing `uv run pytest`, and a note in the handoff.
