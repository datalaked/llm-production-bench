# D1 — Write Conventional Git Commit

**Category:** D — Production-Grade Work  
**Estimated time (human):** 5–10 min  
**Requires writing code:** No (commit message only)

---

## Objective

Ask the agent to write a proper conventional commit message for a real diff, following the project's existing commit conventions.

---

## Prompt

> **Evaluator note:** Before running this task, stage a real set of changes in the working directory — either changes you've made yourself or changes from a recent PR. The diff should be non-trivial (more than a one-line fix).

```
You have staged changes in the working directory. Read the diff and write a conventional commit message for these changes.

First, read the recent git log to understand the commit message format and style used in this project.

Then write the commit message. It should:
1. Follow the project's existing commit style (conventional commits, emoji prefixes, plain English — whatever is used here)
2. Have a subject line under 72 characters that accurately describes what changed
3. Include a body if the changes require explanation (non-obvious motivation, tradeoffs, or context)
4. Reference any issue numbers if the project uses them and they're apparent from the changes

Do not commit anything. Just output the commit message.
```

---

## What to Evaluate

A strong response will:
- Read `git log` to determine the actual commit convention used (not assume conventional commits)
- Write a subject line that accurately describes what changed — not just which files
- Include a body when the changes are non-obvious, omit it when they're clear
- Match the tone and style of existing commits
- Not exceed 72 characters on the subject line

A weak response will:
- Use a generic conventional commit format when the project uses something else
- Write a subject that describes which files changed rather than what changed
- Include a verbose body for a trivial change, or omit a body for a complex one
- Write "fix bug" when the bug is clearly describable

---

## Scoring Notes

- **5:** Matches project convention exactly. Subject accurately describes the change in ≤72 chars. Body included if warranted, omitted if not. Natural, not formulaic.
- **4:** Right format and accurate description, subject line slightly over 72 chars or one style mismatch.
- **3:** Accurate description but wrong format, or right format but description is vague.
- **2:** Right format but wrong or misleading description.
- **1:** Generic commit message that could apply to any change ("update code", "fix issue").
- **0:** Refused, or the commit message is factually wrong about what the diff does.

---

## Notes for Evaluators

This task seems simple but is a good test of attention to style. Many models default to `feat:` / `fix:` conventional commits even when the project uses a completely different style.

Check `git log --oneline -20` before the task to know what to expect. A project with commits like `[JIRA-123] Fix user creation flow when email already exists` requires a very different output than one using standard conventional commits.
