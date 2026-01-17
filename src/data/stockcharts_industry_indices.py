"""
StockCharts US Industry Index Symbols Mapping.

Maps GICS sub-industries to their corresponding StockCharts $DJUS industry index symbols.
These indices provide direct price data for calculating sub-industry relative strength
instead of aggregating from individual stocks.

Source: https://stockcharts.com/freecharts/industrysummary.html
Symbol Catalog: https://stockcharts.com/freecharts/catalog/?sl=do

Last Updated: January 2026
"""

from typing import Dict, NamedTuple, Optional


class IndustryIndex(NamedTuple):
    """StockCharts industry index entry."""
    symbol: str                     # $DJUS symbol (e.g., "$DJUSOL")
    name: str                       # Index name
    gics_subindustry: str           # Matching GICS sub-industry name
    gics_code: Optional[str]        # 8-digit GICS code if known
    sector: str                     # Sector name


# =============================================================================
# STOCKCHARTS INDUSTRY INDEX SYMBOLS
# These are used for direct RS calculation instead of aggregating individual stocks
# =============================================================================

STOCKCHARTS_INDUSTRY_INDICES: Dict[str, IndustryIndex] = {
    
    # =========================================================================
    # ENERGY SECTOR
    # =========================================================================
    "$DJUSOL": IndustryIndex(
        symbol="$DJUSOL",
        name="Dow Jones US Integrated Oil & Gas",
        gics_subindustry="Integrated Oil & Gas",
        gics_code="10102010",
        sector="Energy"
    ),
    "$DJUSOS": IndustryIndex(
        symbol="$DJUSOS",
        name="Dow Jones US Oil & Gas Producers",
        gics_subindustry="Oil & Gas Exploration & Production",
        gics_code="10102020",
        sector="Energy"
    ),
    "$DJUSOI": IndustryIndex(
        symbol="$DJUSOI",
        name="Dow Jones US Oil Equipment & Services",
        gics_subindustry="Oil & Gas Equipment & Services",
        gics_code="10101020",
        sector="Energy"
    ),
    "$DJUSPL": IndustryIndex(
        symbol="$DJUSPL",
        name="Dow Jones US Pipelines",
        gics_subindustry="Oil & Gas Storage & Transportation",
        gics_code="10102040",
        sector="Energy"
    ),
    
    # =========================================================================
    # MATERIALS SECTOR
    # =========================================================================
    "$DJUSAL": IndustryIndex(
        symbol="$DJUSAL",
        name="Dow Jones US Aluminum",
        gics_subindustry="Aluminum",
        gics_code="15104010",
        sector="Materials"
    ),
    "$DJUSCC": IndustryIndex(
        symbol="$DJUSCC",
        name="Dow Jones US Commodity Chemicals",
        gics_subindustry="Commodity Chemicals",
        gics_code="15101010",
        sector="Materials"
    ),
    "$DJUSCX": IndustryIndex(
        symbol="$DJUSCX",
        name="Dow Jones US Specialty Chemicals",
        gics_subindustry="Specialty Chemicals",
        gics_code="15101050",
        sector="Materials"
    ),
    "$DJUSPM": IndustryIndex(
        symbol="$DJUSPM",
        name="Dow Jones US Gold Mining",
        gics_subindustry="Gold",
        gics_code="15104030",
        sector="Materials"
    ),
    "$DJUSMG": IndustryIndex(
        symbol="$DJUSMG",
        name="Dow Jones US General Mining",
        gics_subindustry="Diversified Metals & Mining",
        gics_code="15104020",
        sector="Materials"
    ),
    "$DJUSST": IndustryIndex(
        symbol="$DJUSST",
        name="Dow Jones US Steel",
        gics_subindustry="Steel",
        gics_code="15104050",
        sector="Materials"
    ),
    "$DJUSNF": IndustryIndex(
        symbol="$DJUSNF",
        name="Dow Jones US Nonferrous Metals",
        gics_subindustry="Copper",
        gics_code="15104025",
        sector="Materials"
    ),
    "$DJUSBD": IndustryIndex(
        symbol="$DJUSBD",
        name="Dow Jones US Building Materials & Fixtures",
        gics_subindustry="Construction Materials",
        gics_code="15102010",
        sector="Materials"
    ),
    "$DJUSCN": IndustryIndex(
        symbol="$DJUSCN",
        name="Dow Jones US Containers & Packaging",
        gics_subindustry="Metal, Glass & Plastic Containers",
        gics_code="15103010",
        sector="Materials"
    ),
    "$DJUSFR": IndustryIndex(
        symbol="$DJUSFR",
        name="Dow Jones US Forestry & Paper",
        gics_subindustry="Paper Products",
        gics_code="15105020",
        sector="Materials"
    ),
    
    # =========================================================================
    # INDUSTRIALS SECTOR
    # =========================================================================
    "$DJUSAP": IndustryIndex(
        symbol="$DJUSAP",
        name="Dow Jones US Aerospace",
        gics_subindustry="Aerospace & Defense",
        gics_code="20101010",
        sector="Industrials"
    ),
    "$DJUSDF": IndustryIndex(
        symbol="$DJUSDF",
        name="Dow Jones US Defense",
        gics_subindustry="Aerospace & Defense",
        gics_code="20101010",
        sector="Industrials"
    ),
    "$DJUSAR": IndustryIndex(
        symbol="$DJUSAR",
        name="Dow Jones US Airlines",
        gics_subindustry="Passenger Airlines",
        gics_code="20302010",
        sector="Industrials"
    ),
    "$DJUSRR": IndustryIndex(
        symbol="$DJUSRR",
        name="Dow Jones US Railroads",
        gics_subindustry="Rail Transportation",
        gics_code="20304010",
        sector="Industrials"
    ),
    "$DJUSTK": IndustryIndex(
        symbol="$DJUSTK",
        name="Dow Jones US Trucking",
        gics_subindustry="Cargo Ground Transportation",
        gics_code="20304020",
        sector="Industrials"
    ),
    "$DJUSAF": IndustryIndex(
        symbol="$DJUSAF",
        name="Dow Jones US Delivery Services",
        gics_subindustry="Air Freight & Logistics",
        gics_code="20301010",
        sector="Industrials"
    ),
    "$DJUSFE": IndustryIndex(
        symbol="$DJUSFE",
        name="Dow Jones US Industrial Machinery",
        gics_subindustry="Industrial Machinery & Supplies & Components",
        gics_code="20106020",
        sector="Industrials"
    ),
    "$DJUSHV": IndustryIndex(
        symbol="$DJUSHV",
        name="Dow Jones US Heavy Construction",
        gics_subindustry="Construction & Engineering",
        gics_code="20103010",
        sector="Industrials"
    ),
    "$DJUSID": IndustryIndex(
        symbol="$DJUSID",
        name="Dow Jones US Diversified Industrials",
        gics_subindustry="Industrial Conglomerates",
        gics_code="20105010",
        sector="Industrials"
    ),
    "$DJUSHR": IndustryIndex(
        symbol="$DJUSHR",
        name="Dow Jones US Commercial Vehicles & Trucks",
        gics_subindustry="Construction Machinery & Heavy Transportation Equipment",
        gics_code="20106010",
        sector="Industrials"
    ),
    "$DJUSDS": IndustryIndex(
        symbol="$DJUSDS",
        name="Dow Jones US Business Support Services",
        gics_subindustry="Diversified Support Services",
        gics_code="20201070",
        sector="Industrials"
    ),
    "$DJUSIV": IndustryIndex(
        symbol="$DJUSIV",
        name="Dow Jones US Industrial Suppliers",
        gics_subindustry="Trading Companies & Distributors",
        gics_code="20107010",
        sector="Industrials"
    ),
    "$DJUSWT": IndustryIndex(
        symbol="$DJUSWT",
        name="Dow Jones US Waste & Disposal Services",
        gics_subindustry="Environmental & Facilities Services",
        gics_code="20201050",
        sector="Industrials"
    ),
    
    # =========================================================================
    # CONSUMER DISCRETIONARY SECTOR
    # =========================================================================
    "$DJUSAU": IndustryIndex(
        symbol="$DJUSAU",
        name="Dow Jones US Automobiles",
        gics_subindustry="Automobile Manufacturers",
        gics_code="25102010",
        sector="Consumer Discretionary"
    ),
    "$DJUSAT": IndustryIndex(
        symbol="$DJUSAT",
        name="Dow Jones US Auto Parts",
        gics_subindustry="Automotive Parts & Equipment",
        gics_code="25101010",
        sector="Consumer Discretionary"
    ),
    "$DJUSTR": IndustryIndex(
        symbol="$DJUSTR",
        name="Dow Jones US Tires",
        gics_subindustry="Tires & Rubber",
        gics_code="25101020",
        sector="Consumer Discretionary"
    ),
    "$DJUSHB": IndustryIndex(
        symbol="$DJUSHB",
        name="Dow Jones US Home Construction",
        gics_subindustry="Homebuilding",
        gics_code="25201030",
        sector="Consumer Discretionary"
    ),
    "$DJUSFH": IndustryIndex(
        symbol="$DJUSFH",
        name="Dow Jones US Furnishings",
        gics_subindustry="Home Furnishings",
        gics_code="25201020",
        sector="Consumer Discretionary"
    ),
    "$DJUSRP": IndustryIndex(
        symbol="$DJUSRP",
        name="Dow Jones US Recreational Products",
        gics_subindustry="Leisure Products",
        gics_code="25202010",
        sector="Consumer Discretionary"
    ),
    "$DJUSCA": IndustryIndex(
        symbol="$DJUSCA",
        name="Dow Jones US Gambling",
        gics_subindustry="Casinos & Gaming",
        gics_code="25301010",
        sector="Consumer Discretionary"
    ),
    "$DJUSHL": IndustryIndex(
        symbol="$DJUSHL",
        name="Dow Jones US Hotels",
        gics_subindustry="Hotels, Resorts & Cruise Lines",
        gics_code="25301020",
        sector="Consumer Discretionary"
    ),
    "$DJUSRU": IndustryIndex(
        symbol="$DJUSRU",
        name="Dow Jones US Restaurants & Bars",
        gics_subindustry="Restaurants",
        gics_code="25301040",
        sector="Consumer Discretionary"
    ),
    "$DJUSRA": IndustryIndex(
        symbol="$DJUSRA",
        name="Dow Jones US Apparel Retailers",
        gics_subindustry="Apparel Retail",
        gics_code="25503010",
        sector="Consumer Discretionary"
    ),
    "$DJUSHR": IndustryIndex(
        symbol="$DJUSHIR",
        name="Dow Jones US Home Improvement Retailers",
        gics_subindustry="Home Improvement Retail",
        gics_code="25503030",
        sector="Consumer Discretionary"
    ),
    "$DJUSRT": IndustryIndex(
        symbol="$DJUSRT",
        name="Dow Jones US Retailers",
        gics_subindustry="Other Specialty Retail",
        gics_code="25503040",
        sector="Consumer Discretionary"
    ),
    "$DJUSRB": IndustryIndex(
        symbol="$DJUSRB",
        name="Dow Jones US Broadline Retailers",
        gics_subindustry="Broadline Retail",
        gics_code="25502010",
        sector="Consumer Discretionary"
    ),
    "$DJUSCF": IndustryIndex(
        symbol="$DJUSCF",
        name="Dow Jones US Clothing & Accessories",
        gics_subindustry="Apparel, Accessories & Luxury Goods",
        gics_code="25203010",
        sector="Consumer Discretionary"
    ),
    "$DJUSFT": IndustryIndex(
        symbol="$DJUSFT",
        name="Dow Jones US Footwear",
        gics_subindustry="Footwear",
        gics_code="25203020",
        sector="Consumer Discretionary"
    ),
    
    # =========================================================================
    # CONSUMER STAPLES SECTOR
    # =========================================================================
    "$DJUSFP": IndustryIndex(
        symbol="$DJUSFP",
        name="Dow Jones US Food Producers",
        gics_subindustry="Packaged Foods & Meats",
        gics_code="30202030",
        sector="Consumer Staples"
    ),
    "$DJUSFB": IndustryIndex(
        symbol="$DJUSFB",
        name="Dow Jones US Food & Beverage",
        gics_subindustry="Soft Drinks & Non-alcoholic Beverages",
        gics_code="30201030",
        sector="Consumer Staples"
    ),
    "$DJUSDB": IndustryIndex(
        symbol="$DJUSDB",
        name="Dow Jones US Brewers",
        gics_subindustry="Distillers & Vintners",
        gics_code="30201020",
        sector="Consumer Staples"
    ),
    "$DJUSHN": IndustryIndex(
        symbol="$DJUSHN",
        name="Dow Jones US Household Goods - Nondurables",
        gics_subindustry="Household Products",
        gics_code="30301010",
        sector="Consumer Staples"
    ),
    "$DJUSCM": IndustryIndex(
        symbol="$DJUSCM",
        name="Dow Jones US Personal Products",
        gics_subindustry="Personal Care Products",
        gics_code="30302010",
        sector="Consumer Staples"
    ),
    "$DJUSTB": IndustryIndex(
        symbol="$DJUSTB",
        name="Dow Jones US Tobacco",
        gics_subindustry="Tobacco",
        gics_code="30203010",
        sector="Consumer Staples"
    ),
    "$DJUSFD": IndustryIndex(
        symbol="$DJUSFD",
        name="Dow Jones US Food & Drug Retailers",
        gics_subindustry="Food Retail",
        gics_code="30101030",
        sector="Consumer Staples"
    ),
    "$DJUSRD": IndustryIndex(
        symbol="$DJUSRD",
        name="Dow Jones US Drug Retailers",
        gics_subindustry="Drug Retail",
        gics_code="30101010",
        sector="Consumer Staples"
    ),
    
    # =========================================================================
    # HEALTH CARE SECTOR
    # =========================================================================
    "$DJUSBT": IndustryIndex(
        symbol="$DJUSBT",
        name="Dow Jones US Biotechnology",
        gics_subindustry="Biotechnology",
        gics_code="35201010",
        sector="Health Care"
    ),
    "$DJUSPR": IndustryIndex(
        symbol="$DJUSPR",
        name="Dow Jones US Pharmaceuticals",
        gics_subindustry="Pharmaceuticals",
        gics_code="35202010",
        sector="Health Care"
    ),
    "$DJUSAM": IndustryIndex(
        symbol="$DJUSAM",
        name="Dow Jones US Medical Equipment",
        gics_subindustry="Health Care Equipment",
        gics_code="35101010",
        sector="Health Care"
    ),
    "$DJUSMS": IndustryIndex(
        symbol="$DJUSMS",
        name="Dow Jones US Medical Supplies",
        gics_subindustry="Health Care Supplies",
        gics_code="35101020",
        sector="Health Care"
    ),
    "$DJUSHP": IndustryIndex(
        symbol="$DJUSHP",
        name="Dow Jones US Health Care Providers",
        gics_subindustry="Health Care Services",
        gics_code="35102015",
        sector="Health Care"
    ),
    "$DJUSHM": IndustryIndex(
        symbol="$DJUSHM",
        name="Dow Jones US Managed Health Care",
        gics_subindustry="Managed Health Care",
        gics_code="35102030",
        sector="Health Care"
    ),
    
    # =========================================================================
    # FINANCIALS SECTOR
    # =========================================================================
    "$DJUSBK": IndustryIndex(
        symbol="$DJUSBK",
        name="Dow Jones US Banks",
        gics_subindustry="Diversified Banks",
        gics_code="40101010",
        sector="Financials"
    ),
    "$DJUSSB": IndustryIndex(
        symbol="$DJUSSB",
        name="Dow Jones US Regional Banks",
        gics_subindustry="Regional Banks",
        gics_code="40101015",
        sector="Financials"
    ),
    "$DJUSFA": IndustryIndex(
        symbol="$DJUSFA",
        name="Dow Jones US Financial Administration",
        gics_subindustry="Financial Exchanges & Data",
        gics_code="40203040",
        sector="Financials"
    ),
    "$DJUSFI": IndustryIndex(
        symbol="$DJUSFI",
        name="Dow Jones US Investment Services",
        gics_subindustry="Investment Banking & Brokerage",
        gics_code="40203020",
        sector="Financials"
    ),
    "$DJUSAM": IndustryIndex(
        symbol="$DJUSAS",
        name="Dow Jones US Asset Managers",
        gics_subindustry="Asset Management & Custody Banks",
        gics_code="40203010",
        sector="Financials"
    ),
    "$DJUSCF": IndustryIndex(
        symbol="$DJUSSC",
        name="Dow Jones US Consumer Finance",
        gics_subindustry="Consumer Finance",
        gics_code="40202010",
        sector="Financials"
    ),
    "$DJUSIL": IndustryIndex(
        symbol="$DJUSIL",
        name="Dow Jones US Life Insurance",
        gics_subindustry="Life & Health Insurance",
        gics_code="40301020",
        sector="Financials"
    ),
    "$DJUSIP": IndustryIndex(
        symbol="$DJUSIP",
        name="Dow Jones US Property & Casualty Insurance",
        gics_subindustry="Property & Casualty Insurance",
        gics_code="40301040",
        sector="Financials"
    ),
    "$DJUSIF": IndustryIndex(
        symbol="$DJUSIF",
        name="Dow Jones US Full Line Insurance",
        gics_subindustry="Multi-line Insurance",
        gics_code="40301030",
        sector="Financials"
    ),
    "$DJUSIB": IndustryIndex(
        symbol="$DJUSIB",
        name="Dow Jones US Insurance Brokers",
        gics_subindustry="Insurance Brokers",
        gics_code="40301010",
        sector="Financials"
    ),
    
    # =========================================================================
    # INFORMATION TECHNOLOGY SECTOR
    # =========================================================================
    "$DJUSSW": IndustryIndex(
        symbol="$DJUSSW",
        name="Dow Jones US Software",
        gics_subindustry="Application Software",
        gics_code="45103010",
        sector="Information Technology"
    ),
    "$DJUSDV": IndustryIndex(
        symbol="$DJUSDV",
        name="Dow Jones US Computer Services",
        gics_subindustry="IT Consulting & Other Services",
        gics_code="45102010",
        sector="Information Technology"
    ),
    "$DJUSCR": IndustryIndex(
        symbol="$DJUSCR",
        name="Dow Jones US Computer Hardware",
        gics_subindustry="Technology Hardware, Storage & Peripherals",
        gics_code="45202010",
        sector="Information Technology"
    ),
    "$DJUSSC": IndustryIndex(
        symbol="$DJUSSC",
        name="Dow Jones US Semiconductors",
        gics_subindustry="Semiconductors",
        gics_code="45301020",
        sector="Information Technology"
    ),
    "$DJUSSQ": IndustryIndex(
        symbol="$DJUSSQ",
        name="Dow Jones US Semiconductor Equipment",
        gics_subindustry="Semiconductor Materials & Equipment",
        gics_code="45301010",
        sector="Information Technology"
    ),
    "$DJUSAI": IndustryIndex(
        symbol="$DJUSAI",
        name="Dow Jones US Electrical Components & Equipment",
        gics_subindustry="Electronic Components",
        gics_code="45203015",
        sector="Information Technology"
    ),
    "$DJUSTQ": IndustryIndex(
        symbol="$DJUSTQ",
        name="Dow Jones US Telecom Equipment",
        gics_subindustry="Communications Equipment",
        gics_code="45201010",
        sector="Information Technology"
    ),
    
    # =========================================================================
    # COMMUNICATION SERVICES SECTOR
    # =========================================================================
    "$DJUSNS": IndustryIndex(
        symbol="$DJUSNS",
        name="Dow Jones US Internet",
        gics_subindustry="Interactive Media & Services",
        gics_code="50203010",
        sector="Communication Services"
    ),
    "$DJUSBC": IndustryIndex(
        symbol="$DJUSBC",
        name="Dow Jones US Broadcasting & Entertainment",
        gics_subindustry="Movies & Entertainment",
        gics_code="50202010",
        sector="Communication Services"
    ),
    "$DJUSAV": IndustryIndex(
        symbol="$DJUSAV",
        name="Dow Jones US Media Agencies",
        gics_subindustry="Advertising",
        gics_code="50201010",
        sector="Communication Services"
    ),
    "$DJUSWC": IndustryIndex(
        symbol="$DJUSWC",
        name="Dow Jones US Wireless Telecommunications",
        gics_subindustry="Wireless Telecommunication Services",
        gics_code="50102010",
        sector="Communication Services"
    ),
    "$DJUSFC": IndustryIndex(
        symbol="$DJUSFC",
        name="Dow Jones US Fixed-Line Telecommunications",
        gics_subindustry="Integrated Telecommunication Services",
        gics_code="50101020",
        sector="Communication Services"
    ),
    "$DJUSPB": IndustryIndex(
        symbol="$DJUSPB",
        name="Dow Jones US Publishing",
        gics_subindustry="Publishing",
        gics_code="50201040",
        sector="Communication Services"
    ),
    "$DJUSCB": IndustryIndex(
        symbol="$DJUSCB",
        name="Dow Jones US Cable Television",
        gics_subindustry="Cable & Satellite",
        gics_code="50201030",
        sector="Communication Services"
    ),
    
    # =========================================================================
    # UTILITIES SECTOR
    # =========================================================================
    "$DJUSVE": IndustryIndex(
        symbol="$DJUSVE",
        name="Dow Jones US Conventional Electricity",
        gics_subindustry="Electric Utilities",
        gics_code="55101010",
        sector="Utilities"
    ),
    "$DJUSGU": IndustryIndex(
        symbol="$DJUSGU",
        name="Dow Jones US Gas Utilities",
        gics_subindustry="Gas Utilities",
        gics_code="55102010",
        sector="Utilities"
    ),
    "$DJUSMU": IndustryIndex(
        symbol="$DJUSMU",
        name="Dow Jones US Multi-Utilities",
        gics_subindustry="Multi-Utilities",
        gics_code="55103010",
        sector="Utilities"
    ),
    "$DJUSWU": IndustryIndex(
        symbol="$DJUSWU",
        name="Dow Jones US Water Utilities",
        gics_subindustry="Water Utilities",
        gics_code="55104010",
        sector="Utilities"
    ),
    
    # =========================================================================
    # REAL ESTATE SECTOR
    # =========================================================================
    "$DJUSRL": IndustryIndex(
        symbol="$DJUSRL",
        name="Dow Jones US Real Estate Investment Trusts",
        gics_subindustry="Diversified REITs",
        gics_code="60101010",
        sector="Real Estate"
    ),
    "$DJUSIO": IndustryIndex(
        symbol="$DJUSIO",
        name="Dow Jones US Industrial & Office REITs",
        gics_subindustry="Industrial REITs",
        gics_code="60102510",
        sector="Real Estate"
    ),
    "$DJUSRR": IndustryIndex(
        symbol="$DJUSRK",
        name="Dow Jones US Retail REITs",
        gics_subindustry="Retail REITs",
        gics_code="60107010",
        sector="Real Estate"
    ),
    "$DJUSRS": IndustryIndex(
        symbol="$DJUSRS",
        name="Dow Jones US Residential REITs",
        gics_subindustry="Multi-Family Residential REITs",
        gics_code="60106010",
        sector="Real Estate"
    ),
    "$DJUSHT": IndustryIndex(
        symbol="$DJUSHT",
        name="Dow Jones US Hotel & Lodging REITs",
        gics_subindustry="Hotel & Resort REITs",
        gics_code="60103010",
        sector="Real Estate"
    ),
    "$DJUSES": IndustryIndex(
        symbol="$DJUSES",
        name="Dow Jones US Real Estate Services",
        gics_subindustry="Real Estate Services",
        gics_code="60201040",
        sector="Real Estate"
    ),
    "$DJUSRH": IndustryIndex(
        symbol="$DJUSRH",
        name="Dow Jones US Real Estate Holding & Development",
        gics_subindustry="Real Estate Development",
        gics_code="60201030",
        sector="Real Estate"
    ),
}


