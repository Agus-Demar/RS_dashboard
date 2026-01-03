"""
Sub-Industry Aggregator.

Aggregates individual stock RS values into sub-industry level RS.
Uses market-cap weighting for more accurate representation.
"""
import logging
from datetime import date, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Stock, StockPrice, GICSSubIndustry, RSWeekly
from src.services.rs_calculator import MansfieldRSCalculator, calculate_percentile_ranks

logger = logging.getLogger(__name__)


class SubIndustryAggregator:
    """
    Aggregates individual stock data into sub-industry level RS.
    
    Uses market-cap weighting for accurate representation of
    sub-industry performance.
    """
    
    def __init__(self, db: Session, rs_calculator: Optional[MansfieldRSCalculator] = None):
        """
        Initialize aggregator.
        
        Args:
            db: SQLAlchemy database session
            rs_calculator: Optional RS calculator instance
        """
        self.db = db
        self.rs_calc = rs_calculator or MansfieldRSCalculator()
    
    def get_stock_prices(
        self,
        ticker: str,
        start_date: date,
        end_date: date
    ) -> pd.Series:
        """
        Get adjusted close prices for a stock.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date
            end_date: End date
        
        Returns:
            Series of adjusted close prices indexed by date
        """
        prices = self.db.query(StockPrice).filter(
            StockPrice.ticker == ticker,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        if not prices:
            return pd.Series(dtype=float)
        
        data = {p.date: p.adj_close for p in prices}
        return pd.Series(data).sort_index()
    
    def get_benchmark_prices(
        self,
        start_date: date,
        end_date: date
    ) -> pd.Series:
        """
        Get benchmark (SPY) prices.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Series of benchmark adjusted close prices
        """
        return self.get_stock_prices(settings.BENCHMARK_TICKER, start_date, end_date)
    
    def calculate_subindustry_prices(
        self,
        subindustry_code: str,
        start_date: date,
        end_date: date,
        method: str = "market_cap_weighted",
        min_history_weeks: int = 52
    ) -> pd.Series:
        """
        Calculate aggregated price series for a sub-industry.
        
        Args:
            subindustry_code: GICS sub-industry code
            start_date: Start date
            end_date: End date
            method: Aggregation method - 'market_cap_weighted' or 'equal_weighted'
            min_history_weeks: Minimum weeks of history required for a stock to be included
        
        Returns:
            Series of aggregated prices indexed by date
        """
        # Get all stocks in sub-industry
        stocks = self.db.query(Stock).filter(
            Stock.gics_subindustry_code == subindustry_code,
            Stock.is_active == True
        ).all()
        
        if not stocks:
            logger.debug(f"No stocks found for sub-industry {subindustry_code}")
            return pd.Series(dtype=float)
        
        # Calculate minimum required data points (approximately 5 trading days per week)
        min_data_points = min_history_weeks * 5
        
        # Collect prices and weights, filtering out stocks with insufficient history
        all_prices = []
        weights = []
        excluded_count = 0
        
        for stock in stocks:
            prices = self.get_stock_prices(stock.ticker, start_date, end_date)
            if prices.empty:
                continue
            
            # Filter out stocks with insufficient history
            if len(prices) < min_data_points:
                excluded_count += 1
                continue
            
            all_prices.append(prices)
            
            if method == "market_cap_weighted":
                weight = stock.market_cap if stock.market_cap else 1.0
            else:
                weight = 1.0
            
            weights.append(weight)
        
        if excluded_count > 0:
            logger.debug(
                f"Sub-industry {subindustry_code}: excluded {excluded_count} stocks "
                f"with <{min_history_weeks} weeks of data"
            )
        
        if not all_prices:
            return pd.Series(dtype=float)
        
        # Align all price series using inner join
        prices_df = pd.concat(all_prices, axis=1, join='inner')
        
        if prices_df.empty:
            return pd.Series(dtype=float)
        
        # Normalize weights
        weights_array = np.array(weights)
        weights_array = weights_array / weights_array.sum()
        
        # Calculate weighted average
        weighted_prices = (prices_df * weights_array).sum(axis=1)
        
        return weighted_prices
    
    def calculate_subindustry_rs(
        self,
        subindustry_code: str,
        start_date: date,
        end_date: date,
        method: str = "market_cap_weighted"
    ) -> pd.DataFrame:
        """
        Calculate Mansfield RS for a sub-industry.
        
        Args:
            subindustry_code: GICS sub-industry code
            start_date: Start date (should include 52+ weeks of history)
            end_date: End date
            method: Aggregation method
        
        Returns:
            DataFrame with RS components and metadata
        """
        # Get aggregated sub-industry prices
        subindustry_prices = self.calculate_subindustry_prices(
            subindustry_code, start_date, end_date, method
        )
        
        if subindustry_prices.empty:
            return pd.DataFrame()
        
        # Get benchmark prices
        benchmark_prices = self.get_benchmark_prices(start_date, end_date)
        
        if benchmark_prices.empty:
            logger.warning("No benchmark prices available")
            return pd.DataFrame()
        
        # Calculate RS
        rs_result = self.rs_calc.calculate_full(subindustry_prices, benchmark_prices)
        
        # Add metadata
        rs_result['subindustry_code'] = subindustry_code
        
        # Count constituents
        constituents_count = self.db.query(Stock).filter(
            Stock.gics_subindustry_code == subindustry_code,
            Stock.is_active == True
        ).count()
        rs_result['constituents_count'] = constituents_count
        
        return rs_result
    
    def calculate_weekly_rs_for_all(
        self,
        week_end_date: date,
        lookback_weeks: int = 60
    ) -> List[Dict]:
        """
        Calculate weekly RS for all sub-industries.
        
        Args:
            week_end_date: Friday of the target week
            lookback_weeks: Weeks of history to include for SMA calculation
        
        Returns:
            List of dicts with RS data for each sub-industry
        """
        # Calculate date range
        end_date = week_end_date
        start_date = end_date - timedelta(weeks=lookback_weeks)
        week_start_date = week_end_date - timedelta(days=4)  # Monday
        
        # Get all sub-industries
        subindustries = self.db.query(GICSSubIndustry).all()
        
        results = []
        
        for subindustry in subindustries:
            try:
                rs_df = self.calculate_subindustry_rs(
                    subindustry.code,
                    start_date,
                    end_date
                )
                
                if rs_df.empty:
                    continue
                
                # Get value for target date (or closest prior date)
                # Convert index to Timestamps for consistent comparison
                rs_df.index = pd.to_datetime(rs_df.index)
                target_date = pd.Timestamp(week_end_date)
                valid_data = rs_df[rs_df.index <= target_date]
                
                if valid_data.empty:
                    continue
                
                row = valid_data.iloc[-1]
                
                result = {
                    'subindustry_code': subindustry.code,
                    'week_end_date': week_end_date,
                    'week_start_date': week_start_date,
                    'rs_line': row['rs_line'],
                    'rs_line_sma_52w': row['rs_line_sma_52w'],
                    'mansfield_rs': row['mansfield_rs'],
                    'constituents_count': row['constituents_count'],
                }
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error calculating RS for {subindustry.code}: {e}")
                continue
        
        # Calculate percentile ranks
        if results:
            rs_values = pd.Series({
                r['subindustry_code']: r['mansfield_rs'] 
                for r in results 
                if r['mansfield_rs'] is not None and not np.isnan(r['mansfield_rs'])
            })
            
            percentiles = calculate_percentile_ranks(rs_values)
            
            for result in results:
                code = result['subindustry_code']
                if code in percentiles.index:
                    result['rs_percentile'] = int(percentiles[code])
                else:
                    result['rs_percentile'] = None
        
        logger.info(f"Calculated RS for {len(results)} sub-industries for week {week_end_date}")
        return results
    
    def store_weekly_rs(self, week_end_date: date) -> int:
        """
        Calculate and store weekly RS for all sub-industries.
        
        Args:
            week_end_date: Friday of the target week
        
        Returns:
            Number of records stored
        """
        results = self.calculate_weekly_rs_for_all(week_end_date)
        
        stored = 0
        for result in results:
            # Check for existing record
            existing = self.db.query(RSWeekly).filter(
                RSWeekly.subindustry_code == result['subindustry_code'],
                RSWeekly.week_end_date == result['week_end_date']
            ).first()
            
            if existing:
                # Update existing record
                existing.rs_line = result['rs_line']
                existing.rs_line_sma_52w = result['rs_line_sma_52w']
                existing.mansfield_rs = result['mansfield_rs']
                existing.rs_percentile = result.get('rs_percentile')
                existing.constituents_count = result['constituents_count']
            else:
                # Create new record
                rs_weekly = RSWeekly(
                    subindustry_code=result['subindustry_code'],
                    week_end_date=result['week_end_date'],
                    week_start_date=result['week_start_date'],
                    rs_line=result['rs_line'],
                    rs_line_sma_52w=result['rs_line_sma_52w'],
                    mansfield_rs=result['mansfield_rs'],
                    rs_percentile=result.get('rs_percentile'),
                    constituents_count=result['constituents_count'],
                )
                self.db.add(rs_weekly)
            
            stored += 1
        
        self.db.commit()
        return stored


def get_last_friday(reference_date: Optional[date] = None) -> date:
    """
    Get the most recent Friday (last complete trading week).
    
    Args:
        reference_date: Date to find Friday for (default: today)
    
    Returns:
        Date of the most recent Friday
    """
    if reference_date is None:
        reference_date = date.today()
    
    # weekday(): Monday=0, Friday=4
    days_since_friday = (reference_date.weekday() - 4) % 7
    
    # If today is Friday, use previous Friday (current week not complete)
    if days_since_friday == 0 and reference_date.weekday() == 4:
        days_since_friday = 7
    
    return reference_date - timedelta(days=days_since_friday)


def get_week_ranges(months_back: int = 4, reference_date: Optional[date] = None) -> List[Dict]:
    """
    Generate week ranges for the past N months.
    
    Args:
        months_back: Number of months to go back
        reference_date: Reference date (default: today)
    
    Returns:
        List of dicts with week_start, week_end, and label
    """
    last_friday = get_last_friday(reference_date)
    weeks_count = int(months_back * 4.33)  # ~4.33 weeks per month
    
    weeks = []
    for i in range(weeks_count):
        week_end = last_friday - timedelta(weeks=i)
        week_start = week_end - timedelta(days=4)  # Monday
        
        weeks.append({
            'week_start': week_start,
            'week_end': week_end,
            'label': week_end.strftime("%d/%m/%y"),
            'week_number': i + 1
        })
    
    return weeks

