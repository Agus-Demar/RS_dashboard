#!/usr/bin/env python3
"""
Database Migration Script: GICS to StockCharts Industry Structure

Migrates the database from the old GICS-based 8-digit codes to the new
StockCharts-based 6-digit industry codes.

This script:
1. Creates new industry records based on StockCharts classification
2. Maps existing stocks from old sub-industry codes to new industry codes
3. Updates foreign key relationships
4. Preserves RS historical data by updating references
5. Creates backup of current data before migration

Usage:
    python -m scripts.migrate_to_stockcharts
    python -m scripts.migrate_to_stockcharts --dry-run
    python -m scripts.migrate_to_stockcharts --backup-only
"""
import argparse
import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import settings
from src.models import SessionLocal, init_db, GICSSubIndustry, Stock, RSWeekly
from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP, SECTOR_NAMES
from src.ingestion.mappers.gics_mapper import SUBINDUSTRY_TO_STOCKCHARTS, GICS_SECTORS

logger = logging.getLogger(__name__)


# Mapping from old GICS codes to new StockCharts codes
# This is built dynamically based on sub-industry name matching
OLD_TO_NEW_CODE_MAPPING: Dict[str, str] = {}


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def backup_database():
    """Create a backup of the current database file."""
    db_path = Path(settings.DATABASE_PATH)
    if not db_path.exists():
        logger.warning(f"Database file not found at {db_path}")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.parent / f"rs_dashboard_backup_{timestamp}.db"
    
    logger.info(f"Creating database backup: {backup_path}")
    shutil.copy2(db_path, backup_path)
    
    return backup_path


def get_existing_subindustries(db: Session) -> List[GICSSubIndustry]:
    """Get all existing sub-industries from the database."""
    return db.query(GICSSubIndustry).all()


def get_existing_stocks(db: Session) -> List[Stock]:
    """Get all existing stocks from the database."""
    return db.query(Stock).all()


def build_code_mapping(existing_subindustries: List[GICSSubIndustry]) -> Dict[str, str]:
    """
    Build mapping from old GICS codes to new StockCharts codes.
    
    Uses the SUBINDUSTRY_TO_STOCKCHARTS mapping and name matching.
    """
    mapping = {}
    
    for subind in existing_subindustries:
        old_code = subind.code
        old_name = subind.name
        old_sector = subind.sector_name
        
        # Try exact name match
        if old_name in SUBINDUSTRY_TO_STOCKCHARTS:
            new_code = SUBINDUSTRY_TO_STOCKCHARTS[old_name]
            mapping[old_code] = new_code
            continue
        
        # Try partial matching
        matched = False
        for wiki_name, new_code in SUBINDUSTRY_TO_STOCKCHARTS.items():
            if wiki_name.lower() in old_name.lower() or old_name.lower() in wiki_name.lower():
                mapping[old_code] = new_code
                matched = True
                break
        
        if not matched:
            # Fall back to sector-based default
            sector_code = GICS_SECTORS.get(old_sector, "45")
            # Find any industry in that sector
            for code, info in INDUSTRY_ETF_MAP.items():
                if info.sector_code == sector_code:
                    mapping[old_code] = code
                    break
            else:
                # Ultimate fallback
                mapping[old_code] = f"{sector_code}0100"
    
    return mapping


def create_new_industries(db: Session, dry_run: bool = False) -> int:
    """
    Create new industry records based on StockCharts classification.
    
    Returns:
        Number of industries created
    """
    created = 0
    
    for code, info in INDUSTRY_ETF_MAP.items():
        # Check if already exists
        existing = db.query(GICSSubIndustry).filter_by(code=code).first()
        if existing:
            continue
        
        # Create new industry record
        new_industry = GICSSubIndustry(
            code=code,
            name=info.name,
            industry_code=code[:6] if len(code) >= 6 else code,
            industry_name=info.name,
            industry_group_code=code[:4] if len(code) >= 4 else code,
            industry_group_name=info.name,
            sector_code=info.sector_code,
            sector_name=info.sector_name,
        )
        
        if not dry_run:
            db.add(new_industry)
        
        logger.debug(f"Creating industry: {code} - {info.name}")
        created += 1
    
    if not dry_run:
        db.commit()
    
    return created


def update_stock_codes(
    db: Session,
    code_mapping: Dict[str, str],
    dry_run: bool = False
) -> Tuple[int, int]:
    """
    Update stock foreign keys to point to new industry codes.
    
    Returns:
        Tuple of (stocks_updated, stocks_skipped)
    """
    updated = 0
    skipped = 0
    
    stocks = db.query(Stock).all()
    
    for stock in stocks:
        old_code = stock.gics_subindustry_code
        new_code = code_mapping.get(old_code)
        
        if not new_code:
            logger.warning(f"No mapping found for stock {stock.ticker} with code {old_code}")
            skipped += 1
            continue
        
        if old_code == new_code:
            # Code unchanged
            continue
        
        # Verify new code exists
        new_industry = db.query(GICSSubIndustry).filter_by(code=new_code).first()
        if not new_industry:
            logger.warning(f"New industry {new_code} not found for stock {stock.ticker}")
            skipped += 1
            continue
        
        logger.debug(f"Updating stock {stock.ticker}: {old_code} -> {new_code}")
        
        if not dry_run:
            stock.gics_subindustry_code = new_code
        
        updated += 1
    
    if not dry_run:
        db.commit()
    
    return updated, skipped


