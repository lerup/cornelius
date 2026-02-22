# JARVIS Presentation Deck v1

> 12 slides | ~10 min (follows 20 min live demo)
> Design system: Inflection CI V.1.1
> Target: Figma implementation

---

## Design System Reference

| Element | Spec |
|---|---|
| **Background** | #000000 (primary), #808080 (secondary panels) |
| **Text primary** | #FFFFFF |
| **Text secondary** | #808080 |
| **Accent** | #B3BCB5 (Verdant Gaze) - highlights, active states |
| **Secondary accent** | #B4BACC (Azure Gaze) - data viz only |
| **Typeface** | Studio Pro |
| **Headlines** | Medium, tracking -15 |
| **Subheads** | SemiBold, tracking 0 |
| **Body** | SemiBold, tracking -20, leading +3 |
| **Layout** | Half-split (Janus duality) where appropriate |
| **Frame element** | Deconstructed symbol curves on title + close |

---

## Slide 1: Title

**Layout:** Full black. Inflection frame element (deconstructed symbol curves) framing the center content.

**Center:**
```
JARVIS
```
Studio Pro Medium, ~110pt, white, tracking -15

**Below:**
```
Institutional Intelligence for Venture Capital
```
Studio Pro SemiBold, ~24pt, #808080, tracking -20

**Bottom left:** Inflection combined mark (symbol + wordmark)

**Nothing else.**

---

## Slide 2: The Problem

**Layout:** Half-split. Left panel black, right panel #808080.

### Left Panel (white text)

**Headline:**
```
A VC's most valuable asset
is accumulated judgment.
```

**Body (3 bullets, spaced):**

```
Scale breaks memory.
14 portfolio companies. 12 public positions.
Hundreds of relationships.

Context is fragile.
It walks out the door when someone leaves.

The cost of forgetting is invisible.
You never see the connection you didn't make.
```

### Right Panel (white text on grey)

**Single large statement:**
```
Judgment lives in heads,
emails, and docs
nobody can search.
```
Studio Pro Medium, ~48pt

---

## Slide 3: What Is JARVIS

**Layout:** Full black. Three horizontal bands separated by thin #808080 lines. Active band (Individual Brain) highlighted with Verdant Gaze (#B3BCB5) left border.

### Three Layers

```
┌─────────────────────────────────────────────────────────┐
│  INDIVIDUAL BRAIN                                       │
│  What you just saw: Cornelius - the full demo           │
│  What's next: Each team member gets one                 │
├─────────────────────────────────────────────────────────┤
│  ORG BRAIN                                              │
│  What you just saw: Portfolio synergies, company updates│
│  What's next: Shared layer across the team              │
├─────────────────────────────────────────────────────────┤
│  STAKEHOLDER INTERFACE                                  │
│  What you just saw: —                                   │
│  What's next: Curated feeds for founders and LPs        │
└─────────────────────────────────────────────────────────┘
```

### Bottom text
```
Private by default, shared by intent.
```
Studio Pro SemiBold, #B3BCB5

---

## Slide 4: How It Works

**Layout:** Full black. Vertical three-layer stack diagram. Each layer is a rounded rectangle. Thin connecting lines between layers.

```
┌──────────────────────────────────────────┐
│  WORKFLOWS                               │
│  Natural language commands that trigger   │
│  complex multi-step operations            │
│  "What's new with Hanseatic?"            │
└──────────────┬───────────────────────────┘
               │
┌──────────────┴───────────────────────────┐
│  AI AGENTS                               │
│  Semantic search · Connection discovery   │
│  Insight extraction · Research synthesis  │
│  Claude as the reasoning engine           │
└──────────────┬───────────────────────────┘
               │
┌──────────────┴───────────────────────────┐
│  KNOWLEDGE GRAPH                         │
│  Obsidian · Markdown · Local-first       │
│  No vendor lock-in · 223 notes           │
│  1,300+ connections                       │
└──────────────────────────────────────────┘
```

---

## Slide 5: Architecture - First Principles

**Layout:** Full black. Top-down decomposition. Start from the highest abstraction, break down layer by layer.

**Headline:**
```
From principle to implementation
```

### Top-down breakdown (4 levels, tree structure)

