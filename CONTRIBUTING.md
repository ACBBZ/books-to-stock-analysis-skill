# Contributing

Contributions are welcome when they preserve the project's narrow role: converting user-provided investing sources into copyright-aware, source-traceable Agent Skill Packs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
```

## Requirements

- Keep the repository root installable as an Agent Skill.
- Do not add OCR engines or OCR service dependencies.
- Use native text layers and direct multimodal page inspection.
- Do not add live market-data, brokerage, order-execution, or portfolio-management features to the core project.
- Add or update tests before changing deterministic validators or packaging behavior.
- Keep undefined source parameters explicit; never attribute invented thresholds to an author.
- Do not commit copyrighted books, scans, long quotations, private notes, API keys, or brokerage credentials.
- Generated strategy skills must state that source fidelity is not evidence of profitability.
