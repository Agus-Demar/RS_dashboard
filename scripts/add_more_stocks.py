#!/usr/bin/env python3
"""
Script to add 1500+ additional stocks to the database.

This script:
1. Analyzes current stock distribution per sub-industry
2. Fetches additional US stocks from multiple sources (Russell indexes, major ETFs, Nasdaq/NYSE listings)
3. Maps yfinance industry data to GICS sub-industries
4. Prioritizes adding stocks to underrepresented industries
5. Adds stocks and fetches price data

Usage:
    python scripts/add_more_stocks.py [--target N] [--with-prices] [--dry-run]

Options:
    --target N      Target number of new stocks to add (default: 1500)
    --with-prices   Also fetch price history for new stocks
    --dry-run       Show what would be added without making changes
"""
import argparse
import logging
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import yfinance as yf

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.config import settings
from src.models import GICSSubIndustry, Stock, StockPrice, SessionLocal, init_db
from src.ingestion.sources.yfinance_source import yfinance_source
from src.ingestion.mappers.gics_mapper import GICS_SECTORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Reduce noise from other loggers
logging.getLogger('yfinance').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


# =============================================================================
# YFINANCE INDUSTRY TO GICS MAPPING
# Maps yfinance industry names to GICS sub-industry names
# =============================================================================
YFINANCE_TO_GICS_INDUSTRY = {
    # Energy
    "Oil & Gas Drilling": "Oil & Gas Drilling",
    "Oil & Gas Equipment & Services": "Oil & Gas Equipment & Services",
    "Oil & Gas Integrated": "Integrated Oil & Gas",
    "Oil & Gas E&P": "Oil & Gas Exploration & Production",
    "Oil & Gas Exploration & Production": "Oil & Gas Exploration & Production",
    "Oil & Gas Refining & Marketing": "Oil & Gas Refining & Marketing",
    "Oil & Gas Midstream": "Oil & Gas Storage & Transportation",
    "Thermal Coal": "Coal & Consumable Fuels",
    
    # Materials
    "Agricultural Inputs": "Fertilizers & Agricultural Chemicals",
    "Chemicals": "Diversified Chemicals",
    "Specialty Chemicals": "Specialty Chemicals",
    "Building Materials": "Construction Materials",
    "Paper & Paper Products": "Paper Products",
    "Lumber & Wood Production": "Forest Products",
    "Aluminum": "Aluminum",
    "Copper": "Copper",
    "Gold": "Gold",
    "Silver": "Silver",
    "Steel": "Steel",
    "Other Industrial Metals & Mining": "Diversified Metals & Mining",
    "Other Precious Metals & Mining": "Precious Metals & Minerals",
    "Coking Coal": "Coal & Consumable Fuels",
    
    # Industrials
    "Aerospace & Defense": "Aerospace & Defense",
    "Airlines": "Passenger Airlines",
    "Building Products & Equipment": "Building Products",
    "Conglomerates": "Industrial Conglomerates",
    "Construction": "Construction & Engineering",
    "Engineering & Construction": "Construction & Engineering",
    "Electrical Equipment & Parts": "Electrical Components & Equipment",
    "Farm & Heavy Construction Machinery": "Construction Machinery & Heavy Transportation Equipment",
    "Farm & Construction Machinery": "Construction Machinery & Heavy Transportation Equipment",
    "Industrial Distribution": "Trading Companies & Distributors",
    "Business Equipment & Supplies": "Office Services & Supplies",
    "Specialty Business Services": "Diversified Support Services",
    "Staffing & Employment Services": "Human Resource & Employment Services",
    "Consulting Services": "Research & Consulting Services",
    "Integrated Freight & Logistics": "Air Freight & Logistics",
    "Freight & Logistics Services": "Air Freight & Logistics",
    "Trucking": "Cargo Ground Transportation",
    "Railroads": "Rail Transportation",
    "Marine Shipping": "Marine Transportation",
    "Rental & Leasing Services": "Trading Companies & Distributors",
    "Security & Protection Services": "Security & Alarm Services",
    "Waste Management": "Environmental & Facilities Services",
    "Industrial Machinery": "Industrial Machinery & Supplies & Components",
    "Specialty Industrial Machinery": "Industrial Machinery & Supplies & Components",
    "Tools & Accessories": "Industrial Machinery & Supplies & Components",
    "Metal Fabrication": "Industrial Machinery & Supplies & Components",
    "Pollution & Treatment Controls": "Environmental & Facilities Services",
    "Airports & Air Services": "Airport Services",
    
    # Consumer Discretionary
    "Auto Manufacturers": "Automobile Manufacturers",
    "Auto & Truck Dealerships": "Automotive Retail",
    "Auto Parts": "Automotive Parts & Equipment",
    "Recreational Vehicles": "Automobile Manufacturers",
    "Furnishings, Fixtures & Appliances": "Home Furnishings",
    "Home Improvement Retail": "Home Improvement Retail",
    "Residential Construction": "Homebuilding",
    "Textile Manufacturing": "Textiles",
    "Apparel Manufacturing": "Apparel, Accessories & Luxury Goods",
    "Apparel Retail": "Apparel Retail",
    "Footwear & Accessories": "Footwear",
    "Luxury Goods": "Apparel, Accessories & Luxury Goods",
    "Department Stores": "Broadline Retail",
    "Discount Stores": "Broadline Retail",
    "Internet Retail": "Broadline Retail",
    "Specialty Retail": "Other Specialty Retail",
    "Gambling": "Casinos & Gaming",
    "Resorts & Casinos": "Casinos & Gaming",
    "Leisure": "Leisure Products",
    "Lodging": "Hotels, Resorts & Cruise Lines",
    "Restaurants": "Restaurants",
    "Travel Services": "Hotels, Resorts & Cruise Lines",
    "Personal Services": "Specialized Consumer Services",
    "Education & Training Services": "Education Services",
    
    # Consumer Staples
    "Beverages - Brewers": "Brewers",
    "Beverages - Wineries & Distilleries": "Distillers & Vintners",
    "Beverages - Non-Alcoholic": "Soft Drinks & Non-alcoholic Beverages",
    "Confectioners": "Packaged Foods & Meats",
    "Farm Products": "Agricultural Products & Services",
    "Food Distribution": "Food Distributors",
    "Grocery Stores": "Food Retail",
    "Household & Personal Products": "Household Products",
    "Packaged Foods": "Packaged Foods & Meats",
    "Tobacco": "Tobacco",
    "Consumer Defensive": "Packaged Foods & Meats",
    
    # Health Care
    "Biotechnology": "Biotechnology",
    "Drug Manufacturers - General": "Pharmaceuticals",
    "Drug Manufacturers - Specialty & Generic": "Pharmaceuticals",
    "Diagnostics & Research": "Life Sciences Tools & Services",
    "Health Information Services": "Health Care Technology",
    "Healthcare Plans": "Managed Health Care",
    "Medical Care Facilities": "Health Care Facilities",
    "Medical Devices": "Health Care Equipment",
    "Medical Distribution": "Health Care Distributors",
    "Medical Instruments & Supplies": "Health Care Supplies",
    "Pharmaceutical Retailers": "Drug Retail",
    
    # Financials
    "Banks - Diversified": "Diversified Banks",
    "Banks - Regional": "Regional Banks",
    "Asset Management": "Asset Management & Custody Banks",
    "Capital Markets": "Investment Banking & Brokerage",
    "Credit Services": "Consumer Finance",
    "Financial Data & Stock Exchanges": "Financial Exchanges & Data",
    "Financial Conglomerates": "Diversified Financial Services",
    "Insurance - Diversified": "Multi-line Insurance",
    "Insurance - Life": "Life & Health Insurance",
    "Insurance - Property & Casualty": "Property & Casualty Insurance",
    "Insurance - Reinsurance": "Reinsurance",
    "Insurance - Specialty": "Insurance Brokers",
    "Insurance Brokers": "Insurance Brokers",
    "Mortgage Finance": "Commercial & Residential Mortgage Finance",
    "Shell Companies": "Diversified Financial Services",
    
    # Information Technology
    "Communication Equipment": "Communications Equipment",
    "Computer Hardware": "Technology Hardware, Storage & Peripherals",
    "Consumer Electronics": "Consumer Electronics",
    "Electronic Components": "Electronic Components",
    "Electronic Gaming & Multimedia": "Consumer Electronics",
    "Electronics & Computer Distribution": "Technology Distributors",
    "Information Technology Services": "IT Consulting & Other Services",
    "Semiconductor Equipment & Materials": "Semiconductor Materials & Equipment",
    "Semiconductors": "Semiconductors",
    "Scientific & Technical Instruments": "Electronic Equipment & Instruments",
    "Software - Application": "Application Software",
    "Software - Infrastructure": "Systems Software",
    "Solar": "Semiconductors",  # Many solar are semiconductor-based
    
    # Communication Services
    "Advertising Agencies": "Advertising",
    "Broadcasting": "Broadcasting",
    "Electronic Gaming & Multimedia": "Interactive Home Entertainment",
    "Entertainment": "Movies & Entertainment",
    "Internet Content & Information": "Interactive Media & Services",
    "Publishing": "Publishing",
    "Telecom Services": "Integrated Telecommunication Services",
    
    # Utilities
    "Utilities - Diversified": "Multi-Utilities",
    "Utilities - Independent Power Producers": "Independent Power Producers & Energy Traders",
    "Utilities - Regulated Electric": "Electric Utilities",
    "Utilities - Regulated Gas": "Gas Utilities",
    "Utilities - Regulated Water": "Water Utilities",
    "Utilities - Renewable": "Renewable Electricity",
    
    # Real Estate
    "Real Estate - Development": "Real Estate Development",
    "Real Estate - Diversified": "Diversified Real Estate Activities",
    "Real Estate Services": "Real Estate Services",
    "REIT - Diversified": "Diversified REITs",
    "REIT - Healthcare Facilities": "Health Care REITs",
    "REIT - Hotel & Motel": "Hotel & Resort REITs",
    "REIT - Industrial": "Industrial REITs",
    "REIT - Mortgage": "Mortgage REITs",
    "REIT - Office": "Office REITs",
    "REIT - Residential": "Multi-Family Residential REITs",
    "REIT - Retail": "Retail REITs",
    "REIT - Specialty": "Other Specialized REITs",
}

