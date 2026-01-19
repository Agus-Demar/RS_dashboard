"""
StockCharts Technical Rank (SCTR) Calculator.

Calculates the SCTR using the StockCharts methodology:
- Long-Term (60% weight):
  - Percent above/below 200-day EMA (30%)
  - 125-Day Rate-of-Change (30%)
- Medium-Term (30% weight):
  - Percent above/below 50-day EMA (15%)
  - 20-day Rate-of-Change (15%)
- Short-Term (10% weight):
  - 3-day slope of PPO(12,26,9) Histogram (5%)
  - 14-day RSI (5%)

Reference: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/stockcharts-technical-rank
"""
import logging
from typing import Optional, Dict

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class SCTRCalculator:
    """
    Calculates StockCharts Technical Rank (SCTR).
    
    The SCTR is a numerical score (0-100) that ranks a stock within a group
    based on six key technical indicators covering different timeframes.
    
    Interpretation:
    - > 90: Strong technical leaders
    - 60-90: Above average technical strength
    - 40-60: Average/Neutral
    - 10-40: Below average technical weakness
    - < 10: Strong technical laggards
    """
    
    # Weight constants from StockCharts methodology
    WEIGHT_200_EMA = 0.30  # 30%
    WEIGHT_125_ROC = 0.30  # 30%
    WEIGHT_50_EMA = 0.15   # 15%
    WEIGHT_20_ROC = 0.15   # 15%
    WEIGHT_PPO_SLOPE = 0.05  # 5%
    WEIGHT_RSI = 0.05      # 5%
    
    def __init__(self):
        """Initialize the SCTR calculator."""
        pass
    
    def calculate_ema(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        
        Args:
            prices: Series of closing prices
            period: EMA period (e.g., 50 or 200)
        
        Returns:
            Series of EMA values
        """
        return prices.ewm(span=period, adjust=False).mean()
    
    def calculate_percent_above_ema(
        self,
        prices: pd.Series,
        period: int
    ) -> pd.Series:
        """
        Calculate the percentage above/below the EMA.
        
        Percent = ((Price - EMA) / EMA) * 100
        
        Args:
            prices: Series of closing prices
            period: EMA period
        
        Returns:
            Series of percent values
        """
        ema = self.calculate_ema(prices, period)
        percent = ((prices - ema) / ema) * 100
        return percent
    
    def calculate_roc(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Rate of Change.
        
        ROC = ((Current Price - Price N periods ago) / Price N periods ago) * 100
        
        Args:
            prices: Series of closing prices
            period: ROC period (e.g., 20 or 125)
        
        Returns:
            Series of ROC values
        """
        roc = ((prices - prices.shift(period)) / prices.shift(period)) * 100
        return roc
    
    def calculate_ppo(
        self,
        prices: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> Dict[str, pd.Series]:
        """
        Calculate Percentage Price Oscillator and its histogram.
        
        PPO = ((EMA(fast) - EMA(slow)) / EMA(slow)) * 100
        Signal = EMA(PPO, signal_period)
        Histogram = PPO - Signal
        
        Args:
            prices: Series of closing prices
            fast_period: Fast EMA period (default 12)
            slow_period: Slow EMA period (default 26)
            signal_period: Signal line period (default 9)
        
        Returns:
            Dict with 'ppo', 'signal', 'histogram' Series
        """
        ema_fast = prices.ewm(span=fast_period, adjust=False).mean()
        ema_slow = prices.ewm(span=slow_period, adjust=False).mean()
        
        ppo = ((ema_fast - ema_slow) / ema_slow) * 100
        signal = ppo.ewm(span=signal_period, adjust=False).mean()
        histogram = ppo - signal
        
        return {
            'ppo': ppo,
            'signal': signal,
            'histogram': histogram
        }
    
    def calculate_ppo_histogram_slope(self, prices: pd.Series) -> pd.Series:
        """
        Calculate 3-day slope of PPO(12,26,9) Histogram.
        
        Slope = (Histogram[t] - Histogram[t-2]) / 3
        
        The slope indicates momentum of momentum:
        - Positive slope: PPO histogram rising (bullish momentum increasing)
        - Negative slope: PPO histogram falling (bearish momentum increasing)
        
        Args:
            prices: Series of closing prices
        
        Returns:
            Series of slope values
        """
        ppo_data = self.calculate_ppo(prices)
        histogram = ppo_data['histogram']
        
        # 3-day slope = (current - 2 days ago) / 3
        slope = (histogram - histogram.shift(2)) / 3
        
        return slope
    
    def calculate_ppo_slope_score(self, slope: float) -> float:
        """
        Convert PPO histogram slope to a score contribution.
        
        According to StockCharts:
        - If slope > +1 (i.e., +45 degrees): contributes 5 points (5%)
        - If slope < -1: contributes 0 points
        - Otherwise: contributes 5% of ((Slope + 1) x 50)
        
        Args:
            slope: PPO histogram 3-day slope value
        
        Returns:
            Score contribution (0 to 5)
        """
        if pd.isna(slope):
            return np.nan
        
        if slope > 1:
            return 5.0
        elif slope < -1:
            return 0.0
        else:
            # 5% of ((Slope + 1) x 50) = (slope + 1) * 50 * 0.05 = (slope + 1) * 2.5
            return (slope + 1) * 2.5
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate RSI (Relative Strength Index) using Wilder's smoothing method.
        
        Args:
            prices: Series of closing prices
            period: RSI period (default 14)
        
        Returns:
            Series of RSI values (0-100)
        """
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0.0)
        losses = (-delta).where(delta < 0, 0.0)
        
        # Use Wilder's smoothing (exponential moving average with alpha = 1/period)
        avg_gains = gains.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
        avg_losses = losses.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_sctr_score(self, prices: pd.Series) -> pd.Series:
        """
        Calculate full SCTR indicator score for a price series.
        
        The indicator score combines all six components:
        - Percent above/below 200-day EMA × 0.30
        - 125-day ROC × 0.30
        - Percent above/below 50-day EMA × 0.15
        - 20-day ROC × 0.15
        - PPO histogram slope score (0-5 points)
        - 14-day RSI × 0.05
        
        Note: This returns a raw score, not a percentile rank.
        The final SCTR value is determined by ranking these scores
        against peers in the same universe.
        
        Args:
            prices: Series of closing prices (needs ~250+ data points for accuracy)
        
        Returns:
            Series of SCTR indicator scores
        """
        if len(prices) < 200:
            logger.warning(f"Price series has only {len(prices)} points, need 200+ for accurate SCTR")
            return pd.Series([np.nan] * len(prices), index=prices.index)
        
        # Long-term indicators (60% weight)
        pct_above_200 = self.calculate_percent_above_ema(prices, 200)
        roc_125 = self.calculate_roc(prices, 125)
        
        # Medium-term indicators (30% weight)
        pct_above_50 = self.calculate_percent_above_ema(prices, 50)
        roc_20 = self.calculate_roc(prices, 20)
        
        # Short-term indicators (10% weight)
        ppo_slope = self.calculate_ppo_histogram_slope(prices)
        rsi_14 = self.calculate_rsi(prices, 14)
        
        # Calculate component scores
        # For percentage-based indicators, the raw value is used directly
        # according to the StockCharts methodology
        long_term_score = (
            pct_above_200 * self.WEIGHT_200_EMA +
            roc_125 * self.WEIGHT_125_ROC
        )
        
        medium_term_score = (
            pct_above_50 * self.WEIGHT_50_EMA +
            roc_20 * self.WEIGHT_20_ROC
        )
        
        # PPO slope needs special handling
        ppo_slope_scores = ppo_slope.apply(self.calculate_ppo_slope_score)
        
        # RSI contributes directly (5% of RSI value)
        rsi_contribution = rsi_14 * self.WEIGHT_RSI
        
        short_term_score = ppo_slope_scores + rsi_contribution
        
        # Total indicator score
        total_score = long_term_score + medium_term_score + short_term_score
        
        return total_score
    
    def get_latest_sctr_score(self, prices: pd.Series) -> Optional[float]:
        """
        Get the most recent SCTR indicator score.
        
        Args:
            prices: Series of closing prices
        
        Returns:
            Latest SCTR score or None if not enough data
        """
        scores = self.calculate_sctr_score(prices)
        
        if scores.empty:
            return None
        
        latest = scores.iloc[-1]
        return latest if not pd.isna(latest) else None
    
    def get_sctr_at_date(
        self,
        prices: pd.Series,
        target_date: pd.Timestamp
    ) -> Optional[float]:
        """
        Get SCTR indicator score for a specific date.
        
        Args:
            prices: Series of closing prices
            target_date: Date to get score for
        
        Returns:
            SCTR score at date or None
        """
        scores = self.calculate_sctr_score(prices)
        
        if scores.empty:
            return None
        
        # Find the closest date <= target_date
        valid_dates = scores.index[scores.index <= target_date]
        if len(valid_dates) == 0:
            return None
        
        closest_date = valid_dates[-1]
        score = scores.loc[closest_date]
        
        return score if not pd.isna(score) else None


def calculate_sctr_percentile_ranks(sctr_scores: pd.Series) -> pd.Series:
    """
    Calculate percentile ranks for SCTR scores within a group.
    
    Converts raw SCTR indicator scores to percentile rankings (0-99.99)
    relative to peers in the same universe.
    
    Args:
        sctr_scores: Series of SCTR indicator scores (indexed by ticker/entity)
    
    Returns:
        Series of percentile ranks (0-100)
    """
    # Drop NaN values for ranking
    valid_scores = sctr_scores.dropna()
    
    if valid_scores.empty:
        return pd.Series(dtype=float)
    
    # Calculate percentile rank
    # rank(pct=True) gives values from 0 to 1
    percentiles = valid_scores.rank(pct=True) * 100
    
    # Cap at 99.99 (no stock gets 100)
    percentiles = percentiles.clip(upper=99.99)
    
    return percentiles
