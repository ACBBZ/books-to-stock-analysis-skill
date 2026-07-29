# Contributing

Contributions are welcome when they preserve the project's research-only and evidence-first boundaries.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
```

## Requirements

- Add or update tests before production behavior changes.
- Do not use `eval` or `exec` for rule execution.
- Do not commit copyrighted books, scans, private market data, API keys, or brokerage credentials.
- Keep deterministic calculations separate from LLM interpretation.
- Document whether a change affects source fidelity, empirical validation, or both.
