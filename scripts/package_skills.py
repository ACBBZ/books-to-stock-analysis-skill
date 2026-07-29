#!/usr/bin/env python3
"""Validate and package a generated Agent Skill Pack as a reproducible ZIP archive."""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

from validate_pack import SOURCE_EXTENSIONS, validate_pack


def _files(pack_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in pack_dir.rglob("*")
        if path.is_file() and path.suffix.lower() not in SOURCE_EXTENSIONS and ".git" not in path.parts
    )


def package_pack(pack_dir: Path, output: Path) -> Path:
    report = validate_pack(pack_dir)
    if not report.ok:
        details = "\n".join(report.errors)
        raise ValueError(f"Pack validation failed:\n{details}")

    files = _files(pack_dir)
    checksums = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(pack_dir)
            data = path.read_bytes()
            checksums.append(f"{hashlib.sha256(data).hexdigest()}  {relative.as_posix()}")
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
        checksum_text = "\n".join(checksums) + "\n"
        info = zipfile.ZipInfo("checksums.txt", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, checksum_text.encode("utf-8"))
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    output = args.output or args.pack.with_suffix(".zip")
    try:
        created = package_pack(args.pack, output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(created)
    return 0


if __name__ == "__main__":
    sys.exit(main())
