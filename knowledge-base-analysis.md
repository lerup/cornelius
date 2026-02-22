# Knowledge Base Analysis

> Last updated: 2026-02-10 | 298 notes | 2,354 edges

---

## Executive Summary

The vault is a **venture-capital-oriented knowledge system** centered on Inflection's sovereign computation thesis. It operates as equal parts investment research library, portfolio management hub, and strategic thinking workspace.

**Key metrics:**

| Metric | Value |
|---|---|
| Total notes | 298 |
| Total graph edges | 2,354 |
| Explicit wiki-links | 1,220 |
| Semantic connections | 1,134 |
| Connected components | 1 (fully connected) |
| Isolated nodes | 0 |
| Average degree | 15.8 |

**Vault personality:** Thesis-driven investor with deep conviction in physical-digital infrastructure, sovereignty as organizing principle, and contrarian positioning against consensus capital.

---

## Architecture

### Design Principle

Folders carry exactly one signal: **epistemic status**. Tags carry topic. Links carry relationships. No redundancy between layers.

The numbering reflects the processing pipeline: content enters at 01 (sources), gets processed into 02 (your thinking), references 03 (entities), and exits at 04 (output). 05 and 06 are support infrastructure.

### Directory Layout

| Directory | Notes | Purpose | Type |
|---|---|---|---|
| 00-Inbox | 1 | Quick capture, unprocessed | - |
| 01-Sources/Books | 16 | External book notes | `book` |
| 01-Sources/Clippings | 32 | External articles/web content | `clipping` |
| 01-Sources/Demo | 9 | Demo/sample content | - |
| 01-Sources/Research | 51 | Extracted research insights | `research-finding` |
| 02-Thinking/Notes | 34 | Atomic insights, frameworks, theses | `note` |
| 02-Thinking/Investment Memos | 24 | Public market stock analysis | `stock-memo` |
| 02-Thinking/Portfolio Memos | 11 | VC company investment memos | `investment-memo` |
| 03-Reference/Companies | 28 | Company profiles | `company` |
| 03-Reference/People | 37 | People profiles | `person` |
| 03-Reference/Meetings | 2 | Meeting records | `meeting` |
| 04-Output/Articles | 9 | Published articles | `article` |
| 04-Output/Draft Posts | - | Social media drafts (plain text) | - |
| 05-System | 37 | Changelogs, dashboards, templates, projects | - |
| 06-Tasks | 5 | Task management | - |
| **Total** | **298** | | |

### Epistemic Layers

| Layer | Question it answers | Contents |
|---|---|---|
| **01-Sources** | What did other people write? | Books, external articles, extracted research |
| **02-Thinking** | What do I think? | Insights, frameworks, theses, investment analysis |
| **03-Reference** | What exists in the world? | Companies, people, meetings - entity records |
| **04-Output** | What did I publish? | Articles, drafts - finished artifacts for audiences |
| **05-System** | What keeps the vault running? | Changelogs, dashboards, templates, projects |
| **06-Tasks** | What needs doing? | Task boards, calendars, open/done lists |

### Content Composition

| Category | Count | Location | Examples |
|---|---|---|---|
| Public market stock memos | 24 | 02-Thinking/Investment Memos | TSMC, ASML, BYD, Apple, Cloudflare, PayPal, Pfizer, SQM, P&G, Visa, Ferrari |
| Portfolio company memos | 11 | 02-Thinking/Portfolio Memos | Ark, Fabric, Hedy, Foundational, Radical, Lodestar, Deep Earth, Ubitium, Senken, Tune Insight, Hanseatic |
| Company profiles | 28 | 03-Reference/Companies | Portfolio companies + public market companies |
| People profiles | 37 | 03-Reference/People | Team members, founders, authors, contacts |
| Strategy/thesis notes | ~10 | 02-Thinking/Notes | Inflection Thesis 2025, Strategy 2026, EUVC Panel, Physical AI |
| Research insights | 51 | 01-Sources/Research | Sovereign infrastructure, edge AI, defense robotics, electrification |
| External articles | 32 | 01-Sources/Clippings | Compute Moonshots, Mortal Computing, Production Capital, Taleb as VC |
| Book notes | 16 | 01-Sources/Books | Chip War, Pattern Breakers, Pitch Anything, Range, Material World |
| Published articles | 9 | 04-Output/Articles | Heresy, Europe's New Defense, Depth vs Breadth, Anatomy of Inflections |
| Dashboards | 6 | 05-System/Dashboards | Portfolio Overview, Public Market Holdings, Investment Dashboard |
| Project trackers | 11 | 05-System/Projects | Mars LP Funnel, Dealflow, IR, Admin, Portfolio projects |

