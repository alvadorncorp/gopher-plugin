#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/gopher"
SKILLS = PLUGIN / "skills"
FIXTURE = ROOT / "tests/fixtures/expected-layout.json"

FORBIDDEN_PLACEHOLDERS = (
    "[TO" + "DO:",
    "T" + "BD",
    "implement " + "later",
    "fill in " + "details",
)

# Repository documentation is English-only. These markers target repeated prose
# and headings across published and planning documents. Extend the list when a
# regression exposes another repeated non-English documentation phrase.
PORTUGUESE_MARKERS = (
    "## " + "context" + "o",
    "## decis" + "\u00e3" + "o",
    "## consequ" + "\u00ea" + "ncias",
    "## alternativ" + "as",
    "## ri" + "scos",
    "## plan" + "o de",
    " n" + "\u00e3" + "o ",
    " valida" + "\u00e7\u00e3" + "o ",
    " arqui" + "tetura ",
    " evid" + "\u00eancia ",
    " refer" + "\u00eancias:",
)

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
CATALOG_ROW = re.compile(r"^\| (pattern\.[a-z0-9-]+) \| (full|diagnostic|deferred|boundary) \|")
MAPPING_ROW = re.compile(r"^\| `(pattern\.[a-z0-9-]+)` \| `(go\.[a-z0-9-]+)` \|")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(path: Path):
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("missing YAML frontmatter")
    metadata = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")) or ":" not in raw_line:
            raise ValueError(f"unsupported frontmatter line: {raw_line!r}")
        key, scalar = raw_line.split(":", 1)
        scalar = scalar.strip()
        if len(scalar) >= 2 and scalar[0] == scalar[-1] and scalar[0] in {'"', "'"}:
            scalar = scalar[1:-1]
        metadata[key.strip()] = scalar
    if not metadata:
        raise ValueError("frontmatter is not an object")
    return metadata


def repository_markdown():
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {".git", ".worktrees"}:
            continue
        yield path


def catalog():
    path = SKILLS / "design-patterns/references/diagnostics.md"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CATALOG_ROW.match(line)
        if match:
            rows.append(match.groups())
    return rows


def mapping_rows():
    rows = []
    for path in (
        SKILLS / "developer/references/pattern-mappings.md",
        SKILLS / "architecture/references/pattern-mappings.md",
        SKILLS / "concurrency-performance/references/pattern-mappings.md",
    ):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = MAPPING_ROW.match(line)
            if match:
                rows.append((path, *match.groups()))
    return rows


