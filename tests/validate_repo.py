#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/gopher"
SKILLS = PLUGIN / "skills"
AGENTS = PLUGIN / "agents"
OPENCODE_AGENTS = AGENTS / "opencode"
OMP_AGENTS = PLUGIN / "omp/agents"
FIXTURE = ROOT / "tests/fixtures/expected-layout.json"

CODEX_AGENT_KEYS = {"name", "description", "sandbox_mode", "developer_instructions"}
# A packaged agent carries a binding and a constraint envelope. Restating the
# wrapped skill's own surface is what makes the two drift apart. This is a
# bounded gate, not a proof of non-duplication: it names headings and field
# labels, so prose that reproduces a workflow without them still passes.
AGENT_BANNED_SURFACE = (
    "## Workflow", "## Output format", "## Modes", "## Quality checklist",
    "## References", "## Authorization", "selected_skill:", "primary_owner:", "references/",
)
# A line count measures wrap width rather than content: reflowing a body to
# narrow columns trips it, while a whole SKILL.md body pasted unwrapped slips
# under it. Collapse whitespace and cap the characters instead. Calibration: the
# smallest wrapped skill body is over 4000 normalized characters and the largest
# agent body is under 3000, so this cap separates the two. Headroom is thin, so
# an agent that needs more should shed envelope prose rather than raise it.
AGENT_BODY_MAX_CHARS = 3000

# `parse_frontmatter` strips quotes and does nothing else, so its value agrees
# with a real YAML parser only for an unambiguous plain scalar. A leading
# indicator character, a colon-space, an inline ` #` comment, or a backslash
# escape all make the host's parsed string differ from the one compared here, so
# an agent description that carries any of them is rejected outright.
YAML_INDICATOR_LEADERS = "-?:,[]{}#&*!|>'\"%@`"

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
DOCTOR_RULE_ROW = re.compile(
    r"^\| `([a-z]+\.[a-z-]+)` \| `(gopher:[a-z-]+)` \| ([a-z, ]+) \| ([a-z]+) \| (yes|no) \|"
)
DOCTOR_PROFILE_ROW = re.compile(
    r"^\| `([a-z]+\.[a-z-]+)` \| ([a-z]+) \|([^|]*)\|([^|]*)\|([^|]*)\|"
)
DOCTOR_PROFILE_NAMES = ("quick", "standard", "strict")


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


def agent_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    return text[match.end():] if match else text


def normalized_size(text: str) -> int:
    return len(" ".join(text.split()))


def plain_scalar_problem(value: str) -> str | None:
    """Reject anything a real YAML parser would read differently from the flat
    parser above. See `YAML_INDICATOR_LEADERS` for why this has to be strict."""
    if not value.strip():
        return "must not be empty"
    if value[0] in YAML_INDICATOR_LEADERS:
        return f"must not start with the YAML indicator {value[0]!r}"
    if ": " in value:
        return "must not contain a colon-space"
    if " #" in value:
        return "must not contain an inline comment marker"
    if "\\" in value:
        return "must not contain a backslash"
    return None


