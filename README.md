# books-to-stock-analysis-skill

A greenfield, research-only toolkit for turning reviewed knowledge from trading books into **auditable Agent Skills and deterministic stock-analysis rules**.

The project treats a skill as more than a summary. A published Trading Skill declares its market scope, data contract, rule expressions, rejection conditions, source provenance, and validation status. Numeric conditions are evaluated by code; an AI agent can then route, explain, compare, and challenge the structured result.

> This repository does not contain uploaded books, does not provide investment advice, and does not execute trades.

## MVP capabilities

- Typed Trading Skill IR with Pydantic.
- JSON and YAML skill documents.
- Safe expression interpreter with no Python `eval` or `exec`.
- Deterministic SMA, ATR, rolling-high, volume-ratio, and normalized log-slope features.
- Runtime evaluation with prerequisite gates, required rules, weighted confirmations, rejection vetoes, evidence, and contradictions.
- CLI commands for skill validation and evaluation.
- A synthetic volume-price-breakout example.
- Tests and GitHub Actions CI.

The complete platform design is in [`docs/DESIGN.md`](docs/DESIGN.md). PDF/OCR ingestion, multimodal chart extraction, review UI, market-data adapters, backtesting, and multi-agent orchestration are intentionally later milestones.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Python 3.11 or newer is required.

## Validate the example skill

```bash
books-to-stock-skill validate-skill \
  examples/skills/volume-price-breakout/skill.yaml
```

## Evaluate an observation

```bash
books-to-stock-skill evaluate \
  examples/skills/volume-price-breakout/skill.yaml \
  examples/skills/volume-price-breakout/observation.json
```

Expected classification:

```json
{
  "status": "partial_match",
  "match_score": 0.75
}
```

The score is a **definition match score**, not an estimated probability of future return.

## Python API

```python
from books_to_stock_analysis_skill.io.skills import load_skill
from books_to_stock_analysis_skill.runtime.evaluator import SkillEvaluator

skill = load_skill("examples/skills/volume-price-breakout/skill.yaml")
observations = {
    "bars_count": 120,
    "close": 10.85,
    "recent_high": 10.72,
    "volume_ratio": 1.63,
    "benchmark_up": False,
    "weekly_trend_up": True,
    "overextended": False,
}

result = SkillEvaluator().evaluate(skill, observations)
print(result.model_dump())
```

## Rule DSL

Allowed expression features are deliberately small:

- names supplied by the observation context;
- strings, numbers, booleans, and `None`;
- arithmetic operators;
- boolean `and`, `or`, and `not`;
- comparisons;
- direct calls to explicitly registered functions.

Attribute access, arbitrary indexing, comprehensions, lambdas, imports, and unregistered functions are rejected. See [`docs/rule-dsl.md`](docs/rule-dsl.md).

## Repository policy for books

Commercial books and page images remain private and are ignored by Git. The public repository should contain only the compiler/runtime, schemas, synthetic fixtures, original examples, and derived structures that the contributor has the right to publish.

## Development

```bash
pytest -q
ruff check .
python -m build
```

## Roadmap

1. Market-data contracts and CSV/Parquet feature pipelines.
2. PDF page model, source fragments, and private provenance store.
3. Human review workflow for extracted candidate rules.
4. Detector registry and no-look-ahead event studies.
5. Multi-skill routing, veto graphs, and evidence-based agent reports.

See [`docs/roadmap.md`](docs/roadmap.md) for acceptance criteria.

## License

Apache License 2.0. The license covers this repository's original source code and documentation, not any books processed by users.
