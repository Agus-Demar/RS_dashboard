"""
Data sources for market data ingestion.
"""
from src.ingestion.sources.yfinance_source import YFinanceSource, yfinance_source
from src.ingestion.sources.wikipedia_source import WikipediaSource, wikipedia_source

__all__ = [
    "YFinanceSource",
    "yfinance_source",
    "WikipediaSource", 
    "wikipedia_source",
]

