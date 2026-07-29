from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import activate_pack  # noqa: E402


def _write(path: Path, content: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    skill = pack / "installable" / "demo-skill"
    _write(
        skill / "SKILL.md",
        "---\nname: demo-skill\n"
        "description: Demo source-grounded skill for testing automatic activation.\n"
        "---\n# Demo\n",
    )
    _write(
        skill / "references" / "provenance.yaml",
        "source:\n  locations: []\nconfidence:\n  extraction: 1.0\n",
    )
    _write(
        skill / "tests" / "trigger-tests.yaml",
        "positive: []\nnegative: []\nambiguous: []\nadversarial: []\n",
    )
    return pack


def test_claude_project_activation(tmp_path: Path) -> None:
    pack = _pack(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    report = activate_pack.activate_pack(
        pack,
        host="claude-code",
        workspace=workspace,
        home=tmp_path / "home",
    )

    assert (workspace / ".claude" / "skills" / "demo-skill" / "SKILL.md").exists()
    assert report.activated == ["demo-skill"]
    assert (pack / "reports" / "activation-report.yaml").exists()


def test_openclaw_project_activation(tmp_path: Path) -> None:
    pack = _pack(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    activate_pack.activate_pack(
        pack,
        host="openclaw",
        workspace=workspace,
        home=tmp_path / "home",
    )

    assert (workspace / ".agents" / "skills" / "demo-skill" / "SKILL.md").exists()


def test_hermes_auto_scope_is_global(tmp_path: Path) -> None:
    pack = _pack(tmp_path)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    home = tmp_path / "home"

    activate_pack.activate_pack(
        pack,
        host="hermes",
        workspace=workspace,
        home=home,
    )

    assert (home / ".hermes" / "skills" / "demo-skill" / "SKILL.md").exists()


def test_different_existing_skill_requires_force(tmp_path: Path) -> None:
    pack = _pack(tmp_path)
    workspace = tmp_path / "workspace"
    destination = workspace / ".claude" / "skills" / "demo-skill" / "SKILL.md"
    _write(destination, "different\n")

    with pytest.raises(activate_pack.ActivationError):
        activate_pack.activate_pack(
            pack,
            host="claude-code",
            workspace=workspace,
            home=tmp_path / "home",
        )

    report = activate_pack.activate_pack(
        pack,
        host="claude-code",
        workspace=workspace,
        home=tmp_path / "home",
        force=True,
    )
    assert report.activated == ["demo-skill"]


def test_symlink_is_rejected(tmp_path: Path) -> None:
    pack = _pack(tmp_path)
    outside = tmp_path / "outside.txt"
    _write(outside, "secret\n")
    (pack / "installable" / "demo-skill" / "linked.txt").symlink_to(outside)

    with pytest.raises(activate_pack.ActivationError):
        activate_pack.activate_pack(
            pack,
            host="openclaw",
            workspace=tmp_path / "workspace",
            home=tmp_path / "home",
        )
