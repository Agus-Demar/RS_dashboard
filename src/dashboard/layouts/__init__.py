"""
Dashboard layouts.
"""
from src.dashboard.layouts.main_layout import create_layout
from src.dashboard.layouts.stock_layout import create_layout as create_stock_layout
from src.dashboard.layouts.ticker_layout import create_layout as create_ticker_layout

__all__ = ["create_layout", "create_stock_layout", "create_ticker_layout"]

