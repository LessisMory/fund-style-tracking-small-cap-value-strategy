"""
Score labeling utilities

Convert continuous factor scores into
English-labeled quantile groups
"""

import pandas as pd
from core.config import SCORE_LABELS


def assign_score_labels(score_series: pd.Series) -> pd.Series:
    """
    Assign quantile-based English labels to factor scores.

    Parameters
    ----------
    score_series : pd.Series
        Continuous factor score

    Returns
    -------
    pd.Series
        Categorical labels:
        ['low', 'mid_low', 'mid', 'mid_high', 'high']
    """
    return pd.qcut(
        score_series,
        q=len(SCORE_LABELS),
        labels=SCORE_LABELS
    )
