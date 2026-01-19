"""
Script to check ETF coverage for SCTR calculations.

Checks which ETFs from the StockCharts industry mapping have price data in the database.
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.models import StockPrice
from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP, SECTOR_ETFS

def main():
    # Connect to database
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Get all unique ETFs from the mapping
        all_etfs = set()
        for code, mapping in INDUSTRY_ETF_MAP.items():
            all_etfs.add(mapping.primary_etf)
            if mapping.alt_etf:
                all_etfs.add(mapping.alt_etf)
        
        # Add sector ETFs
        for etf in SECTOR_ETFS.values():
            all_etfs.add(etf)
        
        print(f"\n{'='*60}")
        print(f"ETF Coverage Check for SCTR Calculations")
        print(f"{'='*60}")
        print(f"\nTotal unique ETFs in mapping: {len(all_etfs)}")
        
        # Check which ETFs have price data
        etfs_with_data = []
        etfs_without_data = []
        
        for etf in sorted(all_etfs):
            count = db.query(func.count(StockPrice.id)).filter(
                StockPrice.ticker == etf
            ).scalar()
            
            if count > 0:
                etfs_with_data.append((etf, count))
            else:
                etfs_without_data.append(etf)
        
        print(f"ETFs with price data: {len(etfs_with_data)}")
        print(f"ETFs missing price data: {len(etfs_without_data)}")
        
        if etfs_without_data:
            print(f"\n{'='*60}")
            print("MISSING ETFs (need to download price data):")
            print(f"{'='*60}")
            for etf in etfs_without_data:
                # Find which industries use this ETF
                users = []
                for code, mapping in INDUSTRY_ETF_MAP.items():
                    if mapping.primary_etf == etf:
                        users.append(mapping.name)
                print(f"  {etf}: used by {len(users)} industries")
                if len(users) <= 3:
                    for user in users:
                        print(f"      - {user}")
            
            print(f"\n{'='*60}")
            print("Python list of missing ETFs (for easy copy):")
            print(f"{'='*60}")
            print(f"MISSING_ETFS = {sorted(etfs_without_data)}")
        
        print(f"\n{'='*60}")
        print("ETFs with data (sample):")
        print(f"{'='*60}")
        for etf, count in sorted(etfs_with_data, key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {etf}: {count} price records")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
