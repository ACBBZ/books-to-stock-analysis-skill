#!/usr/bin/env python3
"""Activate generated Agent Skills for OpenClaw, Hermes, or Claude Code.

The command validates a pack, then copies every accepted skill under
PACK/installable into the active host's native skill directory. It is intended
to run automatically after book conversion, so users do not need a second
manual install step.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from validate_pack import validate_pack

SUPPORTED_HOSTS = ("openclaw", "hermes", "claude-code")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ActivationError(RuntimeError):
    """Raised when a pack cannot be activated safely."""


@dataclass
class ActivationReport:
    host: str
    target_root: Path
    activated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _frontmatter_name(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ActivationError(f"{skill_file}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ActivationError(f"{skill_file}: unterminated YAML frontmatter")
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() == "name":
            name = value.strip().strip("\"'")
            if not SKILL_NAME_PATTERN.fullmatch(name):
                raise ActivationError(f"{skill_file}: invalid skill name {name!r}")
            return name
    raise ActivationError(f"{skill_file}: frontmatter must contain name")


def _tree_digest(root: Path) -> str:
    if root.is_symlink():
        raise ActivationError(f"Symlinked skill directories are not allowed: {root}")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        if path.is_symlink():
            raise ActivationError(f"Symlinks are not allowed in generated skills: {path}")
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def discover_skills(pack_dir: Path) -> list[tuple[str, Path]]:
    installable = pack_dir / "installable"
    if not installable.is_dir():
        raise ActivationError(f"Missing installable directory: {installable}")

    skills: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for skill_dir in sorted(path for path in installable.iterdir() if path.is_dir()):
        if skill_dir.is_symlink():
            raise ActivationError(f"Symlinked skill directories are not allowed: {skill_dir}")
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise ActivationError(f"Missing SKILL.md: {skill_dir}")
        name = _frontmatter_name(skill_file)
        if name in seen:
            raise ActivationError(f"Duplicate generated skill name: {name}")
        seen.add(name)
        skills.append((name, skill_dir))

    if not skills:
        raise ActivationError(f"No generated skills found in {installable}")
    return skills


def detect_host(workspace: Path) -> str:
    explicit = os.environ.get("BOOK_SKILL_HOST")
    if explicit:
        if explicit not in SUPPORTED_HOSTS:
            raise ActivationError(
                f"BOOK_SKILL_HOST must be one of {', '.join(SUPPORTED_HOSTS)}"
            )
        return explicit

    markers: list[str] = []
    if (workspace / ".claude").exists():
        markers.append("claude-code")
    if (workspace / ".openclaw").exists() or os.environ.get("OPENCLAW_STATE_DIR"):
        markers.append("openclaw")
    if os.environ.get("HERMES_HOME"):
        markers.append("hermes")

    if len(set(markers)) == 1:
        return markers[0]

    commands = {
        "openclaw": shutil.which("openclaw"),
        "hermes": shutil.which("hermes"),
        "claude-code": shutil.which("claude"),
    }
    available = [name for name, command in commands.items() if command]
    if len(available) == 1:
        return available[0]

    raise ActivationError(
        "Cannot determine the active host safely. Pass --host openclaw, "
        "--host hermes, or --host claude-code."
    )


def target_root_for(host: str, workspace: Path, home: Path, scope: str) -> Path:
    if host not in SUPPORTED_HOSTS:
        raise ActivationError(f"Unsupported host: {host}")

    effective_scope = scope
    if scope == "auto":
        effective_scope = "global" if host == "hermes" else "project"

    if effective_scope == "project":
        if host == "claude-code":
            return workspace / ".claude" / "skills"
        return workspace / ".agents" / "skills"

    if host == "claude-code":
        return home / ".claude" / "skills"
    if host == "openclaw":
        state_dir = Path(os.environ.get("OPENCLAW_STATE_DIR", home / ".openclaw"))
        return state_dir.expanduser() / "skills"
    hermes_home = Path(os.environ.get("HERMES_HOME", home / ".hermes"))
    return hermes_home.expanduser() / "skills"


def _copy_skill(source: Path, destination: Path, force: bool) -> str:
    source_digest = _tree_digest(source)
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink():
            raise ActivationError(f"Activation target must not be a symlink: {destination}")
        if not destination.is_dir():
            raise ActivationError(f"Activation target is not a directory: {destination}")
        destination_digest = _tree_digest(destination)
        if source_digest == destination_digest:
            return "unchanged"
        if not force:
            raise ActivationError(
                f"{destination} already exists with different content; pass --force to replace it"
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".book-skill-",
        dir=destination.parent,
    ) as temp_dir:
        staged = Path(temp_dir) / destination.name
        shutil.copytree(source, staged)
        _tree_digest(staged)
        if destination.exists():
            shutil.rmtree(destination)
        staged.replace(destination)
    return "activated"


def _write_report(pack_dir: Path, report: ActivationReport) -> Path:
    report_path = pack_dir / "reports" / "activation-report.yaml"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        'schema_version: "1.0"',
        f"host: {report.host}",
        f'target_root: "{report.target_root.as_posix()}"',
        "activated:",
    ]
    lines.extend(f"  - {name}" for name in report.activated)
    lines.append("unchanged:")
    lines.extend(f"  - {name}" for name in report.unchanged)
    lines.append("warnings:")
    safe_warnings = (warning.replace('"', "'") for warning in report.warnings)
    lines.extend(f'  - "{warning}"' for warning in safe_warnings)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def activate_pack(
    pack_dir: Path,
    *,
    host: str,
    workspace: Path,
    home: Path,
    scope: str = "auto",
    force: bool = False,
    target_root: Path | None = None,
) -> ActivationReport:
    pack_dir = pack_dir.resolve()
    workspace = workspace.resolve()
    home = home.expanduser().resolve()

    validation = validate_pack(pack_dir)
    if not validation.ok:
        details = "\n".join(validation.errors)
        raise ActivationError(f"Pack validation failed:\n{details}")

    if host == "auto":
        host = detect_host(workspace)

    target = (
        target_root.expanduser().resolve()
        if target_root is not None
        else target_root_for(host, workspace, home, scope).resolve()
    )
    report = ActivationReport(host=host, target_root=target)

    for name, source in discover_skills(pack_dir):
        status = _copy_skill(source, target / name, force=force)
        if status == "activated":
            report.activated.append(name)
        else:
            report.unchanged.append(name)

    if host == "hermes" and scope == "project":
        report.warnings.append(
            "Hermes project activation uses .agents/skills; ensure that path is listed "
            "under skills.external_dirs in ~/.hermes/config.yaml."
        )
    if host == "openclaw":
        report.warnings.append(
            "The parent meta-skill can use generated skills immediately. Native slash-command "
            "discovery may refresh on the next OpenClaw turn or session."
        )
    if host == "claude-code":
        report.warnings.append(
            "Claude Code hot-reloads skills when its skills root is already watched. "
            "The parent meta-skill remains the same-session fallback."
        )

    _write_report(pack_dir, report)
    return report


def _print_report(report: ActivationReport) -> None:
    print(f"Host: {report.host}")
    print(f"Target: {report.target_root}")
    for name in report.activated:
        print(f"ACTIVATED: {name}")
    for name in report.unchanged:
        print(f"UNCHANGED: {name}")
    for warning in report.warnings:
        print(f"WARN: {warning}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="Generated Skill Pack directory")
    parser.add_argument(
        "--host",
        choices=("auto", *SUPPORTED_HOSTS),
        default="auto",
        help="Target agent host",
    )
    parser.add_argument(
        "--scope",
        choices=("auto", "project", "global"),
        default="auto",
        help="Auto uses project scope for OpenClaw/Claude Code and global scope for Hermes",
    )
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--target-root", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = activate_pack(
            args.pack,
            host=args.host,
            workspace=args.workspace,
            home=args.home,
            scope=args.scope,
            force=args.force,
            target_root=args.target_root,
        )
    except (ActivationError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    _print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
