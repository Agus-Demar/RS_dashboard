#!/usr/bin/env python3
"""
Manual Job Runner Script

Run scheduled jobs manually for testing or catch-up.

Usage:
    python -m scripts.run_job weekly    # Run weekly RS calculation
    python -m scripts.run_job daily     # Run daily price refresh
"""
import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models import init_db


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run scheduled jobs manually"
    )
    parser.add_argument(
        "job",
        choices=["weekly", "daily", "both"],
        help="Job to run: weekly (RS calculation), daily (price refresh), or both"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize database
    init_db()
    
    if args.job in ["daily", "both"]:
        logger.info("Running daily price refresh job...")
        from src.jobs.daily_prices_job import run_daily_prices_job
        result = run_daily_prices_job()
        logger.info(f"Daily job result: {result}")
    
    if args.job in ["weekly", "both"]:
        logger.info("Running weekly RS calculation job...")
        from src.jobs.weekly_rs_job import run_weekly_rs_job
        result = run_weekly_rs_job()
        logger.info(f"Weekly job result: {result}")
    
    logger.info("Done!")


if __name__ == "__main__":
    main()