# Sector mapping from yfinance sector to GICS sector code
YFINANCE_SECTOR_TO_GICS = {
    "Energy": "10",
    "Basic Materials": "15",
    "Industrials": "20",
    "Consumer Cyclical": "25",
    "Consumer Defensive": "30",
    "Healthcare": "35",
    "Financial Services": "40",
    "Technology": "45",
    "Communication Services": "50",
    "Utilities": "55",
    "Real Estate": "60",
}


# =============================================================================
# ADDITIONAL STOCK SOURCES
# Comprehensive list of US stock tickers from various ETFs and indexes
# =============================================================================

# Russell 2000 is tracked by IWM - we'll get holdings from multiple ETFs
STOCK_SOURCE_ETFS = [
    # Broad market ETFs
    "VTI",   # Vanguard Total Stock Market - 3,500+ stocks
    "ITOT", # iShares Core S&P Total US Stock Market
    "SPTM", # SPDR Portfolio S&P 1500 Composite Stock Market
    # Russell 2000 (small caps)
    "IWM",   # iShares Russell 2000
    "VTWO",  # Vanguard Russell 2000
    # Mid caps
    "IJH",   # iShares Core S&P MidCap
    "VO",    # Vanguard Mid-Cap ETF
    # Small caps
    "IJR",   # iShares Core S&P SmallCap
    "VB",    # Vanguard Small-Cap
    # Extended market (non-S&P 500)
    "VXF",   # Vanguard Extended Market
    "SCHA",  # Schwab U.S. Small-Cap
]

# Additional source: NASDAQ 100 and industry-specific ETFs for better sector coverage
SECTOR_ETFS_FOR_SCREENING = {
    "10": ["XLE", "VDE", "XOP", "OIH"],  # Energy
    "15": ["XLB", "VAW", "GDX", "XME"],  # Materials
    "20": ["XLI", "VIS", "JETS", "XTN"],  # Industrials
    "25": ["XLY", "VCR", "XHB", "XRT"],  # Consumer Discretionary
    "30": ["XLP", "VDC", "PBJ"],         # Consumer Staples
    "35": ["XLV", "VHT", "XBI", "IBB"],  # Health Care
    "40": ["XLF", "VFH", "KRE", "KBE"],  # Financials
    "45": ["XLK", "VGT", "SMH", "IGV"],  # Information Technology
    "50": ["XLC", "VOX", "SOCL"],        # Communication Services
    "55": ["XLU", "VPU", "IDU"],         # Utilities
    "60": ["XLRE", "VNQ", "IYR"],        # Real Estate
}


def get_current_stock_distribution(db: Session) -> Dict[str, int]:
    """Get current stock count per sub-industry from database."""
    results = db.query(
        GICSSubIndustry.code,
        GICSSubIndustry.name,
        func.count(Stock.ticker).label('stock_count')
    ).outerjoin(
        Stock, Stock.gics_subindustry_code == GICSSubIndustry.code
    ).filter(
        Stock.is_active == True
    ).group_by(
        GICSSubIndustry.code, GICSSubIndustry.name
    ).all()
    
    distribution = {}
    for code, name, count in results:
        distribution[code] = {
            'name': name,
            'count': count
        }
    
    return distribution


def get_subindustry_priority_scores(db: Session) -> Dict[str, float]:
    """
    Calculate priority scores for each sub-industry.
    Higher score = fewer stocks = higher priority for adding.
    """
    distribution = get_current_stock_distribution(db)
    
    if not distribution:
        # Get all sub-industries
        subindustries = db.query(GICSSubIndustry).all()
        for si in subindustries:
            distribution[si.code] = {'name': si.name, 'count': 0}
    
    # Calculate max count for normalization
    max_count = max((d['count'] for d in distribution.values()), default=1)
    if max_count == 0:
        max_count = 1
    
    # Score = 1 - (count / max_count), so fewer stocks = higher score
    scores = {}
    for code, data in distribution.items():
        scores[code] = 1.0 - (data['count'] / max_count)
    
    return scores


