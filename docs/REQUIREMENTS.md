# Requirements

These are the inputs every session starts from. Everything here comes from the user, except the environment and reference facts at the end, which were verified in Session 0.

**Nothing about tools, methods, formats or architecture is decided here.** Each session decides those for its own part.

## The costume

- **Character:** Patrick Bateman, one-time use.
- **Already owned:** a suit and a tie.
- **Needed:** a briefcase, a fake axe and fake blood.
- **The briefcase:**
  - It must hold regular 12 oz cans or beer bottles, with room for a plastic bag or two full of ice.
  - It should be as small as possible so it doesn't look awkward.
  - It must not be so small that it stops looking like a regular briefcase.
- **Budget:** $75 total, with shipping included. Purchases are made online.
- **Add-ons:** recommend things that would make the costume look tough.
- **No finished costume.** The system should not put together one total costume at the end. It should add items to the artifact, and the user puts the costume together later.
- **Location:** Houston, TX, in the Spring Branch / Memorial area.
- **Dates:** research stops and buying happens by **Oct 15, 2026**. Halloween is Oct 31.

## The system

### How it gets built

- There are three systems, each built in its own new session:
  1. **Site list.** A workflow that finds a massive, deep list of sites for the shopping system to search, especially used and resale sites such as Etsy, Depop and eBay.
  2. **Hashtag system.** It takes an item and creates a list of hashtags.
     - It uses the picture, not just the words.
     - It must be advanced, because the whole system is based on it.
     - Its session should include a workflow that finds the best way to do this.
     - Its hashtags curate and guide the shopping system.
  3. **Shopping system.** It does the researching and shopping across the sites, using keywords and hashtags from the hashtag system. Its session should find the best tools and workflow for that research.
- After those three:
  - a **final session** combines everything;
  - a **final final session** double-checks the whole system, looks for holes and makes it better.
- Each session is an entire session, and its only job is to build its part.

### How it runs

- Once built, the whole system runs **20–30 times** before the buy-by date.
- The user starts each run **manually**.

### The artifact

The artifact shows every item with **pictures and links**.

**Rating items**
- The user rates **every item 1–10**, so the system learns their style.
- There is an **easy way to see how the 1–10 scores are distributed**, so the user can judge more accurately.
- The user can **very easily change the rankings**.

**Hashtags**
- The system produces a good amount of hashtags, and the user does not have to rank each one.
- The user can **star, double-star and triple-star** hashtags (★, ★★, ★★★).
- The rating system shows **which hashtags are popular**, so the search gets better.

**Notes**
- The user can add **notes to hashtags and to items**.
- The shopper takes those notes in, along with the rankings.

### How the system learns

- Ranking and hashtag creation must be **advanced**, so the shopping system gets better with each run and works out the vibe and taste for the costume.
- **The shopper looks at the distributions**, not just raw values. For example, if there's only one ★★★ hashtag, that hashtag is very valuable.
- **The shopper uses the hashtag creator on the listings it finds.** It adds the best hashtags to the list, and it uses keywords and hashtags to search for new things.

### How every session works

- **It starts with a workflow that finds the best way to build its part.**
  - It researches tools, plug-ins, MCP servers and so on, looking for the most efficient way to do everything.
  - Nothing is a default, including which web scraper to use.
- **During creation it asks the user 5–10 questions** about how the system should work, and **suggests 1–5 things to implement**.
- **It can and should create agents** whenever that would make the system better.
- **It aims for more, not less.** The user wants the system over-engineered rather than minimal.

## Approvals from the user

- **Retailer images are allowed.** They still have to be added to the environment's allowed domains; see the environment facts below.

## Open questions

- Should the system stay costume-specific, or be general enough for future shopping?

## Environment facts (verified 2026-09-29; facts, not decisions)

- **Retailer sites are blocked.** The container's network proxy returns 403 for retailer sites and their image hosts unless they're added to the environment's allowed domains. As of 2026-09-29, `m.media-amazon.com`, `i.ebayimg.com`, `i5.walmartimages.com`, `i.etsystatic.com` and `target.scene7.com` were still blocked.
- **Some other hosts are reachable.** PyPI, npm and `storage.googleapis.com` all respond.
- **Tools connected today** include a Firecrawl connector and the built-in WebSearch/WebFetch. These are only what happens to be available; they are not defaults.
- **The container has** Python 3.11, uv, Node 22 and a Chromium browser installed.
- **Artifact pages** can't load external images directly.

## Reference facts

- **Houston's combined sales tax rate** is 8.25%.
- **A standard 12 oz can** is about 4.83" tall and 2.6" across.
- **A 12 oz longneck bottle** is roughly 9" tall and 2.5" across.
