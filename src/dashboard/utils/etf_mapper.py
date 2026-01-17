"""
ETF Mapper for StockCharts Sectors and Industries.

Maps sectors and industries to their representative ETFs
for display in the TradingView widget.

Prioritizes industry-level ETFs over sector-level ETFs for more granular analysis.

This module provides backward-compatible name-based lookups while also supporting
the official industry code-based mappings from the data module.
"""
import logging
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)

# Import the comprehensive industry code-based mapping
# Uses backward-compatible aliases for existing code
from src.data.stockcharts_industry_mapping import (
    INDUSTRY_ETF_MAP as GICS_SUBINDUSTRY_ETF_MAP,
    SECTOR_ETFS,
    get_etf_for_industry_code as get_etf_for_gics_code,
    get_alt_etf_for_industry_code as get_alt_etf_for_gics_code,
    get_industry_info as get_subindustry_info,
)


# Comprehensive industry-level ETF mappings
# Maps sub-industry names to specific ETFs (legacy support)
INDUSTRY_ETFS = {
    # ============================================
    # INFORMATION TECHNOLOGY
    # ============================================
    "Semiconductors": "SMH",
    "Semiconductor Materials & Equipment": "SMH",  # Exact name from database
    "Semiconductors & Semiconductor Equipment": "SMH",
    "Semiconductors and Semiconductor Equipment": "SMH",
    "Software": "IGV",
    "Systems Software": "IGV",
    "Application Software": "IGV",
    "Technology Hardware, Storage & Peripherals": "QTEC",
    "Technology Hardware Storage & Peripherals": "QTEC",
    "Technology Hardware Storage and Peripherals": "QTEC",
    "Technology Hardware": "QTEC",
    "IT Services": "SKYY",
    "IT Consulting & Other Services": "SKYY",
    "Data Processing & Outsourced Services": "SKYY",
    "Electronic Equipment & Instruments": "SOXX",
    "Electronic Equipment, Instruments & Components": "SOXX",
    "Electronic Components": "SOXX",
    "Electronic Manufacturing Services": "SOXX",
    "Communications Equipment": "FCOM",
    "Internet Services & Infrastructure": "SKYY",
    "Cloud Computing": "SKYY",
    
    # ============================================
    # HEALTH CARE
    # ============================================
    "Biotechnology": "IBB",
    "Pharmaceuticals": "XPH",
    "Health Care Equipment": "IHI",
    "Health Care Supplies": "IHI",
    "Health Care Equipment & Supplies": "IHI",
    "Health Care Services": "IHF",
    "Health Care Facilities": "IHF",
    "Health Care Providers & Services": "IHF",
    "Managed Health Care": "IHF",
    "Health Care Distributors": "IHF",
    "Life Sciences Tools & Services": "XBI",
    "Health Care Technology": "EDOC",
    "Health Care REITs": "IHF",
    
    # ============================================
    # FINANCIALS
    # ============================================
    "Banks": "KBE",
    "Diversified Banks": "KBE",
    "Regional Banks": "KRE",
    "Thrifts & Mortgage Finance": "IAT",
    "Insurance": "KIE",
    "Life & Health Insurance": "KIE",
    "Property & Casualty Insurance": "KIE",
    "Reinsurance": "KIE",
    "Multi-line Insurance": "KIE",
    "Insurance Brokers": "KIE",
    "Capital Markets": "IYG",
    "Asset Management & Custody Banks": "IYG",
    "Investment Banking & Brokerage": "IYG",
    "Diversified Capital Markets": "IYG",
    "Financial Exchanges & Data": "IYG",
    "Consumer Finance": "KBWP",
    "Diversified Financial Services": "IYG",
    "Multi-Sector Holdings": "IYG",
    "Specialized Finance": "IYG",
    "Mortgage REITs": "REM",
    "Transaction & Payment Processing Services": "IPAY",
    
    # ============================================
    # CONSUMER DISCRETIONARY
    # ============================================
    "Automobiles": "CARZ",
    "Auto Components": "CARZ",
    "Automobile Manufacturers": "CARZ",
    "Automotive Parts & Equipment": "CARZ",
    "Tires & Rubber": "CARZ",
    "Homebuilding": "XHB",
    "Home Improvement Retail": "XHB",
    "Household Durables": "XHB",
    "Building Products": "XHB",
    "Home Furnishings": "XHB",
    "Home Furnishing Retail": "XHB",
    "Homefurnishing Retail": "XHB",    # Alternate spelling
    "Housewares & Specialties": "XHB",
    "Hotels, Resorts & Cruise Lines": "PEJ",
    "Hotels & Motels": "PEJ",
    "Cruise Lines": "PEJ",
    "Casinos & Gaming": "BJK",
    "Restaurants": "PBJ",
    "Leisure Facilities": "PEJ",
    "Leisure Products": "PEJ",
    "Movies & Entertainment": "PEJ",
    "Specialty Retail": "XRT",
    "Specialty Stores": "XRT",      # Specific retail stores
    "Apparel Retail": "XRT",
    "Apparel, Accessories & Luxury Goods": "XRT",
    "Footwear": "XRT",
    "Textiles": "XRT",
    "Textiles, Apparel & Luxury Goods": "XRT",
    "Computer & Electronics Retail": "XRT",
    "Department Stores": "XRT",
    "General Merchandise Stores": "XRT",
    "Distributors": "XRT",
    "Internet & Direct Marketing Retail": "IBUY",
    "Broadline Retail": "IBUY",
    "E-Commerce": "IBUY",
    "Consumer Services": "PEJ",
    "Education Services": "PEJ",
    "Specialized Consumer Services": "PEJ",
    
    # ============================================
    # COMMUNICATION SERVICES
    # ============================================
    "Interactive Media & Services": "SOCL",
    "Interactive Home Entertainment": "ESPO",
    "Movies & Entertainment": "PEJ",
    "Entertainment": "PEJ",
    "Broadcasting": "FCOM",
    "Cable & Satellite": "FCOM",
    "Media": "FCOM",
    "Advertising": "FCOM",
    "Publishing": "FCOM",
    "Wireless Telecommunication Services": "IYZ",
    "Integrated Telecommunication Services": "IYZ",
    "Diversified Telecommunication Services": "IYZ",
    "Alternative Carriers": "IYZ",
    
    # ============================================
    # INDUSTRIALS
    # ============================================
    "Aerospace & Defense": "ITA",
    "Airlines": "JETS",
    "Air Freight & Logistics": "IYT",
    "Railroads": "IYT",
    "Trucking": "IYT",
    "Marine Transportation": "SEA",
    "Marine": "SEA",
    "Transportation Infrastructure": "IYT",
    "Airport Services": "IYT",
    "Highways & Railtracks": "IYT",
    "Passenger Airlines": "JETS",
    "Industrial Machinery & Supplies & Components": "FIW",
    "Machinery": "FIW",
    "Industrial Machinery": "FIW",
    "Agricultural & Farm Machinery": "MOO",
    "Construction Machinery & Heavy Transportation Equipment": "FIW",
    "Construction & Engineering": "PKB",
    "Construction & Farm Machinery & Heavy Trucks": "FIW",
    "Electrical Equipment": "GRID",
    "Electrical Components & Equipment": "GRID",
    "Heavy Electrical Equipment": "GRID",
    "Building Products": "XHB",
    "Industrial Conglomerates": "FIW",
    "Trading Companies & Distributors": "FIW",
    "Commercial Services & Supplies": "FIW",
    "Environmental & Facilities Services": "EVX",
    "Office Services & Supplies": "FIW",
    "Diversified Support Services": "FIW",
    "Security & Alarm Services": "HACK",
    "Human Resource & Employment Services": "FIW",
    "Research & Consulting Services": "FIW",
    "Professional Services": "FIW",
    
    # ============================================
    # CONSUMER STAPLES
    # ============================================
    "Food Retail": "PBJ",
    "Food & Staples Retailing": "PBJ",
    "Hypermarkets & Super Centers": "PBJ",
    "Drug Retail": "PBJ",
    "Beverages": "PBJ",
    "Brewers": "PBJ",
    "Distillers & Vintners": "PBJ",
    "Soft Drinks & Non-alcoholic Beverages": "PBJ",
    "Food Products": "PBJ",
    "Agricultural Products & Services": "MOO",
    "Packaged Foods & Meats": "PBJ",
    "Household Products": "PBJ",
    "Personal Care Products": "PBJ",
    "Personal Products": "PBJ",
    "Tobacco": "PBJ",
    
    # ============================================
    # ENERGY
    # ============================================
    "Oil & Gas Exploration & Production": "XOP",
    "Oil & Gas Equipment & Services": "OIH",
    "Oil & Gas Drilling": "OIH",
    "Oil & Gas Refining & Marketing": "CRAK",
    "Oil & Gas Storage & Transportation": "AMLP",
    "Integrated Oil & Gas": "XOP",
    "Coal & Consumable Fuels": "KOL",
    "Renewable Energy": "ICLN",
    "Solar": "TAN",
    "Wind": "FAN",
    
    # ============================================
    # MATERIALS
    # ============================================
    "Chemicals": "VAW",            # Vanguard Materials ETF
    "Commodity Chemicals": "VAW",  # Vanguard Materials ETF
    "Diversified Chemicals": "VAW",
    "Specialty Chemicals": "PYZ",  # Invesco Dynamic Basic Materials ETF
    "Fertilizers & Agricultural Chemicals": "MOO",
    "Industrial Gases": "FMAT",    # Fidelity MSCI Materials Index ETF
    "Metals & Mining": "XME",
    "Diversified Metals & Mining": "XME",
    "Copper": "COPX",
    "Gold": "GDX",
    "Precious Metals & Minerals": "GDX",
    "Silver": "SIL",
    "Steel": "SLX",
    "Aluminum": "XME",
    "Construction Materials": "PKB",
    "Containers & Packaging": "VAW",
    "Metal, Glass & Plastic Containers": "VAW",
    "Paper & Plastic Packaging Products & Materials": "VAW",
    "Paper & Forest Products": "WOOD",
    "Forest Products": "WOOD",
    "Paper Products": "WOOD",
    "Lumber": "WOOD",
    
    # ============================================
    # UTILITIES
    # ============================================
    "Electric Utilities": "VPU",   # Vanguard Utilities ETF
    "Multi-Utilities": "VPU",
    "Gas Utilities": "FCG",        # First Trust Natural Gas ETF
    "Water Utilities": "PHO",
    "Independent Power Producers & Energy Traders": "VPU",
    "Independent Power and Renewable Electricity Producers": "QCLN",
    "Renewable Electricity": "QCLN",
    
    # ============================================
    # REAL ESTATE
    # ============================================
    "REITs": "VNQ",
    "Diversified REITs": "VNQ",
    "Residential REITs": "REZ",
    "Retail REITs": "RTL",
    "Office REITs": "VNQ",
    "Industrial REITs": "INDS",
    "Specialized REITs": "VNQ",
    "Hotel & Resort REITs": "PEJ",
    "Health Care REITs": "IHF",
    "Data Center REITs": "SRVR",
    "Telecom Tower REITs": "SRVR",   # Infrastructure REITs - telecom towers
    "Infrastructure REITs": "SRVR",
    "Timber REITs": "WOOD",
    "Real Estate Management & Development": "VNQ",
    "Real Estate Operating Companies": "VNQ",
    "Real Estate Services": "VNQ",
}

