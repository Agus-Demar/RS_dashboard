"""
Industry Aggregator.

Aggregates individual stock RS values into industry level RS.
Uses market-cap weighting for more accurate representation.

For industries with unique ETF proxies, uses the corresponding ETF 
as a direct proxy for more accurate RS calculation. Industries that
share an ETF with others use market-cap-weighted aggregation instead.

IMPORTANT: Uses stockcharts_loader as the ground truth for industry/stock
structure. The scraped data from StockCharts.com is the canonical source.
"""
import logging
from datetime import date, timedelta
from typing import Dict, List, Optional, Set

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from src.config import settings
from src.models import Stock, StockPrice, GICSSubIndustry, RSWeekly
from src.services.rs_calculator import MansfieldRSCalculator, calculate_percentile_ranks
from src.data.stockcharts_loader import (
    get_loader,
    get_etf_for_industry,
    should_use_aggregation,
    get_shared_etfs as get_shared_etfs_from_loader,
)

logger = logging.getLogger(__name__)


def _get_shared_etfs() -> Set[str]:
    """
    Get ETFs that are used by multiple industries.
    
    Uses the StockCharts data loader as the source of truth.
    Industries sharing an ETF should use aggregated stock prices
    instead of ETF prices to ensure unique RS/SCTR values.
    
    Returns:
        Set of ETF tickers that are shared by multiple industries
    """
    return get_shared_etfs_from_loader()


# Cache shared ETFs at module load time (will load from scraped data)
SHARED_ETFS = _get_shared_etfs()


