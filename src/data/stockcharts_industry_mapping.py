"""
StockCharts Industry to ETF/Index Mapping.

Industry classification based on StockCharts.com sector drill-down structure.
Each industry is mapped to its most representative ETF for RS calculations.

Code Format: SSIIXX
- SS: Sector code (2 digits, aligned with S&P/GICS standards)
- II: Industry number within sector (2 digits, 01-99)
- XX: Reserved for sub-industry expansion (00 by default)

PRIORITY SYSTEM:
1. Industry-specific ETF (e.g., XBI for Biotechnology)
2. Thematic ETF closely matching the industry
3. Sector ETF as fallback (marked with is_sector_fallback=True)

Sources:
- Industry structure: StockCharts.com Sector Drill-Down
- SPDR Select Industry ETFs: https://www.ssga.com
- iShares Sector & Industry ETFs: https://www.ishares.com
- VanEck Industry ETFs: https://www.vaneck.com
- First Trust Thematic ETFs: https://www.ftportfolios.com
- Global X Thematic ETFs: https://www.globalxetfs.com

Last Updated: January 2026
"""

from typing import Dict, NamedTuple, Optional, List


class IndustryETF(NamedTuple):
    """Industry ETF mapping entry."""
    code: str                    # 6-digit industry code (SSIIXX)
    name: str                    # Industry name from StockCharts
    sector_code: str             # 2-digit sector code
    sector_name: str             # Sector name
    primary_etf: str             # Primary ETF ticker for RS calculation
    alt_etf: Optional[str]       # Alternative ETF (if available)
    index_name: str              # Related index name
    is_sector_fallback: bool = False  # True if using broad sector ETF


# =============================================================================
# SECTOR ETF MAPPINGS (Fallbacks)
# =============================================================================

SECTOR_ETFS: Dict[str, str] = {
    "10": "XLE",    # Energy Select Sector SPDR
    "15": "XLB",    # Materials Select Sector SPDR
    "20": "XLI",    # Industrial Select Sector SPDR
    "25": "XLY",    # Consumer Discretionary Select Sector SPDR
    "30": "XLP",    # Consumer Staples Select Sector SPDR
    "35": "XLV",    # Health Care Select Sector SPDR
    "40": "XLF",    # Financial Select Sector SPDR
    "45": "XLK",    # Technology Select Sector SPDR
    "50": "XLC",    # Communication Services Select Sector SPDR
    "55": "XLU",    # Utilities Select Sector SPDR
    "60": "XLRE",   # Real Estate Select Sector SPDR
}

SECTOR_NAMES: Dict[str, str] = {
    "10": "Energy",
    "15": "Materials",
    "20": "Industrials",
    "25": "Consumer Discretionary",
    "30": "Consumer Staples",
    "35": "Health Care",
    "40": "Financials",
    "45": "Technology",
    "50": "Communication Services",
    "55": "Utilities",
    "60": "Real Estate",
}


# =============================================================================
# STOCKCHARTS INDUSTRY ETF MAPPINGS
# =============================================================================

