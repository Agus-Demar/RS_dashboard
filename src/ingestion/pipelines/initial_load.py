"""
Initial data load pipeline.

Populates the database with:
1. GICS sub-industry reference data
2. S&P 500 stock records
3. Historical price data (2 years)
"""
import logging
from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from src.config import settings
from src.models import GICSSubIndustry, Stock, StockPrice, init_db
from src.ingestion.sources.yfinance_source import yfinance_source
from src.ingestion.sources.wikipedia_source import wikipedia_source
from src.ingestion.mappers.gics_mapper import gics_mapper

logger = logging.getLogger(__name__)


class InitialLoadPipeline:
    """
    Pipeline for initial data population.
    
    Steps:
    1. Initialize database tables
    2. Fetch S&P index constituents from Wikipedia (500 + 400 + 600)
    3. Create GICS sub-industry records
    4. Create Stock records with GICS mapping
    5. Fetch and store 2 years of price history
    
    This provides approximately 1,500 stocks with GICS sub-industry classifications.
    """
    
    def __init__(self, db: Session, use_all_indices: bool = True):
        """
        Initialize pipeline.
        
        Args:
            db: SQLAlchemy database session
            use_all_indices: If True, use all S&P indices (500+400+600).
                           If False, use only S&P 500.
        """
        self.db = db
        self.lookback_years = settings.PRICE_HISTORY_YEARS
        self.use_all_indices = use_all_indices
    
    def run(self) -> dict:
        """
        Execute the full initial load pipeline.
        
        Returns:
            Dict with statistics about loaded data
        """
        logger.info("=" * 50)
        logger.info("Starting initial data load pipeline")
        logger.info("=" * 50)
        
        stats = {
            'subindustries_created': 0,
            'stocks_created': 0,
            'prices_stored': 0,
            'errors': []
        }
        
        try:
            # Step 1: Initialize database
            logger.info("Step 1: Initializing database...")
            init_db()
            
            # Step 2: Load GICS sub-industries
            logger.info("Step 2: Loading GICS sub-industries...")
            stats['subindustries_created'] = self._load_subindustries()
            
            # Step 3: Create stock records
            logger.info("Step 3: Creating stock records...")
            stats['stocks_created'] = self._create_stock_records(use_all_indices=self.use_all_indices)
            
            # Step 4: Fetch price history
            logger.info("Step 4: Fetching price history...")
            stats['prices_stored'] = self._fetch_price_history()
            
            logger.info("=" * 50)
            logger.info("Initial data load complete!")
            logger.info(f"  Sub-industries: {stats['subindustries_created']}")
            logger.info(f"  Stocks: {stats['stocks_created']}")
            logger.info(f"  Price records: {stats['prices_stored']}")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.exception(f"Pipeline failed: {e}")
            stats['errors'].append(str(e))
            raise
        
        return stats
    
    def _load_subindustries(self) -> int:
        """Load GICS sub-industries from Wikipedia data (all S&P indices)."""
        # Get unique sub-industries from all S&P indices
        subindustries_df = gics_mapper.get_all_subindustries()
        
        count = 0
        for _, row in subindustries_df.iterrows():
            code = row['code']
            
            # Check if already exists
            existing = self.db.query(GICSSubIndustry).filter(
                GICSSubIndustry.code == code
            ).first()
            
            if existing:
                continue
            
            subindustry = GICSSubIndustry(
                code=code,
                name=row['sub_industry'],
                industry_code=row['industry_code'],
                industry_name=row['sub_industry'],  # Using sub_industry as industry
                industry_group_code=row['industry_group_code'],
                industry_group_name=row['sub_industry'].split(' - ')[0],
                sector_code=row['sector_code'],
                sector_name=row['sector'],
            )
            self.db.add(subindustry)
            count += 1
        
        self.db.commit()
        logger.info(f"Created {count} GICS sub-industry records")
        return count
    
    def _create_stock_records(self, use_all_indices: bool = True) -> int:
        """
        Create Stock records from S&P index data.
        
        Args:
            use_all_indices: If True, use all S&P indices (500+400+600).
                           If False, use only S&P 500.
        
        Returns:
            Number of stock records created
        """
        if use_all_indices:
            logger.info("Loading stocks from all S&P indices (500 + 400 + 600)...")
            stocks_df = wikipedia_source.fetch_all_sp_constituents()
        else:
            logger.info("Loading stocks from S&P 500 only...")
            stocks_df = wikipedia_source.fetch_sp500_constituents()
        
        logger.info(f"Processing {len(stocks_df)} stocks from Wikipedia...")
        
        count = 0
        skipped_no_mapping = 0
        skipped_no_subindustry = 0
        skipped_existing = 0
        
        for _, row in stocks_df.iterrows():
            ticker = row['ticker']
            
            # Check if already exists
            existing = self.db.query(Stock).filter(Stock.ticker == ticker).first()
            if existing:
                skipped_existing += 1
                continue
            
            # Get GICS mapping
            mapping = gics_mapper.map_ticker(ticker)
            if not mapping:
                logger.debug(f"No GICS mapping for {ticker}, skipping")
                skipped_no_mapping += 1
                continue
            
            # Verify sub-industry exists
            subindustry = self.db.query(GICSSubIndustry).filter(
                GICSSubIndustry.code == mapping['subindustry_code']
            ).first()
            
            if not subindustry:
                logger.debug(f"Sub-industry {mapping['subindustry_code']} not found for {ticker}")
                skipped_no_subindustry += 1
                continue
            
            stock = Stock(
                ticker=ticker,
                name=row.get('name', ticker),
                gics_subindustry_code=mapping['subindustry_code'],
                is_active=True,
            )
            self.db.add(stock)
            count += 1
        
        self.db.commit()
        logger.info(f"Created {count} stock records")
        if skipped_existing > 0:
            logger.info(f"  Skipped {skipped_existing} existing stocks")
        if skipped_no_mapping > 0:
            logger.info(f"  Skipped {skipped_no_mapping} stocks without GICS mapping")
        if skipped_no_subindustry > 0:
            logger.info(f"  Skipped {skipped_no_subindustry} stocks without sub-industry")
        
        return count
    
    def _fetch_price_history(self) -> int:
        """Fetch and store historical prices for all stocks."""
        # Get all active stocks
        stocks = self.db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in stocks]
        
        if not tickers:
            logger.warning("No stocks to fetch prices for")
            return 0
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=self.lookback_years * 365 + 30)
        
        logger.info(f"Fetching prices for {len(tickers)} stocks from {start_date} to {end_date}")
        
        # Fetch prices in batch
        all_prices = yfinance_source.fetch_multiple_prices(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            batch_size=50
        )
        
        # Also fetch benchmark (SPY)
        benchmark_ticker = settings.BENCHMARK_TICKER
        if benchmark_ticker not in all_prices:
            logger.info(f"Fetching benchmark ({benchmark_ticker}) prices...")
            
            # Create a stock record for benchmark if it doesn't exist
            benchmark_stock = self.db.query(Stock).filter(Stock.ticker == benchmark_ticker).first()
            if not benchmark_stock:
                # Get or create a placeholder sub-industry for the benchmark
                benchmark_mapping = gics_mapper.map_ticker(benchmark_ticker)
                if benchmark_mapping:
                    benchmark_stock = Stock(
                        ticker=benchmark_ticker,
                        name="SPDR S&P 500 ETF Trust",
                        gics_subindustry_code=benchmark_mapping['subindustry_code'],
                        is_active=True,
                    )
                    self.db.add(benchmark_stock)
                    self.db.commit()
            
            benchmark_prices = yfinance_source.fetch_price_history(
                benchmark_ticker, start_date, end_date
            )
            if not benchmark_prices.empty:
                all_prices[benchmark_ticker] = benchmark_prices
        
        # Store prices in database
        total_records = 0
        for ticker, df in all_prices.items():
            records_added = self._store_prices(ticker, df)
            total_records += records_added
            
            if total_records % 10000 == 0:
                logger.info(f"Stored {total_records} price records...")
        
        logger.info(f"Total price records stored: {total_records}")
        return total_records
    
    def _store_prices(self, ticker: str, df) -> int:
        """Store price data for a single ticker."""
        if df.empty:
            return 0
        
        count = 0
        for _, row in df.iterrows():
            try:
                # Check for existing record
                existing = self.db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
                price = StockPrice(
                    ticker=ticker,
                    date=row['date'],
                    open=row.get('open'),
                    high=row.get('high'),
                    low=row.get('low'),
                    close=row['close'],
                    adj_close=row.get('adj_close', row['close']),
                    volume=int(row['volume']) if 'volume' in row and row['volume'] else None,
                )
                self.db.add(price)
                count += 1
                
            except Exception as e:
                logger.warning(f"Error storing price for {ticker} on {row.get('date')}: {e}")
        
        # Commit in batches
        if count > 0:
            self.db.commit()
        
        return count
    
    def update_market_caps(self) -> int:
        """Update market caps for all stocks (optional step)."""
        stocks = self.db.query(Stock).filter(Stock.is_active == True).all()
        
        updated = 0
        for stock in stocks:
            try:
                info = yfinance_source.fetch_company_info(stock.ticker)
                if info.get('market_cap'):
                    stock.market_cap = info['market_cap']
                    updated += 1
            except Exception as e:
                logger.warning(f"Could not fetch market cap for {stock.ticker}: {e}")
        
        self.db.commit()
        logger.info(f"Updated market caps for {updated} stocks")
        return updated

