# C2 — Write ADR Following Existing Format

**Category:** C — Reasoning & Design  
**Estimated time (human):** 30–60 min  
**Requires writing code:** No (document only)

---

## Objective

Ask the agent to write an Architecture Decision Record (ADR) for a significant past or proposed decision, following the existing ADR format in the codebase.

---

## Prompt

> **Evaluator note:** Before running this task, identify either (a) a significant past decision in the codebase that doesn't yet have an ADR, or (b) a decision you are currently weighing. Provide this context in the prompt below.

```
This codebase uses Architecture Decision Records (ADRs) to document significant technical decisions.

Read the existing ADRs in this repository to understand the format and writing style used here.

Then write a new ADR for the following decision:

[describe the decision: e.g. "Why we use Celery for async tasks instead of Django Q" or "Whether to migrate from REST to GraphQL for the mobile API"]

Your ADR should:
1. Follow the exact format and style of the existing ADRs in this repo
2. Include the context and forces that drove the decision
3. Describe the decision clearly
4. List the consequences (both positive and negative)
5. Reference relevant existing ADRs if applicable

Write the ADR as a new file. Place it in the correct directory with the correct naming convention for this project.
```

---

## What to Evaluate

A strong response will:
- Read the existing ADRs and actually follow their format (not a generic ADR format from memory)
- Match the writing style and level of detail of existing ADRs
- Name the file and place it correctly
- Write a context section that reflects the actual codebase constraints
- List real consequences, not just generic pros and cons of the technology

A weak response will:
- Use a generic ADR template (MADR, Nygard) without checking what format the project uses
- Write context that is generic and not grounded in this codebase
- List consequences that are obvious without reading the code
- Place the file in the wrong directory or with the wrong naming convention

---

## Scoring Notes

- **5:** Format matches existing ADRs precisely. Context is grounded in the actual codebase. Consequences are specific and non-obvious. File placed correctly.
- **4:** Format mostly matches, context is good, one consequence is generic or one format detail is wrong.
- **3:** Right structure, but format diverges from existing ADRs in style or depth. Context is mostly generic.
- **2:** Correct ADR concept but doesn't follow project format at all. Could apply to any project.
- **1:** Generic ADR boilerplate unrelated to the codebase.
- **0:** Refused, or produced a completely wrong document type.

---

## Notes for Evaluators

The key differentiator for this task is whether the model reads the existing ADRs and matches them, versus writing a generic ADR from memory. Compare the submitted ADR against your existing ones side-by-side.

If the codebase has no existing ADRs, this task is not well-suited to it. Skip it or provide a sample ADR in the prompt as the format reference.
