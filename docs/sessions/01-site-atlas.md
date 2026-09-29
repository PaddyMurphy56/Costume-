# Session 1 kickoff: Site Atlas

Paste everything below the line into a new session on this repo.

---

You are running **Session 1 (Site Atlas)** of a multi-session build. Start by reading `CLAUDE.md` and `docs/ROADMAP.md`. They explain the whole system, the build order, the contracts and the environment limits.

## Your job
Build a **massive, deep list of places to shop**, with used, resale, vintage, auction and estate sites first. Etsy, Depop and eBay are the obvious starting points. The value is in going far beyond them:
- niche, regional and app-first marketplaces
- auction houses and estate-sale aggregators
- online thrift
- liquidation and returns
- international sites reachable through proxy buying
- costume, prop and Halloween specialists
- luggage and office specialists
- deal aggregators
- **Houston-local sources** near Spring Branch and Memorial (the user is there, and local pickup counts): estate sales, thrift and resale shops, classifieds, pickup marketplaces
- anything else a determined bargain hunter would use

This list feeds two later systems:
- the **Tagger** (S2), which turns an item's text and photo into hashtags and keywords;
- the **Hunter** (S3), which searches your sites with those keywords.

The first real use is the costume brief in `config/brief.yaml`, but the Atlas should serve general resale shopping too.

**This session builds the Atlas; it doesn't operate it.** Once all five systems are built, the whole system runs end to end **20–30 times**. Each run adds items to a gallery where the user rates every item, and the system learns from those ratings. That means the Atlas must be refreshable, and it must be able to record per-site yield (which sites produce well-rated items) so later runs can favor the sites that deliver. See ROADMAP §6.

## Start with Method Discovery
Before you build anything, run a workflow that works out **the best way to build the Site Atlas**. ROADMAP §5 gives the minimum bar:
1. frame
2. sweep tools, plugins, skills, MCP servers, connectors, APIs and prior art for **the most efficient way to do each step**, including which web scraper and search tooling to use (nothing is a default)
3. **ask the user 5–10 questions** about how the Site Atlas should work, and **suggest 1–5 things to implement**; wait for the answers before locking the design
4. build at least two genuinely different candidate methods
5. bake-off with the scoring rule written first
6. challenge the winner
7. decision record

Record it in `research/01-site-atlas/method-discovery.md`, using `docs/templates/method-discovery.md`. Questions worth answering:
- How do experienced resellers and bargain hunters find obscure sites?
- Which directories, lists, communities and datasets catalogue marketplaces?
- How do you tell a live site from a dead, merged or rebranded one?
- How can you test, at scale and within each site's terms, whether a site can be searched from this environment?
- How should the Atlas keep growing and track per-site yield across 20–30 runs?
- Which web scraper and search tooling is most efficient for finding, profiling and probing sites at this scale? Compare real options; don't default to whatever is connected.

You can and should create agents in `.claude/agents/` whenever that would make the system better.

## Deliverables
1. **`registry/sites.yaml`**, validated with `uv run costume-validate registry/sites.yaml schemas/site.schema.json`.
   - You own `schemas/site.schema.json`. Revise it if Method Discovery shows it should change: bump `schema_version`, update `schemas/examples/`, keep `uv run pytest` passing.
2. **An access result for every site:** how it can be searched from here (connector, search-engine index, API, or blocked), with evidence.
3. **Tag conventions per site** (hashtags, tag limits, attribute fields) for the Tagger.
4. **A labeled listing sample for S2:** real listings with photo, seller title, seller tags or attributes, site and URL. Cover briefcases, axes and fake blood, plus some general items. S2 uses this as ground truth to test tags against.
5. **A rerunnable workflow**, such as a skill or script, so the Atlas can be refreshed and grown later.
6. **A decision record** in `docs/decisions/`.
7. **A handoff note** in `docs/handoffs/` (template in `docs/templates/`). Include the questions you asked, the user's answers, and which suggestions were accepted.
8. **The Session 2 kickoff prompt** in `docs/sessions/02-tagger.md`, written from what you actually built and learned. Carry forward the S2 brief from ROADMAP §8, including its requirement that tag generation be advanced and learn from ratings. Also carry forward the rule that every session asks 5–10 questions and suggests 1–5 things to implement.

## Done when
- At least 150 live sites are in the registry. That is a floor: set a higher target if Method Discovery supports it.
- Every site has an access result.
- The listing sample exists.
- The user's answers to your questions are reflected in what you built.
- Tests and lint pass.
- The deliverables above are committed and pushed on a branch with a draft PR.

## Constraints
- Retailer hosts are blocked from the container unless they're allowlisted. Retailer images are approved but may not be live yet: check with `uv run costume-netcheck`. Choose your web tooling in Method Discovery; the Firecrawl connector and WebSearch/WebFetch are available today, but they are not defaults.
- Never bypass logins, captchas or bot protection, and never scrape against a site's terms. Record them as blockers instead.
- Cite sources. Mark anything unconfirmed as unverified.
- Timebox: this session should finish on 2026-09-30. Each build session gets about a day, so there's time for 20–30 runs before the costume's buy-by date of 2026-10-15.
