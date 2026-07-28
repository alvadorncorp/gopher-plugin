#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests/fixtures/forward-tests.json"
SCHEMA_PATH = ROOT / "tests/fixtures/response-schema.json"
HARNESSES = ("codex", "claude", "grok")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_corpus(payload):
    errors = []
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["cases must be a non-empty array"]
    ids = []
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        for field in ("id", "prompt", "expected", "tags"):
            if field not in case:
                errors.append(f"{prefix}: missing {field}")
        if isinstance(case.get("id"), str):
            ids.append(case["id"])
        if not isinstance(case.get("expected"), dict) or "selected_skill" not in case.get("expected", {}):
            errors.append(f"{prefix}: expected.selected_skill is required")
        if not isinstance(case.get("tags"), list) or not case.get("tags"):
            errors.append(f"{prefix}: tags must be non-empty")
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicates:
        errors.append(f"duplicate case ids: {duplicates}")
    selected_skills = {case.get("expected", {}).get("selected_skill") for case in cases}
    required = {"gopher:design-patterns", "gopher:application-architecture", "gopher:developer", "gopher:architecture", "gopher:concurrency-performance", "gopher:diagnose", "gopher:security", "gopher:review", "gopher:config", "gopher:complexity", "gopher:test-quality", "gopher:modernize", "gopher:refactor"}
    if not required.issubset(selected_skills):
        errors.append(f"routing coverage missing skills: {sorted(required - selected_skills)}")
    return errors


def get_path(value, dotted):
    current = value
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def compare_expected(actual, expected):
    failures = []
    for key, wanted in expected.items():
        try:
            got = get_path(actual, key)
        except KeyError:
            failures.append(f"missing {key}")
            continue
        if got != wanted:
            failures.append(f"{key}: expected {wanted!r}, got {got!r}")
    return failures


def wrapped_prompt(case):
    return ("Use the installed Gopher plugin naturally for the request below. Return only a JSON object matching the provided schema. Set selected_skill to the canonical Gopher skill handling the request; keep primary_owner for the terminal owner after attribution or handoff. Use exact logical mode names and perform no writes or external actions.\n\nUser request:\n" + case["prompt"])


def run_codex(case, timeout):
    with tempfile.TemporaryDirectory(prefix="gopher-codex-") as temp_dir:
        output = Path(temp_dir) / "last.json"
        command = ["codex", "exec", "--ephemeral", "--sandbox", "read-only", "--cd", str(ROOT), "--output-schema", str(SCHEMA_PATH), "--output-last-message", str(output), wrapped_prompt(case)]
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
        return json.loads(output.read_text(encoding="utf-8"))


def run_claude(case, timeout):
    schema = json.dumps(load_json(SCHEMA_PATH), separators=(",", ":"))
    command = ["claude", "--print", "--no-session-persistence", "--permission-mode", "dontAsk", "--tools", "", "--output-format", "json", "--json-schema", schema, wrapped_prompt(case)]
    completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    payload = json.loads(completed.stdout)
    value = payload.get("structured_output", payload.get("result", payload))
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise RuntimeError("Claude returned no structured object")
    return value


def _coerce_structured(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise RuntimeError("empty structured payload")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start < 0 or end <= start:
                raise
            parsed = json.loads(text[start : end + 1])
        if isinstance(parsed, dict):
            return parsed
    raise RuntimeError("structured payload is not an object")


def run_grok(case, timeout):
    schema = json.dumps(load_json(SCHEMA_PATH), separators=(",", ":"))
    command = [
        "grok",
        "-p",
        wrapped_prompt(case),
        "--cwd",
        str(ROOT),
        "--json-schema",
        schema,
        "--output-format",
        "json",
        "--permission-mode",
        "dontAsk",
        "--tools",
        "",
        "--no-subagents",
    ]
    completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    payload = json.loads(completed.stdout)
    for key in ("structured_output", "result", "text"):
        if key in payload:
            try:
                return _coerce_structured(payload[key])
            except (RuntimeError, json.JSONDecodeError):
                continue
    return _coerce_structured(payload)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Gopher forward tests on Codex, Claude, and Grok")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--harness", action="append", choices=HARNESSES)
    parser.add_argument("--case", default="*")
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    payload = load_json(CASES_PATH)
    errors = validate_corpus(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    cases = [case for case in payload["cases"] if fnmatch.fnmatch(case["id"], args.case)]
    if args.max_cases is not None:
        cases = cases[: args.max_cases]
    if not cases:
        print("ERROR: case filter selected no cases")
        return 1
    harnesses = args.harness or list(HARNESSES)
    if args.validate_only:
        print(f"Validated {len(payload['cases'])} forward-test cases for codex, claude, and grok.")
        return 0
    runners = {"codex": run_codex, "claude": run_claude, "grok": run_grok}
    results = []
    failed = False
    for harness in harnesses:
        for case in cases:
            record = {"harness": harness, "case": case["id"]}
            try:
                actual = runners[harness](case, args.timeout)
                failures = compare_expected(actual, case["expected"])
                record.update(actual=actual, failures=failures, passed=not failures)
                failed = failed or bool(failures)
            except Exception as exc:
                record.update(error=str(exc), passed=False)
                failed = True
            results.append(record)
    report = {"cases": [case["id"] for case in cases], "harnesses": harnesses, "results": results}
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if failed:
        print("Forward tests failed", file=sys.stderr)
        return 1
    print(f"Forward tests passed: {len(cases)} cases x {len(harnesses)} harnesses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
