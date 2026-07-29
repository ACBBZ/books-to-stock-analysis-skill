"""Pydantic models for the versioned Trading Skill intermediate representation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Identity(StrictModel):
    id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9-]*$")
    name: str = Field(min_length=1)
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    locale: str = "zh-CN"
    status: Literal["draft", "reviewed", "published", "deprecated"] = "draft"


class Classification(StrictModel):
    type: Literal[
        "concept",
        "principle",
        "pattern",
        "strategy",
        "risk_rule",
        "anti_pattern",
        "market_regime",
        "execution_guideline",
        "psychology",
    ]
    intents: list[str] = Field(min_length=1)
    domains: list[str] = Field(default_factory=list)


class Timeframes(StrictModel):
    primary: str = Field(min_length=1)
    confirmation: list[str] = Field(default_factory=list)


class Applicability(StrictModel):
    markets: list[str] = Field(min_length=1)
    timeframes: Timeframes
    instruments: list[str] = Field(default_factory=lambda: ["common_stock"])
    preferred_regimes: list[str] = Field(default_factory=list)
    excluded_regimes: list[str] = Field(default_factory=list)


class DataContract(StrictModel):
    minimum_bars: int = Field(ge=1)
    fields: list[str] = Field(min_length=1)
    benchmark_required: bool = False
    industry_required: bool = False
    adjustment: Literal["none", "forward", "backward"] = "forward"

    @field_validator("fields")
    @classmethod
    def fields_are_unique(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("data-contract fields must be unique")
        return value


class RuleGroupAll(StrictModel):
    all: list[str] = Field(min_length=1)


class RuleGroupAny(StrictModel):
    any: list[str] = Field(min_length=1)


class WeightedCondition(StrictModel):
    when: str = Field(min_length=1)
    weight: float = Field(gt=0)
    label: str | None = None


class ConfirmationRules(StrictModel):
    score: list[WeightedCondition] = Field(default_factory=list)


class RuleSet(StrictModel):
    prerequisites: RuleGroupAll | None = None
    required: RuleGroupAll
    confirmation: ConfirmationRules = Field(default_factory=ConfirmationRules)
    rejection: RuleGroupAny | None = None


class SourceFragment(StrictModel):
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    figure_ids: list[str] = Field(default_factory=list)

    @field_validator("page_end")
    @classmethod
    def page_end_is_valid(cls, value: int, info):
        start = info.data.get("page_start")
        if start is not None and value < start:
            raise ValueError("page_end must be greater than or equal to page_start")
        return value


class Provenance(StrictModel):
    book_id: str = Field(min_length=1)
    source_fragments: list[SourceFragment] = Field(default_factory=list)
    extraction_method: list[Literal["text", "vision", "human"]] = Field(default_factory=list)
    source_fidelity_score: float = Field(ge=0, le=1)
    empirical_rating: Literal[
        "unvalidated",
        "descriptive_only",
        "weak_evidence",
        "mixed_evidence",
        "supported",
        "robust",
        "deprecated",
    ] = "unvalidated"


class TradingSkill(StrictModel):
    schema_version: Literal["1.0"]
    identity: Identity
    classification: Classification
    applicability: Applicability
    data_contract: DataContract
    rules: RuleSet
    provenance: Provenance