def get_existing_tickers(db: Session) -> set:
    """Get all existing tickers in the database."""
    stocks = db.query(Stock.ticker).all()
    return {s.ticker for s in stocks}


def get_subindustry_lookup(db: Session) -> Dict[str, str]:
    """Create a lookup from sub-industry name to code."""
    subindustries = db.query(GICSSubIndustry).all()
    return {si.name: si.code for si in subindustries}


def fetch_etf_holdings(etf_ticker: str) -> List[str]:
    """
    Fetch holdings from an ETF using yfinance.
    Returns list of ticker symbols.
    """
    try:
        etf = yf.Ticker(etf_ticker)
        # Try to get holdings
        try:
            holdings = etf.info.get('holdings', [])
            if holdings:
                return [h.get('symbol', '') for h in holdings if h.get('symbol')]
        except:
            pass
        
        # Try to get from fund data
        try:
            if hasattr(etf, 'funds_data'):
                holdings = etf.funds_data.top_holdings
                if holdings is not None and not holdings.empty:
                    return holdings.index.tolist()
        except:
            pass
        
        return []
    except Exception as e:
        logger.debug(f"Could not fetch holdings for {etf_ticker}: {e}")
        return []


def screen_for_us_stocks(min_market_cap: float = 50_000_000) -> List[str]:
    """
    Screen for US stocks meeting minimum market cap criteria.
    Uses yfinance screeners.
    """
    logger.info("Screening for additional US stocks...")
    
    all_tickers = set()
    
    # Method 1: Get holdings from broad market ETFs
    logger.info("Fetching holdings from broad market ETFs...")
    for etf in STOCK_SOURCE_ETFS:
        holdings = fetch_etf_holdings(etf)
        if holdings:
            all_tickers.update(holdings)
            logger.info(f"  {etf}: {len(holdings)} holdings")
        time.sleep(0.5)  # Rate limit
    
    # Method 2: Get holdings from sector ETFs
    logger.info("Fetching holdings from sector ETFs...")
    for sector_code, etfs in SECTOR_ETFS_FOR_SCREENING.items():
        for etf in etfs:
            holdings = fetch_etf_holdings(etf)
            if holdings:
                all_tickers.update(holdings)
            time.sleep(0.3)
    
    # Method 3: Use pre-defined comprehensive ticker list from data module
    # These are common US stocks organized by sector
    from src.data.additional_tickers import get_all_additional_tickers
    additional = get_all_additional_tickers()
    all_tickers.update(additional)
    logger.info(f"  Additional tickers from data module: {len(additional)}")
    
    # Method 4: Add more tickers from inline list for extra coverage
    all_tickers.update(get_comprehensive_ticker_list())
    
    logger.info(f"Total unique tickers found: {len(all_tickers)}")
    return list(all_tickers)


