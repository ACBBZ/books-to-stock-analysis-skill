from books_to_stock_analysis_skill.domain.models import TradingSkill
from books_to_stock_analysis_skill.runtime.evaluator import SkillEvaluator


def make_skill() -> TradingSkill:
    return TradingSkill.model_validate({
        "schema_version": "1.0",
        "identity": {"id": "breakout", "name": "Breakout", "version": "0.1.0"},
        "classification": {"type": "strategy", "intents": ["analyze"]},
        "applicability": {"markets": ["CN_A_SHARE"], "timeframes": {"primary": "1d"}},
        "data_contract": {"minimum_bars": 20, "fields": ["close", "volume_ratio"]},
        "rules": {
            "prerequisites": {"all": ["bars_count >= 20"]},
            "required": {"all": ["close > recent_high"]},
            "confirmation": {"score": [
                {"when": "volume_ratio >= 1.5", "weight": 0.6, "label": "volume confirmation"},
                {"when": "benchmark_up", "weight": 0.4, "label": "benchmark confirmation"},
            ]},
            "rejection": {"any": ["overextended"]},
        },
        "provenance": {"book_id": "synthetic", "source_fidelity_score": 0.9},
    })


def observations(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "bars_count": 20,
        "close": 11,
        "recent_high": 10,
        "volume_ratio": 2,
        "benchmark_up": True,
        "overextended": False,
    }
    values.update(overrides)
    return values


def test_prerequisite_failure_returns_insufficient_data() -> None:
    result = SkillEvaluator().evaluate(make_skill(), observations(bars_count=10))
    assert result.status == "insufficient_data"


def test_full_confirmation_returns_matched() -> None:
    result = SkillEvaluator().evaluate(make_skill(), observations())
    assert result.status == "matched"
    assert result.match_score == 1.0


def test_incomplete_confirmation_returns_partial_match() -> None:
    result = SkillEvaluator().evaluate(make_skill(), observations(benchmark_up=False))
    assert result.status == "partial_match"
    assert result.match_score == 0.6
    assert any(item.label == "benchmark confirmation" for item in result.contradictions)


def test_rejection_rule_vetoes_match() -> None:
    result = SkillEvaluator().evaluate(make_skill(), observations(overextended=True))
    assert result.status == "rejected"
