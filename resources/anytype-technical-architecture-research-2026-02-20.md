# Anytype Technical Architecture - Research Report

**Date**: 2026-02-20
**Prepared by**: Research Specialist Agent
**Research Session**: 2026-02-20 17:43:05 CET

---

## Executive Summary

Anytype is built on a custom peer-to-peer sync protocol (any-sync) using Conflict-free Replicated Data Types (CRDTs) stored as encrypted Directed Acyclic Graphs (DAGs). The internal data model is object-relational rather than a true graph database - objects are SmartBlocks with typed properties, stored locally in a combination of BadgerDB (key-value), Tantivy (full-text search), and a flat file store for binary blobs [1][2][3]. The sync layer borrows IPLD data structures from the IPFS ecosystem but uses entirely custom networking, not IPFS itself [4].

The architecture's key engineering bets are: (1) local-first with full offline capability, (2) end-to-end encryption where even backup nodes see only ciphertext, and (3) CRDT-based conflict resolution that eliminates the need for a central authority. The trade-off is real: search indexes must remain unencrypted on disk to function, there is no native SQL or graph query language, Sets are dynamic views rather than stored collections, and performance degrades measurably above ~3,000 objects due to DAG traversal and history retention [5][6].

For programmatic access, Anytype exposes a gRPC API (port 31010), gRPC-Web (31011), and an HTTP REST API (31012) through the anytype-cli headless server. Self-hosting requires MongoDB, Redis, and S3-compatible storage, with 4 distinct node types to run [7][8].

---

## Research Scope

- **Objective**: Understand Anytype's technical architecture from an engineering perspective
- **Key Questions**: 10 specific technical areas from data storage to performance
- **Methodology**: Primary source review (GitHub repos, official tech docs, HN threads, community forums, developer discussions)
- **Sources Consulted**: 20+ sources including source code repositories, official documentation, developer statements, and community technical discussions

---

## Key Findings

### Finding 1: The Storage Stack Is Multi-Layer, Not a Graph Database

Anytype does NOT use a graph database. The internal storage is a composite of three layers [1][3]:

**Layer 1 - CRDT Change Log (DAG)**
Each object's entire history is stored as an encrypted DAG. Every change is a node in this DAG, cryptographically signed by the device that made it. The DAG is the source of truth and enables CRDT merge operations. This is stored using IPLD data structures (borrowed from the IPFS ecosystem) but backed by BadgerDB, a fast key-value store written in Go.

**Layer 2 - Object Store (Materialized View)**
The current state of each object is materialized from its DAG and stored as a denormalized key-value snapshot. This is what the application queries for normal reads. Object details (properties/relations) live here as key-value pairs. This uses BadgerDB via the `anytypeio/go-ds-badger3` datastore adapter [9].

**Layer 3 - Full-Text Search Index (Tantivy)**
Anytype built Go bindings to Tantivy, a Rust-based full-text search engine (Lucene-equivalent). When objects are created or modified, their decrypted content is indexed into Tantivy locally. This index is NOT encrypted [6][10]. Anytype explicitly acknowledges this: "We have a prerequisite that the user's machine is non-compromised and trusted."

**Binary File Storage**
Files are stored in a `flatfs` directory as encrypted fragments. For sync purposes, Anytype uses IPFS without libp2p for file transfer (for Filecoin/Arweave compatibility), but with their own block retrieval service using gRPC rather than bitswap [4].

**Implication**: "Graph view" in the Anytype UI is a visualization layer, not a query engine against a graph database. There is no Cypher, SPARQL, or Gremlin. Relationship traversal happens at the application layer by following object-type references.

---

### Finding 2: The Object Model - SmartBlocks, Types, Relations, Sets

**Objects as SmartBlocks**
Every piece of data in Anytype is an Object, internally called a SmartBlock [1]. A SmartBlock contains:
- `Blocks map` - content elements (text, files, layouts, dataviews, tables)
- `Details` - key-value metadata (the relations/properties)
- `Relation Links` - references to other objects
- `Object Types` - type declarations

