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
- **Variable:** The underlying model (any model reachable via Claude Code or LiteLLM — cloud API or local inference)

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

## How to Submit Results

Submissions are YAML files validated by a schema and a CI check. One file = one model on one codebase.

### Quick start

```bash
# 1. Fork and clone this repository
git clone https://github.com/your-handle/llm-production-bench
cd llm-production-bench

# 2. Copy the template
cp submissions/template.yaml submissions/results/YYYY-MM-your-handle.yaml

# 3. Fill in your run data (see field descriptions in submissions/schema.yaml)
$EDITOR submissions/results/YYYY-MM-your-handle.yaml

# 4. Validate locally before opening a PR
pip install pyyaml jsonschema
python submissions/validate.py submissions/results/YYYY-MM-your-handle.yaml

# 5. Open a pull request — CI will re-validate automatically
```

### What goes in a submission

| Section | Key fields |
|---------|-----------|
| `metadata` | date, submitter name, optional repo URL |
| `codebase` | stack, LOC, file count, description, complexity tier (XS/S/M/L/XL) |
| `hardware` | device, GPU/CPU, memory, inference engine and version, tok/s nominal |
| `model` | name, architecture (dense/moe), params, quantization, context size, thinking mode |
| `agent` | framework name and version (e.g. Claude Code 1.0.19) |
| `results` | per-task: `time_seconds`, `quality_1_to_5` (1–5), `notes`, optional `disqualified` |
| `integrity` | `git_commit_hash` of codebase at test time, `tok_per_sec_measured` (actual run average) |

**Minimum coverage:** 5 tasks from at least 2 categories (A/B/C/D).

### Scoring

Score each task output **1–5** using the rubric in [`scoring/rubric.md`](scoring/rubric.md).
The rubric's core question: *would a senior engineer on this codebase accept this output as-is?*

Score your outputs honestly and don't re-run tasks — the benchmark's value depends on uncoached first-attempt results.

### Validation

The CI action ([`.github/workflows/validate-submissions.yml`](.github/workflows/validate-submissions.yml)) runs `validate.py` on every PR that touches `submissions/results/`. It checks:

- Required fields and correct types against [`submissions/schema.yaml`](submissions/schema.yaml)
- MoE models have `active_params_b < total_params_b`
- Minimum 5 tasks from 2+ categories
- Time × tok/s plausibility (catches unit errors like milliseconds vs seconds)
- `git_commit_hash` is a valid 40-character SHA-1

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full submission guide.

---

## First Results

**Codebase:** FastAPI + React + PostgreSQL — 145 Alembic migrations, 49 API routers, multi-tenant SaaS architecture.

| Model | Type | Hardware | Score |
|-------|------|----------|-------|
| Claude Sonnet 4.6 | Cloud API | Anthropic API | **63 / 65** |
| Qwen3.6-35B-A3B-Q8 | Local | ASUS GX10, llama.cpp | **55 / 65** |

13 tasks across all four categories (A–D). Both runs used Claude Code as the agent framework.

Full write-up and per-task breakdowns: [LinkedIn series — link coming]

Detailed submissions: [`submissions/results/datalaked-2026-06.yaml`](submissions/results/datalaked-2026-06.yaml) (Claude Sonnet 4.6) · [`submissions/template.yaml`](submissions/template.yaml) (Qwen3.6-35B-A3B-Q8)

---

## Repository Structure

```
llm-production-bench/
├── tasks/
│   ├── A-reading/          # Category A task definitions
│   ├── B-changes/          # Category B task definitions
│   ├── C-reasoning/        # Category C task definitions
│   └── D-production/       # Category D task definitions
├── scoring/
│   ├── rubric.md           # Full 0-5 scoring rubric with examples
│   └── results-template.md
├── setup/
│   ├── claude-code.md      # Agent setup: Claude Code
│   └── litellm-local.md    # Running local models via LiteLLM proxy
├── submissions/
│   ├── schema.yaml         # JSONSchema for submission files
│   ├── validate.py         # Submission validator (run before PR)
│   ├── requirements.txt    # pyyaml + jsonschema
│   ├── template.yaml       # Filled example submission
│   └── results/            # Community-submitted YAML results
│       └── datalaked-2026-06.yaml
├── CONTRIBUTING.md
└── .github/
    ├── workflows/
    │   └── validate-submissions.yml   # CI: validates results on every PR
    └── ISSUE_TEMPLATE/
        └── new-results.md
```

---

## License

MIT — see [LICENSE](LICENSE).
