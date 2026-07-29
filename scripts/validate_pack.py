#!/usr/bin/env python3
"""Validate a generated investing-book Agent Skill Pack using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SOURCE_EXTENSIONS = {".pdf", ".epub", ".mobi", ".azw", ".azw3", ".docx"}
GUARANTEE_PATTERNS = (
    re.compile(r"\bguaranteed?\s+(profit|return|gain)", re.IGNORECASE),
    re.compile(r"\bwill\s+definitely\s+(rise|fall|profit)", re.IGNORECASE),
    re.compile(r"必涨|稳赚|保证收益|一定上涨|一定下跌"),
)
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def _read(path: Path, report: ValidationReport) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error(f"Cannot read UTF-8 text file {path}: {exc}")
        return ""


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip("\"'")
    return values


def _require(path: Path, report: ValidationReport) -> None:
    if not path.exists():
        report.error(f"Missing required path: {path}")


def validate_skill(skill_dir: Path, report: ValidationReport) -> None:
    required = (
        skill_dir / "SKILL.md",
        skill_dir / "references" / "provenance.yaml",
        skill_dir / "tests" / "trigger-tests.yaml",
    )
    for path in required:
        _require(path, report)

    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        text = _read(skill_file, report)
        metadata = _frontmatter(text)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not name:
            report.error(f"{skill_file}: frontmatter must contain name")
        elif not SKILL_NAME_PATTERN.fullmatch(name):
            report.error(f"{skill_file}: invalid skill name {name!r}")
        if not description or len(description) < 24:
            report.error(f"{skill_file}: description must be specific and at least 24 characters")
        for pattern in GUARANTEE_PATTERNS:
            if pattern.search(text):
                report.error(f"{skill_file}: contains guaranteed-return language")

    provenance = skill_dir / "references" / "provenance.yaml"
    if provenance.exists():
        text = _read(provenance, report)
        for key in ("source:", "locations:", "confidence:"):
            if key not in text:
                report.error(f"{provenance}: missing {key}")

    trigger_tests = skill_dir / "tests" / "trigger-tests.yaml"
    if trigger_tests.exists():
        text = _read(trigger_tests, report)
        for section in ("positive:", "negative:", "ambiguous:", "adversarial:"):
            if section not in text:
                report.error(f"{trigger_tests}: missing {section}")

    # Host-specific metadata is optional. SKILL.md is the portable source of truth.
    openai_metadata = skill_dir / "agents" / "openai.yaml"
    if openai_metadata.exists() and "interface:" not in _read(openai_metadata, report):
        report.warn(f"{openai_metadata}: expected an interface section")


def validate_pack(pack_dir: Path, allow_empty: bool = False) -> ValidationReport:
    report = ValidationReport()
    if not pack_dir.is_dir():
        report.error(f"Pack directory does not exist: {pack_dir}")
        return report

    required_root = (
        "PACK.md",
        "manifest.yaml",
        "BOOK_OVERVIEW.md",
        "INDEX.md",
        "GLOSSARY.md",
        "source-map.yaml",
        "installable",
        "provisional",
        "rejected",
        "reports/generation-report.md",
        "reports/visual-coverage.yaml",
        "reports/quality-report.yaml",
        "reports/copyright-report.yaml",
    )
    for relative in required_root:
        _require(pack_dir / relative, report)

    manifest = pack_dir / "manifest.yaml"
    if manifest.exists():
        text = _read(manifest, report)
        for key in ("schema_version:", "pack:", "book_mode:", "counts:", "skills:", "copyright:"):
            if key not in text:
                report.error(f"{manifest}: missing {key}")

    installable = pack_dir / "installable"
    skill_dirs = sorted(path for path in installable.iterdir() if path.is_dir()) if installable.is_dir() else []
    if not skill_dirs and not allow_empty:
        report.error(f"No generated skills found in {installable}")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, report)

    for path in pack_dir.rglob("*"):
        if path.is_symlink():
            report.error(f"Generated pack must not contain symlinks: {path}")
        if path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS:
            report.error(f"Source book file must not be embedded in generated pack: {path}")

    visual_report = pack_dir / "reports" / "visual-coverage.yaml"
    if visual_report.exists():
        text = _read(visual_report, report)
        if "ocr_used: false" not in text:
            report.error(f"{visual_report}: must declare ocr_used: false")
        for key in ("pages_inspected_visually:", "figures_unresolved:", "host_visual_capability:"):
            if key not in text:
                report.error(f"{visual_report}: missing {key}")

    return report


def _print_report(report: ValidationReport) -> None:
    for warning in report.warnings:
        print(f"WARN: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    print(
        f"Validation result: {'PASS' if report.ok else 'FAIL'}; "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="Generated Skill Pack directory")
    parser.add_argument("--allow-empty", action="store_true", help="Allow a pack with no generated skills")
    args = parser.parse_args(argv)
    report = validate_pack(args.pack, allow_empty=args.allow_empty)
    _print_report(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
