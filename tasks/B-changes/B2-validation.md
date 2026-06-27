# B2 — Find and Fix Missing Pydantic Validation

**Category:** B — Targeted Changes  
**Estimated time (human):** 20–40 min  
**Requires writing code:** Yes

---

## Objective

Ask the agent to audit the codebase for API endpoints or data models that accept user input without sufficient Pydantic (or equivalent schema) validation, and fix the most significant gaps.

---

## Prompt

```
Audit this codebase for missing or insufficient input validation on API endpoints and data models.

Specifically look for:
1. Fields that accept arbitrary strings where they should have length limits, pattern constraints, or enum values
2. Numeric fields with no range validation where bad values could cause errors or unexpected behavior
3. Optional fields that are treated as required in the business logic but not enforced at the schema level
4. Nested models that skip validation (e.g. dict fields that should be typed models)
5. Any input that reaches the database or external services without being validated first

Fix the top 3 most significant gaps you find. For each fix:
- Make the change in the relevant schema/model file
- Add a comment explaining why this validation matters
- Do not change business logic — only add or strengthen validation

After making your changes, write a brief summary of what you found and fixed, and list any other gaps you found but did not fix.
```

---

## What to Evaluate

A strong response will:
- Find real validation gaps (not invent ones that don't exist)
- Prioritize gaps that could cause real problems (security, data integrity) over cosmetic ones
- Write correct Pydantic validators (or the equivalent framework) that actually enforce the intended constraint
- Not break existing valid inputs
- Summarize additional gaps honestly

A weak response will:
- Add trivially obvious validators that were already present
- Write validators with syntax errors or that would break valid inputs
- Miss significant gaps while flagging minor ones
- Add validation in the wrong layer (e.g. in the ORM model instead of the API schema)

---

## Scoring Notes

- **5:** Finds real, significant gaps. Fixes are correct and don't break valid inputs. Good prioritization. Honest summary of remaining issues.
- **4:** Finds real gaps, fixes are correct, minor prioritization issues or one fix that's slightly over-constrained.
- **3:** Finds real gaps but fixes have minor issues (slightly wrong constraint, edge case that would break), or prioritization is poor.
- **2:** Fixes are mostly correct but the gaps found are minor; significant gaps were missed.
- **1:** Adds validation that was already there, or validators that are incorrect.
- **0:** Refused, breaks existing functionality, or finds no real gaps in a codebase that clearly has them.

---

## Notes for Evaluators

Test the fixes if possible by running existing tests. A validator that rejects valid data is a regression, not an improvement.

This task is framework-specific. If the codebase uses Django REST Framework serializers, FastAPI schemas, or another validation layer, the model should use that, not raw Pydantic. Adjust your evaluation accordingly.