# =============================================================================
# MAPPING FROM GICS SUB-INDUSTRY NAME TO STOCKCHARTS SYMBOL
# =============================================================================

def get_industry_index_by_subindustry(subindustry_name: str) -> Optional[str]:
    """
    Get the StockCharts industry index symbol for a GICS sub-industry.
    
    Args:
        subindustry_name: GICS sub-industry name
    
    Returns:
        StockCharts symbol (e.g., "$DJUSOL") or None if not found
    """
    normalized = subindustry_name.lower().strip()
    
    for symbol, index in STOCKCHARTS_INDUSTRY_INDICES.items():
        if index.gics_subindustry.lower() == normalized:
            return symbol
    
    return None


def get_industry_index_by_gics_code(gics_code: str) -> Optional[str]:
    """
    Get the StockCharts industry index symbol for a GICS code.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        StockCharts symbol or None if not found
    """
    for symbol, index in STOCKCHARTS_INDUSTRY_INDICES.items():
        if index.gics_code == gics_code:
            return symbol
    
    return None


def get_all_industry_indices() -> Dict[str, IndustryIndex]:
    """Get all StockCharts industry indices."""
    return STOCKCHARTS_INDUSTRY_INDICES.copy()


def get_covered_subindustries() -> list:
    """Get list of GICS sub-industries that have StockCharts index coverage."""
    return [index.gics_subindustry for index in STOCKCHARTS_INDUSTRY_INDICES.values()]


def get_subindustry_to_symbol_map() -> Dict[str, str]:
    """
    Get mapping from GICS sub-industry name to StockCharts symbol.
    
    Returns:
        Dict mapping sub-industry name to $DJUS symbol
    """
    return {
        index.gics_subindustry: symbol 
        for symbol, index in STOCKCHARTS_INDUSTRY_INDICES.items()
    }
