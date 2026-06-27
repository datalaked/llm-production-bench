# B1 — Add Docstring to Complex Endpoint

**Category:** B — Targeted Changes  
**Estimated time (human):** 10–20 min  
**Requires writing code:** Yes (docstring only, no logic changes)

---

## Objective

Ask the agent to find the most complex API endpoint in the codebase and add a comprehensive docstring to it. The docstring must accurately describe what the endpoint does — not just what the parameters are.

---

## Prompt

```
Find the most complex API endpoint in this codebase — the one with the most business logic, most parameters, or most non-obvious behavior.

Add a docstring to that endpoint's handler function. The docstring should:

1. Describe what the endpoint does in plain English (not just restating the function name)
2. Document each parameter: name, type, what it means, and any constraints or defaults
3. Document the response: shape, status codes, and what each means
4. Note any side effects (e.g. sends email, creates audit log, triggers async job)
5. Note any non-obvious behavior or gotchas (e.g. soft delete, idempotency, permission requirements)

Use the docstring format already present in this codebase. If no format is established, use Google style.

Only modify the docstring — do not change any logic.
```

---

## What to Evaluate

A strong response will:
- Select a genuinely complex endpoint (not the simplest one)
- Write a docstring that accurately describes what the endpoint actually does
- Correctly document parameters including types and constraints present in the code
- Correctly document response codes and shapes as implemented
- Note real side effects, not invented ones
- Match the existing docstring style of the codebase

A weak response will:
- Select a trivial endpoint
- Write a docstring that re-states the function name ("Creates a user. Parameters: user data.")
- Invent parameters or response codes not present in the code
- Ignore side effects that are clearly present
- Use an inconsistent style

---

## Scoring Notes

- **5:** Selected a genuinely complex endpoint. Docstring is accurate, complete, and matches codebase style. Notes real side effects and gotchas.
- **4:** Good endpoint selection and accurate docstring, minor gap (one parameter underdocumented, one status code missing).
- **3:** Reasonable endpoint, docstring is accurate but thin — correct but not complete.
- **2:** Poor endpoint selection, or docstring has significant inaccuracies about what the endpoint actually does.
- **1:** Docstring is generic boilerplate that could apply to any endpoint.
- **0:** Refused, changed logic, or docstring is demonstrably wrong.

---

## Notes for Evaluators

Review the selected endpoint yourself. If you disagree that it's the "most complex," that's a minor issue (score -0 to -1). The bigger issue is docstring accuracy — check it against the actual implementation.

Pay particular attention to whether the model correctly identifies side effects. These are often the hardest part to document and the most useful to document correctly.