def get_comprehensive_ticker_list() -> List[str]:
    """
    Return a comprehensive list of US stock tickers.
    This includes Russell 3000 components and other notable stocks.
    """
    # This is a comprehensive list of ~3000+ US stocks
    # Includes Russell 3000 components and other notable tickers
    tickers = [
        # === ENERGY (Sector 10) ===
        # Oil & Gas Drilling
        "HP", "NBR", "RIG", "VAL", "DO", "NE", "PTEN", "PDS", "BORR",
        # Oil & Gas E&P
        "APA", "DVN", "FANG", "EOG", "PXD", "COP", "OXY", "MRO", "HES", "CLR",
        "PR", "MTDR", "CTRA", "CHRD", "OVV", "MGY", "SM", "PDCE", "CRGY",
        "GPOR", "SBOW", "CNX", "RRC", "AR", "SWN", "EQT", "CHK", "TELL",
        "VTLE", "REPX", "BATL", "ESTE", "HNRG", "REI", "VET", "PARR", "DEN",
        # Oil & Gas Refining
        "VLO", "PSX", "MPC", "DK", "HFC", "PBF", "CVI", "DINO", "CLMT",
        # Oil & Gas Midstream/Storage
        "KMI", "WMB", "OKE", "ET", "MPLX", "EPD", "PAA", "WES", "TRGP",
        "AM", "DCP", "HESM", "USAC", "SMLP", "NGL", "CEQP", "ENLC", "CIVI",
        # Oil Services & Equipment
        "SLB", "HAL", "BKR", "NOV", "FTI", "CHX", "WHD", "WTTR", "OII",
        "LBRT", "NEX", "RES", "HLX", "CLB", "XPRO", "SOC", "BOOM", "GEL",
        
        # === MATERIALS (Sector 15) ===
        # Chemicals
        "DOW", "LYB", "CE", "EMN", "HUN", "WLK", "OLN", "TROX", "KRO",
        "ASIX", "MEOH", "IOSP", "KWR", "NGVT", "FUL", "RPM", "GRA", "BCPC",
        # Specialty Chemicals
        "APD", "ECL", "SHW", "PPG", "ALB", "IFF", "AVNT", "AXTA", "ASH",
        "GCP", "CBT", "CC", "FOE", "LTH", "HWKN", "MTX", "UFPI", "LTHM",
        # Agricultural Chemicals
        "NTR", "CF", "MOS", "FMC", "SMG", "CTVA", "AMRS", "AGFY", "ICL",
        # Construction Materials
        "VMC", "MLM", "EXP", "ITE", "USLM", "SUM", "RHI", "ROCK",
        # Metals & Mining
        "NEM", "FCX", "GOLD", "NUE", "STLD", "CLF", "X", "AA", "ATI",
        "CMC", "RS", "CRS", "WOR", "ZEUS", "HAYN", "SGML", "CENX", "KALU",
        "ACM", "ARCH", "HCC", "BTU", "CEIX", "ARLP", "CONSOL", "AMR",
        # Gold & Silver Mining
        "AEM", "KGC", "AU", "PAAS", "HL", "AG", "EXK", "CDE", "FSM",
        "SILV", "MAG", "SSRM", "BTG", "IAG", "HMY", "DRD", "NGD", "GATO",
        # Steel
        "STLD", "TX", "TMST", "ZEUS", "SCHN", "RYI", "SXC", "RDUS", "UFAB",
        # Paper & Forest Products
        "IP", "WRK", "PKG", "SON", "SEE", "BLL", "CCK", "ATR", "GEF",
        "BERY", "UFPT", "SLVM", "PACK", "MERC", "KRT", "CLW", "LSB",
        
        # === INDUSTRIALS (Sector 20) ===
        # Aerospace & Defense
        "BA", "LMT", "NOC", "GD", "RTX", "HII", "TDG", "LHX", "HWM",
        "TXT", "AXON", "CW", "MOG.A", "SPR", "HXL", "DCO", "AIR", "VSEC",
        "KTOS", "MRCY", "AVAV", "RCAT", "BWXT", "LDOS", "CACI", "SAIC",
        "PSN", "VVX", "COHU", "DRS", "ERJ", "PKE", "OEG", "MAXR",
        # Building Products
        "JCI", "CARR", "TT", "LII", "MAS", "FBHS", "AWI", "DOOR", "AZEK",
        "BLD", "APOG", "GFF", "PGTI", "JELD", "TILE", "TREX", "SSD",
        "BLDR", "CNR", "BCC", "OC", "IBP", "ROCK", "CSGS", "CSWI",
        # Construction & Engineering
        "ACM", "MTZ", "PWR", "DY", "EME", "FIX", "PRIM", "TPC", "MYRG",
        "STRL", "ORN", "ROAD", "CTO", "IESC", "GVA", "KBR", "FLR",
        # Electrical Equipment
        "ETN", "ROK", "EMR", "AME", "RBC", "GNRC", "AZZ", "ATKR", "WCC",
        "HUBB", "POWL", "AYI", "EAF", "WIRE", "NVT", "GE", "VRT", "PLUG",
        # Industrial Conglomerates
        "MMM", "HON", "GE", "ITW", "ROP", "DHR", "IEP", "HRI", "OEG",
        # Machinery
        "CAT", "DE", "PCAR", "CMI", "SWK", "GNRC", "EMR", "TTC", "OSK",
        "AGCO", "CNHI", "TEREX", "ALG", "KMT", "MEC", "NPO", "CFX",
        "HAYW", "HLIO", "LNN", "MIDD", "MTW", "SXI", "TWI", "WTS",
        "BMI", "FLOW", "HI", "GTES", "AIT", "GTLS", "IDEX", "IEX",
        "ITT", "LB", "LECO", "MANT", "PNR", "RXO", "TKR", "WMS", "XYL",
        # Trading Companies & Distributors
        "GWW", "FAST", "WSO", "MSM", "SITE", "DXPE", "DNOW", "DXP", "HDSN",
        "PKOH", "NOW", "SYX", "TITN", "WESCO", "HDS", "CNH", "CCMP",
        # Commercial Services
        "WM", "RSG", "WCN", "CWST", "SRCL", "CLH", "ECOL", "HCCI", "NVRI",
        "VSE", "ABM", "CTAS", "ARMK", "BCO", "BRC", "NSIT", "RR", "SLQT",
        # Professional Services
        "ACN", "VRSK", "FTV", "TRI", "BR", "EEFT", "EFX", "EXPO", "FCN",
        "FORR", "HURN", "INFO", "KFRC", "MAN", "MMS", "RHI", "TNET",
        # Airlines
        "DAL", "UAL", "LUV", "AAL", "ALK", "JBLU", "SAVE", "HA", "ALGT",
        "MESA", "SKYW", "RYAAY", "ULCC", "SNCY",
        # Transportation
        "UNP", "CSX", "NSC", "CP", "KSU", "WAB", "GBX", "RAIL", "TRN",
        "FDX", "UPS", "XPO", "JBHT", "ODFL", "SAIA", "WERN", "LSTR",
        "HTLD", "KNX", "MRTN", "SNDR", "ARCB", "CHRW", "EXPD", "HUBG",
        "ECHO", "GXO", "FWRD", "RADL", "RLGT", "USX",
        
        # === CONSUMER DISCRETIONARY (Sector 25) ===
        # Auto Manufacturers
        "F", "GM", "TSLA", "RIVN", "LCID", "FSR", "NIO", "XPEV", "LI",
        "GOEV", "WKHS", "RIDE", "SOLO", "NKLA", "MULN", "FFIE", "ARVL",
        # Auto Parts
        "APTV", "BWA", "LEA", "MGA", "ALV", "ADNT", "AXL", "GNTX", "VC",
        "DAN", "MOD", "PHIN", "SMP", "LCII", "THRM", "CWH", "AEY",
        "DORM", "FOXF", "GTX", "LKQ", "SRI", "STRT", "SUP", "TEN", "TORC",
        # Auto Retail
        "AN", "ABG", "GPI", "PAG", "LAD", "SAH", "RUSHA", "RUSHB",
        "KMX", "CVNA", "SFT", "CARS", "CARG", "VRM", "LOTZ", "CZOO",
        # Home Improvement Retail
        "HD", "LOW", "FND", "LL", "FLOR", "SHC", "TILE",
        # Homebuilding
        "DHI", "LEN", "PHM", "NVR", "TOL", "KBH", "TMHC", "MDC", "MTH",
        "MHO", "TPH", "SKY", "CCS", "HOV", "BZH", "GRBK", "CVCO", "LGIH",
        "DFH", "FBHS", "LEGH", "UHG", "WH", "MERH",
        # Household Appliances
        "WHR", "SEB", "HELE", "IRBT", "SHAK", "NPK", "HBB",
        # Leisure Products
        "HAS", "MAT", "POOL", "BC", "PTON", "NLS", "PRKS", "FNKO",
        "JAKK", "PLNT", "PLAY", "BOWX", "TRAK", "VSTO", "YETI",
        # Apparel & Luxury
        "NKE", "LULU", "TPR", "VFC", "PVH", "RL", "CPRI", "GIII", "GIL",
        "COLM", "UAA", "CROX", "DECK", "SKX", "SHOO", "WWW", "WEYS",
        "CATO", "HNST", "GES", "LEVI", "GOOS", "HBI", "SCVL", "CAL",
        # Home Furnishings
        "RH", "WSM", "ARHS", "ETH", "LOVE", "SNBR", "PRPL", "CSPR",
        "TPX", "LEG", "HVT", "FLXS", "PATK",
        # Casinos & Gaming
        "LVS", "WYNN", "MGM", "CZR", "DKNG", "PENN", "BYD", "MLCO",
        "RRR", "GDEN", "MTN", "IGT", "SGMS", "GAN", "RSI", "BALY",
        # Hotels & Resorts
        "MAR", "HLT", "H", "IHG", "WH", "CHH", "VAC", "TNL", "PLYA",
        "MTN", "HGV", "BHR", "STAY", "APTS", "CLDT", "HT", "RHP",
        # Restaurants
        "MCD", "SBUX", "DPZ", "CMG", "YUM", "QSR", "WEN", "DNUT", "PZZA",
        "DRI", "TXRH", "BLMN", "EAT", "CAKE", "DIN", "JACK", "TACO",
        "WING", "SHAK", "BROS", "CAVA", "SG", "COCO", "LOCO", "ARCO",
        # Specialty Retail
        "AMZN", "TGT", "COST", "WMT", "DG", "DLTR", "FIVE", "OLLI",
        "BBY", "GME", "CHWY", "W", "ZG", "ETSY", "EBAY", "MELI", "WISH",
        "BABA", "JD", "PDD", "SHOP", "SE", "CPNG", "GRPN", "OPEN",
        "FIGS", "RENT", "BIRD", "TDUP", "REAL", "PRTS", "SSTK", "STMP",
        "TCS", "ASO", "DKS", "HIBB", "BGFV", "SPWH", "PLCE", "BURL",
        "ROST", "TJX", "GPS", "AEO", "ANF", "EXPR", "LIND", "ZUMZ",
        "BOOT", "BKE", "CTRN", "CHICO", "CURV", "DXLG", "TLRD",
        # Education Services
        "CHGG", "COUR", "DUOL", "LRN", "ATGE", "LOPE", "PRDO", "STRA",
        "TWOU", "UDMY", "BFAM", "APEI", "LAUR", "LINC", "VCNX",
        
        # === CONSUMER STAPLES (Sector 30) ===
        # Food & Beverage
        "PEP", "KO", "MDLZ", "KHC", "GIS", "K", "CAG", "CPB", "SJM",
        "HRL", "TSN", "PPC", "SAFM", "JJSF", "LANC", "INGR", "DAR", "CALM",
        "HAIN", "SMPL", "THS", "BRBR", "SENEA", "UNFI", "USFD", "PFGC",
        "DOLE", "COCO", "CELH", "FIZZ", "MNST", "REED", "NBEV", "ZVIA",
        # Beverages
        "BUD", "TAP", "SAM", "STZ", "DEO", "BF.B", "ABEV", "CCU",
        # Tobacco
        "PM", "MO", "BTI", "IMBBY", "TPB", "VGR", "UVV", "CRLBF",
        # Household Products
        "PG", "CL", "CHD", "CLX", "KMB", "SPB", "EPC", "ELF", "IPAR",
        "HELE", "REVG", "CENT", "CENT.A", "SMPL", "NUS", "USNA",
        # Personal Products
        "EL", "COTY", "SKIN", "HIMS", "PRGO", "NWL", "HLF", "REV", "GROV",
        # Retail - Grocery
        "KR", "WBA", "CVS", "ACI", "SFM", "IMKTA", "CHEF", "BGS",
        "GO", "UNFI", "PFGC", "NDLS", "CASY", "WEIS", "VLGEA",
        
        # === HEALTH CARE (Sector 35) ===
        # Biotechnology
        "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "BNTX", "SGEN",
        "ALNY", "INCY", "BMRN", "EXEL", "IONS", "UTHR", "RARE", "NBIX",
        "SRPT", "BLUE", "SGMO", "EDIT", "CRSP", "NTLA", "BEAM", "VERV",
        "TWST", "DNA", "ALLO", "RXRX", "KRYS", "ARWR", "FOLD", "DNLI",
        "KYMR", "KROS", "HARP", "BCRX", "ARQT", "DRNA", "VCNX", "MYOV",
        "BGNE", "LEGN", "RPRX", "ROIV", "JANX", "VERA", "IDYA", "RCUS",
        # Pharmaceuticals
        "JNJ", "PFE", "LLY", "MRK", "ABBV", "BMY", "AZN", "NVO", "SNY",
        "GSK", "ZTS", "VTRS", "TEVA", "PRGO", "HLN", "ELAN", "SUPN",
        "CTLT", "JAZZ", "PCRX", "IRWD", "PAHC", "RVNC", "SLNO", "AKBA",
        "ITCI", "AMPH", "ANI", "CORT", "CPRX", "DRRX", "EOLS", "ENTA",
        # Medical Devices
        "ABT", "MDT", "SYK", "BSX", "ISRG", "EW", "ZBH", "DXCM", "HOLX",
        "ALGN", "RMD", "TFX", "NVST", "SWAV", "PEN", "GMED", "RGEN",
        "PODD", "INSP", "TNDM", "GKOS", "LIVN", "STAA", "ATRC", "MMSI",
        "IRTC", "OFIX", "CNMD", "AHCO", "NARI", "LMAT", "NUVA", "UFPT",
        "NVCR", "MASI", "HAE", "ESTA", "ATEC", "AXGN", "INGN", "LUNG",
        # Health Care Facilities
        "UNH", "ELV", "HUM", "CI", "CNC", "MOH", "UHS", "THC", "ACHC",
        "HCA", "DVA", "AMED", "ADUS", "ENSG", "PNTG", "SEM", "NHC",
        "CCRN", "USPH", "SGRY", "OPCH", "ALHC", "HCSG", "LHCG", "BKD",
        # Health Care Services
        "CVS", "WBA", "HCSG", "AMED", "AFMD", "EVH", "GH", "OSH", "ONEM",
        "PRVA", "EHAB", "DOCS", "PHR", "TALK", "AMWL", "TDOC", "HIMS",
        # Life Sciences Tools
        "TMO", "DHR", "A", "BIO", "ILMN", "MTD", "WAT", "PKI", "TECH",
        "BIO.B", "CRL", "ICLR", "MEDP", "RVTY", "CDNA", "EXAS", "VCYT",
        "NVTA", "ME", "VEEV", "RGEN", "MYGN", "NTRA", "TWST", "PACB",
        
        # === FINANCIALS (Sector 40) ===
        # Banks - Diversified
        "JPM", "BAC", "WFC", "C", "GS", "MS", "SCHW", "BK", "STT",
        "PNC", "TFC", "USB", "COF", "AXP", "DFS", "SYF", "ALLY",
        # Banks - Regional
        "HBAN", "KEY", "RF", "CFG", "FITB", "MTB", "ZION", "CMA",
        "FRC", "SIVB", "PACW", "WAL", "FHN", "BOKF", "SNV", "VLY",
        "WBS", "EWBC", "GBCI", "IBKR", "ONB", "PNFP", "SBCF", "SEIC",
        "TOWN", "UBSI", "UMPQ", "WAFD", "WSFS", "ASB", "BHF", "FBK",
        "FFIN", "FULT", "IBOC", "NBTB", "PPBI", "SBNY", "TBBK", "TCBI",
        "UCBI", "COLB", "CATY", "CVBF", "DCOM", "EFSC", "FFWM", "FMBI",
        "FRME", "FVCB", "GABC", "HWC", "INDB", "IBTX", "OFG", "PRK",
        # Asset Management
        "BLK", "BX", "KKR", "APO", "ARES", "OWL", "CG", "TPG", "TROW",
        "IVZ", "BEN", "FHI", "VCTR", "PZN", "GHL", "HL", "PJT", "MC",
        "MKTX", "LPLA", "CBOE", "CME", "ICE", "NDAQ", "COIN",
        # Insurance
        "BRK.B", "PGR", "ALL", "TRV", "CB", "AIG", "MET", "PRU", "AFL",
        "AJG", "MMC", "AON", "WTW", "BRO", "ERIE", "CNA", "Y", "RNR",
        "THG", "WRB", "AIZ", "CNO", "FAF", "FNF", "GL", "HIG", "KMPR",
        "L", "LNC", "ORI", "PFG", "PLMR", "RDN", "RGA", "SLF", "SIGI",
        # Financial Services
        "V", "MA", "PYPL", "SQ", "FIS", "FISV", "GPN", "AFRM", "UPST",
        "SOFI", "HOOD", "LMND", "OPEN", "BILL", "PAYO", "MQ", "TOST",
        "NAVI", "SLM", "ESNT", "MTG", "RDFN", "UWMC", "RKT", "GHLD",
        
        # === INFORMATION TECHNOLOGY (Sector 45) ===
        # Software - Application
        "MSFT", "ORCL", "CRM", "ADBE", "INTU", "NOW", "WDAY", "PANW",
        "ZS", "CRWD", "NET", "DDOG", "ZM", "SNOW", "PLTR", "TEAM",
        "SPLK", "OKTA", "HUBS", "MDB", "TWLO", "U", "PATH", "CFLT",
        "BILL", "DOCU", "ASAN", "APPF", "APPS", "AVLR", "BASE", "BLKB",
        "BSY", "CCSI", "CDNS", "CHKP", "CLDR", "COUP", "CRTO", "DCT",
        "DOMO", "ESTC", "EVBG", "FIVN", "FROG", "FSLY", "GTLB", "JAMF",
        "MANH", "MDSO", "MSTR", "NCNO", "NICE", "OOMA", "OPEN", "OV",
        "PAYC", "PCTY", "PDFS", "PD", "PING", "PLAN", "PS", "PYCR",
        "QTWO", "RAMP", "RNG", "RPD", "SAIL", "SHOP", "SITM", "SMAR",
        "SPT", "SUMO", "TYL", "VEEV", "WIX", "WKME", "ZEN", "ZI", "ZUO",
        # Software - Infrastructure
        "IBM", "VMW", "FTNT", "SNPS", "KEYS", "AKAM", "FFIV", "NLOK",
        "QLYS", "RPD", "SAIL", "SCWX", "SNCR", "TENB", "VRNS", "VRNT",
        # Semiconductors
        "NVDA", "AMD", "INTC", "TXN", "AVGO", "QCOM", "MU", "ADI", "NXPI",
        "MCHP", "LRCX", "AMAT", "KLAC", "MRVL", "ON", "SWKS", "QRVO",
        "MPWR", "SLAB", "DIOD", "RMBS", "CRUS", "FORM", "HIMX", "IMOS",
        "LSCC", "MTSI", "POWI", "SIMO", "SITM", "SMTC", "ENTG", "KLIC",
        "MKSI", "ONTO", "UCTT", "WOLF", "ACMR", "AMKR", "AOSL", "ASML",
        "COHU", "CREE", "LEDS", "NVMI", "PLAB", "QUIK", "SMCI", "TSM",
        # IT Services
        "ACN", "CTSH", "FIS", "FISV", "IT", "WIT", "EPAM", "GLOB", "GDYN",
        "EXLS", "PEGA", "PRFT", "SSNC", "TTEC", "VNET", "WITS",
        # Hardware
        "AAPL", "HPQ", "HPE", "DELL", "NTAP", "WDC", "STX", "PSTG",
        "LOGI", "CRSR", "DGII", "DSGX", "HEAR", "IMMR", "INSG", "NTGR",
        "PSEC", "SMCI", "SSYS", "ZBRA", "LQDT", "VIAV",
        # Communications Equipment
        "CSCO", "MSI", "JNPR", "UI", "ERIC", "NOK", "CIEN", "LITE",
        "ACIA", "CALX", "CASA", "COMM", "HLIT", "INFN", "IRDM", "VIAV",
        
        # === COMMUNICATION SERVICES (Sector 50) ===
        # Interactive Media
        "GOOGL", "META", "SNAP", "PINS", "TWTR", "MTCH", "BMBL", "IAC",
        "ZG", "YELP", "GRPN", "ANGI", "TTD", "MGNI", "PUBM", "CARG",
        # Entertainment
        "DIS", "NFLX", "CMCSA", "CHTR", "WBD", "PARA", "VIAC", "AMC",
        "CNK", "IMAX", "LGF.A", "LGF.B", "LSXMA", "LSXMB", "ROKU", "SIRI",
        "SPOT", "TME", "WMG", "FWONA", "FWONK", "MSGS", "MSGE",
        # Gaming
        "EA", "TTWO", "ATVI", "RBLX", "DKNG", "GOGO", "GLBE", "HUYA",
        "BILI", "DDL", "DOYU", "GRVY", "PLTK", "SKLZ", "SOHU",
        # Telecom
        "T", "VZ", "TMUS", "LUMN", "FTR", "USM", "TDS", "SHEN", "GOGO",
        # Advertising
        "OMC", "IPG", "MGID", "DLX", "QUOT", "SCOR", "MGNI", "ZETA",
        
        # === UTILITIES (Sector 55) ===
        # Electric Utilities
        "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "ED",
        "PCG", "EIX", "WEC", "ES", "DTE", "AEE", "ETR", "FE", "PPL",
        "CMS", "EVRG", "PNW", "AES", "LNT", "OGE", "NWE", "NRG", "POR",
        "IDA", "AVA", "EE", "BKH", "HE", "NWN", "OGS", "PNM", "SWX", "UTL",
        # Gas Utilities
        "NJR", "NFG", "NI", "SR", "SWX", "UGI", "ONE", "CPK", "SJI",
        # Multi-Utilities
        "AWK", "WTRG", "CWT", "SJW", "YORW", "MSEX", "AWR", "ARTNA",
        # Renewable Energy
        "NEP", "AQN", "BEP", "CWEN", "HASI", "ORA", "RUN", "SPWR",
        "NOVA", "ENPH", "SEDG", "FSLR", "JKS", "ARRY", "CSIQ",
        
        # === REAL ESTATE (Sector 60) ===
        # REITs - Diversified
        "SPG", "O", "VICI", "WPC", "STOR", "NNN", "GTY", "GOOD",
        # REITs - Industrial
        "PLD", "DRE", "REXR", "STAG", "TRNO", "FR", "EGP", "GTY",
        # REITs - Office
        "BXP", "KRC", "SLG", "VNO", "HIW", "CUZ", "PGRE", "JBGS",
        "DEI", "PDM", "OFC", "ESRT", "BDN", "CLI", "CDR", "FSP",
        # REITs - Residential
        "EQR", "AVB", "ESS", "UDR", "CPT", "MAA", "AIV", "IRT", "NXRT",
        "ELME", "VRE", "CSR", "AHH", "NXE", "IRET",
        # REITs - Retail
        "REG", "FRT", "KIM", "BRX", "SITC", "ROIC", "RPAI", "UE", "AKR",
        "KRG", "MAC", "PEI", "CBL", "WRI", "WSR", "ALEX",
        # REITs - Healthcare
        "WELL", "VTR", "PEAK", "HR", "OHI", "LTC", "NHI", "SBRA", "CTRE",
        "CHCT", "MPW", "DOC", "GHC",
        # REITs - Self Storage
        "PSA", "EXR", "CUBE", "LSI", "NSA", "JCAP",
        # REITs - Data Center
        "EQIX", "DLR", "AMT", "CCI", "SBAC", "UNIT", "CCOI",
        # REITs - Hotel
        "HST", "PK", "RHP", "PEB", "SHO", "DRH", "XHR", "INN", "CLDT",
        # Real Estate Services
        "CBRE", "JLL", "CWK", "NMRK", "RMR", "RLJ", "FSV", "EXPI",
        "CIGI", "RLGY", "HF", "RMAX", "COMP", "OPEN", "RDFN", "ZG",
        
        # === ADDITIONAL SMALL/MID CAPS ACROSS SECTORS ===
        # These ensure broader coverage across all industries
        "NVAX", "VXRT", "INO", "MRVI", "CRBU", "ATAI", "MNMD", "CMPS",
        "ACCD", "ACIU", "ACLX", "ACRS", "ADGI", "ADPT", "ADVM", "AEHR",
        "AEVA", "AFAR", "AFIB", "AFRM", "AGFY", "AGNC", "AHCO", "AIRT",
        "AKTS", "ALDX", "ALEC", "ALGT", "ALLO", "ALLK", "ALNY", "ALRN",
        "ALTR", "ALVR", "AMEH", "AMLI", "AMPL", "AMRC", "AMRK", "AMRS",
        "AMSC", "AMST", "AMTI", "AMWD", "AMZN", "ANAB", "ANAT", "ANEB",
        "ANET", "ANGI", "ANGN", "ANGO", "ANIK", "ANIP", "ANSS", "ANY",
        "AOSL", "AORT", "AOUT", "APAM", "APCX", "APDN", "APEI", "APGE",
        "APLS", "APLT", "APMR", "APOG", "APPF", "APPS", "APRE", "APTV",
        "AQUA", "AR", "ARAY", "ARCB", "ARCC", "ARCE", "ARCH", "ARCO",
        "ARCT", "ARDX", "AREC", "ARGT", "ARIS", "ARKO", "ARKR", "ARLO",
        "ARMP", "ARNC", "AROC", "AROW", "ARQT", "ARTA", "ARTL", "ARTNA",
        "ARVN", "ARWR", "ARYA", "ASAI", "ASLE", "ASMB", "ASML", "ASND",
        "ASNS", "ASPN", "ASPS", "ASRT", "ASTE", "ASUR", "ASXC", "ATAI",
        "ATAT", "ATCO", "ATEC", "ATEN", "ATEST", "ATHE", "ATKR", "ATLC",
        "ATLO", "ATNF", "ATNM", "ATOM", "ATOS", "ATRA", "ATRC", "ATRI",
        "ATRO", "ATRS", "ATSC", "ATSG", "ATVI", "ATXG", "ATXI", "ATXS",
        "AUBN", "AUPH", "AUTL", "AUTO", "AUVI", "AVAV", "AVDL", "AVDX",
        "AVEL", "AVGO", "AVID", "AVIR", "AVNS", "AVNT", "AVNW", "AVO",
        "AVPT", "AVRO", "AVT", "AVTE", "AVTR", "AVXL", "AWH", "AWI",
        "AWK", "AWR", "AWRE", "AX", "AXAS", "AXDX", "AXGN", "AXLA",
        "AXNX", "AXON", "AXSM", "AXTA", "AXTI", "AY", "AYI", "AYLA",
        "AYRO", "AYTU", "AZN", "AZPN", "AZRE", "AZTA", "AZZ", "B",
    ]
    
    return list(set(tickers))