---

## Hub Architecture

### Top 10 Hub Notes (by total degree)

| Rank | Note | Location | Degree | Role |
|---|---|---|---|---|
| 1 | **Inflection Strategy 2026** | 02-Thinking/Notes | 45 | Gravity center - links all portfolio companies and strategy |
| 2 | **Inflection Thesis 2025** | 02-Thinking/Notes | 35 | Intellectual anchor - sovereign compute framework |
| 3 | TSMC Memo | 02-Thinking/Investment Memos | 33 | Most connected stock analysis |
| 4 | BYD Memo | 02-Thinking/Investment Memos | 31 | Public market hub |
| 5 | Apple Memo | 02-Thinking/Investment Memos | 30 | Public market hub |
| 6 | Cloudflare Memo | 02-Thinking/Investment Memos | 29 | Public market hub |
| 7 | PayPal Memo | 02-Thinking/Investment Memos | 29 | Public market hub |
| 8 | Inflection Team Overview | 02-Thinking/Notes | 28 | People/operations hub |
| 9 | ASML Memo | 02-Thinking/Investment Memos | 28 | Public market hub |
| 10 | SQM Memo | 02-Thinking/Investment Memos | 27 | Public market hub |

**Pattern:** The top 2 hubs are strategy documents in 02-Thinking/Notes. Ranks 3-10 are dominated by stock memos in 02-Thinking/Investment Memos, which have high semantic connectivity due to shared analytical structure.

### Top 10 Bridge Notes (by betweenness centrality)

| Rank | Note | Location | Betweenness | Bridge Function |
|---|---|---|---|---|
| 1 | **Inflection Thesis 2025** | 02-Thinking/Notes | 0.118 | Primary bridge: connects portfolio to public markets to philosophy |
| 2 | **Inflection Strategy 2026** | 02-Thinking/Notes | 0.095 | Operations bridge: connects team, companies, and fundraising |
| 3 | **Chip War** | 01-Sources/Books | 0.069 | Cross-domain: semiconductors to geopolitics to defense |
| 4 | TSMC Memo | 02-Thinking/Investment Memos | 0.063 | Tech-finance bridge |
| 5 | Introducing Kepler | 02-Thinking/Notes | 0.057 | Research platform bridge |
| 6 | Mortal Computing | 01-Sources/Clippings | 0.054 | Compute thesis bridge: Ubitium, Fabric, novel architectures |
| 7 | Europe's New Defense | 04-Output/Articles | 0.046 | Geopolitics-portfolio bridge: Ark, Hedy, defense thesis |
| 8 | Building a Second Brain | 01-Sources/Books | 0.044 | Meta-cognitive bridge |

**Critical insight:** Inflection Thesis 2025 is both the #2 hub AND #1 bridge - the single most important note in the vault. It connects nearly every thematic cluster. It lives in 02-Thinking because it is fundamentally the user's own analytical framework.

---

## Thematic Clusters

