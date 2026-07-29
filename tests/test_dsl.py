import pytest

from books_to_stock_analysis_skill.dsl.evaluator import ExpressionError, SafeExpressionEvaluator


def test_evaluates_arithmetic_comparison_and_boolean_logic() -> None:
    evaluator = SafeExpressionEvaluator()
    result = evaluator.evaluate(
        "close > ma20 and volume_ratio >= 1.5",
        {"close": 11, "ma20": 10, "volume_ratio": 1.6},
    )
    assert result is True


def test_calls_only_registered_functions() -> None:
    evaluator = SafeExpressionEvaluator(functions={"rolling_high": lambda value, window: value + window})
    assert evaluator.evaluate("close > rolling_high(base, 2)", {"close": 13, "base": 10}) is True


def test_rejects_unknown_names() -> None:
    evaluator = SafeExpressionEvaluator()
    with pytest.raises(ExpressionError, match="Unknown name"):
        evaluator.evaluate("close > missing", {"close": 10})


@pytest.mark.parametrize(
    "expression",
    ["unknown_function()", "obj.__class__", "[x for x in values]", "values[0]"],
)
def test_rejects_unsafe_or_unsupported_syntax(expression: str) -> None:
    evaluator = SafeExpressionEvaluator()
    with pytest.raises(ExpressionError):
        evaluator.evaluate(expression, {"obj": object(), "values": [1]})
