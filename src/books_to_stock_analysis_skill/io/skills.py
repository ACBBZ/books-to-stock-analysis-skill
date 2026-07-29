"""Load Trading Skill IR and observation documents from JSON or YAML."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from books_to_stock_analysis_skill.domain.models import TradingSkill


class DocumentLoadError(ValueError):
    """Raised when an input document cannot be parsed into the expected structure."""


def _load_mapping(path: str | Path) -> dict[str, Any]:
    document_path = Path(path)
    if not document_path.is_file():
        raise DocumentLoadError(f"Document does not exist: {document_path}")
    try:
        text = document_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DocumentLoadError(f"Could not read document: {document_path}") from exc

    try:
        if document_path.suffix.lower() == ".json":
            value = json.loads(text)
        elif document_path.suffix.lower() in {".yaml", ".yml"}:
            value = yaml.safe_load(text)
        else:
            raise DocumentLoadError("Supported document formats are .json, .yaml, and .yml")
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise DocumentLoadError(f"Invalid document syntax in {document_path}: {exc}") from exc

    if not isinstance(value, dict):
        raise DocumentLoadError(f"Document root must be an object: {document_path}")
    return value


def load_skill(path: str | Path) -> TradingSkill:
    """Load and validate a Trading Skill document."""
    return TradingSkill.model_validate(_load_mapping(path))


def load_observations(path: str | Path) -> dict[str, Any]:
    """Load an observation context passed to the deterministic evaluator."""
    return _load_mapping(path)
