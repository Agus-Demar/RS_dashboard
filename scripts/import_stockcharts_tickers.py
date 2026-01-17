#!/usr/bin/env python3
"""
Import StockCharts Tickers into Database

Reads the scraped StockCharts data and imports new tickers into the database.
Skips tickers that already exist. Uses yfinance to fetch basic stock info.

Usage:
    python -m scripts.import_stockcharts_tickers
    python -m scripts.import_stockcharts_tickers --dry-run
    python -m scripts.import_stockcharts_tickers --input data/stockcharts_tickers.json
"""
import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from src.models.base import SessionLocal
from src.models import Stock, GICSSubIndustry
from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP

logger = logging.getLogger(__name__)

# Industry name to code mapping (for matching scraped names to our codes)
INDUSTRY_NAME_TO_CODE: Dict[str, str] = {
    # Energy (10)
    "coal": "100100",
    "oil equipment & services": "100400",
    "oil & gas equipment & services": "100400",
    "integrated oil & gas": "100500",
    "pipelines": "100600",
    "oil & gas pipelines": "100600",
    "exploration & production": "100300",
    "oil & gas drilling": "100200",
    "oil & gas refining": "100700",
    
    # Materials (15)
    "aluminum": "150100",
    "nonferrous metals": "150800",
    "metals & mining": "150800",
    "mining": "150800",
    "gold mining": "150700",
    "gold": "150700",
    "specialty chemicals": "151100",
    "commodity chemicals": "150300",
    "chemicals": "150300",
    "steel": "151200",
    "containers & packaging": "150400",
    "paper": "150900",
    "paper & forest products": "150900",
    "copper": "150500",
    "silver": "151000",
    "fertilizers": "150600",
    "building materials": "150200",
    
    # Industrials (20)
    "defense": "201000",
    "aerospace & defense": "200100",
    "aerospace": "200100",
    "marine transportation": "201700",
    "marine shipping": "201700",
    "industrial suppliers": "201600",
    "industrial distribution": "201600",
    "commercial vehicles & trucks": "200700",
    "heavy construction": "201200",
    "engineering & construction": "201200",
    "construction materials": "200900",
    "delivery services": "200200",
    "air freight": "200200",
    "diversified industrials": "200800",
    "conglomerates": "200800",
    "industrial machinery": "201500",
    "heavy machinery": "201500",
    "machinery": "201500",
    "trucking": "202200",
    "business support services": "200500",
    "business services": "200500",
    "building materials & fixtures": "200400",
    "building products": "200400",
    "waste & disposal services": "202300",
    "waste management": "202300",
    "environmental services": "201300",
    "airlines": "200300",
    "railroad": "201900",
    "railroads": "201900",
    "staffing": "202100",
    "security services": "202000",
    "capital goods": "200600",
    "electrical equipment": "201100",
    "farm machinery": "201400",
    "packaging": "201800",
    
    # Real Estate (60)
    "real estate holding & development": "601000",
    "real estate development": "601000",
    "mortgage reits": "600500",
    "reits - mortgage": "600500",
    "diversified reits": "600100",
    "reits - diversified": "600100",
    "specialty reits": "600900",
    "reits - specialty": "600900",
    "real estate services": "601100",
    "retail reits": "600800",
    "reits - retail": "600800",
    "industrial & office reits": "600400",
    "reits - industrial": "600400",
    "reits - office": "600600",
    "residential reits": "600700",
    "reits - residential": "600700",
    "hotel & resort reits": "600300",
    "reits - hotel & motel": "600300",
    "health care reits": "600200",
    "reits - healthcare": "600200",
    
    # Consumer Staples (30)
    "beverages": "300200",
    "beverages: non-alcoholic": "300200",
    "beverages: alcoholic": "300100",
    "food producers": "300400",
    "food products": "300400",
    "food retailers & wholesalers": "300500",
    "food retailers": "300500",
    "personal care, drug & grocery stores": "300300",
    "drug retailers": "300300",
    "household goods & home construction": "300600",
    "household products": "300600",
    "personal goods": "300700",
    "personal products": "300700",
    "tobacco": "300800",
    "leisure goods": "251300",
    
    # Technology (45)
    "software": "450100",
    "application software": "450100",
    "semiconductors": "451200",
    "technology hardware & equipment": "450400",
    "computer hardware": "450400",
    "electronic & electrical equipment": "450800",
    "electronic components": "450800",
    "computer services": "450500",
    "it consulting": "450900",
    "software infrastructure": "451300",
    "cloud computing": "450200",
    "cybersecurity": "450600",
    "data processing": "450700",
    "communication equipment": "450300",
    "semiconductor equipment": "451100",
    "scientific instruments": "451000",
    
    # Utilities (55)
    "electricity": "550100",
    "electric utilities": "550100",
    "gas, water & multi-utilities": "550400",
    "multi-utilities": "550400",
    "gas utilities": "550200",
    "water utilities": "550600",
    "renewable energy equipment": "550500",
    "renewable energy": "550500",
    "independent power": "550300",
    
    # Health Care (35)
    "biotechnology": "350100",
    "pharmaceuticals & biotechnology": "350900",
    "pharmaceuticals": "350900",
    "health care equipment & services": "350700",
    "medical devices": "350700",
    "medical equipment": "350700",
    "medical instruments": "350800",
    "health care providers": "350400",
    "healthcare facilities": "350400",
    "healthcare services": "350600",
    "healthcare plans": "350500",
    "healthcare distributors": "350300",
    "diagnostics & research": "350200",
    
    # Consumer Discretionary (25)
    "automobiles & parts": "250100",
    "auto parts": "250100",
    "automobiles": "250200",
    "household goods & home construction": "250700",
    "furnishings": "250700",
    "leisure goods": "251300",
    "leisure products": "251300",
    "personal goods": "251900",
    "textiles & apparel": "251900",
    "apparel": "251700",
    "retail apparel": "251700",
    "retailers": "251800",
    "specialty retail": "251800",
    "general merchandise": "250800",
    "department stores": "250500",
    "home improvement": "250900",
    "homebuilding & construction": "251000",
    "homebuilders": "251000",
    "travel & leisure": "251400",
    "recreational services": "251400",
    "hotels & entertainment services": "251100",
    "hotels & motels": "251100",
    "media": "500400",
    "media agencies": "500100",
    "gambling": "250300",
    "casinos & gaming": "250300",
    "restaurants & bars": "251600",
    "restaurants": "251600",
    "consumer electronics": "250400",
    "toys": "252100",
    "footwear": "250600",
    "housewares": "251200",
    "recreational vehicles": "251500",
    "tires": "252000",
    
    # Financials (40)
    "banks": "400300",
    "banks: regional": "400300",
    "banks: diversified": "400200",
    "nonlife insurance": "400900",
    "insurance: p&c": "400900",
    "life insurance": "400800",
    "insurance: life": "400800",
    "insurance: brokers": "400700",
    "insurance: specialty": "401000",
    "financial services": "400600",
    "investment banking & brokerage services": "400400",
    "brokers & exchanges": "400400",
    "mortgage finance": "401100",
    "closed end investments": "400100",
    "asset management": "400100",
    "equity investment instruments": "400100",
    "nonequity investment instruments": "400100",
    "consumer finance": "400500",
    "savings & loans": "401200",
    
    # Communication Services (50)
    "media": "500400",
    "entertainment": "500400",
    "publishing": "500600",
    "telecommunications service providers": "500800",
    "telecom services": "500800",
    "telecommunications equipment": "500700",
    "telecom equipment": "500700",
    "internet": "500500",
    "advertising": "500100",
    "broadcasting": "500200",
    "cable & satellite": "500300",
    "fixed line telecommunications": "500800",
    "mobile telecommunications": "500800",
    
    # Additional mappings for missing industries
    "hotel & lodging reits": "600300",
    "distillers & vintners": "300100",
    "brewers": "300100",
    "soft drinks": "300200",
    "electronic equipment": "450800",
    "electrical components & equipment": "450800",
    "multiutilities": "550400",
    "gas distribution": "550200",
    "medical supplies": "350800",
    "recreational products": "251300",
    "specialized consumer services": "251400",
    "clothing & accessories": "251900",
    "travel & tourism": "251400",
    "business training & employment agencies": "202100",
    "full line insurance": "400900",
    "investment services": "400400",
    "asset managers": "400100",
    "insurance brokers": "400700",
    "specialty finance": "400600",
    "financial administration": "400600",
    "reinsurance": "401000",
    "property & casualty insurance": "400900",
}