# Default fallback ETF (S&P 500) - only used when no industry match found
DEFAULT_ETF = "SPY"

# Sector name to ETF mapping (using XL* sector ETFs)
SECTOR_NAME_TO_ETF = {
    "Energy": "XLE",
    "Materials": "XLB",
    "Industrials": "XLI",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Health Care": "XLV",
    "Financials": "XLF",
    "Information Technology": "XLK",
    "Communication Services": "XLC",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
}


def normalize_name(name: str) -> str:
    """
    Normalize sub-industry name for matching.
    
    Handles variations like "and" vs "&", extra spaces, commas, etc.
    
    Args:
        name: Sub-industry name to normalize
    
    Returns:
        Normalized lowercase name
    """
    return (
        name.lower()
        .replace(" and ", " & ")
        .replace(",", "")
        .replace("  ", " ")
        .strip()
    )


def get_etf_for_sector(sector_name: str) -> str:
    """
    Get the representative XL* ETF for a GICS sector.
    
    Args:
        sector_name: Name of the GICS sector (e.g., "Energy", "Information Technology")
    
    Returns:
        ETF ticker symbol (e.g., "XLE", "XLK")
    """
    if not sector_name:
        return DEFAULT_ETF
    
    # Direct lookup
    etf = SECTOR_NAME_TO_ETF.get(sector_name)
    if etf:
        return etf
    
    # Try case-insensitive lookup
    normalized = sector_name.strip().lower()
    for name, ticker in SECTOR_NAME_TO_ETF.items():
        if name.lower() == normalized:
            return ticker
    
    logger.warning(f"No sector ETF mapping found for '{sector_name}', using {DEFAULT_ETF}")
    return DEFAULT_ETF


