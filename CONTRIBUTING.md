# Contributing to llm-production-bench

Thank you for contributing benchmark results. This document explains how.

---

## What We Accept

### Benchmark results

Run results on your own production codebase (or an open-source project you know well) and submit your scores. Results must be:

- Scored by a human evaluator using the rubric in [`scoring/rubric.md`](scoring/rubric.md)
- Run using Claude Code as the agent framework (other frameworks are tagged separately and not compared directly)
- Complete enough to be useful — at minimum, 5 tasks from at least 2 categories

### Task improvements

If a task prompt is unclear, produces consistently bad prompts, or needs codebase-type-specific variants, open a PR with the improvement. Explain what problem the change solves.

### New task proposals

Open an issue with the `task-proposal` label. Include:
- The task prompt
- What it tests that existing tasks don't
- Why it matters for production codebases specifically (not just model capability generally)

---

## How to Submit Results

### Option 1: GitHub Issue (easiest)

1. Use the [New Results issue template](.github/ISSUE_TEMPLATE/new-results.md)
2. Fill in all required fields
3. A maintainer will create the results file and add it to `results/`

### Option 2: Pull Request

1. Fork this repository
2. Copy `scoring/results-template.md` to `results/YYYY-MM-DD-your-handle.md`
3. Fill in all required fields
4. Open a PR with title `results: [model] on [codebase type] - [date]`

---

## Results Filename Convention

```
results/YYYY-MM-DD-github-handle.md
```

Examples:
- `results/2026-06-27-plamen.md`
- `results/2026-07-15-jsmith-gpt4o-run2.md`

If you run the same model multiple times, append `-run2`, `-run3`, etc.

---

## Required Fields

Every results file must include:

| Field | Required |
|-------|----------|
| Date | Yes |
| Model name + version | Yes |
| Agent framework + version | Yes |
| Codebase description | Yes |
| Scores for all tasks run | Yes |
| Tasks skipped and why | Yes |
| Unweighted average | Yes |

Optional but appreciated:
- Raw model outputs for 2–3 tasks
- Observations about patterns across the run

---

## Scoring Integrity

We rely on self-reported scores. A few principles that make the benchmark trustworthy:

**Score honestly.** A 3 from an honest evaluator is more valuable than a 5 from an optimistic one. Calibrate against the rubric examples.

**One evaluator per run.** All tasks in a single run should be scored by the same person.

**Do not iterate.** Run the task once, score the output as-is. Do not re-run a task because the first output was bad.

**Do not provide hints.** If the agent asks a clarifying question during a task, answer minimally ("use your judgment", "no preference"). Do not guide it toward the correct answer.

**Disclose prompt modifications.** If you modified a task prompt in any way, note this in your results. Prompt changes can significantly affect scores.

---

## What Makes a Good Codebase for Benchmarking

The best codebases for this benchmark are:

- **Real and used in production** (not toy projects or tutorial apps)
- **Non-trivial in size** (at least 5,000 LOC across meaningful layers)
- **Have some history** (enough for A2 and A3 tasks to be meaningful)
- **Familiar to the evaluator** (you need to verify the model's claims)

Open-source codebases are ideal because results can be independently verified. Private codebases are acceptable — you can describe the codebase without disclosing its contents.

---

## Code of Conduct

- Be accurate in your scoring — the value of this benchmark depends on honest results
- Do not submit results designed to favor a particular model
- Do not submit results for codebases you don't understand well enough to evaluate

---

## Questions?

Open an issue with the `question` label.