```
INSTITUTIONAL INTELLIGENCE
The firm knows everything every team member knows.
No knowledge is lost. Every connection is discoverable.
          │
          ├── NETWORK OF BRAINS
          │   Every team member runs their own AI-augmented
          │   knowledge graph. The network connects them.
          │
          ├── TWO VAULTS PER PERSON
          │   Personal vault: private thinking, health, personal notes
          │   Company vault: research, portfolio, strategy, contacts
          │   Hard boundary. Separate directories. Separate indexes.
          │
          ├── SYNC VIA GIT
          │   Company vault = git repository on GitHub (private org)
          │   Each Mac Mini clones, pulls, works, commits, pushes.
          │   Full version history. Offline-capable. Audit trail.
          │
          └── AI LAYER IS LOCAL
              Claude Code runs on each Mac Mini.
              FAISS vector index is local per vault.
              No data leaves the machine unless you push to git.
              No cloud AI service sees your private vault.
```

---

## Slide 6: Architecture - Privacy & Sync

**Layout:** Half-split. Left panel: diagram. Right panel: explanation text.

### Left Panel - Network Diagram

```
 Alex's Mac Mini                  Jonatan's Mac Mini
┌───────────────────┐            ┌───────────────────┐
│ ┌───────────────┐ │            │ ┌───────────────┐ │
│ │ Personal Vault│ │  NEVER     │ │ Personal Vault│ │
│ │ (local only)  │ │  SYNCS     │ │ (local only)  │ │
│ └───────────────┘ │            │ └───────────────┘ │
│                   │            │                   │
│ ┌───────────────┐ │   git      │ ┌───────────────┐ │
│ │ Inflection    │◄├───push/───►├►│ Inflection    │ │
│ │ Vault (shared)│ │   pull     │ │ Vault (shared)│ │
│ └───────────────┘ │            │ └───────────────┘ │
│                   │            │                   │
│ Claude Code       │            │ Claude Code       │
│ FAISS Index x2    │            │ FAISS Index x2    │
└───────────────────┘            └───────────────────┘
         │                                │
         └──────── GitHub (Private) ──────┘
                  inflection-brain.git
```

### Right Panel - Privacy Rules

```
What stays private:
Personal vault never leaves your machine.
No symlinks, no shared access, no exceptions.

What syncs:
Company vault syncs via git.
You control what enters the company vault.
One-way valve: personal → company. Never reverse.

How AI stays contained:
Claude Code runs locally on each Mac Mini.
Vector indexes are per-vault, per-machine.
No cloud inference on private data.

How conflicts resolve:
Git handles merge conflicts on markdown.
Last editor owns the merge.
Author attribution via frontmatter on every note.
```

---

## Slide 7: What JARVIS Answers

**Layout:** Full black. Centered headline. This is the section intro slide.

**Center:**
```
One question. Full context.
```
Studio Pro Medium, ~80pt, white

**Below, smaller:**
```
Four queries that take 30 minutes today
and 30 seconds with JARVIS.
```
#808080

---

## Slide 8: Example 1 - Portfolio Intelligence

