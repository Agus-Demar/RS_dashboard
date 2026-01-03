"""
ETF Mapper for GICS Sectors and Industries.

Maps GICS sectors and sub-industries to their representative ETFs
for display in the TradingView widget.

Prioritizes industry-level ETFs over sector-level ETFs for more granular analysis.

This module provides backward-compatible name-based lookups while also supporting
the official GICS 8-digit code-based mappings from the data module.
"""

from typing import Optional

# Import the comprehensive GICS code-based mapping
from src.data.gics_subindustry_etf_mapping import (
    GICS_SUBINDUSTRY_ETF_MAP,
    SECTOR_ETFS,
    get_etf_for_gics_code,
    get_alt_etf_for_gics_code,
    get_subindustry_info,
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
    "Chemicals": "XLB",
    "Commodity Chemicals": "XLB",
    "Diversified Chemicals": "XLB",
    "Specialty Chemicals": "XLB",
    "Fertilizers & Agricultural Chemicals": "MOO",
    "Industrial Gases": "XLB",
    "Metals & Mining": "XME",
    "Diversified Metals & Mining": "XME",
    "Copper": "COPX",
    "Gold": "GDX",
    "Precious Metals & Minerals": "GDX",
    "Silver": "SIL",
    "Steel": "SLX",
    "Aluminum": "XME",
    "Construction Materials": "PKB",
    "Containers & Packaging": "XLB",
    "Metal, Glass & Plastic Containers": "XLB",
    "Paper & Plastic Packaging Products & Materials": "XLB",
    "Paper & Forest Products": "WOOD",
    "Forest Products": "WOOD",
    "Paper Products": "WOOD",
    "Lumber": "WOOD",
    
    # ============================================
    # UTILITIES
    # ============================================
    "Electric Utilities": "XLU",
    "Multi-Utilities": "XLU",
    "Gas Utilities": "XLU",
    "Water Utilities": "PHO",
    "Independent Power Producers & Energy Traders": "XLU",
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
    "Timber REITs": "WOOD",
    "Real Estate Management & Development": "VNQ",
    "Real Estate Operating Companies": "VNQ",
    "Real Estate Services": "VNQ",
}

# Default fallback ETF (S&P 500) - only used when no industry match found
DEFAULT_ETF = "SPY"


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


def get_etf_for_subindustry(subindustry_name: str, sector_name: str) -> str:
    """
    Get the representative ETF for a sub-industry.
    
    Uses normalized matching to handle variations in naming conventions
    (e.g., "and" vs "&", case differences).
    
    Prioritizes industry-level matches and only falls back to SPY
    when no industry match exists.
    
    Args:
        subindustry_name: Name of the GICS sub-industry
        sector_name: Name of the GICS sector (unused, kept for API compatibility)
    
    Returns:
        ETF ticker symbol
    """
    # Normalize the input name
    normalized_input = normalize_name(subindustry_name)
    
    # Try exact normalized match first
    for industry_key, etf in INDUSTRY_ETFS.items():
        if normalize_name(industry_key) == normalized_input:
            return etf
    
    # Try partial normalized match (input contains key)
    for industry_key, etf in INDUSTRY_ETFS.items():
        normalized_key = normalize_name(industry_key)
        if normalized_key in normalized_input:
            return etf
    
    # Try reverse partial normalized match (key contains input)
    for industry_key, etf in INDUSTRY_ETFS.items():
        normalized_key = normalize_name(industry_key)
        if normalized_input in normalized_key:
            return etf
    
    # Try word-based matching (check if key words appear in input)
    input_words = set(normalized_input.split())
    for industry_key, etf in INDUSTRY_ETFS.items():
        key_words = set(normalize_name(industry_key).split())
        # If at least 2 significant words match
        common_words = input_words & key_words
        # Filter out common small words
        significant_common = {w for w in common_words if len(w) > 3}
        if len(significant_common) >= 2:
            return etf
    
    # Final fallback to SPY
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


def get_tradingview_widget_url(symbol: str, interval: str = "W") -> str:
    """
    Generate a TradingView widget embed URL.
    
    Args:
        symbol: Ticker symbol to display
        interval: Chart interval (D=daily, W=weekly, M=monthly)
    
    Returns:
        TradingView widget embed URL
    """
    return (
        f"https://s.tradingview.com/widgetembed/?"
        f"symbol={symbol}&"
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
