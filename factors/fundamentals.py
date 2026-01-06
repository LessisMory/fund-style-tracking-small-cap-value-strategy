"""
Fundamental factor construction and mispricing score calculation

This module builds cross-sectional fundamental factors
and aggregates them into a composite mispricing score.
"""

import pandas as pd
import numpy as np
from jqdata import get_fundamentals, query, valuation, indicator, balance
from factors.labeling import assign_score_labels


def get_fundamental_data(stock_list, date):
    """
    Retrieve raw fundamental data for a given stock universe.

    Parameters
    ----------
    stock_list : list
        List of stock codes
    date : datetime

    Returns
    -------
    pd.DataFrame
    """
    q = query(
        valuation.code,
        valuation.pb_ratio,
        valuation.ps_ratio,
        valuation.pcf_ratio,
        valuation.market_cap,
        balance.total_assets,
        indicator.roe,
        indicator.roa,
        indicator.inc_net_profit_year_on_year,
        indicator.operating_profit_growth_rate
    ).filter(
        valuation.code.in_(stock_list)
    )

    df = get_fundamentals(q, date=date)
    return df


def build_fundamental_factors(df):
    """
    Construct fundamental factors from raw financial data.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    factors = df.copy()

    # =====================
    # Valuation-related factors (inverse form)
    # =====================
    factors['bp'] = 1.0 / factors['pb_ratio']
    factors['sp'] = 1.0 / factors['ps_ratio']
    factors['cp'] = 1.0 / factors['pcf_ratio']

    # =====================
    # Size-adjusted balance sheet factor
    # =====================
    factors['asset_to_mktcap'] = (
        factors['total_assets'] / factors['market_cap']
    )

    # =====================
    # Profitability factors
    # =====================
    factors['roe'] = factors['roe']
    factors['roa'] = factors['roa']

    # =====================
    # Growth-related factors
    # =====================
    factors['profit_growth'] = factors['inc_net_profit_year_on_year']
    factors['operating_profit_growth'] = (
        factors['operating_profit_growth_rate']
    )

    return factors


def rank_factors(factors):
    """
    Rank each factor cross-sectionally.

    Parameters
    ----------
    factors : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    ranked = factors.copy()

    factor_cols = [
        'bp',
        'sp',
        'cp',
        'asset_to_mktcap',
        'roe',
        'roa',
        'profit_growth',
        'operating_profit_growth'
    ]

    for col in factor_cols:
        ranked[col] = ranked[col].rank(pct=True)

    return ranked


def compute_mispricing_score(ranked_factors):
    """
    Aggregate ranked factors into a composite mispricing score.

    Parameters
    ----------
    ranked_factors : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    score_cols = [
        'bp',
        'sp',
        'cp',
        'asset_to_mktcap',
        'roe',
        'roa',
        'profit_growth',
        'operating_profit_growth'
    ]

    ranked_factors['total_score'] = ranked_factors[score_cols].mean(axis=1)

    # Assign English-only score labels
    ranked_factors['score_label'] = assign_score_labels(
        ranked_factors['total_score']
    )

    return ranked_factors


def build_fundamental_score(stock_list, date):
    """
    End-to-end pipeline for fundamental mispricing score construction.

    Parameters
    ----------
    stock_list : list
    date : datetime

    Returns
    -------
    pd.DataFrame
    """
    raw = get_fundamental_data(stock_list, date)
    factors = build_fundamental_factors(raw)
    ranked = rank_factors(factors)
    scored = compute_mispricing_score(ranked)

    return scored