### 1. Sovereign Computation (Core Thesis)
**Hub:** Inflection Thesis 2025 (02-Thinking) → Inflection Strategy 2026 (02-Thinking)
**Key notes:** EUVC Panel, Compute Moonshots, Mortal Computing, Anatomy of Inflections
**Portfolio mapping:**
- Scale: Fabric (crypto hardware), Ubitium (universal processor)
- Resilience: Hedy (network security), Tune Insight (data privacy), Ark (fleet control)
- Exploration: Deep Earth (subsurface), Foundational (space), Radical (stratosphere), Lodestar (ISAM)

### 2. Defense & Geopolitics
**Hub:** Europe's New Defense (04-Output/Articles)
**Key notes:** defence robotics tech, Investing in Robotics, Gen Z Rebellion
**Portfolio:** Ark (drone autonomy), Hedy (contested comms), Lodestar (orbital defense)
**Bridge to thesis:** Sovereignty requires military independence; Europe's defense awakening creates market opportunity

### 3. Public Market Value Investing
**Hub:** Investment Dashboard, Memo Index (05-System/Dashboards)
**Key notes:** 24 stock memos in 02-Thinking/Investment Memos
**Structure:** Each memo follows consistent format: business quality, financials, valuation, risks, recommendation
**Bridge:** Chip War (01-Sources/Books) connects public market semiconductor thesis to portfolio compute investments

### 4. VC Philosophy & Fund Operations
**Hub:** Heresy and the Venture Industrial Complex (04-Output/Articles)
**Key notes:** How to Avoid Becoming a VC Meme (01-Sources), Depth vs Breadth (04-Output), Pattern Breakers (01-Sources)
**Fundraising:** Mars LP Funnel, Mars Fundraising Timeline (05-System/Projects)
**Bridge to thesis:** Contrarian positioning (heresy, non-consensus) as investment edge

### 5. Reading Library & Intellectual Influences
**Hub:** Chip War (01-Sources/Books) - highest betweenness among books
**Key books:** Material World, Pattern Breakers, Pitch Anything, Range, Atomic Habits, Why Greatness Cannot Be Planned, Hard Things, Read Write Own
**Key authors:** 16+ author profiles in 03-Reference/People
**Pattern:** Reading skews toward technology history, strategic thinking, and founder psychology

### 6. Infrastructure Technology Research
**Hub:** 01-Sources/Research (51 extracted research insights)
**Key clusters:** Edge AI benchmarks, sovereign infrastructure policy, defense robotics, space economy, electrification
**Bridge:** Connects academic/research ideas to concrete portfolio investments (Fabric, Ubitium, Deep Earth, Radical)

---

## Portfolio Network Map

The portfolio company notes (03-Reference/Companies) link to investment memos (02-Thinking/Portfolio Memos) and thesis docs (02-Thinking/Notes):

```
                    Inflection Thesis 2025
                           |
                  Inflection Strategy 2026
                    /    |    |    \
              Space    Compute  Defense  Climate
              /   \    /   \     |    \      \
        Foundational  Fabric  Ubitium  Ark   Senken
             |          |              |
          Lodestar   Tune Insight    Hedy
             |                        |
          Radical ---- Deep Earth -- Hanseatic
```

**Intra-portfolio synergies identified:**
- **Zero Trust Stack:** Hedy (network) + Fabric (compute) + Tune Insight (data)
- **Earth Intelligence:** Radical (aerial sensing) + Deep Earth (subsurface AI)
- **Space Cluster:** Foundational (tracking) + Lodestar (robotics) + Radical (HAPS)
- **Edge Compute:** Ubitium (processor) + Ark (drone VCU)
- **Carbon MRV:** Senken (marketplace) + Radical (monitoring from stratosphere)

---

## Intellectual Trajectory

### Phase 1: Foundation (Early vault)
Setup, basic book notes, initial Obsidian configuration, first VC philosophy pieces

### Phase 2: Thesis Crystallization (Mid period)
Inflection Thesis 2025, Sovereign Compute framework, EUVC Panel, Heresy article, Europe's New Defense research

