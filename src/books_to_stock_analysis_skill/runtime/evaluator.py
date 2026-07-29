"""Evaluate a Trading Skill against a precomputed observation context."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from books_to_stock_analysis_skill.domain.models import TradingSkill
from books_to_stock_analysis_skill.dsl.evaluator import SafeExpressionEvaluator


class ConditionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expression: str
    result: bool
    label: str
    category: Literal["prerequisite", "required", "confirmation", "rejection"]
    weight: float | None = None


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str
    skill_version: str
    status: Literal["matched", "partial_match", "not_matched", "rejected", "insufficient_data"]
    match_score: float = Field(ge=0, le=1)
    evidence: list[ConditionResult] = Field(default_factory=list)
    contradictions: list[ConditionResult] = Field(default_factory=list)
    source_fidelity_score: float = Field(ge=0, le=1)
    empirical_rating: str


class SkillEvaluator:
    """Run prerequisite gates, required rules, confirmations, and rejection vetoes."""

    def __init__(self, expression_evaluator: SafeExpressionEvaluator | None = None) -> None:
        self._expressions = expression_evaluator or SafeExpressionEvaluator()

    def evaluate(self, skill: TradingSkill, observations: Mapping[str, Any]) -> EvaluationResult:
        evidence: list[ConditionResult] = []
        contradictions: list[ConditionResult] = []

        if skill.rules.prerequisites is not None:
            prerequisites_ok = self._evaluate_group(
                skill.rules.prerequisites.all,
                "prerequisite",
                observations,
                evidence,
                contradictions,
            )
            if not prerequisites_ok:
                return self._result(skill, "insufficient_data", 0.0, evidence, contradictions)

        required_ok = self._evaluate_group(
            skill.rules.required.all,
            "required",
            observations,
            evidence,
            contradictions,
        )
        if not required_ok:
            return self._result(skill, "not_matched", 0.0, evidence, contradictions)

        if skill.rules.rejection is not None:
            for expression in skill.rules.rejection.any:
                outcome = bool(self._expressions.evaluate(expression, observations))
                item = ConditionResult(
                    expression=expression,
                    result=outcome,
                    label=expression,
                    category="rejection",
                )
                if outcome:
                    contradictions.append(item)
                    return self._result(skill, "rejected", 0.0, evidence, contradictions)
                evidence.append(item)

        confirmations = skill.rules.confirmation.score
        if not confirmations:
            return self._result(skill, "matched", 1.0, evidence, contradictions)

        total_weight = sum(item.weight for item in confirmations)
        earned_weight = 0.0
        for condition in confirmations:
            outcome = bool(self._expressions.evaluate(condition.when, observations))
            item = ConditionResult(
                expression=condition.when,
                result=outcome,
                label=condition.label or condition.when,
                category="confirmation",
                weight=condition.weight,
            )
            if outcome:
                earned_weight += condition.weight
                evidence.append(item)
            else:
                contradictions.append(item)

        score = round(earned_weight / total_weight, 10)
        status: Literal["matched", "partial_match"] = "matched" if score == 1.0 else "partial_match"
        return self._result(skill, status, score, evidence, contradictions)

    def _evaluate_group(
        self,
        expressions: list[str],
        category: Literal["prerequisite", "required"],
        observations: Mapping[str, Any],
        evidence: list[ConditionResult],
        contradictions: list[ConditionResult],
    ) -> bool:
        all_passed = True
        for expression in expressions:
            outcome = bool(self._expressions.evaluate(expression, observations))
            item = ConditionResult(
                expression=expression,
                result=outcome,
                label=expression,
                category=category,
            )
            if outcome:
                evidence.append(item)
            else:
                contradictions.append(item)
                all_passed = False
        return all_passed

    @staticmethod
    def _result(
        skill: TradingSkill,
        status: Literal["matched", "partial_match", "not_matched", "rejected", "insufficient_data"],
        score: float,
        evidence: list[ConditionResult],
        contradictions: list[ConditionResult],
    ) -> EvaluationResult:
        return EvaluationResult(
            skill_id=skill.identity.id,
            skill_version=skill.identity.version,
            status=status,
            match_score=score,
            evidence=evidence,
            contradictions=contradictions,
            source_fidelity_score=skill.provenance.source_fidelity_score,
            empirical_rating=skill.provenance.empirical_rating,
        )