def get_etf_for_subindustry(subindustry_name: str, sector_name: str = "") -> str:
    """
    Get the representative ETF for a sub-industry.
    
    PRIORITY ORDER:
    1. Official GICS_SUBINDUSTRY_ETF_MAP (by exact name match)
    2. Official GICS_SUBINDUSTRY_ETF_MAP (by normalized name match)
    3. Sector ETF fallback based on sector_name
    4. SPY as final fallback
    
    Args:
        subindustry_name: Name of the GICS sub-industry
        sector_name: Name of the GICS sector (used for sector fallback)
    
    Returns:
        ETF ticker symbol
    """
    if not subindustry_name:
        return DEFAULT_ETF
    
    # Normalize the input name
    normalized_input = normalize_name(subindustry_name)
    
    # PRIORITY 1: Try exact match in official GICS mapping
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        if entry.name.lower() == subindustry_name.lower():
            logger.debug(f"Exact match for '{subindustry_name}': {entry.primary_etf}")
            return entry.primary_etf
    
    # PRIORITY 2: Try normalized match in official GICS mapping
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        if normalize_name(entry.name) == normalized_input:
            logger.debug(f"Normalized match for '{subindustry_name}': {entry.primary_etf}")
            return entry.primary_etf
    
    # PRIORITY 3: Try partial match in official GICS mapping (for minor variations)
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        normalized_entry = normalize_name(entry.name)
        # Check if names are substantially similar
        if normalized_input in normalized_entry or normalized_entry in normalized_input:
            logger.debug(f"Partial match for '{subindustry_name}' -> '{entry.name}': {entry.primary_etf}")
            return entry.primary_etf
    
    # PRIORITY 4: Try legacy INDUSTRY_ETFS mapping (for custom/generated codes)
    for industry_key, etf in INDUSTRY_ETFS.items():
        if normalize_name(industry_key) == normalized_input:
            logger.debug(f"Legacy INDUSTRY_ETFS match for '{subindustry_name}': {etf}")
            return etf
    
    # PRIORITY 5: Try partial match in legacy INDUSTRY_ETFS
    for industry_key, etf in INDUSTRY_ETFS.items():
        normalized_key = normalize_name(industry_key)
        if normalized_key in normalized_input or normalized_input in normalized_key:
            logger.debug(f"Legacy INDUSTRY_ETFS partial match for '{subindustry_name}' -> '{industry_key}': {etf}")
            return etf
    
    # PRIORITY 6: Sector fallback
    if sector_name:
        normalized_sector = sector_name.lower().strip()
        for sector_code, etf in SECTOR_ETFS.items():
            # Check if any entry in the mapping has this sector
            for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
                if entry.sector_name.lower() == normalized_sector:
                    logger.debug(f"Sector fallback for '{subindustry_name}' ({sector_name}): {SECTOR_ETFS.get(entry.sector_code, DEFAULT_ETF)}")
                    return SECTOR_ETFS.get(entry.sector_code, DEFAULT_ETF)
    
    # PRIORITY 5: Final fallback to SPY
    logger.warning(f"No ETF mapping found for sub-industry '{subindustry_name}', using {DEFAULT_ETF}")
    return DEFAULT_ETF


