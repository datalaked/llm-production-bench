# Result Integrity

This document explains how `llm-production-bench` protects result quality and where its limits are.

---

## The Problem

Most public LLM coding leaderboards are vulnerable to gaming. A 2026 study by Berkeley RDI found that SWE-bench — one of the most widely cited coding benchmarks — could be exploited to achieve near-perfect scores without actually solving the underlying tasks. When a leaderboard becomes high-stakes, the incentive to optimize for the benchmark rather than for real capability follows.

This is not a new problem. Goodhart's Law applies: once a measure becomes a target, it ceases to be a good measure.

---

## Our Approach

This benchmark is structured to make gaming largely pointless.

You test on **your own production codebase** — code you wrote, maintain, and understand better than anyone else. You are also the evaluator. This means:

- There is no central committee whose approval you are seeking
- Inflated scores don't help you make better model decisions in your actual work
- The person most harmed by dishonest results is the submitter

The primary use case for this benchmark is **personal and team decision-making**: which model should we use as our coding agent? A falsely high score for a model that then underperforms in production is a cost you bear directly.

---

## Structural Protections

The schema and validator enforce several checks that make inflation harder to hide.

**`integrity.git_commit_hash`**
Every submission must include the full SHA-1 commit hash of the codebase at the time of testing. This ties the submission to a specific, reproducible codebase state. For public codebases, anyone can clone that exact commit and rerun the benchmark tasks to verify.

**`integrity.tok_per_sec_measured` vs `time_seconds`**
If a submission claims a task took 5 minutes and reports a generation speed of 5 tok/s, the implied output is 1,500 tokens — plausible. If it claims 30 seconds at 5 tok/s, that's 150 tokens for a task that requires a full architecture explanation — not plausible. The validator checks this arithmetic for every task and flags results outside reasonable bounds.

**Codebase complexity tier (XS → XL)**
Submissions are tagged by codebase size: XS (<1k LOC) through XL (>100k LOC). Results are not aggregated across tiers. A 5/5 on a 200-line hobby project is not comparable to a 5/5 on a 40k-line production system with 145 migrations. The tier prevents inflating scores by choosing trivially easy codebases.

**Minimum task coverage**
Every submission must include at least 5 tasks spanning at least 2 of the 4 categories (A–D). This prevents cherry-picking only the easiest tasks (e.g. submitting only D1 "write a git commit message" and claiming a top score).

---

## Community Peer Challenge

Any submission can be challenged via a GitHub Issue.

To open a challenge, the challenger must specify:
1. **Which submission** (filename and commit hash)
2. **Which task(s)** are being challenged
3. **What is suspicious** — e.g. the claimed score contradicts what the model is known to produce, the time implies an impossible output length, or the codebase description doesn't match the complexity tier
4. **Why** — reasoning or evidence, not just a claim

Maintainers will review flagged submissions and may request the raw model output for the disputed tasks. Submissions that cannot be defended will be marked as disputed in the results index.

---

## What We Can't Prevent

We disclose this openly.

**Multiple runs, best result submitted.** The benchmark protocol says run each task once and submit the output as-is. We cannot technically enforce this. Someone could run A1 five times and submit the best output. We rely on the self-reported single-run constraint and the incentive structure above.

**Prompt-engineered CLAUDE.md.** A heavily tuned `CLAUDE.md` that pre-loads task-specific context can improve scores. This is disclosed in the submission (the agent version and any setup notes), but we cannot audit every submitter's working directory. If your CLAUDE.md contains task-specific hints, your scores reflect that setup, not the model's out-of-the-box capability.

**Generous human scoring.** Scores are self-reported by the evaluator who ran the benchmark. An optimistic evaluator will produce higher scores than a strict one, even on identical outputs. The rubric in [`scoring/rubric.md`](scoring/rubric.md) provides anchored examples to calibrate this, but it cannot eliminate evaluator variance.

We accept these limitations. The alternative — a fully controlled, third-party-verified benchmark — has its own failure modes, as the SWE-bench case illustrates.

---

## The Honest Incentive

The benchmark is most useful when results are real.

If you inflate your scores, you may conclude that a model performs better than it does on your codebase. You then adopt it as your primary coding agent. It underperforms. You've made a worse engineering decision than if you had scored honestly.

The submission that benefits you most is the accurate one.
