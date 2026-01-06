"""
Main strategy engine
"""

from jqdata import *
import pandas as pd

from core.config import (
    REBAlANCE_INTERVAL_DAYS,
    NUM_FIRST_STAGE,
    NUM_SECOND_STAGE
)

from data.calendar import (
    get_recent_trade_days,
    get_month_end_trade_days
)

from data.universe import get_stock_universe
from data.fund_holdings import get_fund_holdings, get_lof_funds

from factors.fundamentals import build_fundamental_score
from selection.selector import (
    first_stage_selection,
    second_stage_selection
)

from portfolio.weighting import compute_portfolio_weights
from portfolio.risk import (
    compute_drawdown,
    adjust_position_ratio,
    should_stop_loss
)


def init(context):
    """
    Strategy initialization
    """
    log.info("Initializing multi-factor strategy")

    context.day_count = 0
    context.wealth = []
    context.selected_stocks = []
    context.target_weights = {}


def before_trading(context):
    """
    Pre-market preparation
    """
    log.info("Running pre-market routines")

    context.day_count += 1
    today = context.current_dt.date()

    universe = get_stock_universe(today)

    # Update factor scores periodically
    if context.day_count % REBAlANCE_INTERVAL_DAYS == 1:
        log.info("Updating fundamental scores")

        score_df = build_fundamental_score(universe, today)
        high_group = score_df[
            score_df['score_label'] == 'high'
        ]['code'].tolist()

        context.high_score_stocks = high_group


def handle_bar(context, bar_dict):
    """
    Intraday execution
    """
    log.info("Executing intraday trading logic")

    today = context.current_dt.date()

    # Rebalance periodically
    if context.day_count % REBAlANCE_INTERVAL_DAYS == 0:
        log.info("Rebalancing portfolio")

        lof_funds = get_lof_funds()
        fund_holdings = get_fund_holdings(lof_funds)

        # Placeholder: portfolio returns need to be constructed externally
        fund_returns = None
        high_score_returns = None

        # Placeholder: stock returns dictionary
        stock_returns = {}

        stage1 = first_stage_selection(
            stock_returns,
            fund_returns,
            NUM_FIRST_STAGE
        )

        final_selection = second_stage_selection(
            stock_returns,
            high_score_returns,
            stage1,
            NUM_SECOND_STAGE
        )

        context.selected_stocks = final_selection
        context.target_weights = compute_portfolio_weights(
            final_selection,
            today
        )

    # Risk control
    if len(context.wealth) >= 2:
        drawdown = compute_drawdown(context.wealth)
        position_ratio = adjust_position_ratio(drawdown)
    else:
        position_ratio = 1.0

    # Stop loss check
    for stock in list(context.portfolio.positions.keys()):
        position = context.portfolio.positions[stock]
        current_price = bar_dict[stock].close

        if should_stop_loss(position.avg_cost, current_price):
            log.info(f"Stop loss triggered for {stock}")
            order_target(stock, 0)


def after_trading(context):
    """
    Post-market updates
    """
    log.info("Post-market bookkeeping")

    context.wealth.append(context.portfolio.total_value)

    # Keep rolling window
    if len(context.wealth) > 20:
        context.wealth.pop(0)
