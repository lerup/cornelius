# 02-Thinking - Your Knowledge Atoms

**Purpose**: Atomic thinking notes - the core of your knowledge graph. These are YOUR insights in YOUR words.

## What Are Thinking Notes?

Thinking notes are:
- **Atomic**: One idea per note
- **Personal**: In your own words, your perspective
- **Connected**: Linked to other notes
- **Standalone**: Independently understandable
- **Timeless**: Worth revisiting years later

## Subdirectories

### Notes/
General-purpose atomic insights - the core knowledge atoms.

### Investment Memos/
Public market stock analyses. Each memo follows consistent format: business quality, financials, valuation, risks, recommendation.

### Portfolio Memos/
Venture portfolio company memos. Thesis alignment, team assessment, market positioning, financing history.

## Characteristics

### Size
- **Ideal**: 50-300 words (13 lines average)
- **Focus**: Single insight or concept
- **Detail**: Enough to understand without source

### Content
- **Clear title**: States the insight explicitly
- **Your voice**: Personal phrasing and perspective
- **Attribution**: Links back to sources
- **Connections**: Links to related notes

### Metadata
```yaml
---
created: YYYY-MM-DD
tags: [tag1, tag2, tag3]
type: permanent
---
```

## Good Thinking Note Examples

**Good titles** (state the insight):
- "Dopamine drives motivation, not pleasure"
- "Confirmation bias reinforces existing beliefs"
- "Flow requires clear immediate feedback"
- "Uncertainty itself can trigger dopamine"

**Bad titles** (too vague):
- "Chapter 3 Notes"
- "Interesting idea"
- "Dopamine" (what about it?)
- "Book summary"

## Creation Workflow

### From Source Material
1. Read and highlight
2. Create source note in `01-Sources/`
3. Extract insights - create atomic notes here
4. Link thinking notes back to source
5. Link thinking notes to each other

### From Original Thinking
1. Capture fleeting note in `00-Inbox/`
2. Develop the thought
3. Create thinking note here
4. Find related notes
5. Add connections

### From AI Extraction
1. Review note in `00-Inbox/Content Extractions/`
2. Validate accuracy and relevance
3. Edit if needed
4. Move to `02-Thinking/Notes/`
5. Run `/find-connections` to integrate

## Linking Strategy

### When to Link

**Definitely link**:
- Related concepts (similar ideas)
- Contrasting concepts (opposite views)
- Source attribution (where it came from)
- Examples (concrete instances)
- Bridge notes (connect clusters)

**Consider linking**:
- Contextual background
- Applications
- Implications
- Questions raised

### How to Link

Use `[[wikilinks]]` with context:
```markdown
**Related concepts**:
- [[Related Note]] - Brief explanation of connection
- [[Contrasting View]] - How they differ
- [[Example Instance]] - Concrete demonstration
```

## Best Practices

### Writing
- **Write for future you**: Assume you'll forget the context
- **Use your voice**: Make it personal and memorable
- **Be specific**: Vague notes are useless
- **Show, don't tell**: Include examples when helpful

### Organizing
- **Don't use deep folders**: Thinking notes stay flat within subdirectories
- **Use tags**: For loose categorization
- **Use links**: For true organization

### Maintaining
- **Update as you learn**: Permanent doesn't mean frozen
- **Add connections**: As you discover relationships
- **Refine wording**: Make clearer over time
- **Split if needed**: If note covers multiple ideas

## Discovery Commands

### Find Connections
```
/find-connections [note name]
```
Discovers hidden relationships with other notes.

### Search
```
/search-vault [topic]
```
Quick search across all notes.

### Deep Recall
```
/recall [topic]
```
3-layer semantic search with context.

## Quality Checklist

Before marking a note as complete:

- [ ] Single, clear insight
- [ ] In my own words
- [ ] Independently understandable
- [ ] Source attributed (if applicable)
- [ ] Connected to related notes
- [ ] Clear, specific title
- [ ] Metadata filled in

## Common Patterns

### Insight Types
- **Definitions**: What something is
- **Mechanisms**: How something works
- **Relationships**: How things connect
- **Principles**: Fundamental rules
- **Observations**: Patterns noticed
- **Frameworks**: Mental models

### Connection Types
- **Definitional**: Defines a concept
- **Evidential**: Supports with evidence
- **Synthesis**: Combines multiple ideas
- **Application**: Practical use
- **Analogical**: Similar in different domain
- **Contrasting**: Opposite perspective

---

**Remember**: Quality over quantity. One excellent thinking note is worth ten mediocre ones.

See `_SAMPLE - Permanent Note Template.md` for a template to get started.