def get_stock_info_batch(tickers: List[str], batch_size: int = 20) -> Dict[str, Dict]:
    """
    Fetch stock info (sector, industry) for multiple tickers.
    Returns dict mapping ticker to info dict.
    """
    all_info = {}
    
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(tickers) + batch_size - 1) // batch_size
        
        if batch_num % 10 == 0:
            logger.info(f"Fetching info batch {batch_num}/{total_batches}...")
        
        for ticker in batch:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if info.get('sector') and info.get('industry'):
                    all_info[ticker] = {
                        'name': info.get('longName') or info.get('shortName', ticker),
                        'sector': info.get('sector'),
                        'industry': info.get('industry'),
                        'market_cap': info.get('marketCap', 0),
                        'exchange': info.get('exchange', ''),
                        'quote_type': info.get('quoteType', ''),
                    }
            except Exception as e:
                logger.debug(f"Could not fetch info for {ticker}: {e}")
            
            time.sleep(0.1)  # Rate limit
        
        time.sleep(0.5)  # Pause between batches
    
    return all_info


def map_yfinance_industry_to_gics(
    yf_sector: str,
    yf_industry: str,
    subindustry_lookup: Dict[str, str]
) -> Optional[str]:
    """
    Map a yfinance industry to a GICS sub-industry code.
    Returns the GICS sub-industry code or None if no match.
    """
    # First try direct mapping
    if yf_industry in YFINANCE_TO_GICS_INDUSTRY:
        gics_name = YFINANCE_TO_GICS_INDUSTRY[yf_industry]
        if gics_name in subindustry_lookup:
            return subindustry_lookup[gics_name]
    
    # Try partial matching
    yf_industry_lower = yf_industry.lower()
    for gics_name, gics_code in subindustry_lookup.items():
        gics_name_lower = gics_name.lower()
        
        # Check if yfinance industry contains GICS name or vice versa
        if yf_industry_lower in gics_name_lower or gics_name_lower in yf_industry_lower:
            return gics_code
    
    # Try sector-based fallback
    if yf_sector in YFINANCE_SECTOR_TO_GICS:
        sector_code = YFINANCE_SECTOR_TO_GICS[yf_sector]
        # Find any sub-industry in this sector
        for gics_name, gics_code in subindustry_lookup.items():
            if gics_code.startswith(sector_code):
                return gics_code
    
    return None


