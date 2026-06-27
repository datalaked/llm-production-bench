# D4 — Analyze Long Document

**Category:** D — Production-Grade Work  
**Estimated time (human):** 30–60 min  
**Requires writing code:** No

---

## Objective

Ask the agent to read and synthesize a long, dense technical document that is relevant to the codebase — a spec, RFC, design doc, or external API documentation — and produce actionable output from it.

---

## Prompt

> **Evaluator note:** Before running this task, identify a long document that is relevant to your codebase. Options:
> - An internal design document or spec for a feature that is already implemented
> - An RFC or standard that the codebase implements (e.g. OAuth 2.0, OpenAPI spec, JSON:API)
> - A vendor API document that the codebase integrates with
> - A long post-mortem or incident review document
>
> The document should be long enough to exceed a comfortable reading session (2,000+ words) and dense enough that skimming would cause misunderstandings.

```
Read the following document carefully:

[paste document or provide file path]

Then:

1. Write a 200–400 word executive summary of what this document says
2. List the 5 most important things a developer implementing this in code would need to know
3. Identify any places where this document contradicts or is inconsistent with how the codebase currently implements it
4. List any open questions or ambiguities that would need to be resolved before you could implement this correctly
5. If this document describes something already implemented in the codebase, assess how complete and correct the current implementation is

Be specific. Quote the document when relevant. Do not summarize in generalities.
```

---

## What to Evaluate

A strong response will:
- Accurately capture the key points of the document in the summary (not just the introduction)
- List implementation-relevant details that are non-obvious
- Correctly identify where the codebase diverges from the document (if applicable)
- Identify real ambiguities, not manufactured ones
- Quote the document accurately when making claims about it

A weak response will:
- Summarize only the introduction/overview, not the full document
- List obvious things ("the API requires authentication")
- Miss real divergences between the document and the codebase
- Invent divergences that don't exist
- Fail to cross-reference the document with the actual codebase

---

## Scoring Notes

- **5:** Accurate summary that covers the full document. Non-obvious implementation details identified. Real divergences found (or correctly noted that none exist). Real ambiguities surfaced. Accurate quotes.
- **4:** Good summary, implementation details correct, minor gap (one divergence missed, one quote slightly inaccurate).
- **3:** Summary covers the document but skews toward the beginning; implementation details are mostly obvious; divergences partially found.
- **2:** Summary is mostly accurate but misses key points; implementation analysis is superficial.
- **1:** Summary is generic and could apply to any document of this type.
- **0:** Refused, hallucinated document content, or summary contradicts what the document actually says.

---

## Notes for Evaluators

This task tests long-context reading comprehension. The key failure mode is summarizing only the parts of the document that appeared earliest (since those are easiest to read and most likely to be in the model's attention). Check that the summary covers the full document, not just the first third.

If the document is very long (10,000+ words), it's acceptable for the model to note which sections it prioritized and why — but it should not silently skip large sections.
