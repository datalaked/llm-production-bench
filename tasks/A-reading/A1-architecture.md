# A1 — Explain Backend Architecture

**Category:** A — Reading & Understanding  
**Estimated time (human):** 15–30 min  
**Requires writing code:** No

---

## Objective

Ask the agent to produce a clear, accurate explanation of the backend architecture of the codebase under test — covering the main layers, data flow, key design decisions, and any non-obvious patterns.

---

## Prompt

```
You are a senior engineer being onboarded to this codebase.

Read the backend source code and produce a written explanation of the architecture. Your explanation should cover:

1. The main layers or modules (e.g. API layer, service layer, data layer) and what each is responsible for
2. How a typical request flows through the system from entry point to response
3. The primary data models and how they relate to each other
4. Any non-obvious design decisions or patterns (e.g. why something is structured the way it is)
5. What you would tell a new engineer on their first day

Write this as a technical document, not a code walkthrough. Aim for 400–800 words. Do not modify any files.
```

---

## What to Evaluate

A strong response will:
- Correctly identify the actual layers present in the codebase (not generic layers that don't exist)
- Trace a real request path, naming real files and functions
- Identify the actual data models, not placeholders
- Note any genuinely non-obvious patterns (not just "they use MVC")
- Be accurate — verifiable against the codebase

A weak response will:
- Describe a generic web architecture without grounding in this specific codebase
- Hallucinate module names or patterns that don't exist
- Miss significant components
- Be vague where specifics are needed ("there is a service layer that handles business logic")

---

## Scoring Notes

- **5:** Accurate, specific, and insightful. Names real components. Identifies non-obvious patterns correctly.
- **4:** Accurate and specific, minor omissions or mild imprecision.
- **3:** Mostly accurate, covers the main points, but stays surface-level or misses one significant component.
- **2:** Some correct observations but significant inaccuracies or major gaps.
- **1:** Generic architecture description that could apply to any web app.
- **0:** Refused, completely wrong, or describes a different codebase.

---

## Notes for Evaluators

Run this task early in the benchmark session, before the model has built up context from other tasks. The model should derive all its knowledge from reading the codebase, not from prior task context.

Compare the output against your own mental model of the codebase. If you're unsure whether a claim is correct, check it.
