#!/usr/bin/env python3
"""Validate the single-skill package and its cross-harness contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "gap"


def _frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)}: missing frontmatter")
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, match.group(2)


def _base_version(version: str) -> str:
    return version.split("+", 1)[0]


def _read_required(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def validate_repository() -> list[str]:
    errors: list[str] = []

    skill_dirs = sorted(
        path.name for path in (ROOT / "skills").iterdir() if path.is_dir()
    )
    if skill_dirs != ["gap"]:
        errors.append(f"skills/: expected only ['gap'], found {skill_dirs}")

    skill_md = SKILL / "SKILL.md"
    try:
        metadata, body = _frontmatter(skill_md)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        metadata, body = {}, ""

    if metadata.get("name") != "gap":
        errors.append("skills/gap/SKILL.md: name must be 'gap'")
    description = metadata.get("description", "")
    for phrase in ("ambiguous", "governed", "Skip simple"):
        if phrase not in description:
            errors.append(f"skills/gap/SKILL.md: description missing '{phrase}'")
    if "disable-model-invocation" in metadata:
        errors.append("skills/gap/SKILL.md: invocation policy belongs in agents/openai.yaml")

    required_refs = {
        "discovery.md",
        "planning.md",
        "problem-solving.md",
        "delivery.md",
        "communication.md",
        "governance.md",
        "retrospective.md",
        "adoption.md",
    }
    actual_refs = {
        path.name for path in (SKILL / "references").glob("*.md")
    }
    if actual_refs != required_refs:
        errors.append(
            f"skills/gap/references: expected {sorted(required_refs)}, "
            f"found {sorted(actual_refs)}"
        )

    required_assets = {
        "state.md",
        "intent.md",
        "spec.md",
        "plan.md",
        "review.md",
        "harness-backlog.md",
        "evolution-log.md",
    }
    actual_assets = {path.name for path in (SKILL / "assets").glob("*.md")}
    if actual_assets != required_assets:
        errors.append(
            f"skills/gap/assets: expected {sorted(required_assets)}, "
            f"found {sorted(actual_assets)}"
        )

    markdown_sources = sorted(ROOT.rglob("*.md"))
    for source in markdown_sources:
        source_text = source.read_text(encoding="utf-8")
        if not source_text.strip():
            errors.append(f"{source.relative_to(ROOT)}: empty Markdown file")
            continue
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", source_text):
            if "://" in target or target.startswith("#"):
                continue
            target_path = target.split("#", 1)[0]
            if not (source.parent / target_path).exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: broken link '{target}'"
                )

    invariants = {
        "Quick route": "**Quick**",
        "Standard route": "**Standard**",
        "Governed route": "**Governed**",
        "read-only default": "Start read-only",
        "durable/working split": "working state separate from durable evidence",
        "evidence limit": "what was not verified",
        "governed completion boundary": "Awaiting authorization is not completion",
    }
    for label, phrase in invariants.items():
        if phrase not in body:
            errors.append(f"skills/gap/SKILL.md: missing {label}")

    adoption = _read_required(SKILL / "references" / "adoption.md", errors)
    for phrase in ("Read-only inventory", "Apply only the approved items", ".agents/skills"):
        if phrase not in adoption:
            errors.append(f"references/adoption.md: missing '{phrase}'")

    delivery = _read_required(SKILL / "references" / "delivery.md", errors)
    for phrase in (
        "Intent/spec",
        "Engineering",
        "Do not collapse the axes",
        "Bounded repair loop",
        "budget exhaustion is not completion",
        "independence was not achieved",
    ):
        if phrase not in delivery:
            errors.append(f"references/delivery.md: missing '{phrase}'")

    governance = _read_required(SKILL / "references" / "governance.md", errors)
    for phrase in ("Protected gate", "fresh explicit authorization", "shell-command substring"):
        if phrase not in governance:
            errors.append(f"references/governance.md: missing '{phrase}'")

    problem_solving = _read_required(
        SKILL / "references" / "problem-solving.md", errors
    )
    for phrase in ("tight feedback loop", "3–5 ranked", "Deletion test", "Merge conflicts"):
        if phrase not in problem_solving:
            errors.append(f"references/problem-solving.md: missing '{phrase}'")

    communication = _read_required(
        SKILL / "references" / "communication.md", errors
    )
    for phrase in ("Use concise Markdown", "self-contained HTML", "view, not a second specification"):
        if phrase not in communication:
            errors.append(f"references/communication.md: missing '{phrase}'")

    openai_yaml = SKILL / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append("skills/gap/agents/openai.yaml: missing")
    else:
        text = openai_yaml.read_text(encoding="utf-8")
        for phrase in ("display_name:", "short_description:", "allow_implicit_invocation: true"):
            if phrase not in text:
                errors.append(f"agents/openai.yaml: missing '{phrase}'")

    try:
        claude_manifest = json.loads(
            (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        codex_manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"plugin manifest: {exc}")
        claude_manifest, codex_manifest = {}, {}

    for label, manifest in (("Claude", claude_manifest), ("Codex", codex_manifest)):
        if manifest.get("name") != "gap-skills":
            errors.append(f"{label} manifest: name must be gap-skills")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:\+[0-9A-Za-z.-]+)?", manifest.get("version", "")):
            errors.append(f"{label} manifest: invalid version")
    if claude_manifest.get("skills") != ["./skills/gap"]:
        errors.append("Claude manifest: must expose only ./skills/gap")
    if codex_manifest.get("skills") != "./skills/":
        errors.append("Codex manifest: skills must be ./skills/")
    if _base_version(claude_manifest.get("version", "")) != _base_version(
        codex_manifest.get("version", "")
    ):
        errors.append("plugin manifests: base versions differ")

    case_files = (
        Path("cases/activation.json"),
        Path("cases/workflows.json"),
    )
    loaded_cases: dict[str, list[dict[str, object]]] = {}
    for relative in case_files:
        try:
            cases = json.loads((ROOT / "tests" / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"tests/{relative}: {exc}")
            continue
        if not isinstance(cases, list) or not cases:
            errors.append(f"tests/{relative}: expected a non-empty list")
            continue
        loaded_cases[relative.name] = cases

    fixture_files = (
        ".gitignore",
        "AGENTS.md",
        "README.md",
        "src/invitations.py",
        "tests/test_invitations.py",
    )
    for fixture_name in ("quick-project", "standard-invitation"):
        fixture = ROOT / "tests" / "fixtures" / fixture_name
        for relative in fixture_files:
            if not (fixture / relative).is_file():
                errors.append(f"tests/fixtures/{fixture_name}/{relative}: missing")

    workflow_cases = loaded_cases.get("workflows.json", [])
    standard_case = next(
        (case for case in workflow_cases if case.get("id") == "standard-ambiguous-feature"),
        {},
    )
    for key in ("fixture", "hidden_evaluator", "reference_solution", "budget"):
        if key not in standard_case:
            errors.append(f"tests/cases/workflows.json: Standard MVP missing '{key}'")
    for key in ("fixture", "hidden_evaluator", "reference_solution"):
        relative = standard_case.get(key)
        if isinstance(relative, str) and not (ROOT / relative).exists():
            errors.append(f"tests/cases/workflows.json: missing {key} path '{relative}'")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print("\n".join(errors))
        return 1
    reference_count = len(list((SKILL / "references").glob("*.md")))
    asset_count = len(list((SKILL / "assets").glob("*.md")))
    print(f"OK — 1 skill, {reference_count} references, {asset_count} assets, 2 manifests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
