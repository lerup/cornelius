# Brain - Your Knowledge Workspace

This is your primary intellectual workspace where knowledge flows from capture to creation.

## Folder Structure

```
Brain/
├── 00-Inbox/              Capture & staging
├── 01-Sources/            Source material (books, articles, research)
│   ├── Books/
│   ├── Clippings/
│   ├── Demo/
│   └── Research/
├── 02-Thinking/           Your atomic insights and analysis (the core)
│   ├── Notes/
│   ├── Investment Memos/
│   └── Portfolio Memos/
├── 03-Reference/          Reference material (companies, people, meetings)
│   ├── Companies/
│   ├── People/
│   └── Meetings/
├── 04-Output/             Published work & synthesis
│   ├── Articles/
│   └── Draft Posts/
├── 05-System/             Workflow, templates, dashboards
│   ├── Changelogs/
│   ├── Dashboards/
│   ├── Templates/
│   └── Projects/
├── 06-Tasks/              Task tracking
├── CHANGELOG.md
└── README.md
```

## Information Flow

```
CAPTURE → PROCESS → ORGANIZE → SYNTHESIZE → CREATE

Inbox/      Sources/      Thinking/     Reference/    Output/
Quick       Book Notes    Atomic        Navigation    Articles
Captures →  Article    →  Insights   →  Hubs       →  Frameworks
            Summaries                   Company       Insights
                                        Profiles
```

## Getting Started

### 1. Capture (00-Inbox/)
- Drop quick thoughts here
- Store AI-extracted content for review
- Do not organize yet - just capture

### 2. Process (01-Sources/ → 02-Thinking/)
- Create source notes for books/articles in `01-Sources/`
- Extract atomic insights into `02-Thinking/Notes/`
- Investment analysis goes in `02-Thinking/Investment Memos/`
- Portfolio company memos go in `02-Thinking/Portfolio Memos/`
- Link thinking notes back to sources

### 3. Organize (03-Reference/)
- Company profiles in `03-Reference/Companies/`
- People profiles in `03-Reference/People/`
- Meeting notes in `03-Reference/Meetings/`

### 4. Synthesize & Create (04-Output/)
- Write articles synthesizing multiple notes
- Develop frameworks from patterns
- Draft social media posts in `04-Output/Draft Posts/`

### 5. Track (05-System/)
- Review changelogs from discovery sessions
- Use templates for consistency
- Document your workflows

### 6. Tasks (06-Tasks/)
- Track tasks and to-dos
- Inline Dataview fields for status tracking

## Key Concepts

### Atomic Notes (02-Thinking/Notes/)
- **One idea per note** - Keep focused
- **Your own words** - Rephrase, don't copy
- **Clear title** - Make insight obvious
- **Source attribution** - Link back
- **Connections** - Link to related notes

### Reference Notes (03-Reference/)
- **Navigation hubs** - Not categories
- **Company profiles** - Portfolio and public market companies
- **People profiles** - Contacts, founders, team
- **Meeting notes** - Dated records with action items

### Changelogs (05-System/Changelogs/)
- **Dated files** - One per session
- **Discovery logs** - What did agents find?
- **Pattern tracking** - Evolution over time
- **Actionable insights** - What to do next

## Best Practices

### Daily
- Empty `00-Inbox/` into permanent notes
- Process 1-2 items from inbox
- Review recent thinking notes

### Weekly
- Run `/find-connections` on new notes
- Update relevant reference notes
- Review latest changelogs
- Plan synthesis opportunities

### Monthly
- Run auto-discovery agent
- Review all changelogs
- Create/update frameworks
- Write synthesis articles

## Quick Navigation

**Looking for something?**
- `/search-vault <query>` - Quick search
- `/recall <topic>` - Deep exploration
- `/find-connections <note>` - Discover relationships

## Sample Workflows

### Processing a Book
1. Read and highlight
2. Create source note in `01-Sources/Books/`
3. Extract permanent notes to `02-Thinking/Notes/`
4. Run `/find-connections` on new notes
5. Review changelog

### Writing an Article
1. Start with a theme or question
2. Run `/find-connections <theme>`
3. Review suggested connections
4. Create outline in `04-Output/Articles/`
5. Synthesize thinking notes
6. Write article

### Weekly Discovery
1. Review notes from this week
2. Run `/find-connections` on each major note
3. Update reference notes
4. Document patterns in changelog
5. Identify synthesis opportunities

## Customization

This structure is a starting point. Adapt it:
- Add subdirectories as needed
- Create additional output folders
- Organize sources by type/topic
- Build your own workflow

## Documentation

See these files for details:
- `../FOLDER-STRUCTURE.md` - Complete organization guide
- `../EXAMPLES.md` - Sample notes and workflows
- `../CLAUDE.md` - System instructions
- `05-System/Templates/` - Note templates
