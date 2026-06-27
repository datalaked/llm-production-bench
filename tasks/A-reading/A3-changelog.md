# A3 — Summarize Changelog Versions

**Category:** A — Reading & Understanding  
**Estimated time (human):** 10–20 min  
**Requires writing code:** No

---

## Objective

Ask the agent to read the project's changelog (or commit history if no changelog exists) and produce a structured summary organized by version or time period, highlighting breaking changes, significant features, and deprecations.

---

## Prompt

```
Read this project's changelog (CHANGELOG.md, HISTORY.md, or similar) and produce a structured summary.

If no changelog file exists, use the git commit history instead.

Your summary should:

1. List each version (or time period if using git history) from newest to oldest
2. For each version, note: major features added, breaking changes, deprecations, and bug fixes (grouped, not listed one-by-one)
3. Identify the 3 most significant changes across the entire history and explain why they were significant
4. Note any versions that appear to have introduced instability (e.g. followed immediately by a patch release)
5. Estimate the overall maturity and release cadence of the project

Write this as a product/engineering summary. Do not modify any files.
```

---

## What to Evaluate

A strong response will:
- Correctly identify the changelog file (or fall back to git log with a clear explanation)
- Accurately summarize what each version changed based on the actual file content
- Correctly identify breaking changes (not just anything that sounds breaking)
- Make a defensible judgment about the 3 most significant changes
- Correctly read the release cadence from dates

A weak response will:
- Invent version descriptions not present in the changelog
- Miss breaking changes or flag non-breaking changes as breaking
- Fail to synthesize across versions (just reprints the changelog verbatim)
- Get dates or version numbers wrong

---

## Scoring Notes

- **5:** Accurate, well-structured, insightful. Synthesizes across versions rather than just reprinting. Correct breaking change identification.
- **4:** Accurate and structured, minor synthesis gaps or one inaccurate claim.
- **3:** Mostly accurate, but stays close to reprinting rather than summarizing. May miss one breaking change.
- **2:** Several inaccuracies or significant gaps. Falls back to generic observations.
- **1:** Generic changelog commentary. Does not reflect this project's actual history.
- **0:** Refused, file not found, or the output does not reflect this project at all.

---

## Notes for Evaluators

If the project uses git commit history (no changelog), the prompt falls back to `git log`. This is a valid path — evaluate it on the same criteria. The key signal is whether the model accurately reads and synthesizes what's there, not whether it finds a changelog file.

For projects with very long histories (100+ versions), it's acceptable for the model to group older versions into time periods rather than enumerate every one.