def validate_agents(expected) -> list[str]:
    errors: list[str] = []
    spec = expected.get("agents")
    if not isinstance(spec, dict):
        return ["layout fixture declares no agents"]
    required = {
        "markdown", "codex", "skill_ids", "frontmatter", "codex_sandbox",
        "policy_contract_marker", "policy_status_values",
    }
    absent = sorted(required - set(spec))
    if absent:
        return [f"layout fixture agents block is missing {absent}"]
    marker = spec["policy_contract_marker"]
    statuses = spec["policy_status_values"]

    codex_dir = AGENTS / "codex"
    md_names = sorted(path.name for path in AGENTS.glob("*.md")) if AGENTS.is_dir() else []
    toml_names = sorted(path.name for path in codex_dir.glob("*.toml")) if codex_dir.is_dir() else []
    if md_names != spec["markdown"]:
        errors.append(f"agent markdown mismatch: expected={spec['markdown']} actual={md_names}")
    if toml_names != spec["codex"]:
        errors.append(f"codex agent mismatch: expected={spec['codex']} actual={toml_names}")

    for role, skill_id in sorted(spec["skill_ids"].items()):
        markdown = AGENTS / f"{role}.md"
        codex_path = codex_dir / f"{role}.toml"
        if not markdown.is_file() or not codex_path.is_file():
            errors.append(f"{role}: missing packaged agent pair")
            continue
        try:
            metadata = parse_frontmatter(markdown)
        except ValueError as exc:
            errors.append(f"agents/{role}.md: {exc}")
            continue

        if metadata.get("name") != role:
            errors.append(f"agents/{role}.md: frontmatter name must match the filename")
        description = metadata.get("description", "")
        problem = plain_scalar_problem(description)
        if problem:
            errors.append(f"agents/{role}.md: description {problem}")
        pinned = spec["frontmatter"].get(role)
        if not isinstance(pinned, dict):
            errors.append(f"agents/{role}.md: fixture declares no frontmatter for this role")
            pinned = {}
        # This exact key-set check already rejects every unsupported key, so no
        # separate allow-list runs beside it and one defect yields one error.
        if set(metadata) - {"name", "description"} != set(pinned):
            errors.append(f"agents/{role}.md: frontmatter key set must match the fixture exactly")
        for key, value in pinned.items():
            if metadata.get(key) != value:
                errors.append(
                    f"agents/{role}.md: {key} expected {value!r}, found {metadata.get(key)!r}"
                )

        body = agent_body(markdown)
        if skill_id not in body:
            errors.append(f"agents/{role}.md: body must delegate to {skill_id}")
        if marker not in body:
            errors.append(f"agents/{role}.md: body must carry the shared policy contract sentence")
        for status in statuses:
            if status not in body:
                errors.append(f"agents/{role}.md: body must report policy_status {status}")
        for banned in AGENT_BANNED_SURFACE:
            if banned in body:
                errors.append(f"agents/{role}.md: body duplicates the skill surface ({banned!r})")
        size = normalized_size(body)
        if size > AGENT_BODY_MAX_CHARS:
            errors.append(
                f"agents/{role}.md: body must stay a thin wrapper "
                f"({size} normalized characters, cap {AGENT_BODY_MAX_CHARS})"
            )

        try:
            with codex_path.open("rb") as handle:
                codex = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"agents/codex/{role}.toml: {exc}")
            continue
        if set(codex) != CODEX_AGENT_KEYS:
            errors.append(
                f"agents/codex/{role}.toml: key set must be exactly {sorted(CODEX_AGENT_KEYS)}"
            )
        if codex.get("name") != role:
            errors.append(f"agents/codex/{role}.toml: name must match the filename")
        if codex.get("description") != description:
            errors.append(f"{role}: Claude and Codex descriptions must be identical")
        sandbox = spec["codex_sandbox"].get(role)
        if sandbox is None:
            errors.append(f"agents/codex/{role}.toml: fixture declares no sandbox for this role")
        elif codex.get("sandbox_mode") != sandbox:
            errors.append(f"agents/codex/{role}.toml: sandbox_mode expected {sandbox!r}")
        instructions = codex.get("developer_instructions", "")
        reference = "$" + skill_id.split(":", 1)[1]
        if reference not in instructions:
            errors.append(f"agents/codex/{role}.toml: instructions must reference {reference}")
        if marker not in instructions:
            errors.append(
                f"agents/codex/{role}.toml: instructions must carry the shared policy contract sentence"
            )
        for status in statuses:
            if status not in instructions:
                errors.append(
                    f"agents/codex/{role}.toml: instructions must report policy_status {status}"
                )
        for banned in AGENT_BANNED_SURFACE:
            if banned in instructions:
                errors.append(
                    f"agents/codex/{role}.toml: instructions duplicate the skill surface ({banned!r})"
                )
        size = normalized_size(instructions)
        if size > AGENT_BODY_MAX_CHARS:
            errors.append(
                f"agents/codex/{role}.toml: instructions must stay a thin wrapper "
                f"({size} normalized characters, cap {AGENT_BODY_MAX_CHARS})"
            )
    return errors


def validate_opencode_package(expected) -> list[str]:
    errors: list[str] = []
    package_path = ROOT / "package.json"
    if not package_path.is_file():
        return ["missing OpenCode package.json"]
    package = load_json(package_path)
    if package.get("name") != "@alvadorncorp/gopher":
        errors.append("OpenCode package name mismatch")
    if package.get("main") != "plugins/gopher/opencode/plugin.js":
        errors.append("OpenCode package main mismatch")
    if package.get("engines", {}).get("opencode") != ">=1.18.15":
        errors.append("OpenCode package engine mismatch")
    if package.get("version") != load_json(PLUGIN / ".codex-plugin/plugin.json").get("version"):
        errors.append("OpenCode package version mismatch")
    entry = PLUGIN / "opencode/plugin.js"
    if not entry.is_file():
        errors.append("missing OpenCode plugin entry")
    spec = expected.get("agents", {})
    expected_agents = spec.get("opencode")
    ids = spec.get("opencode_agent_ids")
    actual_agents = sorted(path.name for path in OPENCODE_AGENTS.glob("*.md")) if OPENCODE_AGENTS.is_dir() else []
    if actual_agents != expected_agents:
        errors.append(f"OpenCode agent mismatch: expected={expected_agents} actual={actual_agents}")
    if not isinstance(ids, dict):
        return errors + ["layout fixture declares no OpenCode agent ids"]
    for role, agent_id in sorted(ids.items()):
        path = OPENCODE_AGENTS / f"{role}.md"
        if not path.is_file():
            continue
        try:
            metadata = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"agents/opencode/{role}.md: {exc}")
            continue
        if metadata.get("name") != agent_id:
            errors.append(f"agents/opencode/{role}.md: name must be {agent_id}")
        if not metadata.get("description"):
            errors.append(f"agents/opencode/{role}.md: missing description")
        body = agent_body(path)
        skill = {"architect": "architecture", "developer": "developer", "reviewer": "review"}[role]
        if f"`{skill}` skill" not in body:
            errors.append(f"agents/opencode/{role}.md: body must load {skill}")
        if "declared policy may narrow this agent and it can never widen it" not in body:
            errors.append(f"agents/opencode/{role}.md: missing policy contract")
    return errors


