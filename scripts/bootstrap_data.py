#!/usr/bin/env python3
"""
Bootstrap Data Script

Initial data population script that:
1. Initializes the database
2. Loads S&P 500 constituents from Wikipedia
3. Creates GICS sub-industry records
4. Creates stock records
5. Fetches 2 years of price history
6. Calculates initial RS values

Usage:
    python -m scripts.bootstrap_data
    
    Or with options:
    python -m scripts.bootstrap_data --skip-prices --no-rs
"""
import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import settings
from src.models import SessionLocal, init_db
from src.ingestion.pipelines.initial_load import InitialLoadPipeline
from src.jobs.weekly_rs_job import backfill_rs


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bootstrap RS Dashboard data"
    )
    parser.add_argument(
        "--skip-prices",
        action="store_true",
        help="Skip fetching price history (useful for testing)"
    )
    parser.add_argument(
        "--no-rs",
        action="store_true",
        help="Skip RS calculation after data load"
    )
    parser.add_argument(
        "--rs-weeks",
        type=int,
        default=17,
        help="Number of weeks to backfill RS (default: 17)"
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
    logger.info("RS Dashboard Data Bootstrap")
    logger.info("=" * 60)
    logger.info(f"Database: {settings.DATABASE_PATH}")
    logger.info(f"Data directory: {settings.DATA_DIR}")
    logger.info("")
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Run initial load pipeline
        pipeline = InitialLoadPipeline(db)
        
        if args.skip_prices:
            # Just load GICS and stock data without prices
            logger.info("Loading GICS sub-industries...")
            pipeline._load_subindustries()
            
            logger.info("Creating stock records...")
            pipeline._create_stock_records()
            
            logger.info("Skipping price history (--skip-prices)")
        else:
            # Full pipeline
            stats = pipeline.run()
            
            logger.info("")
            logger.info("Data load complete:")
            logger.info(f"  Sub-industries: {stats['subindustries_created']}")
            logger.info(f"  Stocks: {stats['stocks_created']}")
            logger.info(f"  Price records: {stats['prices_stored']}")
        
        # Calculate RS values
        if not args.no_rs and not args.skip_prices:
            logger.info("")
            logger.info(f"Backfilling RS for {args.rs_weeks} weeks...")
            rs_results = backfill_rs(weeks=args.rs_weeks)
            
            logger.info("")
            logger.info("RS backfill complete:")
            logger.info(f"  Weeks processed: {rs_results['weeks_processed']}")
            logger.info(f"  Total RS records: {rs_results['total_records']}")
            
            if rs_results['errors']:
                logger.warning(f"  Errors: {len(rs_results['errors'])}")
        elif args.no_rs:
            logger.info("Skipping RS calculation (--no-rs)")
        
    except Exception as e:
        logger.exception(f"Bootstrap failed: {e}")
        sys.exit(1)
    finally:
        db.close()
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Bootstrap complete!")
    logger.info("")
    logger.info("To start the application:")
    logger.info("  uvicorn src.main:app --reload")
    logger.info("")
    logger.info("Dashboard will be available at: http://localhost:8000/dashboard/")
    logger.info("API docs at: http://localhost:8000/api/docs")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

