# Costume

A multi-session build of a shopping system that finds items across a very wide range of sites, guided by hashtags created from each item's words and picture. It learns the user's taste from their ratings. Its first job is sourcing a Patrick Bateman costume.

## Read first
- `docs/REQUIREMENTS.md`: everything the user has asked for, plus the environment facts. These are the inputs.
- `docs/ROADMAP.md`: the session order, and each session's inputs and deliverables.
- `docs/sessions/`: the kickoff prompt for each session.

## Rules for every session
- **Nothing is decided in advance** except the inputs and deliverables. Each session chooses its own tools, methods, formats and structure.
- **Method first.** Start with a workflow that finds the best way to build your part. Research tools, plug-ins, MCP servers and so on for the most efficient way to do everything, including which web scraper to use.
- **Questions and suggestions.** During creation, ask the user 5–10 questions about how the system should work, and suggest 1–5 things to implement.
- **Agents.** Create them whenever that would make the system better.
- **Scope.** Build only your part. Finish with the handoff and the next session's kickoff prompt.
- **Access limits.** Never bypass logins, captchas or bot protection, and never scrape against a site's terms.