def validate_omp_agents(expected) -> list[str]:
    errors: list[str] = []
    spec = expected.get("agents")
    if not isinstance(spec, dict):
        return ["layout fixture declares no agents"]
    expected_agents = spec.get("omp")
    ids = spec.get("omp_agent_ids")
    pinned = spec.get("omp_frontmatter")
    if not isinstance(expected_agents, list):
        return ["layout fixture declares no omp agents"]
    if not isinstance(ids, dict):
        return errors + ["layout fixture declares no omp agent ids"]
    if not isinstance(pinned, dict):
        return errors + ["layout fixture declares no omp frontmatter"]

    actual_agents = sorted(path.name for path in OMP_AGENTS.glob("*.md")) if OMP_AGENTS.is_dir() else []
    if actual_agents != expected_agents:
        errors.append(f"omp agent mismatch: expected={expected_agents} actual={actual_agents}")

    seen_names: list[str] = []
    for role, agent_id in sorted(ids.items()):
        path = OMP_AGENTS / f"{role}.md"
        rel = f"omp/agents/{role}.md"
        if not path.is_file():
            errors.append(f"{rel}: missing packaged omp agent")
            continue
        try:
            metadata = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        name = metadata.get("name")
        if name != agent_id:
            errors.append(f"{rel}: frontmatter name must be {agent_id}")
        if not isinstance(name, str) or not name.startswith("gopher-"):
            errors.append(f"{rel}: frontmatter name must use the gopher- prefix")
        if isinstance(name, str):
            if name in seen_names:
                errors.append(f"{rel}: duplicate omp agent name {name}")
            seen_names.append(name)

        description = metadata.get("description", "")
        problem = plain_scalar_problem(description)
        if problem:
            errors.append(f"{rel}: description {problem}")

        role_pins = pinned.get(role)
        if not isinstance(role_pins, dict):
            errors.append(f"{rel}: fixture declares no frontmatter for this role")
            role_pins = {}
        if set(metadata) - {"name", "description"} != set(role_pins):
            errors.append(f"{rel}: frontmatter key set must match the fixture exactly")
        for key, value in role_pins.items():
            if metadata.get(key) != value:
                errors.append(f"{rel}: {key} expected {value!r}, found {metadata.get(key)!r}")

        skill = role_pins.get("autoloadSkills")
        if isinstance(skill, str) and skill and not (SKILLS / skill / "SKILL.md").is_file():
            errors.append(f"{rel}: autoloadSkills {skill!r} has no skill directory")

        body = agent_body(path)
        size = normalized_size(body)
        if size > AGENT_BODY_MAX_CHARS:
            errors.append(
                f"{rel}: body must stay a thin wrapper "
                f"({size} normalized characters, cap {AGENT_BODY_MAX_CHARS})"
            )
    return errors


