"""
Stock universe construction and filtering
"""

from jqdata import get_all_securities, get_industry
from jqdata import get_security_info


FINANCIAL_INDUSTRY_CODES = {'T27', 'T19'}


def is_st_stock(stock):
    """
    Check if stock is ST or *ST.
    """
    info = get_security_info(stock)
    return info.display_name.startswith('ST') or info.display_name.startswith('*ST')


def is_financial_industry(stock):
    """
    Check if stock belongs to financial industry.
    """
    industry = get_industry(stock)
    return any(code in FINANCIAL_INDUSTRY_CODES for code in industry.values())


def get_stock_universe(date):
    """
    Construct stock universe with filters applied.

    Filters:
    - Exclude ST stocks
    - Exclude financial sector

    Returns
    -------
    list
    """
    stocks = get_all_securities(types=['stock'], date=date).index.tolist()

    filtered = []
    for s in stocks:
        if is_st_stock(s):
            continue
        if is_financial_industry(s):
            continue
        filtered.append(s)

    return filtered
