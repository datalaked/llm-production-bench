# Scoring Rubric

All tasks in this benchmark are scored **0–5** by a human evaluator.

---

## The Core Standard

Every score should answer the question:

> **Would a senior engineer on this codebase accept this output as-is?**

- **5** = Yes, exactly what I'd want.
- **4** = Yes, with minor notes.
- **3** = Needs revision before I'd accept it.
- **2** = Significant rework needed.
- **1** = Doesn't achieve the task, but tried.
- **0** = Failed completely, or made things worse.

---

## Score Definitions

### 5 — Excellent

The output is exactly what a senior engineer would produce. It is:
- **Accurate**: no errors, no hallucinated details
- **Specific**: grounded in this codebase, not generic advice
- **Complete**: covers all aspects of the task
- **Conventional**: follows project style, naming, and patterns
- **Insightful**: captures non-obvious aspects that a junior engineer would miss

**Example (A1 architecture):** The response correctly identifies the three-layer architecture, names real modules by their actual file paths, explains the non-obvious choice to use service-layer objects instead of fat models, and notes that the background task queue is processed by the same worker that handles webhooks (something only discoverable by reading both files).

---

### 4 — Good

The output is correct and useful, with minor issues that would require a small note in a code review — not a rejection.

Typical 4 characteristics:
- One parameter underdocumented
- One non-obvious detail missed
- Style slightly off but not wrong
- Correct but slightly over-verbose or under-verbose

**Example (B1 docstring):** The docstring accurately describes the endpoint, documents all parameters correctly, but misses one non-obvious status code (409 Conflict) that the endpoint returns in a specific edge case.

---

### 3 — Acceptable

The output achieves the basic goal but has gaps that would require revision before use. A reviewer would send this back with comments.

Typical 3 characteristics:
- Correct direction, but surface-level
- Misses 1–2 meaningful aspects
- Style deviates in a noticeable way
- Accurate but incomplete

**Example (C1 bug diagnosis):** The response correctly identifies that the bug is a race condition, but attributes it to the wrong component (says it's in the task scheduler when it's actually in the database transaction). Fix recommendation is correct in principle but not specific enough to implement.

---

### 2 — Partial

The output makes progress on the task but has significant issues that undermine its value.

Typical 2 characteristics:
- Right idea, wrong execution
- Significant inaccuracies
- Misses major aspects of the task
- Generic where specific is needed

**Example (B3 refactor):** The agent correctly identifies duplicated code but extracts it into the wrong module (puts it in `utils.py` when the project has a dedicated `shared/` package), misses two call sites, and the extracted function has a subtle behavior change due to argument ordering.

---

### 1 — Attempted but Off-Track

The output shows an attempt but doesn't substantively achieve the goal. It could have been produced without reading the codebase.

Typical 1 characteristics:
- Generic advice that applies to any codebase
- Correct format, wrong content
- Demonstrates effort but no understanding

**Example (A3 changelog):** The agent reads the changelog file but produces a generic summary ("The project has been actively developed with regular bug fixes and feature additions") rather than summarizing the actual versions and their contents.

---

### 0 — Failure

The output is a complete failure: wrong, refused, broken, or worse than the status quo.

Typical 0 characteristics:
- Refused to attempt the task
- Output is factually wrong in a way that would mislead
- Broke existing functionality
- Describes a different codebase
- Introduced a security vulnerability

**Example (D2 TypeScript):** The agent replaced `any` types but introduced 12 new TypeScript compilation errors and caused 3 existing tests to fail.

---

## Scoring Principles

**Score the output, not the attempt.** Partial credit is in the 1–3 range. A thoughtful failure that got the right approach is a 1, not a 3.

**Ground in the codebase.** A response that would be a 5 in a generic context but misses this specific codebase's conventions is a 3 or 4. The benchmark tests codebase-grounded performance.

**Check accuracy, don't assume it.** For reading tasks (A1–A3, C1–C3), verify claims against the source code. Models often produce plausible-sounding but wrong descriptions.

**Penalize hallucination heavily.** A confident wrong answer is worse than an honest "I'm not sure." A hallucinated function name or migration operation drops the score by at least 2 points.

**One evaluator per run.** To enable comparison across models, the same person should score all task outputs from a single benchmark run.

---

## Category Weighting (for aggregate scores)

When computing an aggregate score across categories, you may weight by category difficulty:

| Category | Default Weight |
|----------|---------------|
| A — Reading | 1.0× |
| B — Changes | 1.5× |
| C — Reasoning | 1.5× |
| D — Production | 2.0× |

Weighted average = `(sum of score × weight) / (sum of weights)`.

This is optional — unweighted averages are also valid for reporting, as long as the methodology is stated.
