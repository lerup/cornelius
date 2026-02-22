# Anytype vs Obsidian for AI-Native Second Brains

> Memo - 2026-02-20 | Research synthesis from architecture analysis, community data, and API audit

---

## Bottom Line

Anytype has a structurally superior data model - typed objects, enforced schemas, real relations. But it lacks the two things that make Cornelius work: frictionless AI access and semantic intelligence. **The file is Obsidian's weakness and its superpower.** Every LLM reads markdown. No API, no auth, no running app. That accident of architecture is worth more than Anytype's type system today.

The right framing is not "which is better" but "which constraints are cheaper to work around." Obsidian's missing schema is fixable with discipline. Anytype's missing intelligence layer requires building external infrastructure that duplicates what you already have.

---

## The Core Architectural Divide

These tools embody two different theories of what a knowledge base is.

**Obsidian:** The file is the primitive. Knowledge is text connected by links. Structure is convention. The graph shows *that* notes connect.

**Anytype:** The typed object is the primitive. Knowledge is entities with enforced schemas and relational properties. The graph shows *how* objects relate.

That difference cascades into everything.

---

## What Anytype Gets Right

### 1. Real Schema Enforcement

Obsidian relies on frontmatter conventions. Nothing stops you from writing `type: compnay` instead of `type: company`. At 300 notes, inconsistency accumulates. Dataview queries break silently.

Anytype enforces schemas at the data layer. A "Company" type has defined properties (revenue, stage, location). A `create-object` call with `type_key: "company"` guarantees the object matches the schema. Invalid values are rejected.

**For Cornelius:** The 24 stock memos, 11 portfolio memos, 28 company profiles - each would have an enforced schema instead of YAML conventions. The 17 discrepancies found in the Feb 2026 audit would have been structurally impossible.

### 2. Typed Relations (Not Just Links)

`[[TSMC]]` in an Obsidian note is an untyped pointer. The graph knows there is a connection. It does not know if TSMC is a supplier, competitor, portfolio company, or casual reference.

Anytype's `objects` property format creates typed, directional relations. A "related_companies" property on an Insight type creates a semantically meaningful edge. You can distinguish "this insight references company X" from "this insight was inspired by book Y" at the data model level.

**What this enables:** "Show all Insights linked to TSMC" is a native query. In Obsidian, you grep for `[[TSMC]]` and hope the context tells you why.

### 3. Structured Properties Replace YAML Parsing

Confidence levels, epistemic status, insight types - these map to select/number properties with validation. No regex parsing of frontmatter strings. No `#hypothesis` vs `#working-hypothesis` tag drift.

### 4. No File System Overhead

No folder paths. No iCloud sync edge cases. No filename collisions. No `touch` commands after terminal moves. No IndexedDB cache corruption. Objects are addressed by stable IDs.

---

## What Anytype Gets Wrong (For This Use Case)

### 1. No Semantic Search - The Critical Gap

Cornelius's core intelligence is FAISS-powered semantic similarity. "Find notes conceptually related to sovereign compute even if they don't mention those words." Anytype has text search only. Exact keyword matching. No embeddings. No vector similarity.

You would need to build the entire Local Brain Search system externally anyway - pulling object content via API, generating embeddings, building a FAISS index. Same architecture, worse plumbing (API calls instead of local file reads).

### 2. No Graph Analytics

Hub detection, bridge identification, betweenness centrality, path-finding between notes - none of this exists. The API creates relations but cannot answer "which object has the most inbound relations" or "what connects defense robotics to sovereign compute through 3 hops." You'd need NetworkX externally, same as today, but fed from API responses instead of local files.

### 3. AI Agent Access Is Worse Today

Obsidian's accidental advantage: any LLM reads `.md` files. Claude Code reads the vault directly. Bash scripts index it. No authentication, no running app, no localhost requirement.

Anytype's MCP tools require a running desktop app on localhost:31009. No headless mode. No background agents. No scheduled jobs. Every operation goes through an API that adds latency and rate limits.

**The 37 Anytype MCP tools we have** cover full CRUD on objects, types, properties, tags, spaces, and search. The surface is complete. But batch operations (extracting 50 insights from a document) may hit rate limits. File-based operations have no such constraint.

### 4. Forced Classification Before Capture

A second brain's first principle: capture fast, organize later. Anytype requires choosing a type before creating an object. "Is this thought an Insight, a Note, a Task, or a Bookmark?" That question before every capture adds friction that compounds.

Obsidian: open a file, write, worry about structure later.

### 5. Performance Degrades at Scale

Community reports: Set loading takes 2-3 seconds at ~1,000 objects, 3.5+ seconds at ~3,200. Sets are full table scans - no pre-built indexes for relation-based filters. The CRDT architecture has no theoretical ceiling, but the query model does.

Cornelius has 298 notes. A growing vault with 1,000+ objects will feel the difference.

### 6. Long-Form Writing Friction

Anytype uses a block-based editor (Notion-style). Consistently rated worse than Obsidian's minimal markdown editor for prose. Articles, investment memos, and thesis documents - the high-value output of a second brain - are harder to write.

---

## Performance Comparison

| Operation | Obsidian + FAISS | Anytype + External Index |
|---|---|---|
| Semantic search | Sub-second (local FAISS) | Same (external FAISS), but indexing requires API pulls |
| Create a note | Write file (~1ms) | API call (~50-200ms) |
| Read a note | Read file (~1ms) | API call (~50-200ms) |
| Batch read 300 notes | `ls + cat` (~100ms) | 300 API calls or paginated list (~5-15s) |
| Full reindex | Read all files (~2s) | Pull all objects via API (~30-60s) |
| Graph analytics | NetworkX on local data (~1s) | Same, but data extraction is slower |
| Set/query execution | Dataview parses YAML (~500ms) | Anytype Set opens (~2-3s at scale) |

