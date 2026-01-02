"""
APScheduler configuration.

Sets up scheduled jobs for:
- Weekly RS calculation (Saturday 6 AM ET)
- Daily price refresh (Mon-Fri 7 PM ET)
"""
import logging
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import settings

logger = logging.getLogger(__name__)

# Global scheduler instance
_scheduler: Optional[BackgroundScheduler] = None


def get_scheduler() -> BackgroundScheduler:
    """Get or create the scheduler instance."""
    global _scheduler
    
    if _scheduler is None:
        _scheduler = BackgroundScheduler(
            timezone=settings.SCHEDULER_TIMEZONE,
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': 3600 * 6,  # 6 hours
            }
        )
    
    return _scheduler


def start_scheduler() -> None:
    """Start the scheduler with configured jobs."""
    scheduler = get_scheduler()
    
    if scheduler.running:
        logger.warning("Scheduler is already running")
        return
    
    # Import job functions
    from src.jobs.weekly_rs_job import run_weekly_rs_job
    from src.jobs.daily_prices_job import run_daily_prices_job
    
    # Weekly RS calculation: Saturday 6 AM ET
    scheduler.add_job(
        run_weekly_rs_job,
        trigger=CronTrigger(
            day_of_week="sat",
            hour=6,
            minute=0,
            timezone=settings.SCHEDULER_TIMEZONE
        ),
        id="weekly_rs_calculation",
        name="Weekly Mansfield RS Calculation",
        replace_existing=True,
    )
    logger.info("Added weekly RS job: Saturday 6 AM ET")
    
    # Daily price refresh: Mon-Fri 7 PM ET
    scheduler.add_job(
        run_daily_prices_job,
        trigger=CronTrigger(
            day_of_week="mon-fri",
            hour=19,
            minute=0,
            timezone=settings.SCHEDULER_TIMEZONE
        ),
        id="daily_price_refresh",
        name="Daily Price Data Refresh",
        replace_existing=True,
    )
    logger.info("Added daily price job: Mon-Fri 7 PM ET")
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started successfully")
    
    # Log scheduled jobs
    for job in scheduler.get_jobs():
        logger.info(f"Scheduled job: {job.name} - Next run: {job.next_run_time}")


def stop_scheduler() -> None:
    """Stop the scheduler gracefully."""
    global _scheduler
    
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=True)
        logger.info("Scheduler stopped")
    
    _scheduler = None


def run_job_now(job_id: str) -> bool:
    """
    Manually trigger a scheduled job immediately.
    
    Args:
        job_id: ID of the job to run
    
    Returns:
        True if job was triggered, False otherwise
    """
    scheduler = get_scheduler()
    
    job = scheduler.get_job(job_id)
    if job is None:
        logger.error(f"Job {job_id} not found")
        return False
    
    job.modify(next_run_time=None)  # Run immediately
    logger.info(f"Triggered job: {job_id}")
    return True

