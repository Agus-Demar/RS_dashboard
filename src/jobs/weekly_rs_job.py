"""
Weekly data update job.

Runs every Saturday to:
1. Refresh price data for the past week (fill any gaps)
2. Calculate Mansfield RS for all sub-industries for the week that just ended
"""
import logging
from datetime import datetime, timezone

from src.models import SessionLocal, JobLog, JobStatus
from src.services.aggregator import SubIndustryAggregator, get_last_friday

logger = logging.getLogger(__name__)


def run_weekly_data_update() -> dict:
    """
    Unified weekly data update job.
    
    1. First refreshes price data to fill any gaps from the past week
    2. Then calculates Mansfield RS for all GICS sub-industries
    
    Returns:
        Dict with combined job results
    """
    logger.info("=" * 60)
    logger.info("Starting weekly data update (prices + RS calculation)")
    logger.info("=" * 60)
    
    db = SessionLocal()
    
    # Create job log entry
    job_log = JobLog(
        job_name="weekly_data_update",
        started_at=datetime.now(timezone.utc),
        status=JobStatus.STARTED
    )
    db.add(job_log)
    db.commit()
    
    result = {
        'success': False,
        'prices_added': 0,
        'stocks_updated': 0,
        'rs_records_processed': 0,
        'error': None
    }
    
    try:
        # Step 1: Refresh any missing prices (smart detection)
        logger.info("-" * 40)
        logger.info("Step 1: Refreshing missing price data...")
        logger.info("-" * 40)
        
        from src.jobs.daily_prices_job import run_missing_prices_job
        # Use 14 days lookback to catch any gaps from the past two weeks
        price_result = run_missing_prices_job(lookback_days=14, db_session=db)
        
        result['prices_added'] = price_result.get('prices_added', 0)
        result['stocks_updated'] = price_result.get('stocks_updated', 0)
        
        if not price_result.get('success'):
            logger.warning(f"Price refresh had issues: {price_result.get('error')}")
            # Continue with RS calculation even if price refresh had issues
        
        # Step 2: Calculate RS for the last complete week
        logger.info("-" * 40)
        logger.info("Step 2: Calculating weekly RS...")
        logger.info("-" * 40)
        
        week_end = get_last_friday()
        logger.info(f"Calculating RS for week ending: {week_end}")
        
        aggregator = SubIndustryAggregator(db)
        records_stored = aggregator.store_weekly_rs(week_end)
        
        result['rs_records_processed'] = records_stored
        
        # Update job log
        job_log.status = JobStatus.SUCCESS
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.records_processed = records_stored
        db.commit()
        
        result['success'] = True
        
        logger.info(f"Updated {result['stocks_updated']} stocks with {result['prices_added']} prices")
        logger.info(f"Calculated RS for {records_stored} sub-industries")
        
    except Exception as e:
        logger.exception(f"Weekly data update failed: {e}")
        
        job_log.status = JobStatus.FAILED
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.error_message = str(e)
        db.commit()
        
        result['error'] = str(e)
        
    finally:
        db.close()
    
    logger.info("=" * 60)
    logger.info("Weekly data update completed")
    logger.info("=" * 60)
    
    return result


# Legacy function for backwards compatibility
def run_weekly_rs_job() -> dict:
    """Legacy function - now calls unified weekly data update."""
    return run_weekly_data_update()


def backfill_rs(weeks: int = 17) -> dict:
    """
    Backfill RS data for historical weeks.
    
    Args:
        weeks: Number of weeks to backfill
    
    Returns:
        Dict with backfill results
    """
    from datetime import timedelta
    
    logger.info(f"Starting RS backfill for {weeks} weeks")
    
    db = SessionLocal()
    aggregator = SubIndustryAggregator(db)
    
    results = {
        'weeks_processed': 0,
        'total_records': 0,
        'errors': []
    }
    
    try:
        # Start from most recent Friday
        current_friday = get_last_friday()
        
        for i in range(weeks):
            week_end = current_friday - timedelta(weeks=i)
            logger.info(f"Backfilling week {i+1}/{weeks}: {week_end}")
            
            try:
                records = aggregator.store_weekly_rs(week_end)
                results['total_records'] += records
                results['weeks_processed'] += 1
                logger.info(f"  Stored {records} records")
            except Exception as e:
                logger.error(f"  Error: {e}")
                results['errors'].append(f"Week {week_end}: {e}")
        
    finally:
        db.close()
    
    logger.info(f"Backfill complete: {results['weeks_processed']} weeks, {results['total_records']} records")
    return results

