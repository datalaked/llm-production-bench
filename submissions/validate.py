#!/usr/bin/env python3
"""Validate YAML benchmark submissions against submissions/schema.yaml.

Usage:
    python submissions/validate.py submissions/results/my-run.yaml [more.yaml ...]
    python submissions/validate.py          # validates all files in submissions/results/

Requires: pyyaml, jsonschema  (pip install pyyaml jsonschema)
"""

import sys
import re
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml jsonschema")

try:
    import jsonschema
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml jsonschema")


SCHEMA_PATH = Path(__file__).parent / "schema.yaml"
RESULTS_DIR = Path(__file__).parent / "results"

TASK_CATEGORIES = {
    "A": ["A1", "A2", "A3"],
    "B": ["B1", "B2", "B3"],
    "C": ["C1", "C2", "C3"],
    "D": ["D1", "D2", "D3", "D4"],
}

# Approximate bytes-per-parameter for common quant formats
QUANT_BYTES_PER_PARAM = {
    "Q2_K": 0.28,
    "Q3_K_S": 0.36, "Q3_K_M": 0.40, "Q3_K_L": 0.42,
    "Q4_0": 0.50, "Q4_K_S": 0.50, "Q4_K_M": 0.55, "Q4_K": 0.55,
    "Q5_0": 0.63, "Q5_K_M": 0.67, "Q5_K": 0.67,
    "Q6_K": 0.75,
    "Q8_0": 1.00, "Q8": 1.00,
    "F16": 2.00, "BF16": 2.00,
    "F32": 4.00,
}

# Plausibility bounds: time_seconds × tok_per_sec_measured
MIN_PLAUSIBLE_TOKENS = 10        # an absurdly short response
MAX_PLAUSIBLE_TOKENS = 200_000   # an absurdly long single-task response

# Ratio beyond which we warn that nominal vs measured tok/s diverge too much
TOK_PER_SEC_RATIO_WARN = 3.0


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return yaml.safe_load(f)


def _safe_get(data: dict, *keys, default=None):
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
        if data is None:
            return default
    return data


