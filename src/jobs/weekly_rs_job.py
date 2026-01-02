"""
Weekly RS calculation job.

Runs every Saturday to calculate Mansfield RS for all sub-industries
for the week that just ended (Friday).
"""
import logging
from datetime import datetime, timezone

from src.models import SessionLocal, JobLog, JobStatus
from src.services.aggregator import SubIndustryAggregator, get_last_friday

logger = logging.getLogger(__name__)


def run_weekly_rs_job() -> dict:
    """
    Main weekly RS calculation job.
    
    Calculates Mansfield RS for all GICS sub-industries
    for the most recent complete week.
    
    Returns:
        Dict with job results
    """
    logger.info("=" * 50)
    logger.info("Starting weekly RS calculation job")
    logger.info("=" * 50)
    
    db = SessionLocal()
    
    # Create job log entry
    job_log = JobLog(
        job_name="weekly_rs_calculation",
        started_at=datetime.now(timezone.utc),
        status=JobStatus.STARTED
    )
    db.add(job_log)
    db.commit()
    
    result = {
        'success': False,
        'records_processed': 0,
        'error': None
    }
    
    try:
        # Get the week to calculate
        week_end = get_last_friday()
        logger.info(f"Calculating RS for week ending: {week_end}")
        
        # Create aggregator and calculate
        aggregator = SubIndustryAggregator(db)
        records_stored = aggregator.store_weekly_rs(week_end)
        
        # Update job log
        job_log.status = JobStatus.SUCCESS
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.records_processed = records_stored
        db.commit()
        
        result['success'] = True
        result['records_processed'] = records_stored
        
        logger.info(f"Successfully calculated RS for {records_stored} sub-industries")
        
    except Exception as e:
        logger.exception(f"Weekly RS job failed: {e}")
        
        job_log.status = JobStatus.FAILED
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.error_message = str(e)
        db.commit()
        
        result['error'] = str(e)
        
    finally:
        db.close()
    
    logger.info("=" * 50)
    logger.info("Weekly RS job completed")
    logger.info("=" * 50)
    
    return result


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