def select_stocks_with_priority(
    stock_candidates: Dict[str, Dict],
    subindustry_lookup: Dict[str, str],
    priority_scores: Dict[str, float],
    target_count: int
) -> List[Tuple[str, str, str]]:
    """
    Select stocks prioritizing underrepresented industries.
    
    Returns list of (ticker, name, gics_subindustry_code) tuples.
    """
    # Score each candidate
    scored_candidates = []
    
    for ticker, info in stock_candidates.items():
        gics_code = map_yfinance_industry_to_gics(
            info.get('sector', ''),
            info.get('industry', ''),
            subindustry_lookup
        )
        
        if gics_code:
            priority = priority_scores.get(gics_code, 0.5)
            # Boost priority for stocks with higher market cap (more liquid)
            market_cap = info.get('market_cap', 0) or 0
            cap_bonus = min(0.2, market_cap / 100_000_000_000)  # Up to 0.2 bonus for $100B+ cap
            
            final_score = priority + cap_bonus
            
            scored_candidates.append((
                ticker,
                info.get('name', ticker),
                gics_code,
                final_score
            ))
    
    # Sort by priority score (descending)
    scored_candidates.sort(key=lambda x: x[3], reverse=True)
    
    # Take top candidates
    selected = [(t, n, c) for t, n, c, _ in scored_candidates[:target_count]]
    
    return selected


