"""
Global configuration and strategy parameters
"""

# =====================
# Strategy schedule
# =====================
REBAlANCE_INTERVAL_DAYS = 20
FACTOR_UPDATE_INTERVAL_DAYS = 20

# =====================
# Risk control
# =====================
MAX_DRAWDOWN_THRESHOLD = 0.08
MIN_POSITION_RATIO = 0.65
SINGLE_STOCK_STOP_LOSS = 0.12

# =====================
# Portfolio construction
# =====================
NUM_FIRST_STAGE = 60
NUM_SECOND_STAGE = 30

# =====================
# Factor labeling (ENGLISH ONLY)
# =====================
SCORE_LABELS = [
    'low',
    'mid_low',
    'mid',
    'mid_high',
    'high'
]

# =====================
# Fund type mapping (Chinese → English)
# =====================
FUND_TYPE_MAP = {
    '股票型': 'equity',
    '混合型': 'balanced'
}

ASSET_TYPE_MAP = {
    '股票': 'stock'
}
