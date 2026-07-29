import pytest
from pydantic import ValidationError

from books_to_stock_analysis_skill.domain.models import TradingSkill


def minimal_skill() -> dict:
    return {
        "schema_version": "1.0",
        "identity": {"id": "volume-breakout", "name": "Volume Breakout", "version": "0.1.0"},
        "classification": {"type": "strategy", "intents": ["analyze"]},
        "applicability": {"markets": ["CN_A_SHARE"], "timeframes": {"primary": "1d"}},
        "data_contract": {"minimum_bars": 20, "fields": ["close", "volume"]},
        "rules": {"required": {"all": ["close > recent_high"]}},
        "provenance": {"book_id": "synthetic", "source_fidelity_score": 0.9},
    }


def test_trading_skill_accepts_minimal_valid_document() -> None:
    skill = TradingSkill.model_validate(minimal_skill())
    assert skill.identity.id == "volume-breakout"
    assert skill.rules.required.all == ["close > recent_high"]


def test_trading_skill_rejects_invalid_fidelity_score() -> None:
    payload = minimal_skill()
    payload["provenance"]["source_fidelity_score"] = 1.5
    with pytest.raises(ValidationError):
        TradingSkill.model_validate(payload)


def test_trading_skill_rejects_empty_required_rules() -> None:
    payload = minimal_skill()
    payload["rules"]["required"]["all"] = []
    with pytest.raises(ValidationError):
        TradingSkill.model_validate(payload)