def add_stocks_to_database(
    db: Session,
    stocks: List[Tuple[str, str, str]],
    dry_run: bool = False
) -> int:
    """
    Add stocks to the database.
    
    Args:
        stocks: List of (ticker, name, gics_subindustry_code) tuples
    
    Returns:
        Number of stocks added
    """
    count = 0
    
    for ticker, name, gics_code in stocks:
        # Verify sub-industry exists
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.code == gics_code
        ).first()
        
        if not subindustry:
            logger.debug(f"Sub-industry {gics_code} not found for {ticker}, skipping")
            continue
        
        if dry_run:
            logger.info(f"  [DRY-RUN] Would add: {ticker} ({name}) -> {subindustry.name}")
        else:
            stock = Stock(
                ticker=ticker,
                name=name[:200] if name else ticker,  # Truncate long names
                gics_subindustry_code=gics_code,
                is_active=True,
            )
            db.add(stock)
        
        count += 1
        
        # Commit in batches
        if not dry_run and count % 100 == 0:
            db.commit()
            logger.info(f"  Added {count} stocks...")
    
    if not dry_run and count > 0:
        db.commit()
    
    return count


def fetch_prices_for_stocks(
    db: Session,
    tickers: List[str],
    dry_run: bool = False
) -> int:
    """Fetch historical prices for new stocks."""
    if dry_run:
        logger.info(f"[DRY-RUN] Would fetch prices for {len(tickers)} stocks")
        return 0
    
    if not tickers:
        return 0
    
    logger.info(f"Fetching price history for {len(tickers)} new stocks...")
    
    # Calculate date range (2 years + buffer)
    end_date = date.today()
    start_date = end_date - timedelta(days=settings.PRICE_HISTORY_YEARS * 365 + 30)
    
    # Fetch prices in batch
    all_prices = yfinance_source.fetch_multiple_prices(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        batch_size=50
    )
    
    # Store prices in database
    total_records = 0
    for ticker, df in all_prices.items():
        if df.empty:
            continue
        
        for _, row in df.iterrows():
            try:
                # Check for existing record
                existing = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
                price = StockPrice(
                    ticker=ticker,
                    date=row['date'],
                    open=row.get('open'),
                    high=row.get('high'),
                    low=row.get('low'),
                    close=row['close'],
                    adj_close=row.get('adj_close', row['close']),
                    volume=int(row['volume']) if 'volume' in row and row['volume'] else None,
                )
                db.add(price)
                total_records += 1
                
            except Exception as e:
                logger.warning(f"Error storing price for {ticker}: {e}")
        
        # Commit in batches
        if total_records > 0 and total_records % 5000 == 0:
            db.commit()
            logger.info(f"  Stored {total_records:,} price records...")
    
    if total_records > 0:
        db.commit()
    
    logger.info(f"Stored {total_records:,} price records")
    return total_records


