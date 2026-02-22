# Recommended Folder Structure

This guide provides a recommended folder structure for your Obsidian vault when using the Claude Code Second Brain system. This structure is optimized for knowledge work with a venture/investment focus.

## Core Philosophy

The folder structure should support:
1. **Clear stages** in the knowledge refinement pipeline
2. **Easy navigation** between raw inputs and refined outputs
3. **Flexibility** to adapt to your workflow
4. **Scalability** as your vault grows

## Recommended Structure

```
your-vault/
├── .claude/                          # Claude Code configuration
│   ├── agents/                       # Sub-agent definitions
│   ├── commands/                     # Slash commands
│   └── settings.local.json          # Permissions & MCP config
│
├── .obsidian/                        # Obsidian settings (standard)
│
├── CLAUDE.md                         # System instructions
├── knowledge-base-analysis.md       # KB structure report (auto-generated)
│
├── 00-Inbox/                         # Capture & staging
│
├── 01-Sources/                       # Source material
│   ├── Books/                       # Book notes
│   ├── Clippings/                   # Web clippings
│   ├── Demo/                        # Demo/sample content
│   └── Research/                    # Research papers, external analysis
│
├── 02-Thinking/                      # Your insights and analysis (the core)
│   ├── Notes/                       # Atomic permanent notes
│   ├── Investment Memos/            # Public market stock analyses
│   └── Portfolio Memos/             # Venture portfolio company memos
│
├── 03-Reference/                     # Reference material
│   ├── Companies/                   # Company profiles
│   ├── People/                      # People profiles
│   └── Meetings/                    # Meeting notes
│
├── 04-Output/                        # Published/synthesized work
│   ├── Articles/                    # Long-form writing
│   └── Draft Posts/                 # Social media drafts (plain text)
│
├── 05-System/                        # Workflow & system
│   ├── Changelogs/                  # Discovery session logs
│   ├── Dashboards/                  # Overview dashboards
│   ├── Templates/                   # Note templates
│   └── Projects/                    # Active project tracking
│
└── 06-Tasks/                         # Task tracking
```

## Folder Purposes

### .claude/
**Purpose**: Claude Code configuration and agent definitions

**Contents**:
- `agents/`: Specialized sub-agent prompt files
- `commands/`: Slash command definitions
- `settings.local.json`: Permissions and MCP configuration

**Notes**:
- Keep in git if sharing setup
- Add `settings.local.json` to `.gitignore` for privacy

### 00-Inbox/
**Purpose**: Capture ideas quickly without friction

**Workflow**:
1. Capture quickly
2. Process into thinking notes regularly
3. Delete or archive after processing

### 01-Sources/
**Purpose**: Reference material and source notes

