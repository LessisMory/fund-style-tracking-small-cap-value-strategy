# Fund Style Tracking and Mispricing-Based Small-Cap Value Strategy

This repository implements a quantitative equity strategy inspired by
public mutual fund investment behavior in the Chinese A-share market.
The strategy combines institutional style tracking with fundamental
mispricing signals to identify undervalued small-cap stocks.

The project is based on a complete research framework originally developed
for a national-level quantitative investment competition.

---

## Research Motivation

In the Chinese equity market, public mutual funds represent informed,
long-horizon institutional investors with demonstrated stock selection
ability. However, even among stocks favored by institutions, pricing
inefficiencies may still exist due to limited attention and market frictions,
especially in the small-cap universe.

This strategy aims to:
1. Track and extract mutual fund stock selection styles,
2. Identify fundamentally mispriced stocks within that universe, and
3. Dynamically adjust portfolio exposure under volatile market conditions.

---

## Stock Universe

The strategy focuses on the CSI 1000 Index constituents, which:
- Represent liquid small- and mid-cap stocks,
- Exhibit higher volatility and stronger reversal effects,
- Receive less market attention than large-cap indices.

---

## Strategy Architecture

The strategy consists of four core modules:

### 1. Fund Style Tracking (First-Stage Selection)

Mutual fund heavy-holding stocks are aggregated into an equal-weighted
portfolio to represent institutional investment style.

For each stock in the CSI 1000 universe, a rolling regression is performed
between individual stock returns and the fund-heavy portfolio returns.
Stocks with the highest beta exposure are selected as candidates that
closely track mutual fund investment behavior.

---

### 2. Fundamental Mispricing Score (Second-Stage Selection)

A composite mispricing score is constructed using eight fundamental anomalies,
covering profitability, valuation, growth, and intangible investment signals.

Each anomaly is ranked cross-sectionally according to its expected return
direction. The final mispricing score is obtained by averaging all ranks.
Stocks with the highest exposure to the mispricing factor portfolio are
selected as the final investment universe.

---

### 3. Volatility and Reversal-Based Weight Scaling

To capture short-term reversal effects commonly observed in the Chinese
equity market, portfolio weights are scaled using:

- Prior-period cumulative returns (reversal signal),
- Prior-period realized volatility.

Stocks with higher volatility and stronger reversal potential receive
higher portfolio weights.

---

### 4. Drawdown-Controlled Position Management

To mitigate downside risk during prolonged market downturns, the strategy
employs a rolling drawdown-based position control mechanism inspired by
dynamic drawdown control frameworks.

When the rolling drawdown exceeds a predefined threshold, total portfolio
exposure is reduced proportionally. Individual stock stop-loss rules are
also applied to control extreme risks.

---

## Key Techniques

- Institutional style replication
- Cross-sectional anomaly ranking
- Two-stage regression-based stock selection
- Volatility and reversal-adjusted weighting
- Rolling drawdown risk control

---

## Repository Structure

---

## Intended Audience

This project is intended as a research-oriented demonstration of quantitative
equity strategy design and is suitable for academic research, buy-side
quantitative roles, and graduate-level applications in quantitative finance.
