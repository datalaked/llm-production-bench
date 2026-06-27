# B3 — Extract Duplicated Code to Shared Utility

**Category:** B — Targeted Changes  
**Estimated time (human):** 20–45 min  
**Requires writing code:** Yes

---

## Objective

Ask the agent to find a meaningful case of duplicated logic in the codebase and extract it into a shared utility — without changing behavior.

---

## Prompt

```
Find a meaningful case of duplicated business logic in this codebase — code that appears in multiple places and should be extracted into a shared utility.

Do not count duplicated boilerplate (e.g. repeated imports, identical error handling stubs). Look for actual logic: data transformation, validation, computation, or query patterns that are copy-pasted across multiple files.

Once you've found a good candidate:
1. Create or extend a utility module in the appropriate location (follow the project's existing convention for shared utilities)
2. Move the shared logic into the utility
3. Update all call sites to use the shared utility
4. Make sure the behavior at each call site is identical to before the refactor
5. Write a brief explanation of what you extracted and why it was a good candidate

Do not change any behavior. Do not add features. Only move code.
```

---

## What to Evaluate

A strong response will:
- Find genuinely duplicated logic (not superficially similar code with different semantics)
- Place the shared utility in the right location according to project conventions
- Update all call sites (not just the ones it found first)
- Preserve behavior — the refactored code should be a pure extraction, not an opportunity to "improve" logic
- Write a clear, brief explanation

A weak response will:
- Extract trivial boilerplate (a single line, an import)
- Miss some call sites
- Change behavior during the extraction (even subtly)
- Place the utility in an arbitrary location that doesn't follow project conventions
- Extract code that isn't actually duplicated (just similar-looking)

---

## Scoring Notes

- **5:** Found real, meaningful duplication. Extraction is clean, placed correctly, all call sites updated, behavior preserved. Explanation is accurate.
- **4:** Good candidate, good extraction, one call site missed or utility placement slightly off.
- **3:** Real duplication found, but extraction has minor behavior drift or misses 2+ call sites.
- **2:** Duplication found but extraction is incorrect (wrong abstraction, wrong location, behavior change).
- **1:** Extracted trivial boilerplate, or extracted code that isn't actually duplicated.
- **0:** Refused, broke existing functionality, or found no duplication where it clearly exists.

---

## Notes for Evaluators

Run the test suite after applying the refactor if one exists. Behavior drift is often subtle — the model might handle a None case differently, or change the order of operations in a way that doesn't matter in existing tests but would matter in production.

Check that all call sites were updated by searching for the original duplicated pattern. It's common for the model to update the two most obvious sites and miss a third.
