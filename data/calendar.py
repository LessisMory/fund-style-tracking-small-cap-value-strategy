"""
Trading calendar utilities
"""

from jqdata import get_trade_days


def get_recent_trade_days(end_date, count):
    """
    Get recent trading days ending at end_date.

    Parameters
    ----------
    end_date : datetime
    count : int

    Returns
    -------
    list
    """
    return get_trade_days(end_date=end_date, count=count)


def get_month_end_trade_days(end_date, months=12):
    """
    Get month-end trading days.

    Parameters
    ----------
    end_date : datetime
    months : int

    Returns
    -------
    list
    """
    trade_days = get_trade_days(end_date=end_date, count=months * 25)
    month_end = []

    last_month = trade_days[0].month
    for d in trade_days:
        if d.month != last_month:
            month_end.append(prev_day)
        prev_day = d
        last_month = d.month

    return month_end


def get_season_end_trade_days(end_date, seasons=8):
    """
    Get quarter-end trading days.

    Parameters
    ----------
    end_date : datetime
    seasons : int

    Returns
    -------
    list
    """
    trade_days = get_trade_days(end_date=end_date, count=seasons * 65)
    season_end = []

    last_quarter = (trade_days[0].month - 1) // 3
    for d in trade_days:
        quarter = (d.month - 1) // 3
        if quarter != last_quarter:
            season_end.append(prev_day)
        prev_day = d
        last_quarter = quarter

    return season_end
