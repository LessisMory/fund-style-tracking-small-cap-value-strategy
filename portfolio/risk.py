"""
Risk management utilities
"""

from core.config import (
    MAX_DRAWDOWN_THRESHOLD,
    MIN_POSITION_RATIO,
    SINGLE_STOCK_STOP_LOSS
)


def compute_drawdown(wealth_series):
    """
    Compute drawdown given historical wealth series.
    """
    peak = max(wealth_series)
    current = wealth_series[-1]
    return 1 - current / peak


def adjust_position_ratio(drawdown):
    """
    Adjust position size based on drawdown level.
    """
    if drawdown < MAX_DRAWDOWN_THRESHOLD:
        return 1.0
    else:
        return max(
            MIN_POSITION_RATIO,
            1 - drawdown
        )


def should_stop_loss(cost, price):
    """
    Check single stock stop loss condition.
    """
    return (price - cost) / cost <= -SINGLE_STOCK_STOP_LOSS
