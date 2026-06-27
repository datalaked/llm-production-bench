---
name: Submit Benchmark Results
about: Share your benchmark run results for a model on a production codebase
title: "results: [MODEL] on [CODEBASE TYPE] - [DATE]"
labels: results
assignees: ''
---

## Run Metadata

**Date:** YYYY-MM-DD  
**Submitted by:** @your-github-handle  
**Agent framework:** e.g. Claude Code v1.x  
**Model tested:** e.g. claude-opus-4-8, gpt-4o-2024-11-20  
**Model API accessed on:** YYYY-MM-DD  
**Codebase description:** e.g. "Django 4.2 monolith, ~50k LOC, PostgreSQL, Celery, React frontend"  
**Codebase public?:** Yes / No (if yes, link)  

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

**Tasks not run:**
<!-- List tasks you skipped and why. E.g.: "D2 — codebase is Python-only" -->

---

## Aggregate

- **Tasks completed:** 
- **Unweighted average:** 
- **Weighted average (optional):** 
- **Category A average:** 
- **Category B average:** 
- **Category C average:** 
- **Category D average:** 

---

## Observations

<!-- 3–5 sentences: what patterns did you notice? What surprised you? -->

---

## Checklist

- [ ] I scored using the rubric in `scoring/rubric.md`
- [ ] I ran each task in a fresh session (no context carryover between tasks)
- [ ] I did not modify task prompts (or I noted modifications in the Notes column)
- [ ] I did not provide hints when the agent asked clarifying questions
- [ ] All scores were assigned by a single evaluator
- [ ] I have disclosed the model version / API snapshot date