**Types**
Types define the schema for objects. They are first-class objects themselves, defined in JSON and code-generated into Go (`types.gen.go`). Three categories exist [1]:
- System Types - built-in with special business logic (Page, Note, Task, etc.)
- Internal Types - non-user-creatable (used by the system)
- User Types - custom types created by users

Each type specifies which relations are relevant and which layouts are available. Types map directly to a visual layout (document, list, grid, etc.).

**Relations (Properties)**
Relations are typed attribute definitions that can be attached to objects. They are NOT relationships between objects in the graph-theory sense - they are closer to typed columns in a relational schema. Relation formats [2][11]:
- Text, Number, Date
- Select (single), Multi-select
- Checkbox
- URL, Email, Phone
- File & Media
- Object (reference to another object - this is the closest to a graph edge)

The critical distinction from Obsidian's wiki-links: an `Object` type relation has a declared type signature. You can say "Task.assignee must be a Person object." Obsidian wiki-links are untyped - `[[Person Name]]` carries no semantic schema. Anytype's Object relations carry ontological meaning and can be queried through Sets.

**Sets**
Sets are NOT stored collections. A Set is a dynamic query - it scans all objects in the space matching a given Type or Relation value, then filters and sorts the results [12]. This is closer to a SQL `SELECT WHERE` than a folder. The implication: Sets are computed at query time, which is why they get slower as object count grows. There is no pre-built index specifically for Set queries; they traverse the object store on each open.

**Collections**
Collections (added later) are stored ordered lists of objects, unlike Sets. They are the equivalent of a manual playlist vs. a smart playlist.

---

### Finding 3: The any-sync Protocol - CRDT Over DAG

The any-sync protocol is the core technical innovation [3][13]. Key mechanics:

**Data Structure**
Each "Space" (workspace) is an encrypted DAG. Each Object within a Space is its own sub-DAG of changes. Every change is:
1. Serialized to bytes (Protocol Buffers)
2. Signed cryptographically by the device's private key
3. Added as a new leaf node in the object's DAG
4. Assigned a content-based identifier derived from the hash of its content + parent references

**CRDT Semantics**
The CRDT is state-based (convergent). When two devices each make changes while offline, they each produce their own DAG branches. On reconnect, the protocol merges the branches deterministically. The CRDT rules ensure that regardless of merge order, the final state is the same. Anytype uses the concept of "multiple heads" when a DAG branches - the merge process resolves multiple heads back to a single tip [14].

**Transport**
The any-sync protocol uses:
- QUIC as the transport (UDP, low-latency, connection multiplexing)
- DRPC (a lighter-weight alternative to gRPC) for the any-sync protocol itself
- Standard gRPC for the client-facing API in anytype-heart

**Node Architecture**
Four node types form the server-side infrastructure [3][8]:
1. **Sync Nodes** - Store Spaces and object DAGs, handle client sync
2. **File Nodes** - Handle file storage separately from metadata
3. **Consensus Nodes** - Monitor ACL (Access Control List) changes
4. **Coordinator Nodes** - Manage network configuration and peer discovery

**Peer Discovery**
Local peers discovered via mDNS. Remote nodes discovered via the coordinator. Anytype notes: "because we know exactly who these peers are we don't need any complicated discovery mechanism." This is fundamentally different from IPFS's DHT-based discovery.

---

### Finding 4: Content Addressing - IPLD Borrowed, Not IPFS Deployed

Anytype's use of "content addressing" is frequently misrepresented [4][14]:

**What They Use**
IPLD (InterPlanetary Linked Data) as a data model specification. IPLD defines how to represent hash-linked data structures. It is the schema layer of IPFS - think of it like Protocol Buffers or JSON-LD, not a network protocol.

