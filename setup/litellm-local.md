# Setup Guide: Local Models via LiteLLM Proxy

This guide covers how to run non-Anthropic models through Claude Code using a local LiteLLM proxy. This allows you to benchmark GPT-4o, Gemini, Mistral, Llama, and other models with the same Claude Code agent framework.

---

## How This Works

Claude Code sends requests to the Anthropic API format. LiteLLM is a proxy that accepts the Anthropic API format and translates it to whatever backend provider you configure. By pointing Claude Code at a local LiteLLM instance, you can swap the underlying model without changing anything else about the agent.

```
Claude Code → LiteLLM proxy (localhost:4000) → OpenAI / Gemini / Bedrock / Ollama / etc.
```

---

## Install LiteLLM

```bash
pip install litellm[proxy]
```

Or with uv:

```bash
uv pip install "litellm[proxy]"
```

---

## Configure LiteLLM

Create a `litellm-config.yaml` file. Examples for common providers:

### OpenAI (GPT-4o)

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: sk-...

general_settings:
  master_key: benchmark-key
```

### Google Gemini

```yaml
model_list:
  - model_name: gemini-2.5-pro
    litellm_params:
      model: gemini/gemini-2.5-pro
      api_key: AIza...

general_settings:
  master_key: benchmark-key
```

### Ollama (local models)

```yaml
model_list:
  - model_name: llama3.1
    litellm_params:
      model: ollama/llama3.1
      api_base: http://localhost:11434

general_settings:
  master_key: benchmark-key
```

### AWS Bedrock

```yaml
model_list:
  - model_name: claude-opus-4
    litellm_params:
      model: bedrock/us.anthropic.claude-opus-4-8-20251001-v1:0
      aws_region_name: us-east-1

general_settings:
  master_key: benchmark-key
```

---

## Start the Proxy

```bash
litellm --config litellm-config.yaml --port 4000
```

Verify it's running:

```bash
curl http://localhost:4000/health
```

---

## Point Claude Code at the Proxy

In a new terminal, set environment variables before starting Claude Code:

```bash
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_API_KEY=benchmark-key  # must match master_key in config
export ANTHROPIC_MODEL=gpt-4o           # must match model_name in config
```

Then start Claude Code normally:

```bash
cd /path/to/your/codebase
claude
```

---

## Verifying the Right Model is Being Used

LiteLLM logs each request. Check the proxy terminal output to confirm requests are being routed to the correct backend model.

You can also add a quick sanity check prompt at the start of each session:

```
What model are you? Just state the model name and nothing else.
```

Note that some models may not accurately self-report their identity. LiteLLM logs are the authoritative source.

---

## Limitations When Using LiteLLM

### Tool use compatibility

Claude Code relies on Anthropic's tool use format. LiteLLM translates this, but not all models support all tool types equally. Specifically:

- Models with weak function-calling support may fail or hallucinate tool calls
- Models with small context windows may struggle with long file reads
- Some local models (Ollama) have limited tool call reliability

If a model fails to use tools correctly, note this in your results — it is a meaningful capability difference, not a benchmark error.

### Context window differences

Claude Code may attempt to read large files or many files simultaneously. Models with smaller context windows (e.g. 32k vs 200k) will fail on tasks that require reading many files at once. This is expected and should be noted in results.

### Rate limits

If using a cloud provider through LiteLLM, apply the same rate limit handling as you would normally. The benchmark does not specify a time limit per task, so running into rate limits and waiting is acceptable.

---

## Comparing Results Across Providers

When submitting results for a non-Anthropic model, include in your results:

- The LiteLLM version used
- The exact model name and version as reported by the provider
- The date the API was accessed (model versions can change silently)
- Any tool use failures or context window issues observed

This allows readers to understand and reproduce your results.
