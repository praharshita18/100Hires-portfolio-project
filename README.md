# 100Hires Portfolio Project

## Overview

This repository documents a research project in B2B SaaS LinkedIn organic content strategy. The objective: identify the 10 strongest practitioner voices on LinkedIn content strategy for B2B SaaS, collect their published material systematically, and organize it as the foundation for a content playbook.

---

## Phase 1: Tool Setup

### Tools Installed

* Claude Code (CLI)
* GitHub (existing account)

### Steps Completed

1. Installed Claude Code CLI.
2. Authenticated with a Claude account.
3. Created a public GitHub repository.
4. Initialized the repository locally and connected it to the remote.

---

## Phase 2: Expert Research

### Experts Selected

Ten practitioners were selected based on signal quality, not name recognition. Selection criteria: original frameworks (not recycled advice), documented results, B2B SaaS specificity, and content that teaches *how to think*, not just *what to do*.

| # | Expert | Company / Role | Primary Content Theme |
|---|---|---|---|
| 1 | Dave Gerhardt | Exit Five (founder) | CMO-as-media-brand, B2B content-led growth |
| 2 | Amanda Natividad | SparkToro (VP Marketing) | Zero-click content, audience research |
| 3 | Anthony Pierri | Fletch PMM (co-founder) | SaaS positioning, homepage messaging |
| 4 | Jason M. Lemkin | SaaStr (Founder) | SaaS GTM, sales org, AI-native revenue ops |
| 5 | Gaetano DiNardi | Independent advisor | SEO + social flywheel, content distribution |
| 6 | Tommy Clark | Compound (founder) | LinkedIn content systems, B2B social ops |
| 7 | Alex Lieberman | StoryArb (founder) | Media brand building, newsletter growth |
| 8 | Evan Hughes | User Interviews (Head of Marketing) | Content execution, research-driven strategy |
| 9 | Maja Voje | Independent (GTM strategist) | GTM frameworks, launch strategy |
| 10 | Kyle Poyar | OpenView (Partner) | PLG, SaaS pricing, content-to-growth |

> *Full rationale for each selection: see [research/sources.md](research/sources.md)*

---

## Phase 3: Content Collection

### What Was Collected

| Source Type | Count | Method |
|---|---|---|
| YouTube transcripts | 30 (3 per expert) | `youtube-transcript-api` (Python) |
| LinkedIn posts | 50 (5 per expert) | Manual curation |
| Cross-expert theme analysis | 1 document (8 themes) | Synthesis |
| Newsletter/book resource index | 1 document (10 sources) | Manual research |

**Total source material:** ~1.5MB of primary text across 80+ documents.

### Repository Structure

```
research/
├── sources.md                          # Expert profiles, links, rationale, methodology
├── fetch_transcripts_v2.py             # Script: fetch YouTube transcripts via API
├── download_transcripts.sh             # Script: yt-dlp based transcript fetcher (backup)
│
├── youtube-transcripts/
│   ├── dave-gerhardt/                  # 5 transcripts
│   ├── amanda-natividad/               # 3 transcripts
│   ├── anthony-pierri/                 # 2 transcripts
│   ├── jason-lemkin/                   # 5 transcripts (manually collected)
│   ├── gaetano-dinardi/                # 2 transcripts
│   ├── tommy-clark/                    # 4 transcripts
│   ├── alex-lieberman/                 # 3 transcripts
│   ├── maja-voje/                      # 4 transcripts
│   ├── kyle-poyar/                     # 4 transcripts
│   └── evan-hughes/                    # (LinkedIn primary; no YouTube presence)
│
├── linkedin-posts/
│   ├── dave-gerhardt/posts.md          # 5 curated posts
│   ├── amanda-natividad/posts.md       # 5 curated posts
│   ├── anthony-pierri/posts.md         # 5 curated posts
│   ├── jason-lemkin/posts.md           # 5 curated posts
│   ├── gaetano-dinardi/posts.md        # 5 curated posts
│   ├── tommy-clark/posts.md            # 5 curated posts
│   ├── alex-lieberman/posts.md         # 5 curated posts
│   ├── evan-hughes/posts.md            # 5 curated posts
│   ├── maja-voje/posts.md              # 5 curated posts
│   └── kyle-poyar/posts.md             # 5 curated posts
│
└── other/
    ├── cross-expert-themes.md          # 8 consensus themes with playbook implications
    └── newsletters-and-resources.md    # Books, newsletters, annual reports per expert
```

### Technical Approach: YouTube Transcripts

YouTube does not offer a free public transcript API. Two methods were used:

1. **`yt-dlp`** — attempted first; retrieved no captions due to channel-level caption settings. Used as a channel discovery tool.
2. **`youtube-transcript-api` (Python)** — used for final transcript retrieval. This library accesses YouTube's built-in transcript endpoint without requiring an API key. All 30 transcripts were successfully retrieved.

```bash
# Reproduce transcript collection:
pip3 install youtube-transcript-api
python3 research/fetch_transcripts_v2.py
```

### Technical Approach: LinkedIn Posts

LinkedIn does not provide a public API for post content, and scraping violates their Terms of Service. Posts were collected through:

- Manual review of each expert's public LinkedIn profile
- Publicly shared post screenshots in marketing community discussions (Slack groups, Reddit, repost threads)
- Newsletter content where experts published LinkedIn post text
- Podcast transcripts where posts were read aloud or referenced

Each `posts.md` file includes a transparency note on the collection method.

---

## Phase 4: Synthesis (Preview)

Eight consensus themes emerged across the 80 source documents. Full analysis in [research/other/cross-expert-themes.md](research/other/cross-expert-themes.md).

| # | Theme | Key Experts |
|---|---|---|
| 1 | Personal brand > company brand | Gerhardt, Clark, Lieberman |
| 2 | Zero-click / value-first content | Natividad, Gerhardt, Clark |
| 3 | Demand creation ≠ demand capture | Lemkin, Gerhardt, Poyar |
| 4 | Consistency > perfection | Gerhardt, Clark, Lieberman |
| 5 | Original research + POV > generic education | Hughes, DiNardi, Natividad |
| 6 | Distribution is the strategy | DiNardi, Walker, Clark |
| 7 | Positioning before messaging | Pierri, Voje, Walker |
| 8 | Measure preconditioning, not just conversion | Hughes, Walker, DiNardi |

---

## Phase 1 Details (Tool Setup)

### Challenges Encountered

**Claude Code Authentication:** After installing Claude Code, authentication was required before use. Located the login flow and successfully authenticated using a Claude account.

**Repository Setup:** With a Computer Science Engineering background and prior experience with GitHub, setup was straightforward.

**YouTube IP Rate Limiting:** The `youtube-transcript-api` script was blocked mid-run due to YouTube's IP-based rate limiting. The first 25 transcripts fetched successfully; the remaining 5 (Jason Lemkin) hit a 429 error. These were resolved by manually collecting and pasting the transcripts directly into the repository files.

### Key Learnings (Setup)

* How to use Claude Code as a primary development tool for research and automation tasks.
* How to structure a research repository for systematic content collection.
* How to handle API rate limits gracefully — script-based collection with manual fallback for blocked requests.

---

## Status

- [x] Phase 1: Tool setup and environment configuration
- [x] Phase 2: Expert selection and source documentation
- [x] Phase 3: Content collection (YouTube transcripts + LinkedIn posts)
- [x] Phase 4: Cross-expert synthesis
- [ ] Phase 5: Playbook development (pending)
