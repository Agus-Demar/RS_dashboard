"""
Daily price refresh job.

Runs every weekday evening to fetch the latest price data
for all tracked stocks.
"""
import logging
from datetime import datetime, date, timedelta, timezone

from src.config import settings
from src.models import SessionLocal, Stock, StockPrice, JobLog, JobStatus
from src.ingestion.sources.yfinance_source import yfinance_source

logger = logging.getLogger(__name__)


def run_daily_prices_job() -> dict:
    """
    Daily price data refresh job.
    
    Fetches today's prices for all active stocks
    and updates the database.
    
    Returns:
        Dict with job results
    """
    logger.info("=" * 50)
    logger.info("Starting daily price refresh job")
    logger.info("=" * 50)
    
    db = SessionLocal()
    
    # Create job log entry
    job_log = JobLog(
        job_name="daily_price_refresh",
        started_at=datetime.now(timezone.utc),
        status=JobStatus.STARTED
    )
    db.add(job_log)
    db.commit()
    
    result = {
        'success': False,
        'stocks_updated': 0,
        'prices_added': 0,
        'error': None
    }
    
    try:
        # Get all active stocks
        stocks = db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in stocks]
        
        logger.info(f"Refreshing prices for {len(tickers)} stocks")
        
        # Fetch last 5 days of prices (to catch any missed days)
        end_date = date.today()
        start_date = end_date - timedelta(days=5)
        
        # Batch fetch prices
        all_prices = yfinance_source.fetch_multiple_prices(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            batch_size=50
        )
        
        # Also fetch benchmark
        benchmark_ticker = settings.BENCHMARK_TICKER
        if benchmark_ticker not in all_prices:
            benchmark_prices = yfinance_source.fetch_price_history(
                benchmark_ticker, start_date, end_date
            )
            if not benchmark_prices.empty:
                all_prices[benchmark_ticker] = benchmark_prices
        
        # Store prices
        prices_added = 0
        stocks_updated = 0
        
        for ticker, df in all_prices.items():
            if df.empty:
                continue
            
            added_for_ticker = 0
            for _, row in df.iterrows():
                # Check if already exists
                existing = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
                try:
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
                    db.add(price)
                    added_for_ticker += 1
                except Exception as e:
                    logger.warning(f"Error adding price for {ticker}: {e}")
            
            if added_for_ticker > 0:
                stocks_updated += 1
                prices_added += added_for_ticker
        
        db.commit()
        
        # Update job log
        job_log.status = JobStatus.SUCCESS
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.records_processed = prices_added
        db.commit()
        
        result['success'] = True
        result['stocks_updated'] = stocks_updated
        result['prices_added'] = prices_added
        
        logger.info(f"Updated {stocks_updated} stocks with {prices_added} new price records")
        
    except Exception as e:
        logger.exception(f"Daily price job failed: {e}")
        
        job_log.status = JobStatus.FAILED
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.error_message = str(e)
        db.commit()
        
        result['error'] = str(e)
        
    finally:
        db.close()
    
    logger.info("=" * 50)
    logger.info("Daily price job completed")
    logger.info("=" * 50)
    
    return result