**Contents**:
- **Books/**: Comprehensive book notes with key quotes
- **Clippings/**: Web clippings and saved articles
- **Demo/**: Demo or sample content
- **Research/**: Research papers, external analysis, document insights

**Best Practices**:
- One file per source
- Include metadata (author, date, URL)
- Link to thinking notes that reference it
- Use frontmatter for structured metadata

**Example Source Note**:
```markdown
---
type: book
author: Author Name
year: 2024
tags: [topic1, topic2]
---

# Book Title

## Key Arguments
- Main point 1
- Main point 2

## Thinking Notes Created
- [[Note 1]] - About topic X
- [[Note 2]] - About topic Y
```

### 02-Thinking/
**Purpose**: Your insights and analysis - the core of the knowledge graph

**Contents**:
- **Notes/**: Atomic permanent notes - single-idea insights in your own words
- **Investment Memos/**: Public market stock analyses with consistent structure
- **Portfolio Memos/**: Venture portfolio company memos

**Best Practices**:
- **One idea per note**: Keep atomic and focused
- **Clear titles**: State the insight explicitly
- **Your own words**: Paraphrase, don't copy
- **Source attribution**: Link back to source notes
- **Date stamp**: Include creation date in frontmatter
- **Average length**: 50-300 words ideal

**Example Thinking Note**:
```markdown
---
created: 2025-10-27
tags: [neuroscience, motivation]
---

# Dopamine drives motivation, not pleasure

Dopamine is responsible for the *desire* to act, not the enjoyment of the action itself. This explains why we can be motivated to do things we don't enjoy.

The "wanting" (dopamine) system is separate from the "liking" (opioid) system in the brain.

**Source**: [[Dopamine Nation - Book Notes]]

**Related**:
- [[Pleasure and pain balance in the brain]]
- [[Reward prediction error]]
- [[Motivation vs. willpower]]
```

### 03-Reference/
**Purpose**: Reference material and navigation hubs

**Contents**:
- **Companies/**: Company profiles (portfolio companies, public market companies)
- **People/**: People profiles (team, founders, contacts)
- **Meetings/**: Meeting notes with dates and action items

**Best Practices**:
- Create company profiles when you have substantial information
- Link people to their companies
- Add brief context for each reference
- Update regularly as information changes

### 04-Output/
**Purpose**: Finished work and synthesis

**Contents**:
- **Articles/**: Long-form published pieces (each article in its own subfolder)
- **Draft Posts/**: Social media drafts in plain text (no Markdown - platforms don't render it)

**Best Practices**:
- Link back to thinking notes used
- Include publication date and status
- Track revisions in git
- Archive outdated versions

### 05-System/
**Purpose**: Workflow documentation and system operations

**Contents**:
- **Changelogs/**: Discovery session logs from agents
- **Dashboards/**: Overview dashboards (portfolio, holdings, etc.)
- **Templates/**: Note templates for consistency
- **Projects/**: Active project tracking and research questions

**Changelog Structure**:
```
Changelogs/
├── CHANGELOG - Auto-Discovery Sessions 2025-10-27.md
├── CHANGELOG - Connection Discovery 2025-10-26.md
└── CHANGELOG - Vault Management 2025-10-25.md
```

### 06-Tasks/
**Purpose**: Task tracking and to-do management

**Contents**:
- Task notes with inline Dataview fields
- Uses `[prio:: N] [due:: YYYY-MM-DD] [completed:: YYYY-MM-DD]`

## Information Flow

The recommended structure supports this knowledge pipeline:

```
CAPTURE → PROCESS → ORGANIZE → SYNTHESIZE → CREATE

Inbox/     Sources/      Thinking/     Reference/    Output/
          ↓             ↓             ↓             ↓
Quick → Source Notes → Thinking   → Reference  → Articles
Captures              Notes         Profiles     Insights
                      Memos         Meetings     Frameworks
```

## Customization Guidelines

### Adapt to Your Needs

This structure is a starting point. Customize based on:

1. **Volume**: More subdirectories if you have 1000+ notes
2. **Workflow**: Adjust stages to match your process
3. **Domain**: Add specialized folders for your field
4. **Team**: Consider shared vs. personal folders

### Principles to Maintain

Whatever structure you choose, maintain:

1. **Clear stages**: Distinguish raw inputs from refined outputs
2. **Atomic thinking notes**: Keep core insights separate
3. **Navigation aids**: Reference notes and dashboards for finding notes
4. **Evolution tracking**: Changelogs or similar
5. **Source attribution**: Link notes back to origins

## Migration Strategy

### From Existing Vault

1. **Don't reorganize everything at once**
2. **Start with new notes** in the new structure
3. **Gradually move frequently accessed notes**
4. **Use aliases for old paths** during transition
5. **Update links with search-replace** carefully

### From Other Systems

- **Roam/Logseq**: Export to markdown, then organize by type
- **Notion**: Export pages, create thinking notes from key insights
- **Evernote**: Export notes, use insight-extractor to process
- **OneNote**: Manual migration, extract atomic notes

## Maintenance

### Regular Tasks

**Daily**: Empty 00-Inbox/ into thinking notes

**Weekly**:
- Review new thinking notes
- Update relevant reference notes
- Run `/find-connections` on recent notes

**Monthly**:
- Run auto-discovery agent
- Review changelogs
- Clean up outdated temporary notes
- Update dashboards

**Quarterly**:
- Run `/analyze-kb` for structural analysis
- Review and refine folder structure
- Archive completed projects
- Evaluate what's working

## Examples

See `EXAMPLES.md` for:
- Sample notes in each folder
- Example MOC structures
- Changelog templates
- Information flow examples

## Next Steps

1. Create the basic folder structure
2. Configure `.claude/settings.local.json` with your paths
3. Start capturing in 00-Inbox/
4. Process into 02-Thinking/ regularly
5. Create reference notes when themes emerge
6. Use agents to discover connections

---

Remember: The structure serves the workflow, not the other way around. Start simple and evolve as your needs become clear.
