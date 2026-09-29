# Roadmap

This roadmap covers the order of the build sessions and each session's inputs and deliverables. **Nothing else is decided.** Every session chooses its own tools, methods, formats and structure. The requirements behind all of it are in `docs/REQUIREMENTS.md`.

## Sessions

| Session | Builds |
|---|---|
| S1 | Site list |
| S2 | Hashtag system |
| S3 | Shopping system |
| S4 | Combined system |
| S5 | Double-check and improve |

After S5, the whole system runs 20–30 times, started manually, before the Oct 15 buy-by date. The build sessions have to leave room for those runs.

## Why this order

- **S1 needs nothing from the others.** Its site list is an input to both S2 and S3.
- **S2 comes before S3.** The shopping system searches with the hashtag system's keywords and hashtags, and it runs the hashtag system on the listings it finds.
- **S4 needs S1–S3.** It combines them into one system with the artifact.
- **S5 needs S4.** It checks and improves the whole thing.

## Every session

**Inputs**
- `docs/REQUIREMENTS.md`
- This roadmap.
- Every earlier session's deliverables and handoff.

**Rules** (from the user)
- **Method first.** Start with a workflow that finds the best way to build your part. Research tools, plug-ins, MCP servers and so on for the most efficient way to do everything. Nothing is a default.
- **Questions and suggestions.** During creation, ask the user 5–10 questions about how the system should work, and suggest 1–5 things to implement.
- **Agents.** Create them whenever that would make the system better.
- **Scope.** Build only your part. Running the system comes after S5.

**Deliverables every session also produces**
- **The record of your method research,** and why you chose what you chose.
- **The Q&A record:** the questions you asked, the user's answers, and the suggestions you made, with which ones were accepted.
- **A handoff for the next session:**
  - what was built;
  - how to use it;
  - what's unfinished or weak.
- **The next session's kickoff prompt,** in `docs/sessions/`. Write it from this roadmap and from what you actually built.
- **Everything committed and pushed,** on a branch with a pull request.

## S1: Site list

**Inputs:** the common inputs.

**Deliverables**
- **A massive, deep list of shopping sites** for the shopping system to search:
  - used and resale sites first, such as Etsy, Depop and eBay, and going far beyond them;
  - local sources for the Houston (Spring Branch / Memorial) area.
- **The workflow that produces the list,** so it can be run again.

## S2: Hashtag system

**Inputs:** the common inputs, plus S1's site list.

**Deliverables**
- **A hashtag system** that takes an item and creates a good amount of hashtags and keywords. It:
  - uses the item's **picture**, not just its words;
  - is advanced, because the whole system is based on it;
  - works on items the shopping system finds, as well as on the costume's items;
  - takes in the user's 1–10 item ratings, hashtag stars (★/★★/★★★) and notes, reading them against their distributions.
- **The workflow and findings** that established the best way to do this.

## S3: Shopping system

**Inputs:** the common inputs, plus S1's site list and S2's hashtag system.

**Deliverables**
- **A shopping and research system** that:
  - searches the site list using keywords and hashtags from the hashtag system;
  - runs the hashtag system on the listings it finds, adds the best hashtags to the list, and uses keywords and hashtags to search for new things;
  - ranks every item with an advanced ranking that gets better each run and works out the costume's vibe and taste;
  - looks at the distributions of item ratings and hashtag stars (for example, a lone ★★★ hashtag is very valuable);
  - takes in the user's notes and rankings;
  - shows each item's cost including shipping, against the $75 budget.
- **The workflow and findings** that established the best tools and workflow for this.

## S4: Combined system

**Inputs:** the common inputs, plus the deliverables of S1–S3.

**Deliverables**
- **One system** that runs end to end, is started manually, and can run 20–30 times.
- **The artifact.** It adds items over time and never assembles a costume. It includes:
  - every item, with pictures and links;
  - a 1–10 rating for every item;
  - an easy way to see how the 1–10 scores are distributed;
  - a very easy way to change the rankings;
  - ★ / ★★ / ★★★ on hashtags, with no need to rate each hashtag;
  - notes on items and hashtags;
  - which hashtags are popular.
- **Recommendations** for add-ons that would make the costume look tough.
- **Feedback that reaches the other systems:** ratings, rankings, stars and notes feed back into hashtag creation and shopping.

## S5: Double-check and improve

**Inputs:** the common inputs, plus the deliverables of S1–S4.

**Deliverables**
- **A review of the whole system** that looks for holes.
- **Improvements,** made to the system.
- **A list** of whatever is still open.