def get_industry_code(industry_name: str, sector_code: str) -> Optional[str]:
    """Get industry code from name."""
    name_lower = industry_name.lower().strip()
    
    # Try direct match
    if name_lower in INDUSTRY_NAME_TO_CODE:
        return INDUSTRY_NAME_TO_CODE[name_lower]
    
    # Try partial match
    for key, code in INDUSTRY_NAME_TO_CODE.items():
        if key in name_lower or name_lower in key:
            return code
    
    # Return None if no match found
    return None


def get_existing_tickers(db: Session) -> Set[str]:
    """Get set of all existing tickers in database."""
    tickers = db.query(Stock.ticker).all()
    return {t[0].upper() for t in tickers}


def get_existing_industries(db: Session) -> Set[str]:
    """Get set of all existing industry codes in database."""
    codes = db.query(GICSSubIndustry.code).all()
    return {c[0] for c in codes}


def fetch_stock_info(ticker: str) -> Optional[Dict[str, Any]]:
    """Fetch stock info from yfinance."""
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or 'symbol' not in info:
            return None
        
        return {
            'name': info.get('shortName') or info.get('longName') or ticker,
            'market_cap': info.get('marketCap'),
        }
    except Exception as e:
        logger.debug(f"Could not fetch info for {ticker}: {e}")
        return None


