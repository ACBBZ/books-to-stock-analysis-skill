"""Command-line interface for validating and evaluating Trading Skills."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from books_to_stock_analysis_skill.io.skills import load_observations, load_skill
from books_to_stock_analysis_skill.runtime.evaluator import SkillEvaluator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="books-to-stock-skill",
        description="Validate and deterministically evaluate trading-book skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate-skill", help="Validate a JSON or YAML Trading Skill document.")
    validate_parser.add_argument("skill", help="Path to a .json, .yaml, or .yml skill document.")

    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate a skill against an observation JSON/YAML object.",
    )
    evaluate_parser.add_argument("skill", help="Path to the Trading Skill document.")
    evaluate_parser.add_argument("observations", help="Path to the observation document.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate-skill":
        skill = load_skill(args.skill)
        output = {
            "valid": True,
            "schema_version": skill.schema_version,
            "id": skill.identity.id,
            "name": skill.identity.name,
            "version": skill.identity.version,
            "status": skill.identity.status,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    if args.command == "evaluate":
        skill = load_skill(args.skill)
        observations = load_observations(args.observations)
        result = SkillEvaluator().evaluate(skill, observations)
        print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0

    raise RuntimeError(f"Unhandled command: {args.command}")


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
