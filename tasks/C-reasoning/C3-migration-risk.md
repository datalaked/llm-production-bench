# C3 — Analyze Migration Risk

**Category:** C — Reasoning & Design  
**Estimated time (human):** 20–40 min  
**Requires writing code:** No (analysis only)

---

## Objective

Give the agent a pending or hypothetical database migration and ask it to analyze the production risk — locking behavior, data loss potential, rollback feasibility, and deployment strategy.

---

## Prompt

> **Evaluator note:** Before running this task, identify a real migration in your codebase (pending or recently run) that had some non-trivial risk. Paste its content into the prompt below. Good candidates: adding a NOT NULL column, renaming a column, dropping a table, changing a column type, backfilling data.

```
The following database migration is scheduled to run in production next week. Analyze its risk.

--- MIGRATION ---
[paste migration content here]
--- END MIGRATION ---

Your analysis should cover:

1. What this migration does, step by step
2. Table locking: which operations will lock which tables, for how long, and whether this is a problem at our data volumes
3. Data risk: could any operation here cause data loss, corruption, or constraint violations? Under what conditions?
4. Rollback feasibility: if something goes wrong mid-migration, can we roll back? What would we lose?
5. Deployment strategy: should this be run during a maintenance window? Does the application need to be updated before or after? Are there any zero-downtime deployment concerns?
6. Your overall risk rating: LOW / MEDIUM / HIGH / CRITICAL, with justification

Do not modify any files. Read the codebase to understand the data volumes and usage patterns if that information is available.
```

---

## What to Evaluate

A strong response will:
- Correctly identify which operations cause table locks and which are safe online
- Accurately assess data risk based on the actual migration content
- Give a specific, correct assessment of rollback feasibility
- Note deployment order dependencies if they exist in the codebase (e.g. code that assumes the new column exists)
- Assign an appropriate risk rating with accurate justification

A weak response will:
- Call every migration "HIGH risk" regardless of content
- Miss locking behavior (e.g. not knowing that `ADD COLUMN NOT NULL DEFAULT` locks in PostgreSQL < 11)
- Ignore the codebase context when assessing deployment order
- Give a generic "test in staging first" recommendation without specific analysis

---

## Scoring Notes

- **5:** Correct locking analysis. Correct data risk assessment. Specific rollback plan. Correct deployment strategy. Risk rating matches the actual risk.
- **4:** Correct on the main risks, minor gap (one locking detail wrong, deployment order not fully analyzed).
- **3:** Gets the big picture right but misses important details (e.g. knows there's locking risk but doesn't know why or for how long).
- **2:** Risk rating is wrong, or analysis misses a major risk present in the migration.
- **1:** Generic migration safety advice not specific to this migration.
- **0:** Refused, or analysis is demonstrably wrong (calls a DROP TABLE "low risk").

---

## Notes for Evaluators

This task tests database-specific knowledge (locking behavior, constraint evaluation order) as much as it tests code reading. A model may do well on the code-reading aspect but fail on the PostgreSQL/MySQL-specific locking semantics. Both matter.

If possible, know the answer yourself before running this task — it's the only way to score it accurately.
