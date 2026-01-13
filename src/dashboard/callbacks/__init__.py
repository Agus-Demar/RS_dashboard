"""
Dashboard callbacks.
"""
from src.dashboard.callbacks.heatmap_callbacks import register_callbacks
from src.dashboard.callbacks.stock_callbacks import register_stock_callbacks
from src.dashboard.callbacks.ticker_callbacks import register_ticker_callbacks

__all__ = ["register_callbacks", "register_stock_callbacks", "register_ticker_callbacks"]