def validate_submission(path: Path, schema: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single submission file."""
    errors: list[str] = []
    warnings: list[str] = []

    # ---- YAML parse --------------------------------------------------------
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        return [f"YAML parse error: {exc}"], []

    if not isinstance(data, dict):
        return ["Submission must be a YAML mapping at the top level"], []

    # ---- JSON Schema validation --------------------------------------------
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as exc:
        path_str = ".".join(str(p) for p in exc.absolute_path) or "<root>"
        errors.append(f"Schema violation at {path_str}: {exc.message}")
    except jsonschema.SchemaError as exc:
        errors.append(f"Internal schema error (report a bug): {exc.message}")

    # After a schema error the structure may be malformed; still run checks
    # that operate on optional/partial data so we surface as many issues as
    # possible in one pass.

    # ---- Date validity -----------------------------------------------------
    raw_date = _safe_get(data, "metadata", "date", default="")
    try:
        datetime.strptime(str(raw_date), "%Y-%m-%d")
    except ValueError:
        errors.append(
            f"metadata.date '{raw_date}' is not a valid calendar date (expected YYYY-MM-DD)"
        )

    # ---- MoE consistency ---------------------------------------------------
    model = data.get("model") or {}
    arch = model.get("architecture")
    total_b = model.get("total_params_b") or 0
    active_b = model.get("active_params_b")

    if arch == "moe":
        if active_b is None:
            errors.append(
                "model.active_params_b is required for MoE architecture models"
            )
        elif active_b >= total_b and total_b > 0:
            errors.append(
                f"model.active_params_b ({active_b}B) must be less than "
                f"model.total_params_b ({total_b}B) for a MoE model"
            )

    if arch == "dense" and active_b is not None and total_b > 0:
        if abs(active_b - total_b) / total_b > 0.01:
            warnings.append(
                f"model.active_params_b ({active_b}B) differs from total_params_b ({total_b}B) "
                f"but architecture is 'dense' — all parameters should be active. "
                f"Did you mean architecture: moe?"
            )

    # ---- Category coverage -------------------------------------------------
    results = data.get("results") or {}
    non_dq_tasks = {
        task_id
        for task_id, result in results.items()
        if isinstance(result, dict) and not result.get("disqualified", False)
    }
    cats_covered = {
        cat
        for cat, tasks in TASK_CATEGORIES.items()
        if any(t in non_dq_tasks for t in tasks)
    }

    if len(non_dq_tasks) < 5:
        errors.append(
            f"At least 5 non-disqualified task results required (found {len(non_dq_tasks)}). "
            f"See CONTRIBUTING.md for minimum coverage requirements."
        )
    if len(cats_covered) < 2:
        errors.append(
            f"Results must cover at least 2 task categories (A/B/C/D). "
            f"Found {len(cats_covered)}: {sorted(cats_covered) or 'none'}."
        )

    # ---- Per-task checks ---------------------------------------------------
    for task_id, result in results.items():
        if not isinstance(result, dict):
            errors.append(f"results.{task_id}: must be a mapping")
            continue

        is_dq = result.get("disqualified", False)

        if is_dq and "quality_1_to_5" in result:
            warnings.append(
                f"results.{task_id}: quality_1_to_5 is set but disqualified=true — "
                f"score will be excluded from aggregates"
            )

        if not is_dq and "quality_1_to_5" not in result and "time_seconds" in result:
            warnings.append(
                f"results.{task_id}: has time_seconds but no quality_1_to_5 score"
            )

    # ---- Time × tok/s plausibility -----------------------------------------
    measured_tps = _safe_get(data, "integrity", "tok_per_sec_measured")
    if measured_tps and measured_tps > 0:
        for task_id, result in results.items():
            if not isinstance(result, dict) or result.get("disqualified"):
                continue
            t = result.get("time_seconds")
            if t and t > 0:
                estimated_tokens = t * measured_tps
                if estimated_tokens < MIN_PLAUSIBLE_TOKENS:
                    errors.append(
                        f"results.{task_id}: time_seconds={t}s × tok_per_sec_measured="
                        f"{measured_tps} ≈ {estimated_tokens:.0f} tokens — "
                        f"implausibly low (minimum ~{MIN_PLAUSIBLE_TOKENS} tokens for any response). "
                        f"Check that time_seconds is in seconds, not milliseconds."
                    )
                elif estimated_tokens > MAX_PLAUSIBLE_TOKENS:
                    warnings.append(
                        f"results.{task_id}: time_seconds={t}s × tok_per_sec_measured="
                        f"{measured_tps} ≈ {int(estimated_tokens):,} tokens — "
                        f"unusually high (>{MAX_PLAUSIBLE_TOKENS:,} tokens for a single task). "
                        f"Verify time_seconds is accurate."
                    )

    # ---- Nominal vs measured tok/s ratio -----------------------------------
    hw_nominal = _safe_get(data, "hardware", "tok_per_sec_generation")
    if hw_nominal and hw_nominal > 0 and measured_tps and measured_tps > 0:
        ratio = measured_tps / hw_nominal
        if ratio < (1 / TOK_PER_SEC_RATIO_WARN) or ratio > TOK_PER_SEC_RATIO_WARN:
            warnings.append(
                f"integrity.tok_per_sec_measured ({measured_tps} t/s) differs substantially "
                f"from hardware.tok_per_sec_generation ({hw_nominal} t/s) — ratio={ratio:.2f}x. "
                f"hardware.tok_per_sec_generation is a hardware baseline; "
                f"tok_per_sec_measured is the actual run average. "
                f"A {ratio:.1f}x difference is unusual unless caused by thermal throttling "
                f"or heavy context lengths."
            )

    # ---- Memory estimate (warning only) ------------------------------------
    hw = data.get("hardware") or {}
    quant_raw = (model.get("quant") or "").upper().replace("-", "_")
    bytes_per = QUANT_BYTES_PER_PARAM.get(quant_raw)
    mem_type = hw.get("memory_type", "")
    mem_gb = hw.get("memory_gb") or 0

    if bytes_per and total_b > 0 and mem_type not in ("system",) and mem_gb > 0:
        model_size_gb = total_b * bytes_per
        # For ram+vram the model spills into system RAM; allow 4× the VRAM
        factor = 4.0 if mem_type == "ram+vram" else 1.2
        if model_size_gb > mem_gb * factor:
            warnings.append(
                f"Model weight estimate: {total_b}B × {bytes_per} bytes/param ≈ "
                f"{model_size_gb:.1f}GB, but hardware.memory_gb={mem_gb}GB "
                f"(memory_type={mem_type}). "
                f"This may require more aggressive quantization or additional CPU offloading "
                f"than reported. Verify hardware.memory_gb and memory_type are correct."
            )

    # ---- git_commit_hash format --------------------------------------------
    commit = _safe_get(data, "integrity", "git_commit_hash", default="")
    if commit and not re.fullmatch(r"[0-9a-f]{40}", str(commit)):
        errors.append(
            f"integrity.git_commit_hash must be a 40-character lowercase hex SHA-1 "
            f"(got: '{commit}'). Run: git rev-parse HEAD"
        )

    return errors, warnings


def main() -> int:
    schema = load_schema()

    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = sorted(RESULTS_DIR.glob("*.yaml"))
        if not paths:
            print(f"No *.yaml files found in {RESULTS_DIR}")
            return 0

    total_invalid = 0

    for path in paths:
        if not path.exists():
            print(f"\n--- {path} ---")
            print(f"  ERROR  File not found: {path}")
            total_invalid += 1
            continue

        errors, warnings = validate_submission(path, schema)

        print(f"\n--- {path.name} ---")
        for msg in warnings:
            print(f"  WARN   {msg}")
        for msg in errors:
            print(f"  ERROR  {msg}")

        if errors:
            total_invalid += 1
            print(f"  INVALID  ({len(errors)} error(s), {len(warnings)} warning(s))")
        else:
            print(f"  OK  ({len(warnings)} warning(s))")

    print()
    if total_invalid == 0:
        print(f"All {len(paths)} submission(s) valid.")
        return 0
    else:
        print(f"{total_invalid}/{len(paths)} submission(s) invalid.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
