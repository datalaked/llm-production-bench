# Benchmark Results Template

Copy this file to `results/YYYY-MM-DD-your-name.md` and fill it in after running the benchmark.

---

## Run Metadata

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Submitted by | your name / GitHub handle |
| Agent framework | e.g. Claude Code v1.x |
| Model tested | e.g. claude-opus-4-8, gpt-4o-2024-11-20 |
| Model version / API snapshot | e.g. API accessed on YYYY-MM-DD |
| Codebase description | e.g. "Django 4.2 monolith, ~50k LOC, PostgreSQL, Celery, React frontend" |
| Codebase public? | Yes / No (if yes, link) |
| Tasks run | List task IDs, e.g. A1, A2, B1, C1, D3 |

---

## Scores

| Task ID | Task Name | Score (0–5) | Notes |
|---------|-----------|-------------|-------|
| A1 | Architecture explanation | | |
| A2 | Migration audit | | |
| A3 | Changelog summary | | |
| B1 | Docstring | | |
| B2 | Pydantic validation | | |
| B3 | Refactor | | |
| C1 | Bug diagnosis | | |
| C2 | ADR writing | | |
| C3 | Migration risk | | |
| D1 | Git commit | | |
| D2 | TypeScript any | | |
| D3 | E2E feature | | |
| D4 | Document analysis | | |

**Tasks not run:** List any tasks you skipped and why (e.g. "D2 — TypeScript: codebase is Python-only")

---

## Aggregate Scores

| Metric | Value |
|--------|-------|
| Tasks completed (n) | |
| Unweighted average | |
| Weighted average (optional) | |
| Category A average | |
| Category B average | |
| Category C average | |
| Category D average | |

---

## Highlights

### Best task (highest score)

**Task:** [ID and name]  
**Score:** [score]  
**Why it scored well:** [1–3 sentences]

### Worst task (lowest score)

**Task:** [ID and name]  
**Score:** [score]  
**Why it scored poorly:** [1–3 sentences]

---

## Observations

Write 3–5 sentences about patterns you noticed across the run. What did the model do consistently well or poorly? Were there any surprises?

---

## Raw Outputs (Optional)

If you want to share the raw model outputs for any tasks, paste them below. This is optional but helps others calibrate scores.

### [Task ID] Raw Output

```
[paste output here]
```

---

## Evaluator Notes

Any notes on the evaluation process, codebase characteristics that made certain tasks easier or harder, or anything else reviewers should know.
