"""
LOF fund holdings extraction and preprocessing
"""

import pandas as pd
from jqdata import get_all_securities, finance
from core.config import FUND_TYPE_MAP, ASSET_TYPE_MAP


def get_lof_funds():
    """
    Get LOF funds filtered by investment type.

    Returns
    -------
    list
    """
    lof = get_all_securities(types=['lof'])
    lof = lof[lof['fund_investment_type'].isin(FUND_TYPE_MAP.keys())]
    return lof.index.tolist()


def get_fund_holdings(fund_list):
    """
    Get stock holdings of LOF funds.

    Returns
    -------
    pd.DataFrame
    """
    q = query(
        finance.FUND_PORTFOLIO_STOCK
    ).filter(
        finance.FUND_PORTFOLIO_STOCK.code.in_(fund_list)
    )

    df = finance.run_query(q)

    # Map Chinese fields to English labels
    df['fund_type'] = df['fund_investment_type'].map(FUND_TYPE_MAP)
    df['asset_type'] = df['top_detail_type'].map(ASSET_TYPE_MAP)

    # Keep stock holdings only
    df = df[df['asset_type'] == 'stock']

    # Time features
    df['year'] = df['report_date'].dt.year
    df['month'] = df['report_date'].dt.month
    df['season'] = (df['month'] - 1) // 3 + 1

    return df