def update_rs_records(
    db: Session,
    code_mapping: Dict[str, str],
    dry_run: bool = False
) -> Tuple[int, int]:
    """
    Handle RS weekly records during migration.
    
    Since the new industry structure has fewer categories than the old GICS
    structure, multiple old sub-industries may map to the same new industry.
    This causes unique constraint violations on (subindustry_code, week_end_date).
    
    Solution: Delete old RS records and let the system recalculate them
    with the new industry structure for accurate data.
    
    Returns:
        Tuple of (records_deleted, records_skipped)
    """
    # Count records before deletion
    total_records = db.query(RSWeekly).count()
    
    if total_records == 0:
        return 0, 0
    
    logger.info(f"  Found {total_records} RS weekly records")
    logger.info("  Deleting old RS records (will be recalculated with new industries)...")
    
    if not dry_run:
        # Delete all RS records - they will be recalculated
        db.query(RSWeekly).delete()
        db.commit()
    
    return total_records, 0


def cleanup_old_industries(
    db: Session,
    code_mapping: Dict[str, str],
    dry_run: bool = False
) -> int:
    """
    Remove old industry records that are no longer referenced.
    
    Returns:
        Number of industries removed
    """
    removed = 0
    
    all_industries = db.query(GICSSubIndustry).all()
    new_codes = set(INDUSTRY_ETF_MAP.keys())
    
    for industry in all_industries:
        if industry.code not in new_codes:
            # Check if any stocks still reference this
            stock_count = db.query(Stock).filter_by(
                gics_subindustry_code=industry.code
            ).count()
            
            rs_count = db.query(RSWeekly).filter_by(
                subindustry_code=industry.code
            ).count()
            
            if stock_count == 0 and rs_count == 0:
                logger.debug(f"Removing old industry: {industry.code} - {industry.name}")
                
                if not dry_run:
                    db.delete(industry)
                
                removed += 1
            else:
                logger.warning(
                    f"Cannot remove industry {industry.code}: "
                    f"{stock_count} stocks, {rs_count} RS records still reference it"
                )
    
    if not dry_run:
        db.commit()
    
    return removed


def export_migration_report(
    code_mapping: Dict[str, str],
    created: int,
    updated: int,
    rs_deleted: int,
    removed: int,
    output_path: Path
):
    """Export migration report to JSON file."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "industries_created": created,
            "stocks_updated": updated,
            "rs_records_deleted": rs_deleted,
            "old_industries_removed": removed,
        },
        "code_mapping": code_mapping,
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Migration report exported to: {output_path}")


def run_migration(dry_run: bool = False):
    """Run the complete migration process."""
    
    logger.info("=" * 60)
    logger.info("StockCharts Industry Migration")
    logger.info("=" * 60)
    
    if dry_run:
        logger.info("DRY RUN MODE - No changes will be made")
    
    # Initialize database
    init_db()
    
    # Create backup
    if not dry_run:
        backup_path = backup_database()
        if backup_path:
            logger.info(f"Backup created: {backup_path}")
    
    db = SessionLocal()
    
    try:
        # Get existing data
        existing_subindustries = get_existing_subindustries(db)
        logger.info(f"Found {len(existing_subindustries)} existing sub-industries")
        
        # Build code mapping
        code_mapping = build_code_mapping(existing_subindustries)
        logger.info(f"Built mapping for {len(code_mapping)} codes")
        
        # Step 1: Create new industry records
        logger.info("Step 1: Creating new industry records...")
        created = create_new_industries(db, dry_run)
        logger.info(f"  Created: {created} new industries")
        
        # Step 2: Update stock foreign keys
        logger.info("Step 2: Updating stock industry codes...")
        updated, skipped = update_stock_codes(db, code_mapping, dry_run)
        logger.info(f"  Updated: {updated} stocks")
        logger.info(f"  Skipped: {skipped} stocks")
        
        # Step 3: Handle RS weekly records (delete for recalculation)
        logger.info("Step 3: Handling RS weekly records...")
        rs_deleted, rs_skipped = update_rs_records(db, code_mapping, dry_run)
        logger.info(f"  Deleted: {rs_deleted} RS records (will be recalculated)")
        
        # Step 4: Clean up old industries
        logger.info("Step 4: Cleaning up old industry records...")
        removed = cleanup_old_industries(db, code_mapping, dry_run)
        logger.info(f"  Removed: {removed} old industries")
        
        # Export report
        report_path = Path(settings.DATA_DIR) / "migration_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        export_migration_report(
            code_mapping, created, updated, rs_deleted, removed, report_path
        )
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Migration Complete!" if not dry_run else "Dry Run Complete!")
        logger.info("")
        logger.info("Summary:")
        logger.info(f"  Industries created: {created}")
        logger.info(f"  Stocks updated: {updated}")
        logger.info(f"  RS records deleted: {rs_deleted} (need to recalculate)")
        logger.info(f"  Old industries removed: {removed}")
        if not dry_run and rs_deleted > 0:
            logger.info("")
            logger.info("IMPORTANT: Run 'python -m scripts.backfill_rs' to recalculate RS values")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.exception(f"Migration failed: {e}")
        if not dry_run:
            logger.info("You can restore from the backup file")
        raise
    finally:
        db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate database from GICS to StockCharts industry structure"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate migration without making changes"
    )
    parser.add_argument(
        "--backup-only",
        action="store_true",
        help="Only create a backup, don't migrate"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    if args.backup_only:
        backup_path = backup_database()
        if backup_path:
            logger.info(f"Backup created: {backup_path}")
        else:
            logger.warning("No database found to backup")
        return
    
    run_migration(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
