# A2 — Audit Migrations Chronologically

**Category:** A — Reading & Understanding  
**Estimated time (human):** 20–40 min  
**Requires writing code:** No

---

## Objective

Ask the agent to read and summarize the database migration history of the codebase in chronological order, identifying what changed at each significant step, and flagging any migrations that look risky or unusual.

---

## Prompt

```
Read all database migrations in this codebase in chronological order.

Produce a written audit that includes:

1. A chronological summary of what each migration does (group minor migrations if there are many — focus on significant schema changes)
2. The current schema state: what tables and key columns exist today as a result of the migration history
3. Any migrations that look risky, unusual, or that required special handling (e.g. data migrations, column renames without a transition period, dropping columns, changing column types on large tables)
4. Any migrations that appear to be out of order, incomplete, or potentially conflicting

Write this as an audit document. Do not modify any files. Do not run any migrations.
```

---

## What to Evaluate

A strong response will:
- Read migrations in actual chronological order (by timestamp or sequence number, not alphabetically)
- Accurately describe what each migration does based on the actual operations in the file
- Correctly identify the resulting schema state
- Flag genuinely risky operations (not just call everything "potentially risky")
- Note missing rollback logic, data-destructive operations, or race conditions where they actually exist

A weak response will:
- Summarize migrations out of order
- Describe operations incorrectly (e.g. calling an `ALTER TABLE ADD COLUMN` a "column rename")
- Miss risky migrations or flag safe ones as risky
- Fail to synthesize the current schema state

---

## Scoring Notes

- **5:** Correct chronological order, accurate descriptions, correct risk flags, accurate current schema summary.
- **4:** Correct order and descriptions, minor inaccuracies in risk assessment or schema summary.
- **3:** Right idea, but some migrations mis-described or out of order, or current schema partially wrong.
- **2:** Significant inaccuracies in migration descriptions or order; current schema mostly wrong.
- **1:** Generic migration commentary that doesn't reflect this codebase's actual migrations.
- **0:** Refused, file not found, or output is about a different system entirely.

---

## Notes for Evaluators

This task is a good signal for whether the model can maintain state across many files and synthesize a sequential narrative. Check a sample of the migration descriptions for accuracy — don't assume the whole thing is right because one or two are correct.

If the codebase uses Django, Alembic, Flyway, or Prisma migrations, the model should use the framework's ordering convention (not filesystem order, which may differ).
