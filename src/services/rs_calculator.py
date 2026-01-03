"""
Mansfield Relative Strength Calculator.

Calculates the Mansfield RS using the 3-step process:
1. RS Line = (Asset Price / Benchmark Price) × 100
2. RS SMA = 52-week Simple Moving Average of RS Line
3. Mansfield RS = ((RS Line - RS SMA) / RS SMA) × 100
"""
import logging
from typing import Optional

import numpy as np
import pandas as pd

from src.config import settings

logger = logging.getLogger(__name__)


class MansfieldRSCalculator:
    """
    Calculates Mansfield Relative Strength.
    
    The Mansfield RS is a normalized measure of relative performance
    that shows how far the current RS is from its 52-week average.
    
    Interpretation:
    - > +10: Strong outperformance
    - +5 to +10: Moderate outperformance
    - -5 to +5: Neutral
    - -10 to -5: Moderate underperformance
    - < -10: Strong underperformance
    """
    
    def __init__(self, sma_period_weeks: int = None):
        """
        Initialize calculator.
        
        Args:
            sma_period_weeks: Number of weeks for SMA calculation (default: 52)
        """
        self.sma_period = sma_period_weeks or settings.RS_SMA_PERIOD_WEEKS
    
    def calculate_rs_line(
        self,
        asset_prices: pd.Series,
        benchmark_prices: pd.Series
    ) -> pd.Series:
        """
        Step 1: Calculate the raw RS Line.
        
        RS_Line = (Asset Price / Benchmark Price) × 100
        
        Args:
            asset_prices: Series of asset adjusted close prices (indexed by date)
            benchmark_prices: Series of benchmark adjusted close prices (indexed by date)
        
        Returns:
            Series of RS Line values
        """
        # Align dates - keep only dates present in both series
        aligned = pd.concat([asset_prices, benchmark_prices], axis=1, join='inner')
        aligned.columns = ['asset', 'benchmark']
        
        # Calculate RS Line
        rs_line = (aligned['asset'] / aligned['benchmark']) * 100
        
        return rs_line
    
    def calculate_rs_sma(self, rs_line: pd.Series) -> pd.Series:
        """
        Step 2: Calculate the 52-week SMA of the RS Line.
        
        Uses a rolling window based on weekly data points.
        For daily data, this is approximately 252 trading days (52 weeks × ~5 days).
        For weekly data, this is exactly 52 data points.
        
        Args:
            rs_line: Series of RS Line values
        
        Returns:
            Series of RS Line SMA values
        """
        # Determine if data is daily or weekly by checking average gap
        if len(rs_line) < 2:
            return pd.Series([np.nan] * len(rs_line), index=rs_line.index)
        
        # Calculate window size
        # For daily data: ~252 trading days per year, so 52 weeks ≈ 252 days
        # For weekly data: 52 weeks = 52 data points
        dates = pd.to_datetime(rs_line.index)
        avg_gap_days = (dates.max() - dates.min()).days / len(rs_line)
        
        if avg_gap_days < 3:
            # Daily data - use approximately 252 trading days
            window = self.sma_period * 5  # ~5 trading days per week
        else:
            # Weekly data - use exact week count
            window = self.sma_period
        
        # Calculate rolling SMA - requires full 52 weeks of data
        rs_sma = rs_line.rolling(window=window, min_periods=window).mean()
        
        return rs_sma
    
    def calculate_mansfield_rs(
        self,
        rs_line: pd.Series,
        rs_sma: pd.Series
    ) -> pd.Series:
        """
        Step 3: Calculate Mansfield RS.
        
        Mansfield RS = ((RS Line - RS SMA) / RS SMA) × 100
        
        Args:
            rs_line: Series of RS Line values
            rs_sma: Series of RS Line SMA values
        
        Returns:
            Series of Mansfield RS values
        """
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            mansfield_rs = ((rs_line - rs_sma) / rs_sma) * 100
        
        return mansfield_rs
    
    def calculate_full(
        self,
        asset_prices: pd.Series,
        benchmark_prices: pd.Series
    ) -> pd.DataFrame:
        """
        Complete Mansfield RS calculation pipeline.
        
        Args:
            asset_prices: Series of asset adjusted close prices
            benchmark_prices: Series of benchmark adjusted close prices
        
        Returns:
            DataFrame with columns: rs_line, rs_line_sma_52w, mansfield_rs
        """
        # Step 1: Calculate RS Line
        rs_line = self.calculate_rs_line(asset_prices, benchmark_prices)
        
        # Step 2: Calculate 52-week SMA
        rs_sma = self.calculate_rs_sma(rs_line)
        
        # Step 3: Calculate Mansfield RS
        mansfield_rs = self.calculate_mansfield_rs(rs_line, rs_sma)
        
        # Combine results
        result = pd.DataFrame({
            'rs_line': rs_line,
            'rs_line_sma_52w': rs_sma,
            'mansfield_rs': mansfield_rs
        })
        
        return result
    
    def get_weekly_rs(
        self,
        asset_prices: pd.Series,
        benchmark_prices: pd.Series,
        as_of_date: Optional[pd.Timestamp] = None
    ) -> dict:
        """
        Get RS values for a specific week (or latest week).
        
        Args:
            asset_prices: Series of asset adjusted close prices
            benchmark_prices: Series of benchmark adjusted close prices
            as_of_date: Optional date to get RS for (uses Friday of that week)
        
        Returns:
            Dict with rs_line, rs_line_sma_52w, mansfield_rs for the week
        """
        # Calculate full history
        result = self.calculate_full(asset_prices, benchmark_prices)
        
        if result.empty:
            return {
                'rs_line': None,
                'rs_line_sma_52w': None,
                'mansfield_rs': None
            }
        
        # Get value for specific date or latest
        if as_of_date:
            # Find the Friday of the week containing as_of_date
            target = pd.Timestamp(as_of_date)
            # Filter to dates <= target
            valid = result[result.index <= target]
            if valid.empty:
                return {
                    'rs_line': None,
                    'rs_line_sma_52w': None,
                    'mansfield_rs': None
                }
            row = valid.iloc[-1]
        else:
            row = result.iloc[-1]
        
        return {
            'rs_line': row['rs_line'],
            'rs_line_sma_52w': row['rs_line_sma_52w'],
            'mansfield_rs': row['mansfield_rs']
        }


def calculate_percentile_ranks(rs_values: pd.Series) -> pd.Series:
    """
    Calculate percentile ranks for RS values across sub-industries.
    
    Used for color coding in the heatmap:
    - Top 33% (percentile >= 67): GREEN (strong)
    - Middle 34% (33 <= percentile < 67): YELLOW (neutral)
    - Bottom 33% (percentile < 33): RED (weak)
    
    Args:
        rs_values: Series of Mansfield RS values (indexed by sub-industry code)
    
    Returns:
        Series of percentile ranks (0-100)
    """
    # Drop NaN values for ranking
    valid_rs = rs_values.dropna()
    
    if valid_rs.empty:
        return pd.Series(dtype=float)
    
    # Calculate percentile rank
    percentiles = valid_rs.rank(pct=True) * 100
    
    return percentiles

