import numpy as np
import pytest

from books_to_stock_analysis_skill.features.indicators import atr, normalized_log_slope, rolling_high, sma, volume_ratio


def test_sma_returns_mean_of_trailing_window() -> None:
    assert sma([1, 2, 3, 4], 3) == pytest.approx(3.0)


def test_rolling_high_uses_trailing_window() -> None:
    assert rolling_high([4, 3, 7, 6], 3) == 7


def test_volume_ratio_compares_last_value_to_trailing_mean() -> None:
    assert volume_ratio([10, 10, 20], 3) == pytest.approx(1.5)


def test_atr_uses_true_range_with_previous_close() -> None:
    highs = [11, 13, 12]
    lows = [9, 10, 8]
    closes = [10, 12, 9]
    assert atr(highs, lows, closes, 3) == pytest.approx((2 + 3 + 4) / 3)


def test_normalized_log_slope_is_positive_for_exponential_rise() -> None:
    prices = np.exp(np.arange(10) * 0.02)
    value = normalized_log_slope(prices.tolist(), window=10, normalizer=0.1)
    assert value == pytest.approx(0.2, rel=1e-6)


def test_indicators_reject_insufficient_data() -> None:
    with pytest.raises(ValueError, match="at least"):
        sma([1, 2], 3)