### Phase 3: Portfolio Buildout
11 portfolio company notes enriched with full memo content, cross-linked with thesis and each other. Public market stock analysis library built in parallel.

### Phase 4: Architecture Restructuring (Current - Feb 2026)
Vault restructured from flat PARA-inspired layout to epistemic-status-based Zettelkasten. Three-layer taxonomy: Sources (external) → Thinking (analysis) → Reference (entities) → Output (published). All notes classified with clean `type:` frontmatter. 51 research insights integrated from deep research sessions.

### Current Focus
- Fund III (Mars) fundraising: LP funnel tracking, strategy documents
- Portfolio intelligence: company memos integrated, synergies mapped
- Research publishing: Kepler platform, Defense article series
- Dual-track investing: private (sovereign compute) + public (value investing)
- Attio CRM integration planned as live MCP query layer (no vault replication)

---

## Network Health

| Metric | Value | Assessment |
|---|---|---|
| Connectivity | 1 component, 0 isolates | Excellent - fully connected graph |
| Avg degree | 15.8 | Strong - every note averages 16 connections (up from 12.2) |
| Hub concentration | Top 2 notes in 02-Thinking | Healthy - intellectual work is the center of gravity |
| Bridge diversity | Bridges span all layers | Good - Sources, Thinking, Output all serve as cross-domain bridges |
| Explicit/semantic ratio | 1,220:1,134 | 52% explicit, 48% semantic - strong intentional linking |
| Frontmatter consistency | 100% typed | Every note has a `type:` field matching its folder |

---

## Recommendations

### Completed

1. ~~**Activate folder hierarchy.**~~ **Done (Feb 2026).** Restructured from flat layout to epistemic-status taxonomy: Sources/Thinking/Reference/Output/System/Tasks. Each folder answers one question about the note's nature.

2. ~~**Create Portfolio Overview notes.**~~ **Done.** Two dashboards in 05-System/Dashboards: Inflection Portfolio Overview and Public Market Holdings.

3. ~~**Increase explicit wiki-links.**~~ **Done.** 1,220 explicit links (up from 625). Ratio flipped from 48:52 to 52:48 explicit-dominant.

4. ~~**Archive system notes.**~~ **Done.** Setup docs, security screens, config notes moved to 05-System. Projects moved to 05-System/Projects.

5. ~~**Add frontmatter to all notes.**~~ **Done.** Every note has a `type:` field matching its folder location.

### Open

6. **Extract atomic notes from book notes.** Books like Chip War, Material World, Pattern Breakers contain insights that should exist as standalone notes in 02-Thinking/Notes for better reuse and connection.

7. **Consolidate stock analysis methodology.** The 24 stock memos follow a consistent pattern. A methodology note in 02-Thinking/Notes would formalize the framework.

8. **Populate 00-Inbox workflow.** Currently 1 note. Could serve as the landing zone for quick captures before processing into 02-Thinking or 01-Sources.

9. **Integrate Attio CRM via MCP.** Planned as live query layer - Cornelius queries Attio directly for operational data (meetings, LP pipeline, company status) while vault holds analytical layer.

---

## Cognitive Fingerprint

The vault reveals a mind that:
- **Thinks in systems:** Every investment analyzed through interconnected cause-effect chains (sovereignty → compute → defense → hardware → geopolitics)
- **Values contrarian positioning:** Multiple notes on heresy, non-consensus investing, and the failure of institutional groupthink
- **Bridges abstraction levels:** Moves fluently between Shannon-Hartley theorem calculations and civilizational strategy
- **Prioritizes physical-digital intersection:** Software-only plays are notably absent; every portfolio company touches atoms
- **Reads for models, not information:** Book notes extract frameworks (Klaff's frame control, Maples' pattern breaking) rather than summaries

The vault's deepest organizing principle is **sovereignty at every layer** - individual, data, financial, technological, industrial, military, national. The Inflection thesis is not just a fund strategy but a complete worldview expressed through investment decisions.