def validate_doctor_catalog() -> list[str]:
    """The rule count and the three profile counts are written out in prose in
    two files. Derive them from the tables so a moved row fails here first."""
    errors: list[str] = []
    rules_text = (SKILLS / "doctor/references/rules.md").read_text(encoding="utf-8")
    profiles_text = (SKILLS / "doctor/references/profiles.md").read_text(encoding="utf-8")

    rules: dict[str, tuple[set[str], bool]] = {}
    for line in rules_text.splitlines():
        match = DOCTOR_RULE_ROW.match(line)
        if match:
            rule_id, _owner, declared, _cost, blocking = match.groups()
            rules[rule_id] = ({item.strip() for item in declared.split(",")}, blocking == "yes")
    if len(rules) != 11:
        errors.append(f"doctor catalog must contain 11 rules, found {len(rules)}")
    block_eligible = sorted(rule for rule, (_, flag) in rules.items() if flag)
    if len(block_eligible) != 3:
        errors.append(f"doctor must declare 3 block-eligible rules, found {block_eligible}")

    matrix: dict[str, set[str]] = {}
    for line in profiles_text.splitlines():
        match = DOCTOR_PROFILE_ROW.match(line)
        if match:
            cells = match.group(3), match.group(4), match.group(5)
            matrix[match.group(1)] = {
                name for name, cell in zip(DOCTOR_PROFILE_NAMES, cells) if cell.strip() == "yes"
            }
    if set(matrix) != set(rules):
        errors.append("doctor profile matrix and rule catalog list different rules")
    counts = {name: sum(name in row for row in matrix.values()) for name in DOCTOR_PROFILE_NAMES}
    if counts != {"quick": 6, "standard": 9, "strict": 11}:
        errors.append(f"doctor profile counts mismatch: {counts}")
    for rule_id, profiles in sorted(matrix.items()):
        declared = rules.get(rule_id, (set(), False))[0]
        if declared != profiles:
            errors.append(
                f"doctor rule {rule_id}: rules.md declares {sorted(declared)} "
                f"and profiles.md declares {sorted(profiles)}"
            )

    for phrase, text, label in (
        ("Eleven rules, and only these eleven", rules_text, "rules.md rule count"),
        ("Three of the eleven rules are block-eligible", rules_text, "rules.md blocking count"),
        ("Six rules,", profiles_text, "profiles.md quick count"),
        ("Nine rules:", profiles_text, "profiles.md standard count"),
        ("All eleven rules:", profiles_text, "profiles.md strict count"),
    ):
        if phrase not in text:
            errors.append(f"{label} prose disagrees with the derived count ({phrase!r})")
    return errors


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
        SKILLS / "concurrency/references/pattern-mappings.md",
        SKILLS / "performance/references/pattern-mappings.md",
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
    grok_market = load_json(ROOT / ".grok-plugin/marketplace.json")
    omp_market = load_json(ROOT / ".omp-plugin/marketplace.json")
    kimi_market = load_json(ROOT / ".kimi-plugin/marketplace.json")
    codex_plugin = load_json(PLUGIN / ".codex-plugin/plugin.json")
    claude_plugin = load_json(PLUGIN / ".claude-plugin/plugin.json")
    grok_plugin = load_json(PLUGIN / ".grok-plugin/plugin.json")
    kimi_plugin = load_json(PLUGIN / ".kimi-plugin/plugin.json")

    if codex_market.get("name") != expected["marketplace_name"]:
        errors.append("Codex marketplace name mismatch")
    if claude_market.get("name") != expected["marketplace_name"]:
        errors.append("Claude marketplace name mismatch")
    if grok_market.get("name") != expected["marketplace_name"]:
        errors.append("Grok marketplace name mismatch")
    if kimi_market.get("name") != expected["marketplace_name"]:
        errors.append("Kimi marketplace name mismatch")
    if omp_market.get("name") != expected["marketplace_name"]:
        errors.append("omp marketplace name mismatch")
    # Official host packaging validators own catalog/manifest version compatibility.
    # This repository gate preserves identity, source, and cross-manifest parity
    # without copying a release number into the structural layout fixture.
    for key in ("name", "version", "description", "author"):
        if codex_plugin.get(key) != claude_plugin.get(key):
            errors.append(f"plugin manifest parity mismatch: {key}")
        if codex_plugin.get(key) != grok_plugin.get(key):
            errors.append(f"plugin manifest parity mismatch (grok): {key}")
        if codex_plugin.get(key) != kimi_plugin.get(key):
            errors.append(f"plugin manifest parity mismatch (kimi): {key}")
    if codex_plugin.get("name") != expected["plugin_name"]:
        errors.append("plugin name mismatch")
    grok_source = (grok_market.get("plugins") or [{}])[0].get("source")
    if not isinstance(grok_source, dict) or grok_source.get("path") != "./plugins/gopher":
        errors.append("Grok marketplace source path mismatch")
    kimi_source = (kimi_market.get("plugins") or [{}])[0].get("source")
    if kimi_source != "./plugins/gopher":
        errors.append("Kimi marketplace source path mismatch")
    omp_source = (omp_market.get("plugins") or [{}])[0].get("source")
    if omp_source != "./plugins/gopher":
        errors.append("omp marketplace source path mismatch")

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
    if dispositions != {"full": 23, "diagnostic": 10, "deferred": 0, "boundary": 3}:
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

    errors.extend(validate_agents(expected))
    errors.extend(validate_opencode_package(expected))
    errors.extend(validate_omp_agents(expected))
    errors.extend(validate_doctor_catalog())

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
    agent_count = len(expected["agents"]["skill_ids"])
    print(
        f"Repository validation passed ({skill_count} skills, "
        f"{reference_total} references, {agent_count} agents, "
        f"4 manifests, 5 marketplaces, and 1 OpenCode package)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
