"""
Yahoo Finance data source using yfinance library.

Provides free access to historical price data without API key.
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf

from src.ingestion.utils.rate_limiter import RateLimiter
from src.ingestion.utils.retry import with_retry

logger = logging.getLogger(__name__)


class YFinanceSource:
    """
    Yahoo Finance data source via yfinance library.
    
    Features:
    - Completely FREE - no API key required
    - Reliable historical price data
    - Basic sector/industry info
    - Batch download support for efficiency
    
    Note: Industry names from yfinance don't match GICS exactly,
    so we use Wikipedia for GICS mapping instead.
    """
    
    def __init__(self, rate_limit: float = 0.5):
        """
        Initialize yfinance source.
        
        Args:
            rate_limit: Requests per second (conservative default)
        """
        self.rate_limiter = RateLimiter(calls_per_second=rate_limit)
        self._executor = ThreadPoolExecutor(max_workers=5)
    
    @with_retry(max_retries=3, base_delay=2.0)
    def fetch_price_history(
        self,
        ticker: str,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a single ticker.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
        
        Returns:
            DataFrame with columns: date, open, high, low, close, adj_close, volume
        """
        self.rate_limiter.acquire_sync()
        
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(
                start=start_date.isoformat(),
                end=(end_date + timedelta(days=1)).isoformat(),
                auto_adjust=False
            )
            
            if df.empty:
                logger.warning(f"No price data returned for {ticker}")
                return pd.DataFrame()
            
            # Standardize column names
            df = df.reset_index()
            df.columns = [c.lower().replace(' ', '_') for c in df.columns]
            
            # Rename Adj Close
            if 'adj_close' not in df.columns and 'adjclose' in df.columns:
                df = df.rename(columns={'adjclose': 'adj_close'})
            
            # Ensure date column is date type
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # Select and order columns
            columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
            available_columns = [c for c in columns if c in df.columns]
            
            return df[available_columns]
            
        except Exception as e:
            logger.error(f"Error fetching price history for {ticker}: {e}")
            raise
    
    @with_retry(max_retries=2, base_delay=1.0)
    def fetch_company_info(self, ticker: str) -> dict:
        """
        Fetch company metadata.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dict with: ticker, name, sector, industry, market_cap
        """
        self.rate_limiter.acquire_sync()
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'name': info.get('longName') or info.get('shortName', ticker),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'market_cap': info.get('marketCap'),
                'exchange': info.get('exchange'),
                'currency': info.get('currency', 'USD'),
            }
        except Exception as e:
            logger.error(f"Error fetching company info for {ticker}: {e}")
            raise
    
    def fetch_multiple_prices(
        self,
        tickers: List[str],
        start_date: date,
        end_date: date,
        batch_size: int = 50
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch price history for multiple tickers efficiently.
        
        Uses yfinance batch download for speed.
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date
            end_date: End date
            batch_size: Number of tickers per batch
        
        Returns:
            Dict mapping ticker to DataFrame
        """
        all_data: Dict[str, pd.DataFrame] = {}
        
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(tickers) + batch_size - 1) // batch_size
            
            logger.info(f"Fetching batch {batch_num}/{total_batches}: {len(batch)} tickers")
            
            self.rate_limiter.acquire_sync()
            
            try:
                df = yf.download(
                    tickers=batch,
                    start=start_date.isoformat(),
                    end=(end_date + timedelta(days=1)).isoformat(),
                    auto_adjust=False,
                    group_by='ticker',
                    threads=True,
                    progress=False
                )
                
                if df.empty:
                    logger.warning(f"No data returned for batch {batch_num}")
                    continue
                
                # Parse results
                if len(batch) == 1:
                    # Single ticker returns flat columns
                    ticker = batch[0]
                    result_df = self._process_single_ticker_df(df)
                    if not result_df.empty:
                        all_data[ticker] = result_df
                else:
                    # Multiple tickers return multi-level columns
                    for ticker in batch:
                        try:
                            if ticker in df.columns.get_level_values(0):
                                ticker_df = df[ticker]
                                result_df = self._process_single_ticker_df(ticker_df)
                                if not result_df.empty:
                                    all_data[ticker] = result_df
                        except Exception as e:
                            logger.warning(f"Error parsing {ticker}: {e}")
                            
            except Exception as e:
                logger.error(f"Error fetching batch {batch_num}: {e}")
            
            # Small delay between batches
            import time
            time.sleep(1)
        
        logger.info(f"Successfully fetched data for {len(all_data)}/{len(tickers)} tickers")
        return all_data
    
    def _process_single_ticker_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process a single ticker's DataFrame from yfinance."""
        if df.empty:
            return pd.DataFrame()
        
        df = df.reset_index()
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        
        # Handle column name variations
        if 'adj_close' not in df.columns:
            if 'adjclose' in df.columns:
                df = df.rename(columns={'adjclose': 'adj_close'})
            elif 'close' in df.columns:
                df['adj_close'] = df['close']
        
        # Convert date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Drop rows with missing close price
        if 'close' in df.columns:
            df = df.dropna(subset=['close'])
        
        return df
    
    def fetch_benchmark_prices(
        self,
        ticker: str = "SPY",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> pd.DataFrame:
        """
        Fetch benchmark (SPY) price history.
        
        Args:
            ticker: Benchmark ticker (default: SPY for S&P 500)
            start_date: Start date (default: 2 years ago)
            end_date: End date (default: today)
        
        Returns:
            DataFrame with benchmark prices
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=365 * 2 + 30)  # 2 years + buffer
        
        return self.fetch_price_history(ticker, start_date, end_date)


# Singleton instance
yfinance_source = YFinanceSource()

