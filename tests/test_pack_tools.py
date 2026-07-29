from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import package_skills  # noqa: E402
import validate_pack  # noqa: E402


def _write(path: Path, content: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _valid_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "book-pack"
    for name in ("PACK.md", "BOOK_OVERVIEW.md", "INDEX.md", "GLOSSARY.md", "source-map.yaml"):
        _write(pack / name)
    _write(
        pack / "manifest.yaml",
        "schema_version: '1.0'\npack:\n  id: demo\nbook_mode: [technical_analysis]\n"
        "counts:\n  installable: 1\nskills: []\ncopyright:\n  source_files_embedded: false\n",
    )
    for directory in ("provisional", "rejected"):
        (pack / directory).mkdir(parents=True)
    _write(pack / "reports" / "generation-report.md")
    _write(
        pack / "reports" / "visual-coverage.yaml",
        "pages_inspected_visually: []\nfigures_unresolved: []\n"
        "host_visual_capability: available\nocr_used: false\n",
    )
    _write(pack / "reports" / "quality-report.yaml")
    _write(pack / "reports" / "copyright-report.yaml")

    skill = pack / "installable" / "demo-skill"
    _write(
        skill / "SKILL.md",
        "---\nname: demo-skill\ndescription: Use for a specific source-grounded demonstration workflow.\n---\n# Goal\n",
    )
    _write(skill / "agents" / "openai.yaml", "interface:\n  display_name: Demo\n")
    _write(
        skill / "references" / "provenance.yaml",
        "source:\n  locations: []\nconfidence:\n  extraction: 1.0\n",
    )
    _write(
        skill / "tests" / "trigger-tests.yaml",
        "positive: []\nnegative: []\nambiguous: []\nadversarial: []\n",
    )
    return pack


def test_valid_pack_passes(tmp_path: Path) -> None:
    report = validate_pack.validate_pack(_valid_pack(tmp_path))
    assert report.ok, report.errors


def test_missing_provenance_fails(tmp_path: Path) -> None:
    pack = _valid_pack(tmp_path)
    (pack / "installable" / "demo-skill" / "references" / "provenance.yaml").unlink()
    report = validate_pack.validate_pack(pack)
    assert not report.ok
    assert any("provenance.yaml" in error for error in report.errors)


def test_packaging_is_reproducible_and_excludes_source_books(tmp_path: Path) -> None:
    pack = _valid_pack(tmp_path)
    first = package_skills.package_pack(pack, tmp_path / "first.zip")
    second = package_skills.package_pack(pack, tmp_path / "second.zip")
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        assert "checksums.txt" in archive.namelist()
        assert not any(name.endswith(".pdf") for name in archive.namelist())
