#!/usr/bin/env python3
"""
Cleanup Industries Script

Removes industries from the database that are not present in the 
StockCharts scraped data. This ensures the database only contains
industries that have actual ticker data available.

Usage:
    python -m scripts.cleanup_industries --dry-run
    python -m scripts.cleanup_industries
"""
import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from src.models import SessionLocal, init_db, GICSSubIndustry, Stock, RSWeekly
from scripts.import_stockcharts_tickers import INDUSTRY_NAME_TO_CODE

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_scraped_industry_codes() -> set:
    """Get industry codes from the scraped StockCharts data."""
    data_file = project_root / "data" / "stockcharts_tickers.json"
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    scraped_codes = set()
    for sector in data['sectors']:
        for ind in sector['industries']:
            name_lower = ind['name'].lower()
            code = INDUSTRY_NAME_TO_CODE.get(name_lower)
            if code:
                scraped_codes.add(code)
    
    return scraped_codes


def run_cleanup(dry_run: bool = False):
    """Run the industry cleanup."""
    logger.info("=" * 60)
    logger.info("Industry Cleanup Script")
    logger.info("=" * 60)
    
    if dry_run:
        logger.info("DRY RUN MODE - No changes will be made")
    
    # Get valid industry codes from scraped data
    valid_codes = get_scraped_industry_codes()
    logger.info(f"Valid industry codes from scraped data: {len(valid_codes)}")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Get current industries in database
        current_industries = db.query(GICSSubIndustry).all()
        current_codes = {ind.code for ind in current_industries}
        logger.info(f"Current industries in database: {len(current_codes)}")
        
        # Find industries to remove
        codes_to_remove = current_codes - valid_codes
        logger.info(f"Industries to remove: {len(codes_to_remove)}")
        
        if not codes_to_remove:
            logger.info("No industries need to be removed.")
            return
        
        # Show industries to remove
        logger.info("")
        logger.info("Industries to be removed:")
        for code in sorted(codes_to_remove):
            ind = db.query(GICSSubIndustry).filter_by(code=code).first()
            if ind:
                logger.info(f"  {code}: {ind.name} [{ind.sector_name}]")
        
        # Count affected records
        stocks_to_update = db.query(Stock).filter(
            Stock.gics_subindustry_code.in_(codes_to_remove)
        ).count()
        
        rs_to_delete = db.query(RSWeekly).filter(
            RSWeekly.subindustry_code.in_(codes_to_remove)
        ).count()
        
        logger.info("")
        logger.info(f"Stocks to be orphaned: {stocks_to_update}")
        logger.info(f"RS records to be deleted: {rs_to_delete}")
        
        if dry_run:
            logger.info("")
            logger.info("[DRY RUN] No changes made.")
            return
        
        # Delete RS records for removed industries
        logger.info("")
        logger.info("Step 1: Deleting RS records...")
        deleted_rs = db.query(RSWeekly).filter(
            RSWeekly.subindustry_code.in_(codes_to_remove)
        ).delete(synchronize_session='fetch')
        logger.info(f"  Deleted {deleted_rs} RS records")
        
        # Delete stocks in removed industries (they can't be used)
        logger.info("Step 2: Deleting stocks in removed industries...")
        deleted_stocks = db.query(Stock).filter(
            Stock.gics_subindustry_code.in_(codes_to_remove)
        ).delete(synchronize_session='fetch')
        logger.info(f"  Deleted {deleted_stocks} stocks")
        
        # Delete the industries
        logger.info("Step 3: Deleting industries...")
        for code in codes_to_remove:
            ind = db.query(GICSSubIndustry).filter_by(code=code).first()
            if ind:
                db.delete(ind)
        logger.info(f"  Deleted {len(codes_to_remove)} industries")
        
        db.commit()
        
        # Verify final state
        final_industries = db.query(GICSSubIndustry).count()
        final_stocks = db.query(Stock).count()
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Cleanup Complete!")
        logger.info(f"  Industries remaining: {final_industries}")
        logger.info(f"  Stocks remaining: {final_stocks}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.exception(f"Cleanup failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Remove industries not in StockCharts scraped data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without making changes"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    run_cleanup(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
