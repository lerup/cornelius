---
description: Display all tasks completed since Monday of the current week
allowed-tools: Grep, Read, Bash
---

# Weekly Done - Completed Tasks

Display all tasks completed since Monday 00:00 of the week containing today's date.

## Instructions

1. **Determine the reference Monday** using `Bash`:
   - Run: `date '+%Y-%m-%d %u'` to get today's date and day-of-week number (1=Monday, 7=Sunday)
   - Calculate the Monday at or before today. For example, if today is Wednesday (day 3), Monday was 2 days ago.
   - Use: `date -v-$(($(date '+%u') - 1))d '+%Y-%m-%d'` to get this Monday's date on macOS.
   - Store this as the cutoff date.

2. **Collect all completed tasks** - Use `Grep` to find all `- \[x\]` lines across `*.md` files in the vault at `/Users/alexanderruppert/Desktop/Claude/OBSIDIAN VAULT`. Exclude `.obsidian/` plugin files.

3. **Filter out non-actionable entries** - Exclude:
   - Template files (in `Templates/` folder)
   - Task Board entries (`Task Board.md` - these mirror tasks from other projects)
   - Large reference checklists: `Project Mac Mini Claude Setup.md` and `Project Security Screen for Claude Code Repos.md`

4. **Parse each task** extracting:
   - Task text (clean, without inline field syntax)
   - Project name (from the source filename, without `.md`)
   - Completion date (from `[completed:: YYYY-MM-DD]` field)
   - Due date (from `[due:: YYYY-MM-DD]` field, if present)

5. **Filter by date**:
   - Include tasks where `[completed:: YYYY-MM-DD]` date is >= the reference Monday
   - Tasks with `[x]` but NO `[completed:: ]` field: list separately as "Undated completions"

6. **Sort** by completion date (most recent first), then by project name.

7. **Output format**:

```
## Tasks Done - Week of [Monday date]

### Completed This Week
| Task | Project | Completed | Due |
|---|---|---|---|

### Undated Completions
| Task | Project |
|---|---|
(These tasks are checked off but have no [completed:: ] date - consider adding dates)

---
Summary: X tasks completed this week | Y undated completions
```

Keep task names concise. Show wiki-link targets as plain text.
