#!/usr/bin/env python3
"""
RS Backfill Script

Calculates and stores Mansfield RS values for historical weeks.
Useful for:
- Initial setup after loading price data
- Rebuilding RS data after changes
- Catching up after missed scheduled runs

Usage:
    python -m scripts.backfill_rs
    
    With options:
    python -m scripts.backfill_rs --weeks 26
    python -m scripts.backfill_rs --from-date 2024-01-01
"""
import argparse
import logging
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import settings
from src.models import SessionLocal, init_db
from src.services.aggregator import SubIndustryAggregator, get_last_friday


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Backfill RS Dashboard historical data"
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=17,
        help="Number of weeks to backfill (default: 17)"
    )
    parser.add_argument(
        "--from-date",
        type=str,
        help="Start backfill from this date (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--to-date",
        type=str,
        help="End backfill at this date (YYYY-MM-DD, default: last Friday)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("RS Backfill Script")
    logger.info("=" * 60)
    
    # Initialize database
    init_db()
    
    # Parse dates
    end_friday = get_last_friday()
    if args.to_date:
        try:
            to_date = datetime.strptime(args.to_date, "%Y-%m-%d").date()
            # Find Friday of that week
            days_to_friday = (4 - to_date.weekday()) % 7
            end_friday = to_date + timedelta(days=days_to_friday)
        except ValueError:
            logger.error(f"Invalid date format: {args.to_date}")
            sys.exit(1)
    
    if args.from_date:
        try:
            from_date = datetime.strptime(args.from_date, "%Y-%m-%d").date()
            # Calculate weeks between from_date and end_friday
            weeks = ((end_friday - from_date).days // 7) + 1
        except ValueError:
            logger.error(f"Invalid date format: {args.from_date}")
            sys.exit(1)
    else:
        weeks = args.weeks
    
    logger.info(f"Backfilling {weeks} weeks ending at {end_friday}")
    
    db = SessionLocal()
    aggregator = SubIndustryAggregator(db)
    
    results = {
        'weeks_processed': 0,
        'total_records': 0,
        'errors': []
    }
    
    try:
        for i in range(weeks):
            week_end = end_friday - timedelta(weeks=i)
            week_num = i + 1
            
            logger.info(f"[{week_num}/{weeks}] Processing week ending {week_end}...")
            
            try:
                records = aggregator.store_weekly_rs(week_end)
                results['total_records'] += records
                results['weeks_processed'] += 1
                logger.info(f"  -> Stored {records} RS records")
            except Exception as e:
                logger.error(f"  -> Error: {e}")
                results['errors'].append(f"Week {week_end}: {str(e)}")
        
    finally:
        db.close()
    
    # Print summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Backfill Complete")
    logger.info("=" * 60)
    logger.info(f"Weeks processed: {results['weeks_processed']}/{weeks}")
    logger.info(f"Total RS records: {results['total_records']}")
    
    if results['errors']:
        logger.warning(f"Errors encountered: {len(results['errors'])}")
        for error in results['errors'][:5]:
            logger.warning(f"  - {error}")
        if len(results['errors']) > 5:
            logger.warning(f"  ... and {len(results['errors']) - 5} more")
    
    logger.info("")


if __name__ == "__main__":
    main()