**The bottleneck shifts.** Obsidian's bottleneck is parsing unstructured text. Anytype's bottleneck is API latency and full-scan queries. For a 300-note vault, both are fast enough. At 1,000+, Obsidian with local files stays fast while Anytype's query model degrades.

---

## The 37 Anytype MCP Tools We Have

Full CRUD coverage across the entire object model:

| Category | Tools | Capability |
|---|---|---|
| Objects | 5 | Create, read, update, delete objects with typed properties |
| Types | 5 | Create custom types with schema definitions |
| Properties | 5 | Create typed properties (text, number, date, select, objects, etc.) |
| Tags | 5 | Manage select/multi-select tag values with colors |
| Search | 2 | Global and space-scoped full-text search with type filtering |
| Lists/Sets | 4 | Manage collections and set memberships |
| Templates | 2 | Read templates (read-only - cannot create via API) |
| Members | 2 | Read space members (read-only) |
| Spaces | 4 | Create and manage workspaces |

**What's strong:** Object/type/property CRUD. The type system is fully programmable. An agent could bootstrap the entire Cornelius schema (Insight, Company, StockMemo, etc.) via API calls.

**What's missing:** No semantic search. No graph traversal. No property-value filtering in search. No template creation. No webhook/event streaming.

---

## Migration Cost

### What Transfers

- `[[wiki-links]]` become Object references (topology preserved)
- YAML frontmatter becomes typed properties
- Hashtags become Tag values
- Markdown body text transfers as-is

### What You Lose

- All Dataview queries (must rebuild as Sets)
- All CSS snippets (task hiding, custom layouts)
- The FAISS index and all semantic connections
- Templater syntax
- DataviewJS scripts (Task Calendar, dashboards)
- Link *semantics* - even after import, all relations are untyped

### What You Must Rebuild

- Entire Local Brain Search system (re-plumbed for API instead of files)
- All 9 project trackers as Anytype Sets
- Dashboard system (different paradigm)
- Agent configurations (all agents switch from file I/O to MCP calls)
- Template system (must be built in Anytype client, not via API)

**Estimated rebuild:** Mechanical import takes minutes. Operational layer rebuild takes weeks.

---

## The Hybrid Thesis

The ideal second brain for an AI-native workflow would combine:
- Anytype's typed object model (schema enforcement, typed relations)
- Obsidian's plain-text accessibility (any LLM reads files directly)
- FAISS's semantic intelligence (vector similarity, connection discovery)

No tool delivers this combination today. **Obsidian with disciplined frontmatter is the closest practical approximation.** You can approximate typed relations with `relation_type:` YAML fields. You cannot approximate frictionless AI access in Anytype.

---

## Recommendation

**Do not migrate.**

The switching cost is high and the marginal gain is mostly in data integrity - a problem solvable with frontmatter discipline and periodic audits. The intelligence layer (FAISS, graph analytics, connection discovery) would need to be rebuilt with worse plumbing.

**What to do instead:**

1. **Tighten Obsidian's schema.** Add `relation_type:` fields to frontmatter links. Enforce with periodic Grep audits. This gets you 60% of Anytype's typed relations at 5% of the migration cost.

2. **Watch Anytype for three developments:**
   - Headless API access (no running desktop app)
   - Semantic/vector search native
   - Collections 2.0 (multi-type queries)
   When all three ship, reassess.

3. **Consider Anytype for a fresh, parallel project** - not a migration. If you start a new knowledge base (different domain, different team), Anytype's type system is genuinely better for structured data from day one. The cost is only high when migrating existing infrastructure.

4. **The real opportunity:** Build a thin abstraction layer that works with both backends. If Cornelius agents spoke to an interface (create_insight, find_connections, search_semantic) rather than directly to files or APIs, you could swap backends without rewriting agents. That architectural investment pays off regardless of which tool wins.

---

## Summary Table

| Dimension | Obsidian | Anytype | Winner |
|---|---|---|---|
| Data model | Flat files + YAML | Typed object graph | Anytype |
| Schema enforcement | Convention | Native | Anytype |
| Typed relations | No (untyped links) | Yes (property-level) | Anytype |
| AI agent access | Direct file read | API + running app | Obsidian |
| Semantic search | FAISS (local) | Text-only | Obsidian |
| Graph analytics | External (NetworkX) | None | Obsidian |
| Long-form writing | Excellent | Block-editor friction | Obsidian |
| Capture friction | Minimal | Type selection required | Obsidian |
| Data portability | Perfect (plain text) | Good (export is lossy) | Obsidian |
| Plugin ecosystem | 2,000+ mature | Nascent | Obsidian |
| Mobile parity | Weak | Strong | Anytype |
| Query stability | Fragile (no schema) | Stable (enforced) | Anytype |
| Performance at scale | Stays fast (local files) | Degrades (full scans) | Obsidian |
| Self-hosting | N/A (local files) | Complex (4 services) | Obsidian |
| MCP API completeness | File I/O (unlimited) | 37 tools (rate-limited) | Tie |

**Score: Obsidian 8, Anytype 4, Tie 1.** But the 4 where Anytype wins (schema, types, relations, query stability) are real structural advantages that will matter more as the vault grows past 1,000 notes.