**What They Don't Use**
- IPFS's DHT (distributed hash table) for peer discovery
- bitswap (IPFS's block exchange protocol)
- libp2p (IPFS's networking stack) for object sync (they do use IPFS without libp2p for file storage only)

**Why They Diverged**
The core problem: IPFS's Content Identifiers (CIDs) change with every modification to a document. You cannot have stable object links if the ID changes every edit. Anytype needs stable identifiers to maintain relations between objects across edits. Their solution: use IPLD's data model (DAG structure, content hashing for change nodes) but assign a separate stable UUID as the canonical object identifier. The content-addressed change nodes are internal to the DAG; the object's stable ID is separate.

**Practical Implication**
Your data is content-addressed at the change-log level (each change is verifiable by its hash) but your objects have stable human-meaningful IDs. This is the right engineering call - pure CID-based addressing would break all your links every time you edited a note.

---

### Finding 5: Encryption Architecture - Two-Layer with an Important Gap

**Encryption Scheme** [15]
- Algorithm: AES in CFB (Cipher Feedback) mode
- Two-layer structure per object's change history:
  - Layer 1: Groups changes within objects (shared with backup nodes)
  - Layer 2: Encrypts actual content (never shared with backup nodes)

**What This Means for Backup Nodes**
Backup nodes receive Layer 1 keys only. They can:
- Group changes by object
- Route sync to the right devices
- Store encrypted blobs

They cannot:
- Read content
- See relation values
- Access filenames or metadata

**The Unencrypted Gap**
The Tantivy full-text search index on local disk is NOT encrypted. This is a deliberate design choice - searchable encryption is computationally expensive and would eliminate full-text search practicality. The threat model assumes the local device is trusted. An attacker with filesystem access can read all indexed content [6].

**Key Derivation**
The mnemonic phrase follows BIP-39 standard. The documentation does not fully detail the key derivation path from BIP-39 mnemonic to the AES keys used for content encryption - this detail lives in the source code rather than public documentation.

**No Published Security Audit**
No external security audit of the encryption implementation was found in any public source as of February 2026.

---

### Finding 6: API and Programmatic Access

Anytype provides three access mechanisms [7][16]:

**HTTP REST API (Port 31012)**
Available when running anytype-cli (headless server). Uses bearer token authentication with versioned headers (`Anytype-Version: 2025-11-08`). Exposes resource-based endpoints for spaces, objects, and relations. The full API reference lives at developers.anytype.io.

**gRPC API (Port 31010)**
Standard gRPC protocol. This is the native interface that all Anytype clients use to communicate with the anytype-heart middleware. Protocol Buffer definitions live in `anytype-heart/pb/`. This is the most complete access method - the client app itself uses nothing else.

**gRPC-Web (Port 31011)**
WebSocket-based gRPC for browser-compatible access.

**Bot Account Model**
External access uses a "bot account" - a separate identity from the human user. Created via `anytype auth create`. Bot accounts only access spaces they explicitly join. API keys can be revoked from the desktop app without revoking the account.

**Limitations**
- All endpoints bind to 127.0.0.1 by default. Remote access requires explicit configuration.
- No direct database query capability (no SQL, no Cypher)
- No official webhook/event streaming for external consumers
- API is effectively a read/write wrapper around the SmartBlock model, not a general graph query interface

**Tantivy Full-Text Search**
Anytype built `anyproto/tantivy-go` - Go bindings to the Rust Tantivy engine [10]. This is compiled with CGO and linked statically. It provides: custom query building, thread-safe operations, cross-platform support (including iOS, Android, ARM64). This is why the CLI has a CGO compilation requirement.

---

### Finding 7: Self-Hosting Infrastructure Requirements

Self-hosting any-sync requires running 4 components [8][17]:

| Component | Purpose | Backend Dependency |
|---|---|---|
| any-sync-node | Sync + object storage | MongoDB |
| any-sync-filenode | File storage | Redis + S3-compatible storage |
| any-sync-consensusnode | ACL change monitoring | MongoDB |
| any-sync-coordinator | Network config + discovery | MongoDB |

**Database Requirements**
- MongoDB in replica set mode (even single-node deployments must run as a replica set)
- Redis for the file node
- S3-compatible storage: AWS S3, MinIO, DigitalOcean Spaces, Cloudflare R2, Backblaze B2

**Network Requirements**
- TCP 33010 (DRPC protocol)
- UDP 33020 (QUIC protocol)
- External IP must be configured or clients show "Syncing" indefinitely

**Simplified Deployment: any-sync-bundle**
The community project `grishy/any-sync-bundle` consolidates all 4 components into a single container with embedded MongoDB and Redis [8]. Runs on a Raspberry Pi. Suitable for personal/small team use.

**Important Limitation**
Self-hosting is a complete network switch. You cannot mix devices between the Anytype-hosted network and a self-hosted network with the same identity. Anytype "strongly recommend[s] using dedicated identities for each network."

---

### Finding 8: Type System vs. Obsidian Frontmatter

This is a meaningful architectural difference, not just a feature difference.

**Obsidian's Model**
YAML frontmatter is a convention over plain text files. The type system is implicit and optional. Dataview plugin interprets frontmatter as queryable properties, but this is a third-party read of unstructured text. Two notes with `status: active` and `status: Active` are different values - there's no enforcement. Wiki-links are untyped text pointers.

**Anytype's Model**
Relations are first-class typed schema objects, defined globally across the space [2][11]. When you create a `Status` relation, it has:
- A format (Select, Text, Date, etc.)
- A globally unique key
- A set of valid options (for Select format)
- An owner (the space, not just one object type)

The same `Status` relation can be used across multiple Types (Tasks, Projects, Notes), and all share the same option values. This is schema reuse. Obsidian has no equivalent - each note's frontmatter is independent.

**Object Relations as Typed Graph Edges**
Anytype's `Object` format relation is the most powerful difference. It creates a typed directed edge in the knowledge graph. You can declare "Task.project must be a Project object." The link carries semantic meaning and can be queried via Sets. Obsidian's `[[wiki-link]]` is untyped - any note can link to any note, and nothing enforces that a link is to the "right" type of note.

**Query Capability**
Anytype Sets filter by Type + Relation values, which is a structured query. You can create a Set of "Tasks where Status = In Progress and Assignee = [[Me]]." Obsidian requires the Dataview plugin to get similar capability, and even then it's parsing frontmatter text, not querying a type system.

**The Trade-off**
Anytype's type system requires upfront schema design. The freedom of Obsidian's markdown-everything is also its weakness - no schema enforcement. Anytype's schema provides structure at the cost of rigidity and migration complexity.

---

### Finding 9: Performance Characteristics

**Documented Performance Data** [5]

| Object Count | Observed Behavior |
|---|---|
| ~1,000 objects | Set loading: 2-3 second wait times |
| ~3,200 objects | Set loading: 1.4 to 3.5+ seconds |
| Large sets with images | Significantly longer due to cover image rendering |
| Export with large data | Exponential scaling reported (1hr → 3hr with 20% data growth) |

**Root Causes Identified**
1. **Full DAG history retention** - Anytype stores every change in the DAG. The object store grows as history accumulates, and there is no pruning or compaction. Deleted Types persist in selection menus.
2. **Set queries are full scans** - Opening a Set triggers a filter+sort pass over all objects matching the base type. No pre-built indexes for Set queries.
3. **Electron overhead** - The desktop client is Electron-based. The Hacker News thread noted measurably higher memory usage and slower load times vs. native alternatives [18].
4. **Sync architecture bottleneck** - Developer acknowledged in 2022 that sync "isn't exactly known for being fast" and identified "redundant data structures" in the sync layer. Infrastructure redesign was promised before performance benchmarking.
5. **Search index** - Tantivy is fast for FTS queries. The bottleneck is the object store layer, not search.

**Mobile vs. Desktop**
The iOS client was noted as significantly more performant than the Electron desktop app. This suggests much of the desktop performance issue is Electron, not the anytype-heart Go backend.

**Scale Ceiling**
No official benchmark for 10,000+ objects exists in public documentation. Community reports suggest noticeable degradation begins around 3,000+ objects. There is no architectural ceiling (the CRDT DAG can grow indefinitely) but UX becomes painful well before theoretical limits.

---

## Technical Architecture Summary Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ANYTYPE CLIENT (Electron)                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              anytype-heart (Go middleware)            │   │
│  │                                                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │   │
│  │  │  gRPC    │  │  Object  │  │  any-sync CRDT     │  │   │
│  │  │  Server  │  │  Store   │  │  Engine            │  │   │
│  │  │  :31010  │  │(BadgerDB)│  │  (DAG + Merge)     │  │   │
│  │  └──────────┘  └──────────┘  └────────────────────┘  │   │
│  │                                                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │   │
│  │  │  Tantivy │  │  FlatFS  │  │  IPLD Data         │  │   │
│  │  │  FTS     │  │  (Files) │  │  Structures        │  │   │
│  │  │(Unencr.) │  │(Encr.)   │  │  (Change Nodes)    │  │   │
│  │  └──────────┘  └──────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
            │                              │
    mDNS (local)              QUIC/DRPC (remote)
            │                              │
            ▼                              ▼
   ┌─────────────────┐        ┌─────────────────────────────┐
   │  Local Peer     │        │   any-sync Node Network     │
   │  (same network) │        │                             │
   └─────────────────┘        │  ┌───────┐  ┌───────────┐  │
                               │  │ Sync  │  │  File     │  │
                               │  │ Node  │  │  Node     │  │
                               │  │(Mongo)│  │(Redis+S3) │  │
                               │  └───────┘  └───────────┘  │
                               │  ┌─────────────────────┐    │
                               │  │ Consensus + Coord.  │    │
                               │  │ (MongoDB)           │    │
                               │  └─────────────────────┘    │
                               └─────────────────────────────┘
```

---

## Engineering Trade-offs Assessment

### Strengths

**CRDT for conflict resolution** - Correct choice for local-first. The alternative (operational transforms, used by Google Docs) requires a central server to sequence operations. CRDTs enable true peer-to-peer merge without a coordinator.

**Typed relations** - Significantly more expressive than plain wiki-links. Enables structured querying that Obsidian cannot do natively.

**Two-layer encryption** - Smart design: backup nodes provide sync infrastructure without data access. This is architecturally sound for a privacy-first product.

**Tantivy for FTS** - Better than the Go alternatives (Bleve). Cross-platform, fast, battle-tested.

**Stable IDs over CIDs** - Correct call. Pure content-addressing (full IPFS) would break all inter-object links on every edit. The hybrid approach preserves link stability.

### Weaknesses

**No graph query language** - "Graph" in Anytype's marketing means a visualization, not a queryable graph DB. You cannot express "find all objects connected to X within 2 hops" without multiple application-level queries.

**Full history retention** - No WAL compaction or history pruning. Disk usage grows unboundedly. Deleted objects leave metadata artifacts. This is a fundamental CRDT trade-off that Anytype has not resolved.

**Unencrypted FTS index** - Known limitation, but it means the local machine's security posture determines data confidentiality. For a product with strong E2EE messaging, this is a significant gap.

**Set performance degrades with scale** - Full-scan query model without dedicated indexes for relation-based queries. Engineering acknowledged this but architectural resolution has not been publicly shipped.

**Electron client** - Performance overhead is Electron's original sin. The Go backend (anytype-heart) is fast; the UI wrapper is not.

**No SQL/structured query** - The API exposes the object model, not a query interface. Complex data extraction requires iterating all objects and filtering client-side.

**Self-hosting complexity** - Requires MongoDB (in replica set mode), Redis, S3 storage, and 4 service types. This is substantial infrastructure for a personal knowledge tool.

---

## Data Points and Statistics

- anytype-heart codebase: 99.7% Go, 19,577 commits on develop branch [1]
- anytype-cli: Tantivy-go v1.0.4 linked via CGO [7]
- API port range: 31010-31012 (CLI) vs. 31007-31009 (desktop app) [7]
- Self-hosting ports: TCP 33010 (DRPC), UDP 33020 (QUIC) [8]
- Encryption: AES-CFB, two-layer per object [15]
- Key standard: BIP-39 mnemonic for seed phrase [15]
- Set loading degradation: observed at ~1,000 objects (2-3s), ~3,200 objects (up to 3.5s) [5]
- Tantivy: Rust-based, faster than Go's Bleve, supports ARM64/x86/iOS/Android [10]
- CRDT type: state-based (convergent), not operation-based [14]
- File node dependencies: Redis + S3-compatible storage [8]
- Sync nodes: MongoDB backend [8]

---

## Sources

[1] Object Types and Relations - anyproto/anytype-heart - DeepWiki - https://deepwiki.com/anyproto/anytype-heart/3.1-object-types-and-relations

[2] Relations System - anyproto/anytype-swift - DeepWiki - https://deepwiki.com/anyproto/anytype-swift/5.2-relations-system

[3] any-sync Protocol - GitHub - anyproto/any-sync - https://github.com/anyproto/any-sync

[4] Anytype IPFS Discussion - GitHub anyproto Discussions #15 - https://github.com/orgs/anyproto/discussions/15

[5] Anytype Scalability Discussion - Anytype Community Forum - https://community.anytype.io/t/how-will-anytype-scale-with-tens-of-thousands-of-objects-questions-about-anytypes-scalability-and-performance/4497

[6] Anytype Search Index Thread - Anytype Community Forum - https://community.anytype.io/t/the-search-index/7188

[7] Anytype CLI Technical Architecture - DeepWiki - anyproto/anytype-cli - https://deepwiki.com/anyproto/anytype-cli

[8] any-sync-bundle Self-Hosting - GitHub - grishy/any-sync-bundle - https://github.com/grishy/any-sync-bundle

[9] go-ds-badger3 Datastore - GitHub - anytypeio/go-ds-badger3 - https://github.com/anytypeio/go-ds-badger3

[10] tantivy-go Go Bindings - GitHub - anyproto/tantivy-go - https://github.com/anyproto/tantivy-go

[11] Relations Documentation - Anytype Docs - https://doc.anytype.io/anytype-docs/basics/relations

[12] Sets and Collections Documentation - Anytype Community Discussion - https://community.anytype.io/t/a-clarification-on-how-relations-work-with-types-and-sets/9644

[13] any-sync Protocol Overview - Anytype Tech Docs - https://tech.anytype.io/any-sync/overview

[14] Anytype IPLD Technical Discussion - Hacker News - https://news.ycombinator.com/item?id=38798196

[15] Privacy & Encryption - Anytype Docs - https://doc.anytype.io/anytype-docs/advanced/data-and-security/how-we-keep-your-data-safe

[16] Anytype Developer API - https://developers.anytype.io/docs/examples/featured/cli/

[17] Self-Hosted Documentation - Anytype Docs - https://doc.anytype.io/anytype-docs/advanced/data-and-security/self-hosting/self-hosted

[18] Anytype Show HN Thread - Hacker News - https://news.ycombinator.com/item?id=38794733

---

## Research Notes

**Areas of remaining uncertainty:**
- Exact BIP-39 to AES key derivation path (not publicly documented, lives in source)
- Whether any Set query indexes have been added since 2022 community complaints (no public announcement found)
- Full API endpoint catalog (developers.anytype.io was partially accessible)
- Whether any external security audit has been conducted (none found in any public source)

**Recommended follow-up:**
- Read `anytype-heart/core/` source directly for storage layer implementation details
- Track GitHub issues for any-sync for performance improvements
- Review `pb/` directory for full gRPC API surface area (Protocol Buffer definitions)
- Check `anyproto/anytype-test` for integration test patterns that reveal API capabilities