def get_etf_by_gics_code(gics_code: str) -> str:
    """
    Get the representative ETF for a GICS sub-industry code.
    
    Uses the official GICS 8-digit code to find the most appropriate ETF.
    Falls back to sector ETF if sub-industry not found.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        ETF ticker symbol
    """
    return get_etf_for_gics_code(gics_code)


def get_etf_with_fallback(
    gics_code: Optional[str] = None,
    subindustry_name: Optional[str] = None,
    sector_name: Optional[str] = None
) -> str:
    """
    Get ETF using multiple fallback strategies.
    
    Priority:
    1. GICS code lookup (most accurate)
    2. Sub-industry name lookup
    3. Sector ETF fallback
    4. SPY as ultimate fallback
    
    Args:
        gics_code: Optional 8-digit GICS code
        subindustry_name: Optional sub-industry name
        sector_name: Optional sector name for fallback
    
    Returns:
        ETF ticker symbol
    """
    # Try GICS code first (most accurate)
    if gics_code and gics_code in GICS_SUBINDUSTRY_ETF_MAP:
        return GICS_SUBINDUSTRY_ETF_MAP[gics_code].primary_etf
    
    # Try name-based lookup
    if subindustry_name:
        etf = get_etf_for_subindustry(subindustry_name, sector_name or "")
        if etf != DEFAULT_ETF:
            return etf
    
    # Try sector fallback via GICS code
    if gics_code and len(gics_code) >= 2:
        sector_code = gics_code[:2]
        if sector_code in SECTOR_ETFS:
            return SECTOR_ETFS[sector_code]
    
    return DEFAULT_ETF


