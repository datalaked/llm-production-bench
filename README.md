# llm-production-bench

**Benchmark methodology for evaluating LLM coding agents on real production codebases.**

---

## What This Is

`llm-production-bench` is an open methodology for benchmarking LLM coding agents on **real, production-grade codebases** — not toy examples, not synthetic puzzles.

Most existing LLM coding benchmarks (HumanEval, SWE-bench lite, etc.) evaluate models on isolated, hand-crafted tasks. This tells you how a model performs on clean, decontextualized problems. It does not tell you how it performs when dropped into *your actual codebase* — with legacy decisions, inconsistent naming, implicit conventions, and dozens of files of context.

This benchmark exists to answer a different question:

> **Which model performs best when used as a coding agent on a real, messy, production codebase?**

---

## Why Real Code Matters

Synthetic benchmarks optimize for synthetic performance. Real codebases have:

- **Implicit conventions** not documented anywhere
- **Legacy decisions** that constrain what's possible today
- **Cross-file dependencies** that require navigating many files to understand a single change
- **Inconsistent patterns** where "the right thing" is whatever is already done elsewhere
- **Production constraints** — migrations can't break existing data, APIs have consumers, types must stay compatible

A model that scores 90% on HumanEval may still struggle to write a meaningful docstring for a complex endpoint because it fails to understand what the endpoint actually does in context.

---

## Methodology: One Constant, One Variable

The benchmark controls for the **agent framework** and varies only the **model**.

- **Constant:** [Claude Code](https://claude.ai/code) as the agent framework (same tools, same system prompt, same working directory)
- **Variable:** The underlying model (Claude Opus 4.8, Claude Sonnet 4.6, GPT-4o, Gemini 2.5 Pro, etc.)

This isolates model capability from agent scaffolding. You run the same tasks, with the same agent, on the same codebase — and swap only the model underneath.

> Results submitted with different agent frameworks are tagged separately and not compared directly.

---

## Task Taxonomy

Tasks are organized into four categories by cognitive demand:

### Category A — Reading & Understanding
Tasks that require reading and synthesizing existing code without making changes.

| ID | Task |
|----|------|
| A1 | Explain backend architecture |
| A2 | Audit migrations chronologically |
| A3 | Summarize changelog versions |

### Category B — Targeted Changes
Tasks that require making a specific, scoped change to existing code.

| ID | Task |
|----|------|
| B1 | Add docstring to complex endpoint |
| B2 | Find and fix missing Pydantic validation |
| B3 | Extract duplicated code to shared utility |

### Category C — Reasoning & Design
Tasks that require reasoning about tradeoffs, diagnosing problems, or producing structured artifacts.

| ID | Task |
|----|------|
| C1 | Diagnose production traceback |
| C2 | Write ADR following existing format |
| C3 | Analyze migration risk |

### Category D — Production-Grade Work
Tasks that require end-to-end, production-quality output across multiple files or systems.

| ID | Task |
|----|------|
| D1 | Write conventional git commit |
| D2 | Fix TypeScript `any` usages |
| D3 | Implement end-to-end feature |
| D4 | Analyze long document |

---

## Scoring Rubric

Tasks are scored **0–5** by a human reviewer using the rubric in [`scoring/rubric.md`](scoring/rubric.md).

| Score | Meaning |
|-------|---------|
| 0 | Complete failure — wrong, broken, or refused |
| 1 | Attempted but fundamentally off-track |
| 2 | Partial — correct direction, significant gaps |
| 3 | Acceptable — works but misses nuance or context |
| 4 | Good — correct, fits the codebase, minor issues |
| 5 | Excellent — exactly what a senior engineer would produce |

---

## How to Contribute Results

1. Pick a real production codebase you have access to (your own project, an open-source repo, etc.)
2. Run the tasks using the setup guide in [`setup/claude-code.md`](setup/claude-code.md)
3. Score each task output using [`scoring/rubric.md`](scoring/rubric.md)
4. Fill in [`scoring/results-template.md`](scoring/results-template.md)
5. Submit via GitHub Issue using the [results template](.github/ISSUE_TEMPLATE/new-results.md) or open a PR adding your results file to `results/`

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full instructions.

---

## First Results

> Results from the first benchmark run will be published here.
> 
> **[Coming soon]** — Initial results across Claude Opus 4.8, Claude Sonnet 4.6, GPT-4o, and Gemini 2.5 Pro on a production Django + React codebase.

---

## Repository Structure

```
llm-production-bench/
├── tasks/
│   ├── A-reading/      # Category A task definitions
│   ├── B-changes/      # Category B task definitions
│   ├── C-reasoning/    # Category C task definitions
│   └── D-production/   # Category D task definitions
├── scoring/
│   ├── rubric.md       # Full 0-5 scoring rubric with examples
│   └── results-template.md
├── setup/
│   ├── claude-code.md  # Agent setup: Claude Code
│   └── litellm-local.md # Running local models via LiteLLM proxy
├── results/            # Community-submitted benchmark results
├── CONTRIBUTING.md
└── .github/
    └── ISSUE_TEMPLATE/
        └── new-results.md
```

---

## License

MIT — see [LICENSE](LICENSE).
