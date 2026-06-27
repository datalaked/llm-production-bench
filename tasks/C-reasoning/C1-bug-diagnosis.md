# C1 — Diagnose Production Traceback

**Category:** C — Reasoning & Design  
**Estimated time (human):** 15–30 min  
**Requires writing code:** No (diagnosis only)

---

## Objective

Give the agent a real (or realistic) production traceback from the codebase and ask it to diagnose the root cause, explain why it happened, and propose a fix — without necessarily implementing the fix.

---

## Prompt

> **Evaluator note:** Before running this task, prepare a real traceback from your codebase. Use an actual exception from your error tracker (Sentry, Datadog, etc.) or construct a realistic one from a known bug. Paste it into the prompt below.

```
The following traceback was captured in production. Diagnose it.

--- TRACEBACK ---
[paste traceback here]
--- END TRACEBACK ---

Your diagnosis should include:
1. What went wrong (the immediate cause)
2. Why it went wrong (the root cause — trace back through the code to understand what led to this state)
3. Under what conditions this error occurs (what inputs, timing, or state triggers it)
4. How to fix it (a specific, actionable recommendation — you do not need to implement the fix)
5. Whether this is likely a one-time occurrence or a recurring issue, and why

Read the relevant source files before answering. Do not guess — if you can't find the relevant code, say so.
```

---

## What to Evaluate

A strong response will:
- Correctly identify the immediate cause from the traceback
- Trace back to the actual root cause in the source code (not just restate the exception message)
- Correctly identify the triggering conditions (not just "bad input" but specifically what)
- Propose a fix that addresses the root cause, not just the symptom
- Accurately assess recurrence risk

A weak response will:
- Restate the traceback without reading the source
- Propose a generic fix (e.g. "add a null check") without explaining where or why
- Misidentify the root cause because it didn't read the relevant file
- Over-hedge ("this could be caused by many things") without committing to a diagnosis

---

## Scoring Notes

- **5:** Correct root cause. Triggering conditions accurately described. Fix addresses root cause. Confident, specific, verifiable diagnosis.
- **4:** Correct root cause, good fix, minor imprecision about triggering conditions or recurrence.
- **3:** Root cause direction is right, but diagnosis stays at the surface (identifies the wrong function, or gets the cause right but the triggering conditions wrong).
- **2:** Partially correct — identifies one contributing factor but misses the root cause.
- **1:** Generic diagnosis that doesn't require reading any source code.
- **0:** Refused, wrong traceback, or diagnosis is demonstrably incorrect.

---

## Notes for Evaluators

This task requires a real traceback. The quality of the task depends on how realistic and complex the traceback is. Prefer tracebacks that:
- Span multiple files
- Involve a non-obvious root cause (not just a missing None check)
- Have triggering conditions that require reading the code to understand

A one-line `AttributeError: 'NoneType' object has no attribute 'id'` in a simple getter is too easy. A `KeyError` in a celery task that only happens when a race condition occurs between two async operations is a good example.
