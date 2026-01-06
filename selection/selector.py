"""
Two-stage stock selection logic
"""

import numpy as np
from selection.regression import estimate_beta_series


def first_stage_selection(
    stock_returns,
    fund_portfolio_returns,
    top_n
):
    """
    First-stage selection:
    Select stocks with highest beta exposure
    to fund holdings portfolio.

    Parameters
    ----------
    stock_returns : dict
        {stock_code: np.ndarray}
    fund_portfolio_returns : np.ndarray
    top_n : int

    Returns
    -------
    list
        Selected stock codes
    """
    beta_dict = estimate_beta_series(
        stock_returns,
        fund_portfolio_returns
    )

    ranked = sorted(
        beta_dict.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [s for s, _ in ranked[:top_n]]


def second_stage_selection(
    stock_returns,
    high_score_portfolio_returns,
    candidate_stocks,
    top_n
):
    """
    Second-stage selection:
    Select stocks with highest beta exposure
    to high-score (mispricing) portfolio.

    Parameters
    ----------
    stock_returns : dict
        {stock_code: np.ndarray}
    high_score_portfolio_returns : np.ndarray
    candidate_stocks : list
    top_n : int

    Returns
    -------
    list
        Final selected stock codes
    """
    filtered_returns = {
        s: stock_returns[s]
        for s in candidate_stocks
    }

    beta_dict = estimate_beta_series(
        filtered_returns,
        high_score_portfolio_returns
    )

    ranked = sorted(
        beta_dict.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [s for s, _ in ranked[:top_n]]