class SubIndustryAggregator:
    """
    Aggregates individual stock data into sub-industry level RS.
    
    Uses market-cap weighting for accurate representation of
    sub-industry performance.
    
    For sub-industries with StockCharts industry index symbols, uses
    the primary ETF as a direct proxy for RS calculation.
    """
    
    def __init__(
        self, 
        db: Session, 
        rs_calculator: Optional[MansfieldRSCalculator] = None,
        use_industry_indices: bool = True
    ):
        """
        Initialize aggregator.
        
        Args:
            db: SQLAlchemy database session
            rs_calculator: Optional RS calculator instance
            use_industry_indices: If True, use ETF proxies for sub-industries
                                  with StockCharts index symbols
        """
        self.db = db
        self.rs_calc = rs_calculator or MansfieldRSCalculator()
        self.use_industry_indices = use_industry_indices
    
    def get_subindustry_etf(self, subindustry_code: str) -> Optional[str]:
        """
        Get the ETF ticker to use as proxy for a sub-industry RS calculation.
        
        Uses the StockCharts data loader as the source of truth.
        
        Returns an ETF only if it meets ALL of these criteria:
        - The ETF is not a broad sector fallback (is_sector_fallback=False)
        - The ETF is NOT shared by multiple industries
        - The ETF specifically tracks this sub-industry
        
        Industries sharing an ETF with others should use aggregated stock prices
        to ensure unique RS/SCTR evolutions.
        
        Examples of unique ETFs (will be used):
        - XBI for Biotechnology
        - XOP for Oil & Gas E&P
        - SMH for Semiconductors
        - JETS for Airlines
        
        Examples of shared ETFs (will use aggregation instead):
        - XRT (shared by retail industries)
        - XHB (shared by homebuilding industries)
        - KIE (shared by insurance industries)
        - ITA (shared by Aerospace and Defense)
        
        Args:
            subindustry_code: 6-digit StockCharts industry code
        
        Returns:
            ETF ticker or None if should use aggregated calculation
        """
        if not self.use_industry_indices:
            return None
        
        # Use the StockCharts data loader as source of truth
        etf = get_etf_for_industry(subindustry_code)
        
        if etf is None:
            # Log why we're using aggregation
            if should_use_aggregation(subindustry_code):
                loader = get_loader()
                industry = loader.get_industry(subindustry_code)
                if industry:
                    if industry.is_sector_fallback:
                        logger.debug(
                            f"Industry {subindustry_code} ({industry.name}) uses sector fallback ETF, "
                            f"using aggregation"
                        )
                    elif industry.primary_etf in loader.shared_etfs:
                        logger.debug(
                            f"ETF {industry.primary_etf} is shared by multiple industries, "
                            f"using aggregation for {subindustry_code} ({industry.name})"
                        )
        
        return etf
    
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
        min_history_weeks: int = 52,
        max_stocks: int = 20
    ) -> pd.Series:
        """
        Calculate aggregated price series for a sub-industry.
        
        Uses top stocks by market cap with sanity checks to ensure
        consistent price series without corrupted data.
        
        Args:
            subindustry_code: GICS sub-industry code
            start_date: Start date
            end_date: End date
            method: Aggregation method - 'market_cap_weighted' or 'equal_weighted'
            min_history_weeks: Minimum weeks of history required for a stock to be included
            max_stocks: Maximum number of stocks to include
        
        Returns:
            Series of aggregated prices indexed by date
        """
        from sqlalchemy import desc
        
        # Get stocks ordered by market cap (use a larger pool to filter from)
        stocks = self.db.query(Stock).filter(
            Stock.gics_subindustry_code == subindustry_code,
            Stock.is_active == True
        ).order_by(desc(Stock.market_cap)).limit(max_stocks * 5).all()
        
        if not stocks:
            logger.debug(f"No stocks found for sub-industry {subindustry_code}")
            return pd.Series(dtype=float)
        
        # Calculate minimum required data points
        min_data_points = min_history_weeks * 5
        
        # Collect valid price series with sanity checks
        valid_stocks = []
        
        for stock in stocks:
            prices = self.get_stock_prices(stock.ticker, start_date, end_date)
            if prices.empty:
                continue
            
            # Filter out stocks with insufficient history
            if len(prices) < min_data_points:
                continue
            
            # Sanity check: reject stocks with extreme price swings
            # Max price should not be more than 100x min price (likely data errors)
            price_ratio = prices.max() / prices.min() if prices.min() > 0 else float('inf')
            if price_ratio > 100:
                logger.debug(f"Excluding {stock.ticker} from aggregation - extreme price ratio: {price_ratio:.1f}")
                continue
            
            # Reject prices over $10000 (likely data errors for most stocks)
            if prices.max() > 10000:
                logger.debug(f"Excluding {stock.ticker} from aggregation - price too high: {prices.max():.2f}")
                continue
            
            weight = stock.market_cap if (method == "market_cap_weighted" and stock.market_cap) else 1.0
            
            valid_stocks.append({
                'ticker': stock.ticker,
                'prices': prices,
                'weight': weight,
                'count': len(prices)
            })
            
            if len(valid_stocks) >= max_stocks:
                break
        
        if not valid_stocks:
            logger.debug(f"No valid stocks for sub-industry {subindustry_code} after filtering")
            return pd.Series(dtype=float)
        
        if len(valid_stocks) < 3:
            logger.debug(f"Sub-industry {subindustry_code}: only {len(valid_stocks)} stocks available")
        
        # Use inner join for clean overlapping dates
        prices_list = [d['prices'] for d in valid_stocks]
        weights = [d['weight'] for d in valid_stocks]
        
        prices_df = pd.concat(prices_list, axis=1, join='inner')
        
        if prices_df.empty:
            logger.debug(f"No overlapping price data for sub-industry {subindustry_code}")
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
        
        Priority order for price data:
        1. Unique industry ETF (not shared, not sector fallback)
        2. Market-cap-weighted aggregation of constituent stocks
        
        Industries sharing an ETF with others use aggregation to ensure
        unique RS evolutions. No sector ETF fallback is used.
        
        Args:
            subindustry_code: GICS sub-industry code
            start_date: Start date (should include 52+ weeks of history)
            end_date: End date
            method: Aggregation method (used only for fallback calculation)
        
        Returns:
            DataFrame with RS components and metadata (empty if no data available)
        """
        subindustry_prices = pd.Series(dtype=float)
        use_etf = False
        etf_ticker = None
        
        # Step 1: Try unique industry ETF (not shared, not sector fallback)
        unique_etf = self.get_subindustry_etf(subindustry_code)
        if unique_etf:
            etf_prices = self.get_stock_prices(unique_etf, start_date, end_date)
            if not etf_prices.empty and len(etf_prices) >= 200:
                subindustry_prices = etf_prices
                use_etf = True
                etf_ticker = unique_etf
                logger.debug(f"Using unique ETF {unique_etf} for industry {subindustry_code}")
        
        # Step 2: Try aggregated stock prices if no unique ETF or insufficient data
        if subindustry_prices.empty:
            subindustry_prices = self.calculate_subindustry_prices(
                subindustry_code, start_date, end_date, method
            )
            if not subindustry_prices.empty:
                logger.debug(f"Using aggregated stock prices for industry {subindustry_code}")
        
        # No sector ETF fallback - industries without stocks will have NaN values
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
        rs_result['uses_etf_proxy'] = use_etf
        if use_etf:
            rs_result['etf_ticker'] = etf_ticker
        
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
        
        Includes ALL industries from the database. Industries without sufficient
        data will have NaN values for RS metrics.
        
        Args:
            week_end_date: Friday of the target week
            lookback_weeks: Weeks of history to include for SMA calculation
        
        Returns:
            List of dicts with RS data for each sub-industry (all industries included)
        """
        # Calculate date range
        end_date = week_end_date
        start_date = end_date - timedelta(weeks=lookback_weeks)
        week_start_date = week_end_date - timedelta(days=4)  # Monday
        
        # Get all sub-industries
        subindustries = self.db.query(GICSSubIndustry).all()
        
        results = []
        industries_with_data = 0
        industries_without_data = 0
        
        for subindustry in subindustries:
            # Count constituents for this industry
            constituents_count = self.db.query(Stock).filter(
                Stock.gics_subindustry_code == subindustry.code,
                Stock.is_active == True
            ).count()
            
            try:
                rs_df = self.calculate_subindustry_rs(
                    subindustry.code,
                    start_date,
                    end_date
                )
                
                if rs_df.empty:
                    # No data available - include with NaN values
                    result = {
                        'subindustry_code': subindustry.code,
                        'week_end_date': week_end_date,
                        'week_start_date': week_start_date,
                        'rs_line': np.nan,
                        'rs_line_sma_52w': np.nan,
                        'mansfield_rs': np.nan,
                        'constituents_count': constituents_count,
                    }
                    results.append(result)
                    industries_without_data += 1
                    continue
                
                # Get value for target date (or closest prior date)
                # Convert index to Timestamps for consistent comparison
                rs_df.index = pd.to_datetime(rs_df.index)
                target_date = pd.Timestamp(week_end_date)
                valid_data = rs_df[rs_df.index <= target_date]
                
                if valid_data.empty:
                    # No data for target date - include with NaN values
                    result = {
                        'subindustry_code': subindustry.code,
                        'week_end_date': week_end_date,
                        'week_start_date': week_start_date,
                        'rs_line': np.nan,
                        'rs_line_sma_52w': np.nan,
                        'mansfield_rs': np.nan,
                        'constituents_count': constituents_count,
                    }
                    results.append(result)
                    industries_without_data += 1
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
                industries_with_data += 1
                
            except Exception as e:
                logger.error(f"Error calculating RS for {subindustry.code}: {e}")
                # Include with NaN values on error
                result = {
                    'subindustry_code': subindustry.code,
                    'week_end_date': week_end_date,
                    'week_start_date': week_start_date,
                    'rs_line': np.nan,
                    'rs_line_sma_52w': np.nan,
                    'mansfield_rs': np.nan,
                    'constituents_count': constituents_count,
                }
                results.append(result)
                industries_without_data += 1
        
        # Calculate percentile ranks (only for industries with valid RS values)
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
        
        logger.info(
            f"Calculated RS for {len(results)} industries for week {week_end_date} "
            f"({industries_with_data} with data, {industries_without_data} without)"
        )
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

