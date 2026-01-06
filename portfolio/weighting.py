"""
Portfolio weighting logic
"""

import numpy as np
import pandas as pd
from jqdata import get_price


def compute_realized_volatility(stock_list, end_date, window=5):
    """
    Compute realized volatility using intraday prices.

    Parameters
    ----------
    stock_list : list
    end_date : datetime
    window : int

    Returns
    -------
    pd.Series
    """
    vol = {}

    for stock in stock_list:
        price = get_price(
            stock,
            end_date=end_date,
            frequency='5m',
            fields=['close'],
            count=window * 48
        )['close']

        log_ret = np.log(price / price.shift(1)).dropna()
        vol[stock] = np.sqrt((log_ret ** 2).sum())

    return pd.Series(vol)


def compute_cumulative_return(stock_list, end_date, window=20):
    """
    Compute cumulative returns over a rolling window.
    """
    ret = {}

    for stock in stock_list:
        price = get_price(
            stock,
            end_date=end_date,
            frequency='1d',
            fields=['close'],
            count=window
        )['close']

        ret[stock] = price.iloc[-1] / price.iloc[0] - 1

    return pd.Series(ret)


def compute_portfolio_weights(stock_list, end_date):
    """
    Combine volatility and return information to generate portfolio weights.
    """
    vol = compute_realized_volatility(stock_list, end_date)
    cum_ret = compute_cumulative_return(stock_list, end_date)

    corr_rank = (
        pd.concat([vol, cum_ret], axis=1)
        .corr()
        .iloc[0]
        .rank(pct=True)
    )

    raw_weight = vol * corr_rank * cum_ret.rank(pct=True)
    weight = raw_weight / raw_weight.sum()

    return weight