def get_subindustry_etf_info(gics_code: str) -> Optional[dict]:
    """
    Get complete ETF information for a GICS sub-industry.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        Dict with ETF info or None if not found
    """
    info = get_subindustry_info(gics_code)
    if info:
        return {
            "code": info.code,
            "name": info.name,
            "primary_etf": info.primary_etf,
            "alt_etf": info.alt_etf,
            "index_name": info.index_name,
            "sector_name": info.sector_name,
            "industry_name": info.industry_name,
        }
    return None


# Common ETFs that are listed on AMEX/NYSE Arca
AMEX_ETFS = {
    # Sector SPDRs
    "XLE", "XLF", "XLK", "XLV", "XLI", "XLY", "XLP", "XLB", "XLU", "XLRE", "XLC",
    # Industry SPDRs
    "XBI", "XHB", "XHE", "XHS", "XME", "XOP", "XPH", "XRT", "XSD", "XSW", "XTH", "XTN",
    "KBE", "KCE", "KIE", "KRE",
    # iShares
    "IYW", "IYZ", "IYK", "IYM", "IYT", "IYR", "IYE", "IYF", "IYG", "IYH", "IYJ", "IYC",
    "IBB", "IGV", "IHI", "IHF", "ITA", "ITB", "IAI", "IAK", "IAT", "IEO", "IEZ",
    # Vanguard
    "VGT", "VHT", "VIS", "VCR", "VDC", "VDE", "VFH", "VAW", "VNQ", "VPU", "VOX",
    # First Trust
    "FDN", "SKYY", "WCLD", "GRID", "FIW", "CIBR",
    # VanEck
    "SMH", "GDX", "GDXJ", "OIH", "XES", "MOO", "SLX", "KOL",
    # Global X
    "LIT", "COPX", "DRIV", "FINX", "SOCL", "ESPO",
    # Other popular ETFs (NYSE Arca listed)
    "SPY", "DIA", "IWM", "EFA", "EEM", "GLD", "SLV", "USO", "UNG",
    "JETS", "ARKK", "ARKG", "ARKW", "ARKF", "AMLP", "MLPA",
}

# Known NASDAQ-listed stocks/ETFs (major tech companies and NASDAQ ETFs)
NASDAQ_SYMBOLS = {
    # Major NASDAQ stocks
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "NFLX", "ADBE",
    "INTC", "CSCO", "CMCSA", "PEP", "AVGO", "COST", "TXN", "QCOM", "TMUS", "AMGN",
    "SBUX", "INTU", "ISRG", "MDLZ", "GILD", "ADI", "REGN", "VRTX", "FISV", "ATVI",
    "PYPL", "MU", "LRCX", "KLAC", "SNPS", "CDNS", "MRVL", "AMAT", "PANW", "DXCM",
    "NXPI", "CRWD", "FTNT", "ZS", "WDAY", "TEAM", "OKTA", "DDOG", "ZM", "DOCU",
    "ABNB", "DASH", "COIN", "HOOD", "RBLX", "U", "PLTR", "SNOW", "NET", "MDB",
    # NASDAQ-listed ETFs
    "QQQ", "TQQQ", "SQQQ", "PSQ", "ONEQ", "QQQM", "QQQJ",
}