def main():
    parser = argparse.ArgumentParser(
        description='Add additional stocks to the RS Dashboard database, prioritizing underrepresented industries'
    )
    parser.add_argument(
        '--target', type=int, default=1500,
        help='Target number of new stocks to add (default: 1500)'
    )
    parser.add_argument(
        '--with-prices', action='store_true',
        help='Also fetch price history for new stocks'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be added without making changes'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 70)
    logger.info("RS Dashboard - Add More Stocks (Priority-Based)")
    logger.info("=" * 70)
    logger.info(f"Target: {args.target} new stocks")
    
    if args.dry_run:
        logger.info("*** DRY RUN MODE - No changes will be made ***")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Step 1: Get current state
        logger.info("\nStep 1: Analyzing current stock distribution...")
        existing_tickers = get_existing_tickers(db)
        logger.info(f"  Current stocks in database: {len(existing_tickers)}")
        
        distribution = get_current_stock_distribution(db)
        priority_scores = get_subindustry_priority_scores(db)
        subindustry_lookup = get_subindustry_lookup(db)
        
        # Log priority analysis
        sorted_priorities = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
        logger.info("\n  Top 10 underrepresented industries (highest priority):")
        for code, score in sorted_priorities[:10]:
            if code in distribution:
                name = distribution[code]['name']
                count = distribution[code]['count']
                logger.info(f"    {name}: {count} stocks (priority: {score:.2f})")
        
        # Step 2: Get candidate stocks
        logger.info("\nStep 2: Building candidate stock list...")
        candidate_tickers = screen_for_us_stocks()
        
        # Filter out existing stocks
        new_candidates = [t for t in candidate_tickers if t not in existing_tickers]
        logger.info(f"  Candidates after filtering existing: {len(new_candidates)}")
        
        # Step 3: Fetch stock info
        logger.info("\nStep 3: Fetching stock info from Yahoo Finance...")
        stock_info = get_stock_info_batch(new_candidates)
        logger.info(f"  Successfully fetched info for {len(stock_info)} stocks")
        
        # Step 4: Select stocks with priority
        logger.info("\nStep 4: Selecting stocks with industry priority weighting...")
        selected_stocks = select_stocks_with_priority(
            stock_info,
            subindustry_lookup,
            priority_scores,
            args.target
        )
        logger.info(f"  Selected {len(selected_stocks)} stocks")
        
        # Log sector distribution of selected stocks
        sector_counts = defaultdict(int)
        for _, _, code in selected_stocks:
            sector_code = code[:2]
            sector_counts[sector_code] += 1
        
        logger.info("\n  Selected stocks by sector:")
        sector_names = {v: k for k, v in GICS_SECTORS.items()}
        for sector_code in sorted(sector_counts.keys()):
            sector_name = sector_names.get(sector_code, f"Unknown ({sector_code})")
            logger.info(f"    {sector_name}: {sector_counts[sector_code]}")
        
        # Step 5: Add stocks to database
        logger.info("\nStep 5: Adding stocks to database...")
        added_count = add_stocks_to_database(db, selected_stocks, dry_run=args.dry_run)
        logger.info(f"  {'Would add' if args.dry_run else 'Added'} {added_count} stocks")
        
        # Step 6: Fetch prices if requested
        if args.with_prices and selected_stocks:
            logger.info("\nStep 6: Fetching price history...")
            new_tickers = [t for t, _, _ in selected_stocks]
            fetch_prices_for_stocks(db, new_tickers, dry_run=args.dry_run)
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("Summary:")
        logger.info(f"  Stocks analyzed: {len(candidate_tickers)}")
        logger.info(f"  Stocks with valid info: {len(stock_info)}")
        logger.info(f"  Stocks selected: {len(selected_stocks)}")
        logger.info(f"  Stocks {'would be' if args.dry_run else ''} added: {added_count}")
        logger.info(f"  Total stocks {'would be' if args.dry_run else 'now'} in database: {len(existing_tickers) + (0 if args.dry_run else added_count)}")
        logger.info("=" * 70)
        
        if not args.dry_run and added_count > 0:
            logger.info("\nNext steps:")
            logger.info("1. Run backfill script to fetch prices: python scripts/backfill_new_stocks.py")
            logger.info("2. Recalculate RS values: python scripts/backfill_rs.py --weeks 17")
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user.")
    except Exception as e:
        logger.exception(f"Error: {e}")
        sys.exit(1)
    finally:
        db.close()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