INDUSTRY_ETF_MAP: Dict[str, IndustryETF] = {
    
    # =========================================================================
    # SECTOR 10: ENERGY
    # =========================================================================
    
    "100100": IndustryETF(
        code="100100",
        name="Coal",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XLE",      # Energy Select Sector SPDR (KOL delisted)
        alt_etf=None,
        index_name="MVIS Global Coal Index",
        is_sector_fallback=True
    ),    "100300": IndustryETF(
        code="100300",
        name="Oil & Gas - E&P",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XOP",      # SPDR S&P Oil & Gas E&P ETF
        alt_etf="IEO",
        index_name="S&P Oil & Gas Exploration & Production Select Industry Index"
    ),
    "100400": IndustryETF(
        code="100400",
        name="Oil & Gas - Equipment & Services",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XES",      # SPDR S&P Oil & Gas Equipment & Services ETF
        alt_etf="IEZ",
        index_name="S&P Oil & Gas Equipment & Services Select Industry Index"
    ),
    "100500": IndustryETF(
        code="100500",
        name="Oil & Gas - Integrated",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XLE",      # Energy Select Sector SPDR (integrated majors)
        alt_etf="VDE",
        index_name="Energy Select Sector Index",
        is_sector_fallback=True
    ),
    "100600": IndustryETF(
        code="100600",
        name="Oil & Gas - Pipelines",
        sector_code="10",
        sector_name="Energy",
        primary_etf="AMLP",     # Alerian MLP ETF
        alt_etf="MLPA",
        index_name="Alerian MLP Infrastructure Index"
    ),    
    # =========================================================================
    # SECTOR 15: MATERIALS
    # =========================================================================
    
    "150100": IndustryETF(
        code="150100",
        name="Aluminum",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XME",      # SPDR S&P Metals & Mining ETF
        alt_etf="PICK",
        index_name="S&P Metals & Mining Select Industry Index"
    ),    "150300": IndustryETF(
        code="150300",
        name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",      # Materials Select Sector SPDR
        alt_etf="VAW",
        index_name="Materials Select Sector Index",
        is_sector_fallback=True
    ),
    "150400": IndustryETF(
        code="150400",
        name="Containers & Packaging",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",      # Materials Select Sector SPDR
        alt_etf="IYM",
        index_name="Materials Select Sector Index",
        is_sector_fallback=True
    ),    "150700": IndustryETF(
        code="150700",
        name="Gold",
        sector_code="15",
        sector_name="Materials",
        primary_etf="GDX",      # VanEck Gold Miners ETF
        alt_etf="GDXJ",
        index_name="NYSE Arca Gold Miners Index"
    ),
    "150800": IndustryETF(
        code="150800",
        name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XME",      # SPDR S&P Metals & Mining ETF
        alt_etf="PICK",
        index_name="S&P Metals & Mining Select Industry Index"
    ),
    "150900": IndustryETF(
        code="150900",
        name="Paper & Forest Products",
        sector_code="15",
        sector_name="Materials",
        primary_etf="WOOD",     # iShares Global Timber & Forestry ETF
        alt_etf="CUT",
        index_name="S&P Global Timber & Forestry Index"
    ),    "151100": IndustryETF(
        code="151100",
        name="Specialty Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",      # Materials Select Sector SPDR
        alt_etf="VAW",
        index_name="Materials Select Sector Index",
        is_sector_fallback=True
    ),
    "151200": IndustryETF(
        code="151200",
        name="Steel",
        sector_code="15",
        sector_name="Materials",
        primary_etf="SLX",      # VanEck Steel ETF
        alt_etf="XME",
        index_name="NYSE Arca Steel Index"
    ),
    
    # =========================================================================
    # SECTOR 20: INDUSTRIALS
    # =========================================================================
    
    "200100": IndustryETF(
        code="200100",
        name="Aerospace",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="ITA",      # iShares U.S. Aerospace & Defense ETF
        alt_etf="XAR",
        index_name="Dow Jones U.S. Select Aerospace & Defense Index"
    ),
    "200200": IndustryETF(
        code="200200",
        name="Air Freight",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="IYT",      # iShares U.S. Transportation ETF
        alt_etf="XTN",
        index_name="Dow Jones U.S. Select Transportation Index"
    ),
    "200300": IndustryETF(
        code="200300",
        name="Airlines",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="JETS",     # U.S. Global Jets ETF
        alt_etf="IYT",
        index_name="U.S. Global Jets Index"
    ),
    "200400": IndustryETF(
        code="200400",
        name="Building Products",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XHB",      # SPDR S&P Homebuilders ETF
        alt_etf="ITB",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "200500": IndustryETF(
        code="200500",
        name="Business Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",      # Industrial Select Sector SPDR
        alt_etf="VIS",
        index_name="Industrial Select Sector Index",
        is_sector_fallback=True
    ),    "200700": IndustryETF(
        code="200700",
        name="Commercial Vehicles",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",      # Industrial Select Sector SPDR
        alt_etf="PAVE",
        index_name="Industrial Select Sector Index",
        is_sector_fallback=True
    ),
    "200800": IndustryETF(
        code="200800",
        name="Conglomerates",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",      # Industrial Select Sector SPDR
        alt_etf="VIS",
        index_name="Industrial Select Sector Index",
        is_sector_fallback=True
    ),    "201000": IndustryETF(
        code="201000",
        name="Defense",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="ITA",      # iShares U.S. Aerospace & Defense ETF
        alt_etf="XAR",
        index_name="Dow Jones U.S. Select Aerospace & Defense Index"
    ),    "201200": IndustryETF(
        code="201200",
        name="Engineering & Construction",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PAVE",     # Global X U.S. Infrastructure Development ETF
        alt_etf="PKB",
        index_name="Indxx U.S. Infrastructure Development Index"
    ),    "201500": IndustryETF(
        code="201500",
        name="Heavy Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PAVE",     # Global X U.S. Infrastructure Development ETF
        alt_etf="XLI",
        index_name="Indxx U.S. Infrastructure Development Index"
    ),
    "201600": IndustryETF(
        code="201600",
        name="Industrial Distribution",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",      # Industrial Select Sector SPDR
        alt_etf="VIS",
        index_name="Industrial Select Sector Index",
        is_sector_fallback=True
    ),
    "201700": IndustryETF(
        code="201700",
        name="Marine Shipping",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SEA",      # U.S. Global Sea to Sky Cargo ETF
        alt_etf="IYT",
        index_name="U.S. Global Sea to Sky Cargo Index"
    ),    "201900": IndustryETF(
        code="201900",
        name="Railroads",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="IYT",      # iShares U.S. Transportation ETF
        alt_etf="XTN",
        index_name="Dow Jones U.S. Select Transportation Index"
    ),    "202100": IndustryETF(
        code="202100",
        name="Staffing",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",      # Industrial Select Sector SPDR
        alt_etf="VIS",
        index_name="Industrial Select Sector Index",
        is_sector_fallback=True
    ),
    "202200": IndustryETF(
        code="202200",
        name="Trucking",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="IYT",      # iShares U.S. Transportation ETF
        alt_etf="XTN",
        index_name="Dow Jones U.S. Select Transportation Index"
    ),
    "202300": IndustryETF(
        code="202300",
        name="Waste Management",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="EVX",      # VanEck Environmental Services ETF
        alt_etf="XLI",
        index_name="NYSE Arca Environmental Services Index"
    ),
    
    # =========================================================================
    # SECTOR 25: CONSUMER DISCRETIONARY
    # =========================================================================
    
    "250100": IndustryETF(
        code="250100",
        name="Auto Parts",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",     # First Trust S-Network Electric & Future Vehicle Ecosystem ETF
        alt_etf="XLY",
        index_name="S-Network Electric & Future Vehicle Ecosystem Index"
    ),
    "250200": IndustryETF(
        code="250200",
        name="Automobiles",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",     # First Trust S-Network Electric & Future Vehicle Ecosystem ETF
        alt_etf="XLY",
        index_name="S-Network Electric & Future Vehicle Ecosystem Index"
    ),
    "250300": IndustryETF(
        code="250300",
        name="Casinos & Gaming",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="BJK",      # VanEck Gaming ETF
        alt_etf="BETZ",
        index_name="MVIS Global Gaming Index"
    ),    "250600": IndustryETF(
        code="250600",
        name="Footwear",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "250700": IndustryETF(
        code="250700",
        name="Furnishings",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",      # SPDR S&P Homebuilders ETF
        alt_etf="XLY",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "250800": IndustryETF(
        code="250800",
        name="General Merchandise",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="RTH",
        index_name="S&P Retail Select Industry Index"
    ),
    "250900": IndustryETF(
        code="250900",
        name="Home Improvement",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",      # SPDR S&P Homebuilders ETF
        alt_etf="ITB",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "251000": IndustryETF(
        code="251000",
        name="Homebuilders",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",      # SPDR S&P Homebuilders ETF
        alt_etf="ITB",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "251100": IndustryETF(
        code="251100",
        name="Hotels & Motels",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="BEDZ",     # AdvisorShares Hotel ETF
        alt_etf="PEJ",
        index_name="AdvisorShares Hotel Index"
    ),    "251300": IndustryETF(
        code="251300",
        name="Leisure Products",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",      # Invesco Leisure and Entertainment ETF
        alt_etf="XLY",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),
    "251400": IndustryETF(
        code="251400",
        name="Recreational Services",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",      # Invesco Leisure and Entertainment ETF
        alt_etf="XLY",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),    "251600": IndustryETF(
        code="251600",
        name="Restaurants",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="EATZ",     # AdvisorShares Restaurant ETF
        alt_etf="PBJ",
        index_name="AdvisorShares Restaurant Index"
    ),
    "251700": IndustryETF(
        code="251700",
        name="Retail Apparel",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="RTH",
        index_name="S&P Retail Select Industry Index"
    ),
    "251800": IndustryETF(
        code="251800",
        name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="RTH",
        index_name="S&P Retail Select Industry Index"
    ),
    "251900": IndustryETF(
        code="251900",
        name="Textiles & Apparel",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "252000": IndustryETF(
        code="252000",
        name="Tires",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XLY",      # Consumer Discretionary Select Sector SPDR
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index",
        is_sector_fallback=True
    ),
    "252100": IndustryETF(
        code="252100",
        name="Toys",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XLY",      # Consumer Discretionary Select Sector SPDR
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index",
        is_sector_fallback=True
    ),
    
    # =========================================================================
    # SECTOR 30: CONSUMER STAPLES
    # =========================================================================
    
    "300100": IndustryETF(
        code="300100",
        name="Beverages: Alcoholic",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",      # Invesco Food & Beverage ETF
        alt_etf="XLP",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "300200": IndustryETF(
        code="300200",
        name="Beverages: Non-Alcoholic",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",      # Invesco Food & Beverage ETF
        alt_etf="XLP",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "300300": IndustryETF(
        code="300300",
        name="Drug Retailers",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XRT",      # SPDR S&P Retail ETF
        alt_etf="XLP",
        index_name="S&P Retail Select Industry Index"
    ),
    "300400": IndustryETF(
        code="300400",
        name="Food Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",      # Invesco Food & Beverage ETF
        alt_etf="VDC",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "300500": IndustryETF(
        code="300500",
        name="Food Retailers",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",      # Consumer Staples Select Sector SPDR
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index",
        is_sector_fallback=True
    ),
    "300600": IndustryETF(
        code="300600",
        name="Household Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",      # Consumer Staples Select Sector SPDR
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index",
        is_sector_fallback=True
    ),
    "300700": IndustryETF(
        code="300700",
        name="Personal Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",      # Consumer Staples Select Sector SPDR
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index",
        is_sector_fallback=True
    ),
    "300800": IndustryETF(
        code="300800",
        name="Tobacco",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",      # Consumer Staples Select Sector SPDR
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index",
        is_sector_fallback=True
    ),
    
    # =========================================================================
    # SECTOR 35: HEALTH CARE
    # =========================================================================
    
    "350100": IndustryETF(
        code="350100",
        name="Biotechnology",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XBI",      # SPDR S&P Biotech ETF
        alt_etf="IBB",
        index_name="S&P Biotechnology Select Industry Index"
    ),    "350400": IndustryETF(
        code="350400",
        name="Healthcare Facilities",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XHS",      # SPDR S&P Health Care Services ETF
        alt_etf="IHF",
        index_name="S&P Health Care Services Select Industry Index"
    ),
    "350700": IndustryETF(
        code="350700",
        name="Medical Devices",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHI",      # iShares U.S. Medical Devices ETF
        alt_etf="XHE",
        index_name="Dow Jones U.S. Select Medical Equipment Index"
    ),
    "350800": IndustryETF(
        code="350800",
        name="Medical Instruments",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHI",      # iShares U.S. Medical Devices ETF
        alt_etf="XHE",
        index_name="Dow Jones U.S. Select Medical Equipment Index"
    ),
    "350900": IndustryETF(
        code="350900",
        name="Pharmaceuticals",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XPH",      # SPDR S&P Pharmaceuticals ETF
        alt_etf="IHE",
        index_name="S&P Pharmaceuticals Select Industry Index"
    ),
    
    # =========================================================================
    # SECTOR 40: FINANCIALS
    # =========================================================================
    
    "400100": IndustryETF(
        code="400100",
        name="Asset Management",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",      # Financial Select Sector SPDR
        alt_etf="VFH",
        index_name="Financial Select Sector Index",
        is_sector_fallback=True
    ),    "400300": IndustryETF(
        code="400300",
        name="Banks: Regional",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KRE",      # SPDR S&P Regional Banking ETF
        alt_etf="IAT",
        index_name="S&P Regional Banks Select Industry Index"
    ),
    "400400": IndustryETF(
        code="400400",
        name="Brokers & Exchanges",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IAI",      # iShares U.S. Broker-Dealers & Securities Exchanges ETF
        alt_etf="XLF",
        index_name="Dow Jones U.S. Select Investment Services Index"
    ),
    "400500": IndustryETF(
        code="400500",
        name="Consumer Finance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",      # Financial Select Sector SPDR
        alt_etf="VFH",
        index_name="Financial Select Sector Index",
        is_sector_fallback=True
    ),
    "400600": IndustryETF(
        code="400600",
        name="Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",      # Financial Select Sector SPDR
        alt_etf="VFH",
        index_name="Financial Select Sector Index",
        is_sector_fallback=True
    ),
    "400700": IndustryETF(
        code="400700",
        name="Insurance: Brokers",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",      # SPDR S&P Insurance ETF
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "400800": IndustryETF(
        code="400800",
        name="Insurance: Life",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",      # SPDR S&P Insurance ETF
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "400900": IndustryETF(
        code="400900",
        name="Insurance: P&C",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",      # SPDR S&P Insurance ETF
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "401000": IndustryETF(
        code="401000",
        name="Insurance: Specialty",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",      # SPDR S&P Insurance ETF
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "401100": IndustryETF(
        code="401100",
        name="Mortgage Finance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="REM",      # iShares Mortgage Real Estate ETF
        alt_etf="XLF",
        index_name="FTSE NAREIT All Mortgage Capped Index"
    ),    
    # =========================================================================
    # SECTOR 45: TECHNOLOGY
    # =========================================================================
    
    "450100": IndustryETF(
        code="450100",
        name="Application Software",
        sector_code="45",
        sector_name="Technology",
        primary_etf="IGV",      # iShares Expanded Tech-Software Sector ETF
        alt_etf="XSW",
        index_name="S&P North American Expanded Technology Software Index"
    ),    "450400": IndustryETF(
        code="450400",
        name="Computer Hardware",
        sector_code="45",
        sector_name="Technology",
        primary_etf="XLK",      # Technology Select Sector SPDR
        alt_etf="VGT",
        index_name="Technology Select Sector Index",
        is_sector_fallback=True
    ),
    "450500": IndustryETF(
        code="450500",
        name="Computer Services",
        sector_code="45",
        sector_name="Technology",
        primary_etf="XLK",      # Technology Select Sector SPDR
        alt_etf="VGT",
        index_name="Technology Select Sector Index",
        is_sector_fallback=True
    ),    "450800": IndustryETF(
        code="450800",
        name="Electronic Components",
        sector_code="45",
        sector_name="Technology",
        primary_etf="XLK",      # Technology Select Sector SPDR
        alt_etf="VGT",
        index_name="Technology Select Sector Index",
        is_sector_fallback=True
    ),
    "451200": IndustryETF(
        code="451200",
        name="Semiconductors",
        sector_code="45",
        sector_name="Technology",
        primary_etf="SMH",      # VanEck Semiconductor ETF
        alt_etf="SOXX",
        index_name="MVIS US Listed Semiconductor 25 Index"
    ),    
    # =========================================================================
    # SECTOR 50: COMMUNICATION SERVICES
    # =========================================================================
    
    "500100": IndustryETF(
        code="500100",
        name="Advertising",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",      # Communication Services Select Sector SPDR
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index",
        is_sector_fallback=True
    ),    "500400": IndustryETF(
        code="500400",
        name="Entertainment",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="PEJ",      # Invesco Leisure and Entertainment ETF
        alt_etf="XLC",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),
    "500500": IndustryETF(
        code="500500",
        name="Internet",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="FDN",      # First Trust Dow Jones Internet Index Fund
        alt_etf="PNQI",
        index_name="Dow Jones Internet Composite Index"
    ),
    "500600": IndustryETF(
        code="500600",
        name="Publishing",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",      # Communication Services Select Sector SPDR
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index",
        is_sector_fallback=True
    ),
    "500700": IndustryETF(
        code="500700",
        name="Telecom Equipment",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",      # Communication Services Select Sector SPDR
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index",
        is_sector_fallback=True
    ),
    "500800": IndustryETF(
        code="500800",
        name="Telecom Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",      # Communication Services Select Sector SPDR
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index",
        is_sector_fallback=True
    ),
    
    # =========================================================================
    # SECTOR 55: UTILITIES
    # =========================================================================
    
    "550100": IndustryETF(
        code="550100",
        name="Electric Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",      # Utilities Select Sector SPDR
        alt_etf="VPU",
        index_name="Utilities Select Sector Index",
        is_sector_fallback=True
    ),
    "550200": IndustryETF(
        code="550200",
        name="Gas Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",      # Utilities Select Sector SPDR
        alt_etf="VPU",
        index_name="Utilities Select Sector Index",
        is_sector_fallback=True
    ),    "550400": IndustryETF(
        code="550400",
        name="Multi-Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",      # Utilities Select Sector SPDR
        alt_etf="VPU",
        index_name="Utilities Select Sector Index",
        is_sector_fallback=True
    ),
    "550500": IndustryETF(
        code="550500",
        name="Renewable Energy",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="ICLN",     # iShares Global Clean Energy ETF
        alt_etf="TAN",
        index_name="S&P Global Clean Energy Index"
    ),
    "550600": IndustryETF(
        code="550600",
        name="Water Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="PHO",      # Invesco Water Resources ETF
        alt_etf="FIW",
        index_name="Nasdaq OMX US Water Index"
    ),
    
    # =========================================================================
    # SECTOR 60: REAL ESTATE
    # =========================================================================
    
    "600100": IndustryETF(
        code="600100",
        name="REITs - Diversified",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",      # Vanguard Real Estate ETF
        alt_etf="IYR",
        index_name="MSCI US Investable Market Real Estate 25/50 Index"
    ),    "600300": IndustryETF(
        code="600300",
        name="REITs - Hotel & Motel",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
    "600400": IndustryETF(
        code="600400",
        name="REITs - Industrial",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
    "600500": IndustryETF(
        code="600500",
        name="REITs - Mortgage",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="REM",      # iShares Mortgage Real Estate ETF
        alt_etf="MORT",
        index_name="FTSE NAREIT All Mortgage Capped Index"
    ),    "600700": IndustryETF(
        code="600700",
        name="REITs - Residential",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="REZ",      # iShares Residential and Multisector Real Estate ETF
        alt_etf="VNQ",
        index_name="FTSE NAREIT All Residential Capped Index"
    ),
    "600800": IndustryETF(
        code="600800",
        name="REITs - Retail",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
    "600900": IndustryETF(
        code="600900",
        name="REITs - Specialty",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
    "601000": IndustryETF(
        code="601000",
        name="Real Estate Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
    "601100": IndustryETF(
        code="601100",
        name="Real Estate Services",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index",
        is_sector_fallback=True
    ),
}


# =============================================================================
# BACKWARD COMPATIBILITY ALIAS
# =============================================================================

# Alias for backward compatibility with code expecting GICS naming
GICS_SUBINDUSTRY_ETF_MAP = INDUSTRY_ETF_MAP


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_etf_for_industry_code(industry_code: str) -> str:
    """
    Get the primary ETF for an industry code.
    
    Args:
        industry_code: 6-digit industry code
    
    Returns:
        ETF ticker symbol (primary or sector fallback)
    """
    if industry_code in INDUSTRY_ETF_MAP:
        return INDUSTRY_ETF_MAP[industry_code].primary_etf
    
    # Fallback to sector ETF
    sector_code = industry_code[:2] if len(industry_code) >= 2 else "45"
    return SECTOR_ETFS.get(sector_code, "SPY")


def get_alt_etf_for_industry_code(industry_code: str) -> Optional[str]:
    """
    Get the alternative ETF for an industry code.
    
    Args:
        industry_code: 6-digit industry code
    
    Returns:
        Alternative ETF ticker symbol or None
    """
    if industry_code in INDUSTRY_ETF_MAP:
        return INDUSTRY_ETF_MAP[industry_code].alt_etf
    return None


def get_industry_info(industry_code: str) -> Optional[IndustryETF]:
    """
    Get full industry information including ETF mapping.
    
    Args:
        industry_code: 6-digit industry code
    
    Returns:
        IndustryETF named tuple or None
    """
    return INDUSTRY_ETF_MAP.get(industry_code)


def get_etf_for_industry_name(name: str) -> str:
    """
    Get ETF for an industry by name (fuzzy matching).
    
    Args:
        name: Industry name
    
    Returns:
        ETF ticker symbol
    """
    normalized_name = name.lower().strip()
    
    # Exact match first
    for entry in INDUSTRY_ETF_MAP.values():
        if entry.name.lower() == normalized_name:
            return entry.primary_etf
    
    # Partial match
    for entry in INDUSTRY_ETF_MAP.values():
        if normalized_name in entry.name.lower() or entry.name.lower() in normalized_name:
            return entry.primary_etf
    
    # Default fallback
    return "SPY"


def get_all_industries_by_sector(sector_code: str) -> List[IndustryETF]:
    """
    Get all industries for a given sector.
    
    Args:
        sector_code: 2-digit sector code
    
    Returns:
        List of IndustryETF entries
    """
    return [
        entry for entry in INDUSTRY_ETF_MAP.values()
        if entry.sector_code == sector_code
    ]


def get_unique_etfs() -> set:
    """
    Get all unique ETF tickers used in the mapping.
    
    Returns:
        Set of ETF ticker symbols
    """
    etfs = set()
    for entry in INDUSTRY_ETF_MAP.values():
        etfs.add(entry.primary_etf)
        if entry.alt_etf:
            etfs.add(entry.alt_etf)
    return etfs


def get_etf_usage_stats() -> Dict[str, int]:
    """
    Get statistics on how many times each ETF is used as primary.
    
    Returns:
        Dict mapping ETF ticker to usage count
    """
    usage = {}
    for entry in INDUSTRY_ETF_MAP.values():
        etf = entry.primary_etf
        usage[etf] = usage.get(etf, 0) + 1
    return dict(sorted(usage.items(), key=lambda x: x[1], reverse=True))


def get_sector_fallback_count() -> int:
    """
    Get count of industries using sector-level fallback ETFs.
    
    Returns:
        Number of industries marked as sector fallbacks
    """
    return sum(1 for entry in INDUSTRY_ETF_MAP.values() if entry.is_sector_fallback)


def get_industry_by_name(name: str) -> Optional[IndustryETF]:
    """
    Find an industry by its name.
    
    Args:
        name: Industry name (case-insensitive)
    
    Returns:
        IndustryETF entry or None
    """
    normalized = name.lower().strip()
    for entry in INDUSTRY_ETF_MAP.values():
        if entry.name.lower() == normalized:
            return entry
    return None


# Backward compatibility aliases
get_etf_for_gics_code = get_etf_for_industry_code
get_alt_etf_for_gics_code = get_alt_etf_for_industry_code
get_subindustry_info = get_industry_info
get_etf_for_subindustry_name = get_etf_for_industry_name
get_all_subindustries_by_sector = get_all_industries_by_sector