def import_tickers(
    input_path: Path,
    dry_run: bool = False,
    batch_size: int = 50,
    skip_yfinance: bool = False
) -> Dict[str, int]:
    """
    Import tickers from scraped data file.
    
    Args:
        input_path: Path to stockcharts_tickers.json
        dry_run: If True, don't actually add to database
        batch_size: Number of stocks to commit at once
        skip_yfinance: Skip yfinance lookups (faster but less data)
        
    Returns:
        Dictionary with import statistics
    """
    # Load scraped data
    with open(input_path) as f:
        data = json.load(f)
    
    db = SessionLocal()
    
    try:
        # Get existing tickers
        existing_tickers = get_existing_tickers(db)
        existing_industries = get_existing_industries(db)
        
        logger.info(f"Existing stocks in database: {len(existing_tickers)}")
        logger.info(f"Existing industries in database: {len(existing_industries)}")
        
        stats = {
            'total_scraped': 0,
            'already_exists': 0,
            'added': 0,
            'skipped_no_industry': 0,
            'skipped_invalid': 0,
            'failed': 0,
        }
        
        stocks_to_add = []
        
        for sector in data.get('sectors', []):
            sector_code = sector.get('code', '')
            sector_name = sector.get('name', '')
            
            for industry in sector.get('industries', []):
                industry_name = industry.get('name', '')
                industry_code = get_industry_code(industry_name, sector_code)
                
                if not industry_code:
                    # Try to find in our mapping
                    for code, info in INDUSTRY_ETF_MAP.items():
                        if info.name.lower() == industry_name.lower():
                            industry_code = code
                            break
                
                if not industry_code:
                    logger.warning(f"No industry code found for: {industry_name}")
                    industry_code = f"{sector_code}9900"  # Fallback
                
                # Check if industry exists
                if industry_code not in existing_industries:
                    logger.debug(f"Industry {industry_code} not in database")
                
                for ticker in industry.get('tickers', []):
                    stats['total_scraped'] += 1
                    ticker_upper = ticker.upper().strip()
                    
                    # Skip invalid tickers
                    if not ticker_upper or len(ticker_upper) > 10:
                        stats['skipped_invalid'] += 1
                        continue
                    
                    # Skip if already exists
                    if ticker_upper in existing_tickers:
                        stats['already_exists'] += 1
                        continue
                    
                    # Prepare stock data
                    stock_data = {
                        'ticker': ticker_upper,
                        'name': ticker_upper,  # Default name
                        'gics_subindustry_code': industry_code,
                        'market_cap': None,
                        'is_active': True,
                    }
                    
                    stocks_to_add.append(stock_data)
                    existing_tickers.add(ticker_upper)  # Prevent duplicates within batch
        
        logger.info(f"Found {len(stocks_to_add)} new stocks to add")
        
        # Fetch yfinance info in batches
        if not skip_yfinance and stocks_to_add:
            logger.info("Fetching stock info from yfinance...")
            for i, stock_data in enumerate(stocks_to_add):
                if i % 10 == 0:
                    logger.info(f"  Progress: {i}/{len(stocks_to_add)}")
                
                info = fetch_stock_info(stock_data['ticker'])
                if info:
                    stock_data['name'] = info.get('name', stock_data['ticker'])
                    stock_data['market_cap'] = info.get('market_cap')
                
                # Rate limit
                time.sleep(0.1)
        
        # Add stocks to database
        if not dry_run:
            logger.info("Adding stocks to database...")
            for i, stock_data in enumerate(stocks_to_add):
                try:
                    # Check if industry exists, create if not
                    if stock_data['gics_subindustry_code'] not in existing_industries:
                        # Check if we have this industry in our mapping
                        if stock_data['gics_subindustry_code'] in INDUSTRY_ETF_MAP:
                            info = INDUSTRY_ETF_MAP[stock_data['gics_subindustry_code']]
                            new_industry = GICSSubIndustry(
                                code=info.code,
                                name=info.name,
                                industry_code=info.code[:4],
                                industry_name=info.name,
                                industry_group_code=info.code[:4],
                                industry_group_name=info.name,
                                sector_code=info.sector_code,
                                sector_name=info.sector_name,
                            )
                            db.add(new_industry)
                            existing_industries.add(info.code)
                            logger.info(f"Created industry: {info.code} - {info.name}")
                    
                    stock = Stock(
                        ticker=stock_data['ticker'],
                        name=stock_data['name'],
                        gics_subindustry_code=stock_data['gics_subindustry_code'],
                        market_cap=stock_data['market_cap'],
                        is_active=True,
                    )
                    db.add(stock)
                    stats['added'] += 1
                    
                    # Commit in batches
                    if (i + 1) % batch_size == 0:
                        db.commit()
                        logger.info(f"  Committed batch {(i + 1) // batch_size}")
                        
                except Exception as e:
                    logger.error(f"Failed to add {stock_data['ticker']}: {e}")
                    stats['failed'] += 1
                    db.rollback()
            
            # Final commit
            db.commit()
            logger.info(f"Added {stats['added']} new stocks to database")
        else:
            stats['added'] = len(stocks_to_add)
            logger.info(f"[DRY RUN] Would add {len(stocks_to_add)} new stocks")
        
        return stats
        
    finally:
        db.close()


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Reduce yfinance noise
    logging.getLogger('yfinance').setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser(description="Import StockCharts tickers into database")
    parser.add_argument(
        "--input", "-i",
        default="data/stockcharts_tickers.json",
        help="Input JSON file from scraper"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually add to database, just report what would be added"
    )
    parser.add_argument(
        "--skip-yfinance",
        action="store_true",
        help="Skip yfinance lookups (faster but less data)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for database commits"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    logger.info(f"Importing tickers from {input_path}")
    
    stats = import_tickers(
        input_path,
        dry_run=args.dry_run,
        batch_size=args.batch_size,
        skip_yfinance=args.skip_yfinance,
    )
    
    logger.info("")
    logger.info("=" * 50)
    logger.info("Import Summary:")
    logger.info(f"  Total scraped tickers: {stats['total_scraped']}")
    logger.info(f"  Already in database:   {stats['already_exists']}")
    logger.info(f"  Added to database:     {stats['added']}")
    logger.info(f"  Skipped (no industry): {stats['skipped_no_industry']}")
    logger.info(f"  Skipped (invalid):     {stats['skipped_invalid']}")
    logger.info(f"  Failed:                {stats['failed']}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
