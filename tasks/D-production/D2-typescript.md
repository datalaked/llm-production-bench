# D2 — Fix TypeScript `any` Usages

**Category:** D — Production-Grade Work  
**Estimated time (human):** 30–60 min  
**Requires writing code:** Yes

---

## Objective

Ask the agent to audit the codebase for TypeScript `any` usages and replace them with accurate types, without breaking existing behavior.

---

## Prompt

```
This codebase uses TypeScript. Audit it for usages of `any` that should be replaced with proper types.

Do not change every `any` — only the ones where a more accurate type can be derived from context. Skip:
- `any` in test files where it's used for mocking
- `any` in third-party type declarations you didn't write
- `any` in places where `unknown` with a type guard is clearly the right answer but would require significant refactoring

For each `any` you fix:
1. Replace it with the most accurate type you can derive from how the value is actually used
2. Do not use `as any` as a workaround — the fix must be a real type
3. If fixing one `any` reveals that a downstream value also needs a type, fix that too

After making your changes:
- Run `tsc --noEmit` to verify no new type errors were introduced
- Write a summary of what you changed and why

Aim to fix at least 5 meaningful `any` usages.
```

---

## What to Evaluate

A strong response will:
- Identify `any` usages that are actually fixable (not just every `any` in the codebase)
- Derive accurate types from how the values are actually used — not just substitute `unknown`
- Handle downstream type propagation (fixing one `any` often reveals others)
- Pass `tsc --noEmit` without new errors
- Write accurate types that match runtime behavior

A weak response will:
- Replace `any` with `unknown` everywhere without adding type guards (technically safer, but not more useful)
- Introduce types that are too broad (e.g. `Record<string, unknown>` when a specific interface is derivable)
- Miss obvious type opportunities
- Introduce new `tsc` errors while fixing old ones
- Fix `any` usages that were intentional (e.g. necessary `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with a comment explaining why)

---

## Scoring Notes

- **5:** Fixed meaningful `any` usages with accurate types. No new `tsc` errors. Downstream propagation handled. Summary is accurate.
- **4:** Fixed real usages with mostly accurate types, one or two are slightly too broad. No new errors.
- **3:** Fixed real usages but types are mostly `unknown` or too broad. No new errors.
- **2:** Fixed trivial or unimportant usages while missing significant ones, or introduced new `tsc` errors.
- **1:** Replaced `any` with `unknown` everywhere or made changes that are mechanically correct but semantically useless.
- **0:** Refused, introduced breaking type errors, or the TypeScript now errors on valid code.

---

## Notes for Evaluators

Run `tsc --noEmit` before and after and diff the output. A good fix has the same or fewer errors. Any new errors introduced by the fix are a regression.

This task is only applicable to codebases with TypeScript. If the codebase is Python-only, skip this task or adapt it to mypy / missing type annotations.
