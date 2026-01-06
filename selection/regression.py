"""
Regression utilities for factor exposure estimation
"""

import numpy as np


def ols_beta(y, x):
    """
    Estimate OLS beta using pseudo-inverse.

    Parameters
    ----------
    y : np.ndarray
        Dependent variable (asset returns)
    x : np.ndarray
        Independent variable (factor or portfolio returns)

    Returns
    -------
    float
        Estimated beta
    """
    x = x.reshape(-1, 1)
    beta = np.linalg.pinv(x).dot(y)
    return beta[0]


def estimate_beta_series(stock_returns, factor_returns):
    """
    Estimate beta exposure for each stock to a given factor.

    Parameters
    ----------
    stock_returns : dict
        {stock_code: np.ndarray}
    factor_returns : np.ndarray

    Returns
    -------
    dict
        {stock_code: beta}
    """
    beta_dict = {}

    for stock, ret in stock_returns.items():
        beta_dict[stock] = ols_beta(ret, factor_returns)

    return beta_dict
