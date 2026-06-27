# Setup Guide: Claude Code as Agent

This guide covers how to set up Claude Code as the benchmark agent. Claude Code is the reference agent for this benchmark — results using Claude Code are directly comparable across model choices.

---

## Prerequisites

- Node.js 18+ installed
- An Anthropic API key (for Claude models) or compatible API key (for other providers via LiteLLM)
- Access to the codebase you want to benchmark

---

## Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify the installation:

```bash
claude --version
```

---

## Configure Your API Key

For Claude models directly:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

For other models via LiteLLM proxy, see [`setup/litellm-local.md`](litellm-local.md).

---

## Point Claude Code at a Different Model

Claude Code supports model overrides via environment variable or flag.

**Via environment variable:**
```bash
export ANTHROPIC_MODEL=claude-opus-4-8
# or
export ANTHROPIC_MODEL=claude-sonnet-4-6
```

**Via flag at invocation:**
```bash
claude --model claude-opus-4-8
```

When using a LiteLLM proxy to test non-Anthropic models, set the base URL:

```bash
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_API_KEY=anything  # LiteLLM accepts any key value
export ANTHROPIC_MODEL=gpt-4o      # or whatever model your proxy exposes
```

---

## Running a Benchmark Task

1. Navigate to the codebase you're benchmarking:
   ```bash
   cd /path/to/your/production/codebase
   ```

2. Start a fresh Claude Code session for each task:
   ```bash
   claude
   ```

3. Paste the task prompt from the relevant task file (e.g. `tasks/A-reading/A1-architecture.md`).

4. Let the agent run to completion. Do not intervene or provide hints.

5. Copy the final output for scoring.

---

## Important: Session Isolation

**Run each task in a fresh session.** Do not carry context from one task to the next.

Why: Context from prior tasks (especially reading tasks) can artificially improve performance on later tasks. The benchmark assumes each task is run cold.

To start a fresh session in Claude Code, close the terminal or start a new `claude` invocation. Do not use `/continue` or provide prior task outputs as context.

---

## Reproducibility Settings

To maximize reproducibility across runs and models, use these settings when available:

| Setting | Value |
|---------|-------|
| Temperature | 0 or as low as possible |
| Max tokens | Default (do not reduce) |
| System prompt | Do not add custom system prompts |
| Tools | Default Claude Code tools (no additions or removals) |

Note: Claude Code does not expose a temperature setting directly. The default is used. This is consistent across all model runs if you use Claude Code as the agent.

---

## Logging the Run

Keep a log of each task run:

- The exact prompt used
- The model and version
- The timestamp
- The full output (before scoring)

Claude Code generates a session transcript. You can find it at:

```
~/.claude/projects/<hash>/sessions/<session-id>.jsonl
```

This is useful if you need to re-score or share the raw output.

---

## Known Limitations

- Claude Code's tool use (file reads, shell commands) counts as part of the agent's work. Do not interrupt or redirect tool calls.
- If Claude Code asks a clarifying question, answer minimally ("no preference", "use your judgment"). Do not provide hints about the correct answer.
- Some tasks (C1, C3) require you to provide a traceback or migration file. Do this by pasting it into the initial prompt — do not use a separate file unless the task instructions say to.
