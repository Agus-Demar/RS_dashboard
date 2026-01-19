"""
Script to remove Canadian and other foreign stocks from the database.

These are stocks that are dual-listed on US exchanges but are headquartered
in foreign countries (primarily Canada).
"""
import sys
sys.path.insert(0, '.')

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.models import Stock, StockPrice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Canadian stocks to remove (dual-listed on US exchanges)
CANADIAN_STOCKS = [
    # Energy
    "ENB",   # Enbridge Inc
    "CNQ",   # Canadian Natural Resources
    "SU",    # Suncor Energy Inc
    "CVE",   # Cenovus Energy Inc
    "TRP",   # TC Energy Corporation
    "IMO",   # Imperial Oil Limited
    
    # Banks
    "TD",    # Toronto-Dominion Bank
    "BMO",   # Bank of Montreal
    "BNS",   # Bank of Nova Scotia
    "RY",    # Royal Bank of Canada
    "CM",    # Canadian Imperial Bank of Commerce
    
    # Mining
    "WPM",   # Wheaton Precious Metals Corp
    "AEM",   # Agnico Eagle Mines Limited
    "TECK",  # Teck Resources Ltd
    "ABX",   # Barrick Gold (now traded as GOLD, but may have ABX entries)
    "FM",    # First Quantum Minerals
    
    # Insurance/Financial
    "SLF",   # Sun Life Financial Inc
    "MFC",   # Manulife Financial Corporation
    
    # Transportation
    "CP",    # Canadian Pacific Kansas City Limited
    "CNR",   # CNR (if exists - may be "Canadian National Railway" old ticker)
    
    # Other Canadian
    "NTR",   # Nutrien Ltd
    "GOOS",  # Canada Goose Holdings Inc
    "CSIQ",  # Canadian Solar Inc
    "SHOP",  # Shopify Inc (Canadian company)
    "LULU",  # Lululemon Athletica (Canadian origin)
    "BB",    # BlackBerry (Canadian company)
    "RCI",   # Rogers Communications (Canadian telecom)
    "BCE",   # BCE Inc (Canadian telecom)
    "TU",    # TELUS Corporation (Canadian telecom)
]


def main():
    """Remove foreign stocks from the database."""
    # Connect to database
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print(f"\n{'='*60}")
        print("Remove Foreign Stocks Script")
        print(f"{'='*60}")
        print(f"Stocks to check: {len(CANADIAN_STOCKS)}")
        
        removed_stocks = []
        not_found = []
        
        for ticker in CANADIAN_STOCKS:
            # Check if stock exists
            stock = db.query(Stock).filter(Stock.ticker == ticker).first()
            
            if stock:
                stock_name = stock.name
                
                # Count price records
                price_count = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker
                ).count()
                
                # Delete price records first (foreign key constraint)
                db.query(StockPrice).filter(StockPrice.ticker == ticker).delete()
                
                # Delete stock record
                db.delete(stock)
                
                db.commit()
                removed_stocks.append((ticker, stock_name, price_count))
                logger.info(f"Removed {ticker} ({stock_name}) - {price_count} price records deleted")
            else:
                not_found.append(ticker)
        
        print(f"\n{'='*60}")
        print("Results")
        print(f"{'='*60}")
        print(f"Stocks removed: {len(removed_stocks)}")
        print(f"Stocks not found: {len(not_found)}")
        
        if removed_stocks:
            print(f"\nRemoved stocks:")
            for ticker, name, count in removed_stocks:
                print(f"  {ticker}: {name} ({count} prices)")
        
        if not_found:
            print(f"\nNot found in database:")
            for ticker in not_found:
                print(f"  {ticker}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
