"""Small, deterministic technical-indicator primitives used by compiled skills."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def _window(values: Sequence[float], window: int, name: str = "values") -> np.ndarray:
    if window < 1:
        raise ValueError("window must be at least 1")
    if len(values) < window:
        raise ValueError(f"{name} must contain at least {window} values")
    array = np.asarray(values[-window:], dtype=float)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def sma(values: Sequence[float], window: int) -> float:
    """Return the arithmetic mean of the trailing window."""
    return float(np.mean(_window(values, window)))


def rolling_high(values: Sequence[float], window: int) -> float:
    """Return the maximum value in the trailing window."""
    return float(np.max(_window(values, window)))


def volume_ratio(values: Sequence[float], window: int) -> float:
    """Return the latest volume divided by the trailing-window mean volume."""
    trailing = _window(values, window, "volume")
    average = float(np.mean(trailing))
    if average <= 0:
        raise ValueError("mean volume must be greater than zero")
    return float(trailing[-1] / average)


def atr(highs: Sequence[float], lows: Sequence[float], closes: Sequence[float], window: int) -> float:
    """Return the mean true range over the trailing window."""
    if not (len(highs) == len(lows) == len(closes)):
        raise ValueError("highs, lows, and closes must have the same length")
    if len(highs) < window:
        raise ValueError(f"price series must contain at least {window} values")
    high_array = np.asarray(highs, dtype=float)
    low_array = np.asarray(lows, dtype=float)
    close_array = np.asarray(closes, dtype=float)
    if not np.all(np.isfinite(np.concatenate([high_array, low_array, close_array]))):
        raise ValueError("price series must contain only finite values")
    if np.any(high_array < low_array):
        raise ValueError("high values must be greater than or equal to low values")

    true_ranges = np.empty(len(high_array), dtype=float)
    true_ranges[0] = high_array[0] - low_array[0]
    for index in range(1, len(high_array)):
        true_ranges[index] = max(
            high_array[index] - low_array[index],
            abs(high_array[index] - close_array[index - 1]),
            abs(low_array[index] - close_array[index - 1]),
        )
    return float(np.mean(true_ranges[-window:]))


def normalized_log_slope(prices: Sequence[float], window: int, normalizer: float) -> float:
    """Return the trailing log-price regression slope divided by a positive normalizer."""
    trailing = _window(prices, window, "prices")
    if np.any(trailing <= 0):
        raise ValueError("prices must be greater than zero")
    if not np.isfinite(normalizer) or normalizer <= 0:
        raise ValueError("normalizer must be a finite value greater than zero")
    x = np.arange(window, dtype=float)
    slope = float(np.polyfit(x, np.log(trailing), 1)[0])
    return slope / normalizer
