---
description: Display all open tasks grouped by urgency, sorted by project, priority, due date
allowed-tools: Grep, Read, Bash
---

# Weekly Priorities - Open Tasks

Display all open tasks from the Obsidian vault, grouped by urgency and sorted by project, priority, then due date.

## Instructions

1. **Collect all open tasks** - Use `Grep` to find all `- \[ \]` lines across `*.md` files in the vault at `/Users/alexanderruppert/Desktop/Claude/OBSIDIAN VAULT`. Exclude `.obsidian/` plugin files.

2. **Filter out non-actionable tasks** - Exclude:
   - Template files (in `Templates/` folder)
   - Empty checkbox lines (just `- [ ]` with no text)
   - Task Board entries (these mirror tasks from other projects, skip the entire `Task Board.md` file)
   - Large reference checklists: `Project Mac Mini Claude Setup.md` and `Project Security Screen for Claude Code Repos.md` (these are setup guides, not active tasks - mention them as a count at the bottom)

3. **Parse each task** extracting:
   - Task text (clean, without inline field syntax)
   - Project name (from the source filename, without `.md`)
   - Priority (from `[prio:: N]` field, or `-` if missing)
   - Due date (from `[due:: YYYY-MM-DD]` field, or empty if missing)

4. **Determine today's date** using `Bash`: `date '+%Y-%m-%d'`

5. **Sort and group** tasks into these sections:
   - **Overdue** - due date before today (flag these clearly)
   - **Due Today** - due date equals today
   - **This Week** - due date within 7 days from today
   - **Later** - due date beyond 7 days
   - **No Due Date** - tasks without a due date

   **Within each section**, sort tasks by:
   1. **Project name** (alphabetical)
   2. **Priority** (prio 1 first, then 2, then 3, then missing)
   3. **Due date** (earliest first)

6. **Output format** - Display as markdown tables:

```
## Open Tasks - [today's date]

### Overdue
| Task | Project | Prio | Due |
|---|---|---|---|

### Due Today
| Task | Project | Prio |
|---|---|---|

### This Week
| Task | Project | Prio | Due |
|---|---|---|---|

### Later
| Task | Project | Prio | Due |
|---|---|---|---|

### No Due Date
| Task | Project | Prio |
|---|---|---|

---
Summary: X tasks total | Y overdue | Z due today
Note: N tasks in Mac Mini Setup checklist and M tasks in Security Screen checklist excluded.
```

Keep task names concise. Show wiki-link targets as plain text (e.g., `[[Theo]]` becomes `Theo`).