@lru_cache(maxsize=2000)
def _get_exchange_from_yfinance(symbol: str) -> Optional[str]:
    """
    Fetch exchange information from yfinance (cached).
    
    Args:
        symbol: Ticker symbol
    
    Returns:
        Exchange name or None if not found
    """
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        info = ticker.info
        exchange = info.get('exchange', '')
        
        # Map yfinance exchange names to TradingView prefixes
        exchange_mapping = {
            'NYQ': 'NYSE',
            'NMS': 'NASDAQ',
            'NGM': 'NASDAQ',
            'NCM': 'NASDAQ',
            'NYS': 'NYSE',
            'ASE': 'AMEX',
            'PCX': 'AMEX',  # NYSE Arca
            'BTS': 'AMEX',  # BATS
            'NASDAQ': 'NASDAQ',
            'NYSE': 'NYSE',
        }
        
        return exchange_mapping.get(exchange, None)
    except Exception as e:
        logger.debug(f"Could not fetch exchange for {symbol}: {e}")
        return None


def get_exchange_for_symbol(symbol: str, use_yfinance_fallback: bool = False) -> str:
    """
    Determine the likely exchange for a given symbol.
    
    TradingView requires exchange prefix for accurate symbol lookup.
    
    Args:
        symbol: Ticker symbol
        use_yfinance_fallback: If True, query yfinance for unknown symbols
    
    Returns:
        Exchange prefix (NYSE, NASDAQ, AMEX, etc.)
    """
    symbol_upper = symbol.upper()
    
    # ETFs are typically on AMEX (NYSE Arca)
    if symbol_upper in AMEX_ETFS:
        return "AMEX"
    
    # Check if it's a known NASDAQ stock
    if symbol_upper in NASDAQ_SYMBOLS:
        return "NASDAQ"
    
    # ETFs with common suffixes (3-4 letter symbols starting with common ETF prefixes)
    if len(symbol_upper) <= 4 and symbol_upper.startswith(("X", "I", "V", "S", "K")):
        # Likely an ETF - use AMEX
        if symbol_upper not in NASDAQ_SYMBOLS:
            return "AMEX"
    
    # Try yfinance lookup for unknown symbols (optional, can be slow)
    if use_yfinance_fallback:
        exchange = _get_exchange_from_yfinance(symbol_upper)
        if exchange:
            return exchange
    
    # Default to NYSE for most stocks
    return "NYSE"


def get_tradingview_symbol(symbol: str, exchange: str = None) -> str:
    """
    Get the TradingView symbol.
    
    Just returns the uppercase ticker - TradingView will automatically
    resolve to the first/best match for the symbol.
    
    Args:
        symbol: Ticker symbol
        exchange: Deprecated, kept for backward compatibility
    
    Returns:
        Uppercase ticker symbol (e.g., "AAPL", "SPY")
    """
    return symbol.upper()


def get_tradingview_widget_url(symbol: str, interval: str = "W", exchange: str = None) -> str:
    """
    Generate a TradingView widget embed URL.
    
    Uses just the ticker symbol without exchange prefix - TradingView
    automatically resolves to the first/best match.
    
    Args:
        symbol: Ticker symbol to display (stock or ETF)
        interval: Chart interval (D=daily, W=weekly, M=monthly)
        exchange: Deprecated, kept for backward compatibility
    
    Returns:
        TradingView widget embed URL
    """
    # Use just the ticker - TradingView will show first match
    ticker = symbol.upper()
    
    return (
        f"https://s.tradingview.com/widgetembed/?"
        f"symbol={ticker}&"
        f"interval={interval}&"
        f"theme=dark&"
        f"style=1&"
        f"locale=en&"
        f"enable_publishing=false&"
        f"hide_top_toolbar=false&"
        f"hide_legend=false&"
        f"save_image=false&"
        f"hide_volume=false&"
        f"support_host=https%3A%2F%2Fwww.tradingview.com"
    )