def validate_repository() -> list[str]:
    expected = load_json(FIXTURE)
    errors: list[str] = []

    codex_market = load_json(ROOT / ".agents/plugins/marketplace.json")
    claude_market = load_json(ROOT / ".claude-plugin/marketplace.json")
    codex_plugin = load_json(PLUGIN / ".codex-plugin/plugin.json")
    claude_plugin = load_json(PLUGIN / ".claude-plugin/plugin.json")

    if codex_market.get("name") != expected["marketplace_name"]:
        errors.append("Codex marketplace name mismatch")
    if claude_market.get("name") != expected["marketplace_name"]:
        errors.append("Claude marketplace name mismatch")
    for key in ("name", "version", "description", "author"):
        if codex_plugin.get(key) != claude_plugin.get(key):
            errors.append(f"plugin manifest parity mismatch: {key}")
    if codex_plugin.get("name") != expected["plugin_name"]:
        errors.append("plugin name mismatch")
    if codex_plugin.get("version") != expected["plugin_version"]:
        errors.append("plugin version mismatch")

    actual_skills = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    expected_skills = set(expected["skills"])
    if actual_skills != expected_skills:
        errors.append(
            f"skill inventory mismatch: expected={sorted(expected_skills)} actual={sorted(actual_skills)}"
        )

    reference_count = 0
    for skill_name, expected_refs in expected["skills"].items():
        skill = SKILLS / skill_name
        skill_md = skill / "SKILL.md"
        agent_yaml = skill / "agents/openai.yaml"
        if not skill_md.is_file():
            errors.append(f"{skill_name}: missing SKILL.md")
            continue
        if not agent_yaml.is_file():
            errors.append(f"{skill_name}: missing agents/openai.yaml")
        try:
            metadata = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{skill_name}: {exc}")
            metadata = {}
        if metadata.get("name") != skill_name:
            errors.append(f"{skill_name}: frontmatter name mismatch")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{skill_name}: missing description")
        if len(skill_md.read_text(encoding="utf-8").splitlines()) >= 500:
            errors.append(f"{skill_name}: SKILL.md must remain below 500 lines")

        actual_refs = sorted(
            str(path.relative_to(skill)).replace("\\", "/")
            for path in (skill / "references").rglob("*.md")
        )
        if actual_refs != expected_refs:
            errors.append(
                f"{skill_name}: reference mismatch expected={expected_refs} actual={actual_refs}"
            )
        reference_count += len(actual_refs)

    expected_reference_total = sum(len(refs) for refs in expected["skills"].values())
    if reference_count != expected_reference_total:
        errors.append(
            f"expected {expected_reference_total} references, found {reference_count}"
        )

    for path in PLUGIN.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {path.relative_to(ROOT)}")
    for forbidden in ("hooks", "assets", ".mcp.json", ".app.json", ".lsp.json"):
        if (PLUGIN / forbidden).exists():
            errors.append(f"v1 optional component is present: {forbidden}")

    for path in repository_markdown():
        text = path.read_text(encoding="utf-8")
        lower = f" {text.lower()} "
        for marker in FORBIDDEN_PLACEHOLDERS:
            if marker.lower() in lower:
                errors.append(f"placeholder {marker!r} in {path.relative_to(ROOT)}")
        for marker in PORTUGUESE_MARKERS:
            if marker in lower:
                errors.append(
                    f"documentation must be English; marker {marker!r} in {path.relative_to(ROOT)}"
                )

    catalog_rows = catalog()
    catalog_ids = [row[0] for row in catalog_rows]
    dispositions = {kind: sum(row[1] == kind for row in catalog_rows) for kind in (
        "full", "diagnostic", "deferred", "boundary"
    )}
    if len(catalog_ids) != 36 or len(set(catalog_ids)) != 36:
        errors.append("catalog must contain 36 unique pattern IDs")
    if dispositions != {"full": 19, "diagnostic": 10, "deferred": 4, "boundary": 3}:
        errors.append(f"catalog disposition mismatch: {dispositions}")

    mapped_general = []
    for path, general_id, go_id in mapping_rows():
        if general_id not in set(catalog_ids):
            errors.append(f"unknown mapping source {general_id} in {path.relative_to(ROOT)}")
        if not go_id.startswith("go."):
            errors.append(f"invalid Go mapping {go_id} in {path.relative_to(ROOT)}")
        mapped_general.append(general_id)
    duplicates = sorted({item for item in mapped_general if mapped_general.count(item) > 1})
    if duplicates:
        errors.append(f"general pattern IDs have multiple Go owners: {duplicates}")

    review_refs = SKILLS / "review/references"
    lenses = sorted(path.stem for path in (review_refs / "lenses").glob("*.md"))
    harnesses = sorted(path.stem for path in (review_refs / "harnesses").glob("*.md"))
    if lenses != expected["review_lenses"]:
        errors.append(f"review lens mismatch: {lenses}")
    if harnesses != expected["review_harnesses"]:
        errors.append(f"review harness mismatch: {harnesses}")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    expected = load_json(FIXTURE)
    skill_count = len(expected["skills"])
    reference_total = sum(len(refs) for refs in expected["skills"].values())
    print(
        f"Repository validation passed ({skill_count} skills, "
        f"{reference_total} references, 2 manifests, 2 marketplaces)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