**Layout:** Half-split. Left: input (dark grey #1A1A1A panel). Right: output (black with data).

### Left Panel - The Query

```
INPUT

"I need a quick view of the portfolio.
What are our top 5 positions by NAV
and trajectory?"
```

### Right Panel - The Output

**Pie chart** (use Azure Gaze #B4BACC for segments, Verdant Gaze #B3BCB5 for top position):

```
NAV Allocation - Top 5

  Fabric         28%    ████████████████
  Ark            19%    ███████████
  Ubitium        14%    ████████
  Hedy           12%    ███████
  Tune Insight    9%    █████
  Other (9)      18%    ██████████
```

**Trajectory Table:**

| Company | NAV (€M) | Trajectory | Signal |
|---|---|---|---|
| **Fabric** | 4.2 | ▲▲ Strong up | Series A termsheet from Lux Capital at 3.2x markup. VPU tape-out on schedule. |
| **Ark** | 2.9 | ▲▲ Strong up | NATO DIANA cohort selected. 2,400 units deployed. Revenue 3x YoY. |
| **Ubitium** | 2.1 | ▲ Up | Elite CTO hired (ex-NVIDIA). First silicon Q3. $1.2M in LOIs from edge AI customers. |
| **Hedy** | 1.8 | ▲ Up | Bundeswehr pilot contract signed. Team doubled to 14. Runway 24 months. |
| **Tune Insight** | 1.4 | ● Stable | Revenue growing 40% QoQ. FHE performance breakthrough - 12x speedup. Bridge round closing. |

---

## Slide 9: Example 2 - LP Network Intelligence

**Layout:** Half-split. Left: input. Right: output.

### Left Panel - The Query

```
INPUT

"I need a list of the top 10 LPs
who can write $500K-$3M checks
and who are based in NY or Boston."
```

### Right Panel - The Output

| # | LP / Family Office | Location | Check Range | Partner Contact | Status |
|---|---|---|---|---|---|
| 1 | Serafund | New York, NY | $1M - $3M | David Wachtel | Met at EUVC Summit. Follow-up scheduled Feb 18. |
| 2 | Northstar Ventures FO | Boston, MA | $500K - $2M | Rebecca Haines | Warm intro via Lakestar. First call completed. |
| 3 | Comerica Wealth | New York, NY | $1M - $2.5M | James Okoro | LP in Outsized. Asked for intro to sovereign compute funds. |
| 4 | Tiedemann Advisors | New York, NY | $500K - $1.5M | Sarah Lindgren | Met at Slush NYC side event. Deep tech allocation expanding. |
| 5 | Kendall Capital Partners | Boston, MA | $1M - $3M | Michael Cheng | Cold outreach responded. Ex-a16z scout. Interested in EU defense. |
| 6 | Beacon Hill FO | Boston, MA | $500K - $1M | Anna Kowalski | Referred by Earlybird. Prefers co-invest rights. |
| 7 | Sievert Family Office | New York, NY | $2M - $3M | Henrik Sievert | German-American family. Infrastructure background. Second meeting done. |
| 8 | Winthrop Partners | Boston, MA | $500K - $2M | Thomas Walsh | MIT endowment adjacent. Interested in compute thesis. |
| 9 | Atlas Merchant Capital | New York, NY | $1M - $2M | Diana Proust | Allocating to emerging managers 2026. Requested data room. |
| 10 | Peregrine Ventures FO | New York, NY | $500K - $1.5M | Robert Tanaka | LP in Blueyard. Looking for complementary EU exposure. |

**Bottom note (small, grey):**
```
Sources: Mars LP CRM, meeting notes, email threads, event logs.
3 have requested data room access. 2 have existing LP relationships with our co-investors.
```

---

## Slide 10: Example 3 - Expert Network

**Layout:** Half-split. Left: input. Right: output.

### Left Panel - The Query

```
INPUT

"I am researching the electrification
of the mining industry. Who are the top 5
experts on this topic in my network?

Pick one for each: founder, policy expert,
co-investor."
```

### Right Panel - The Output

**FOUNDER**

| Name | Company | Role | Relevance |
|---|---|---|---|
| **Lars Henriksson** | Epiroc Electrification (prev. Boliden) | CEO & Founder | Built the first fully electric underground mine in Sweden. 15 years in mining electrification. Met at Nordic Innovation Summit. Connected via Radical Semiconductor deal. |

**POLICY EXPERT**

| Name | Organization | Role | Relevance |
|---|---|---|---|
| **Dr. Maria Teresa Vasconcelos** | European Commission DG GROW | Head of Unit, Raw Materials & Circular Economy | Led the Critical Raw Materials Act. Keynote speaker at our EUVC panel. Direct contact - exchanged emails on SQM and lithium supply chains. |

**CO-INVESTOR**

| Name | Fund | Role | Relevance |
|---|---|---|---|
| **Arnaud Castaignet** | Lux Capital | Partner, Climate & Industrial | Led Lux's investment in Redwood Materials and Lilac Solutions. Co-invested with us in Fabric. Active in battery/mining convergence thesis. Monthly sync calls. |

**ADDITIONAL NETWORK (unsolicited but relevant)**

| Name | Affiliation | Why flagged |
|---|---|---|
| **Prof. Kai Vuorilehto** | Aalto University, Battery Technology Lab | Author of 3 papers in our research library on mining fleet electrification economics. Connected via Hedy's CTO. |
| **Jessica Obermayer** | McKinsey, Metals & Mining Practice | Co-authored the McKinsey mining electrification report we clipped last month. Jonatan met her at a dinner in Zurich. |

---

## Slide 11: Example 4 - Competitive Landscape

**Layout:** Half-split. Left: input. Right: output (may need smaller font - dense table).

### Left Panel - The Query

```
INPUT

"I am researching a company that builds
counter-UAS technologies. I need a list of
all companies we've seen in the last 12 months
building competitive or complementary products."
```

### Right Panel - The Output

**COMPETITIVE (direct counter-UAS)**

| Company | HQ | What they build | Stage | Our notes |
|---|---|---|---|---|
| **Dedrone** | Virginia, US | RF-based drone detection + classification. Software platform for airspace security. | Growth (acq. by Axon) | Seen at Hedy board prep. Strong in detection, weak in kinetic defeat. |
| **DroneShield** | Sydney, AU | Multi-sensor detection (RF, radar, acoustic) + electronic countermeasures. | Public (ASX: DRO) | Reviewed Q3 2025. Hardware-heavy, high unit cost. NATO procurement. |
| **Sentrycs** | Tel Aviv, IL | Protocol-based detection and cyber takeover of drones. Non-kinetic defeat. | Series B | Passed. Single-vector approach fragile against autonomous drones. |

**COMPLEMENTARY (adjacent stack components)**

| Company | What they build | Complementary layer | Our connection |
|---|---|---|---|
| **Hedy** (portfolio) | Resilient mesh communications | Comms infrastructure for counter-UAS networks. Operates in contested RF environments. | Portfolio company. Direct bridge to any C-UAS investment. |
| **Echodyne** | Metamaterial electronically scanning radar (MESA) | Radar layer - compact, solid-state, drone-class detection at range. | Reviewed Nov 2025. Too late stage for us. Potential Hedy partner. |
| **Teledyne FLIR** | Infrared and thermal imaging sensors | Sensor layer - visual confirmation and tracking in low visibility. | Public company. Referenced in Ark's sensor fusion architecture. |
| **Bluehalo** | Directed energy weapons (LOCUST laser system) | Kinetic defeat layer - laser-based hard kill at short range. | Seen in defense robotics research. US-focused, no EU presence yet. |
| **Quantum Systems** | Fixed-wing VTOL reconnaissance drones | ISR layer - provides the aerial surveillance that feeds C-UAS targeting. | Met founder at Munich Security adjacent event. German company, Bundeswehr supplier. |
| **Phosphorus Cybersecurity** | IoT/OT security for connected defense systems | Cyber hardening layer - secures the network that C-UAS systems run on. | Flagged by auto-discovery. Tune Insight connection via encrypted compute. |

**Bottom summary (small, grey):**
```
3 direct competitors identified. 6 complementary stack components mapped.
1 portfolio company (Hedy) has direct integration potential.
Recommendation: evaluate the deal through the lens of our Zero Trust Compute Stack thesis.
```

---

## Slide 12: Roadmap + Close

**Layout:** Top half: timeline. Bottom half: Inflection close mark.

### Timeline (horizontal, 4 blocks)

Use Verdant Gaze (#B3BCB5) background for Q1 (current). Others in dark grey.

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Q1 2026     │  │  Q2 2026     │  │  Q3 2026     │  │  LONG TERM   │
│  ▓▓▓▓▓▓▓▓▓▓ │  │              │  │              │  │              │
│  Individual  │  │  Shared org  │  │  Stakeholder │  │  External    │
│  brains to   │  │  layer       │  │  interface   │  │  rollout     │
│  full team   │  │              │  │              │  │              │
│              │  │  Git-synced  │  │  Founder     │  │  Offer to    │
│  Mac Mini    │  │  company     │  │  briefs      │  │  portfolio   │
│  per person  │  │  vault       │  │  LP updates  │  │  companies   │
│  2 vaults    │  │  Cross-brain │  │  Curated     │  │  and beyond  │
│  each        │  │  search      │  │  feeds       │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

### Bottom Half

**Center:** Inflection symbol (large, white on black)

**Below symbol:**
```
inflection©
```

**Nothing else.**

---

## Speaker Notes (not on slides)

### Slide 7-11 transition framing:
"The demo showed you the engine. Now let me show you what the engine produces when you ask it real questions we deal with every week."

### Slide 8 (Portfolio):
"This is a 30-second portfolio review. Today this takes opening a spreadsheet, cross-referencing emails, checking our CRM. JARVIS pulls from the knowledge graph - every investor update, every board note, every piece of research - and synthesizes it into a decision-ready view."

### Slide 9 (LP Network):
"Fundraising is a relationship game. Every LP interaction lives somewhere - email, CRM, meeting notes, event badges. JARVIS surfaces the full picture: who they are, what they allocate, who introduced them, and where we left off."

### Slide 10 (Expert Network):
"When you start researching a new sector, the first question is: who do I already know? JARVIS maps your network against the research question. The unsolicited suggestions at the bottom are connections it found that I didn't ask for - but should have."

### Slide 11 (Competitive Landscape):
"Deal evaluation requires competitive context. JARVIS doesn't just search a database - it connects the new company to everything we've already seen, including our own portfolio. The recommendation at the bottom - evaluate through the Zero Trust Stack lens - comes from the same connection engine you saw in the demo."

---

## File Manifest

```
resources/jarvis-presentation/
├── JARVIS-Deck-v1.md          ← this file (content + speaker notes)
└── [figma assets to be added]
```
