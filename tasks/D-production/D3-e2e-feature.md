# D3 — Implement End-to-End Feature

**Category:** D — Production-Grade Work  
**Estimated time (human):** 2–4 hours  
**Requires writing code:** Yes (multiple files)

---

## Objective

Ask the agent to implement a small but complete feature across the full stack — from database schema to API endpoint to frontend component (or from schema to API to tests, depending on the codebase). The feature must fit the existing architecture and conventions.

---

## Prompt

> **Evaluator note:** Before running this task, define a specific small feature that is realistic for your codebase. The feature should require changes in at least 2–3 layers (e.g. model + migration + endpoint, or endpoint + serializer + tests). It should be non-trivial but completable in a single session.
>
> Example features:
> - "Add a `is_archived` flag to the Project model and expose it on the API so clients can filter archived projects"
> - "Add a `/health` endpoint that checks database connectivity and returns status"
> - "Add pagination to the `/users` list endpoint using the same cursor-based pagination used by `/orders`"

```
Implement the following feature in this codebase:

[describe the feature here]

Requirements:
1. Follow all existing conventions in this codebase — naming, file organization, patterns, style
2. Include everything needed for the feature to work: schema changes, business logic, API layer, and any tests that exist for similar features
3. Do not introduce new dependencies unless absolutely necessary
4. The implementation should be production-ready: handle edge cases, validate inputs, and handle errors the same way the rest of the codebase does
5. After implementing, write a brief summary of what you did and any decisions you made

Do not add features beyond what was asked. Do not refactor unrelated code.
```

---

## What to Evaluate

A strong response will:
- Implement the feature completely across all required layers
- Follow naming, organization, and style conventions precisely
- Match existing patterns (e.g. if pagination is done with cursors elsewhere, use cursors — don't invent offset-based)
- Include the same level of test coverage as similar features
- Handle edge cases correctly (null values, empty collections, permission checks)
- Not over-engineer or add unrequested functionality

A weak response will:
- Implement only part of the feature (e.g. the model change but not the API endpoint)
- Deviate from project conventions (different serializer pattern, different error handling)
- Miss edge cases that the rest of the codebase handles
- Add tests in a style that doesn't match existing tests
- Over-engineer (add caching, add new abstractions) or under-engineer (skip input validation)

---

## Scoring Notes

- **5:** Complete implementation across all layers. Conventions followed precisely. Edge cases handled. Tests match existing style. Production-ready.
- **4:** Complete implementation, mostly follows conventions, one significant omission (edge case, one layer done differently).
- **3:** Feature mostly works but has gaps (missing migration, tests missing, one layer incomplete).
- **2:** Feature partially implemented with significant gaps or convention deviations.
- **1:** Feature started but not functional or missing critical layers.
- **0:** Refused, broke existing functionality, or implementation is fundamentally wrong.

---

## Notes for Evaluators

This is the highest-effort task in the benchmark. Set a time limit on the agent (e.g. 30 minutes) and evaluate what was produced within that window — a partial but correct implementation in 30 minutes is different from an incomplete implementation that ran for an hour.

Run existing tests after the implementation. Any regressions in existing tests are a significant penalty regardless of how good the new code is.
