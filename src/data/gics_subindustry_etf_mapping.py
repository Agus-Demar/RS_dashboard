"""
GICS Sub-Industry to ETF/Index Mapping.

Official GICS (Global Industry Classification Standard) sub-industry codes
mapped to their most representative ETFs and indexes.

PRIORITY SYSTEM:
1. Sub-industry specific ETF (e.g., XBI for Biotechnology)
2. Industry-level ETF (e.g., IBB as alternative for Biotech)
3. Thematic ETF closely matching the sub-industry
4. Sector ETF only as last resort (marked with is_sector_fallback=True)

GICS Structure:
- 11 Sectors (2-digit code)
- 25 Industry Groups (4-digit code)
- 74 Industries (6-digit code)
- 163 Sub-Industries (8-digit code)

Sources:
- MSCI/S&P GICS Structure: https://www.msci.com/gics
- SPDR Select Industry ETFs: https://www.ssga.com
- iShares Sector & Industry ETFs: https://www.ishares.com
- VanEck Industry ETFs: https://www.vaneck.com
- First Trust Thematic ETFs: https://www.ftportfolios.com
- Global X Thematic ETFs: https://www.globalxetfs.com

Last Updated: January 2026
"""

from typing import Dict, NamedTuple, Optional


class SubIndustryETF(NamedTuple):
    """Sub-industry ETF mapping entry."""
    code: str                    # 8-digit GICS code
    name: str                    # Official sub-industry name
    industry_code: str           # 6-digit industry code
    industry_name: str           # Official industry name
    sector_code: str             # 2-digit sector code
    sector_name: str             # Official sector name
    primary_etf: str             # Primary ETF ticker
    alt_etf: Optional[str]       # Alternative ETF (if available)
    index_name: str              # Related index name
    is_sector_fallback: bool = False  # True if using broad sector ETF


# =============================================================================
# GICS SUB-INDUSTRY ETF MAPPINGS
# Prioritizes unique sub-industry/industry ETFs over sector ETFs
# =============================================================================

GICS_SUBINDUSTRY_ETF_MAP: Dict[str, SubIndustryETF] = {
    
    # =========================================================================
    # SECTOR 10: ENERGY
    # =========================================================================
    
    # Industry 101010: Energy Equipment & Services
    "10101010": SubIndustryETF(
        code="10101010",
        name="Oil & Gas Drilling",
        industry_code="101010",
        industry_name="Energy Equipment & Services",
        sector_code="10",
        sector_name="Energy",
        primary_etf="OIH",      # VanEck Oil Services ETF - specific to drilling/services
        alt_etf="XES",
        index_name="MVIS US Listed Oil Services 25 Index"
    ),
    "10101020": SubIndustryETF(
        code="10101020",
        name="Oil & Gas Equipment & Services",
        industry_code="101010",
        industry_name="Energy Equipment & Services",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XES",      # SPDR S&P Oil & Gas Equipment & Services
        alt_etf="IEZ",          # iShares U.S. Oil Equipment & Services
        index_name="S&P Oil & Gas Equipment & Services Select Industry Index"
    ),
    
    # Industry 101020: Oil, Gas & Consumable Fuels
    "10102010": SubIndustryETF(
        code="10102010",
        name="Integrated Oil & Gas",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="IEO",      # iShares U.S. Oil & Gas Exploration & Production
        alt_etf="VDE",
        index_name="Dow Jones U.S. Select Oil Exploration & Production Index"
    ),
    "10102020": SubIndustryETF(
        code="10102020",
        name="Oil & Gas Exploration & Production",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XOP",      # SPDR S&P Oil & Gas E&P - highly specific
        alt_etf="FCG",          # First Trust Natural Gas
        index_name="S&P Oil & Gas Exploration & Production Select Industry Index"
    ),
    "10102030": SubIndustryETF(
        code="10102030",
        name="Oil & Gas Refining & Marketing",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="CRAK",     # VanEck Oil Refiners ETF - specific to refining
        alt_etf="PXE",
        index_name="MVIS Global Oil Refiners Index"
    ),
    "10102040": SubIndustryETF(
        code="10102040",
        name="Oil & Gas Storage & Transportation",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="AMLP",     # Alerian MLP ETF - specific to midstream
        alt_etf="MLPA",
        index_name="Alerian MLP Index"
    ),
    "10102050": SubIndustryETF(
        code="10102050",
        name="Coal & Consumable Fuels",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="KOL",      # VanEck Coal ETF - specific to coal
        alt_etf="PICK",
        index_name="MVIS Global Coal Index"
    ),
    
    # =========================================================================
    # SECTOR 15: MATERIALS
    # =========================================================================
    
    # Industry 151010: Chemicals
    "15101010": SubIndustryETF(
        code="15101010",
        name="Commodity Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="LIT",      # Global X Lithium & Battery Tech - specific commodity
        alt_etf="VAW",
        index_name="Solactive Global Lithium Index"
    ),
    "15101020": SubIndustryETF(
        code="15101020",
        name="Diversified Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="VAW",      # Vanguard Materials - broad materials
        alt_etf="IYM",
        index_name="MSCI US IMI Materials 25/50 Index",
        is_sector_fallback=True
    ),
    "15101030": SubIndustryETF(
        code="15101030",
        name="Fertilizers & Agricultural Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="MOO",      # VanEck Agribusiness ETF - specific to ag
        alt_etf="VEGI",
        index_name="MVIS Global Agribusiness Index"
    ),
    "15101040": SubIndustryETF(
        code="15101040",
        name="Industrial Gases",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="IYM",      # iShares U.S. Basic Materials
        alt_etf="VAW",
        index_name="Dow Jones U.S. Basic Materials Index",
        is_sector_fallback=True
    ),
    "15101050": SubIndustryETF(
        code="15101050",
        name="Specialty Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="PYZ",      # Invesco Dynamic Basic Materials
        alt_etf="VAW",
        index_name="Dynamic Basic Materials Intellidex Index"
    ),
    
    # Industry 151020: Construction Materials
    "15102010": SubIndustryETF(
        code="15102010",
        name="Construction Materials",
        industry_code="151020",
        industry_name="Construction Materials",
        sector_code="15",
        sector_name="Materials",
        primary_etf="PKB",      # Invesco Dynamic Building & Construction
        alt_etf="XHB",
        index_name="Dynamic Building & Construction Intellidex Index"
    ),
    
    # Industry 151030: Containers & Packaging
    "15103010": SubIndustryETF(
        code="15103010",
        name="Metal, Glass & Plastic Containers",
        industry_code="151030",
        industry_name="Containers & Packaging",
        sector_code="15",
        sector_name="Materials",
        primary_etf="VAW",      # Vanguard Materials
        alt_etf="IYM",
        index_name="MSCI US IMI Materials 25/50 Index",
        is_sector_fallback=True
    ),
    "15103020": SubIndustryETF(
        code="15103020",
        name="Paper & Plastic Packaging Products & Materials",
        industry_code="151030",
        industry_name="Containers & Packaging",
        sector_code="15",
        sector_name="Materials",
        primary_etf="WOOD",     # iShares Global Timber & Forestry
        alt_etf="CUT",
        index_name="S&P Global Timber & Forestry Index"
    ),
    
    # Industry 151040: Metals & Mining
    "15104010": SubIndustryETF(
        code="15104010",
        name="Aluminum",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="PICK",     # iShares MSCI Global Metals & Mining Producers
        alt_etf="XME",
        index_name="MSCI ACWI Select Metals & Mining Producers Ex Gold & Silver IMI"
    ),
    "15104020": SubIndustryETF(
        code="15104020",
        name="Diversified Metals & Mining",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XME",      # SPDR S&P Metals & Mining
        alt_etf="PICK",
        index_name="S&P Metals & Mining Select Industry Index"
    ),
    "15104025": SubIndustryETF(
        code="15104025",
        name="Copper",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="COPX",     # Global X Copper Miners - highly specific
        alt_etf="CPER",
        index_name="Solactive Global Copper Miners Index"
    ),
    "15104030": SubIndustryETF(
        code="15104030",
        name="Gold",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="GDX",      # VanEck Gold Miners - highly specific
        alt_etf="GDXJ",
        index_name="NYSE Arca Gold Miners Index"
    ),
    "15104040": SubIndustryETF(
        code="15104040",
        name="Precious Metals & Minerals",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="GDXJ",     # VanEck Junior Gold Miners
        alt_etf="RING",
        index_name="MVIS Global Junior Gold Miners Index"
    ),
    "15104045": SubIndustryETF(
        code="15104045",
        name="Silver",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="SIL",      # Global X Silver Miners - highly specific
        alt_etf="SILJ",
        index_name="Solactive Global Silver Miners Index"
    ),
    "15104050": SubIndustryETF(
        code="15104050",
        name="Steel",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="SLX",      # VanEck Steel ETF - highly specific
        alt_etf="XME",
        index_name="NYSE Arca Steel Index"
    ),
    
    # Industry 151050: Paper & Forest Products
    "15105010": SubIndustryETF(
        code="15105010",
        name="Forest Products",
        industry_code="151050",
        industry_name="Paper & Forest Products",
        sector_code="15",
        sector_name="Materials",
        primary_etf="CUT",      # Invesco MSCI Global Timber
        alt_etf="WOOD",
        index_name="MSCI ACWI IMI Timber Select Capped Index"
    ),
    "15105020": SubIndustryETF(
        code="15105020",
        name="Paper Products",
        industry_code="151050",
        industry_name="Paper & Forest Products",
        sector_code="15",
        sector_name="Materials",
        primary_etf="WOOD",     # iShares Global Timber & Forestry
        alt_etf="CUT",
        index_name="S&P Global Timber & Forestry Index"
    ),
    
    # =========================================================================
    # SECTOR 20: INDUSTRIALS
    # =========================================================================
    
    # Industry 201010: Aerospace & Defense
    "20101010": SubIndustryETF(
        code="20101010",
        name="Aerospace & Defense",
        industry_code="201010",
        industry_name="Aerospace & Defense",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="ITA",      # iShares U.S. Aerospace & Defense
        alt_etf="XAR",          # SPDR S&P Aerospace & Defense
        index_name="Dow Jones U.S. Select Aerospace & Defense Index"
    ),
    
    # Industry 201020: Building Products
    "20102010": SubIndustryETF(
        code="20102010",
        name="Building Products",
        industry_code="201020",
        industry_name="Building Products",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PKB",      # Invesco Dynamic Building & Construction
        alt_etf="XHB",
        index_name="Dynamic Building & Construction Intellidex Index"
    ),
    
    # Industry 201030: Construction & Engineering
    "20103010": SubIndustryETF(
        code="20103010",
        name="Construction & Engineering",
        industry_code="201030",
        industry_name="Construction & Engineering",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PAVE",     # Global X U.S. Infrastructure Development
        alt_etf="PKB",
        index_name="Indxx U.S. Infrastructure Development Index"
    ),
    
    # Industry 201040: Electrical Equipment
    "20104010": SubIndustryETF(
        code="20104010",
        name="Electrical Components & Equipment",
        industry_code="201040",
        industry_name="Electrical Equipment",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="GRID",     # First Trust NASDAQ Clean Edge Smart Grid
        alt_etf="QCLN",
        index_name="NASDAQ OMX Clean Edge Smart Grid Infrastructure Index"
    ),
    "20104020": SubIndustryETF(
        code="20104020",
        name="Heavy Electrical Equipment",
        industry_code="201040",
        industry_name="Electrical Equipment",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="ICLN",     # iShares Global Clean Energy (heavy electrical for renewables)
        alt_etf="GRID",
        index_name="S&P Global Clean Energy Index"
    ),
    
    # Industry 201050: Industrial Conglomerates
    "20105010": SubIndustryETF(
        code="20105010",
        name="Industrial Conglomerates",
        industry_code="201050",
        industry_name="Industrial Conglomerates",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",      # Vanguard Industrials
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 201060: Machinery
    "20106010": SubIndustryETF(
        code="20106010",
        name="Construction Machinery & Heavy Transportation Equipment",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PAVE",     # Global X U.S. Infrastructure Development
        alt_etf="VIS",
        index_name="Indxx U.S. Infrastructure Development Index"
    ),
    "20106015": SubIndustryETF(
        code="20106015",
        name="Agricultural & Farm Machinery",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="MOO",      # VanEck Agribusiness
        alt_etf="VEGI",
        index_name="MVIS Global Agribusiness Index"
    ),
    "20106020": SubIndustryETF(
        code="20106020",
        name="Industrial Machinery & Supplies & Components",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="FIW",      # First Trust Water ETF (water machinery)
        alt_etf="VIS",
        index_name="ISE Clean Edge Water Index"
    ),
    
    # Industry 201070: Trading Companies & Distributors
    "20107010": SubIndustryETF(
        code="20107010",
        name="Trading Companies & Distributors",
        industry_code="201070",
        industry_name="Trading Companies & Distributors",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",      # Vanguard Industrials
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 202010: Commercial Services & Supplies
    "20201010": SubIndustryETF(
        code="20201010",
        name="Commercial Printing",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    "20201050": SubIndustryETF(
        code="20201050",
        name="Environmental & Facilities Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="EVX",      # VanEck Environmental Services
        alt_etf="PBW",
        index_name="NYSE Arca Environmental Services Index"
    ),
    "20201060": SubIndustryETF(
        code="20201060",
        name="Office Services & Supplies",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    "20201070": SubIndustryETF(
        code="20201070",
        name="Diversified Support Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    "20201080": SubIndustryETF(
        code="20201080",
        name="Security & Alarm Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="CIBR",     # First Trust NASDAQ Cybersecurity
        alt_etf="HACK",
        index_name="Nasdaq CTA Cybersecurity Index"
    ),
    
    # Industry 202020: Professional Services
    "20202010": SubIndustryETF(
        code="20202010",
        name="Human Resource & Employment Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    "20202020": SubIndustryETF(
        code="20202020",
        name="Research & Consulting Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="VIS",
        alt_etf="XLI",
        index_name="MSCI US IMI Industrials 25/50 Index",
        is_sector_fallback=True
    ),
    "20202030": SubIndustryETF(
        code="20202030",
        name="Data Processing & Outsourced Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SKYY",     # First Trust Cloud Computing
        alt_etf="WCLD",
        index_name="ISE CTA Cloud Computing Index"
    ),
    
    # Industry 203010: Air Freight & Logistics
    "20301010": SubIndustryETF(
        code="20301010",
        name="Air Freight & Logistics",
        industry_code="203010",
        industry_name="Air Freight & Logistics",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",      # SPDR S&P Transportation
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    
    # Industry 203020: Passenger Airlines
    "20302010": SubIndustryETF(
        code="20302010",
        name="Passenger Airlines",
        industry_code="203020",
        industry_name="Passenger Airlines",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="JETS",     # U.S. Global Jets - highly specific
        alt_etf="XTN",
        index_name="U.S. Global Jets Index"
    ),
    
    # Industry 203030: Marine Transportation
    "20303010": SubIndustryETF(
        code="20303010",
        name="Marine Transportation",
        industry_code="203030",
        industry_name="Marine Transportation",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SEA",      # U.S. Global Sea to Sky Cargo
        alt_etf="BOAT",
        index_name="U.S. Global Sea to Sky Cargo Index"
    ),
    
    # Industry 203040: Ground Transportation
    "20304010": SubIndustryETF(
        code="20304010",
        name="Rail Transportation",
        industry_code="203040",
        industry_name="Ground Transportation",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="IYT",      # iShares U.S. Transportation
        alt_etf="XTN",
        index_name="Dow Jones U.S. Select Transportation Index"
    ),
    "20304020": SubIndustryETF(
        code="20304020",
        name="Cargo Ground Transportation",
        industry_code="203040",
        industry_name="Ground Transportation",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",      # SPDR S&P Transportation
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    "20304030": SubIndustryETF(
        code="20304030",
        name="Passenger Ground Transportation",
        industry_code="203040",
        industry_name="Ground Transportation",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="DRIV",     # Global X Autonomous & Electric Vehicles
        alt_etf="XTN",
        index_name="Solactive Autonomous & Electric Vehicles Index"
    ),
    
    # Industry 203050: Transportation Infrastructure
    "20305010": SubIndustryETF(
        code="20305010",
        name="Airport Services",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="JETS",     # Related to airline infrastructure
        alt_etf="IYT",
        index_name="U.S. Global Jets Index"
    ),
    "20305020": SubIndustryETF(
        code="20305020",
        name="Highways & Railtracks",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="IGF",      # iShares Global Infrastructure
        alt_etf="PAVE",
        index_name="S&P Global Infrastructure Index"
    ),
    "20305030": SubIndustryETF(
        code="20305030",
        name="Marine Ports & Services",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SEA",
        alt_etf="IGF",
        index_name="U.S. Global Sea to Sky Cargo Index"
    ),
    
    # =========================================================================
    # SECTOR 25: CONSUMER DISCRETIONARY
    # =========================================================================
    
    # Industry 251010: Automobile Components
    "25101010": SubIndustryETF(
        code="25101010",
        name="Automotive Parts & Equipment",
        industry_code="251010",
        industry_name="Automobile Components",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",     # First Trust NASDAQ Global Auto
        alt_etf="DRIV",
        index_name="NASDAQ OMX Global Automobile Index"
    ),
    "25101020": SubIndustryETF(
        code="25101020",
        name="Tires & Rubber",
        industry_code="251010",
        industry_name="Automobile Components",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="VCR",
        index_name="NASDAQ OMX Global Automobile Index"
    ),
    
    # Industry 251020: Automobiles
    "25102010": SubIndustryETF(
        code="25102010",
        name="Automobile Manufacturers",
        industry_code="251020",
        industry_name="Automobiles",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="DRIV",     # Global X Autonomous & Electric Vehicles
        alt_etf="CARZ",
        index_name="Solactive Autonomous & Electric Vehicles Index"
    ),
    "25102020": SubIndustryETF(
        code="25102020",
        name="Motorcycle Manufacturers",
        industry_code="251020",
        industry_name="Automobiles",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="VCR",
        index_name="NASDAQ OMX Global Automobile Index"
    ),
    
    # Industry 252010: Household Durables
    "25201010": SubIndustryETF(
        code="25201010",
        name="Consumer Electronics",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="SNSR",     # Global X Internet of Things
        alt_etf="VCR",
        index_name="Indxx Global Internet of Things Thematic Index"
    ),
    "25201020": SubIndustryETF(
        code="25201020",
        name="Home Furnishings",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",      # SPDR S&P Homebuilders
        alt_etf="ITB",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "25201030": SubIndustryETF(
        code="25201030",
        name="Homebuilding",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="ITB",      # iShares U.S. Home Construction
        alt_etf="XHB",
        index_name="Dow Jones U.S. Select Home Construction Index"
    ),
    "25201040": SubIndustryETF(
        code="25201040",
        name="Household Appliances",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="VCR",      # Vanguard Consumer Discretionary
        alt_etf="XLY",
        index_name="MSCI US IMI Consumer Discretionary 25/50 Index",
        is_sector_fallback=True
    ),
    "25201050": SubIndustryETF(
        code="25201050",
        name="Housewares & Specialties",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="VCR",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    
    # Industry 252020: Leisure Products
    "25202010": SubIndustryETF(
        code="25202010",
        name="Leisure Products",
        industry_code="252020",
        industry_name="Leisure Products",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",      # Invesco Dynamic Leisure & Entertainment
        alt_etf="VCR",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),
    
    # Industry 252030: Textiles, Apparel & Luxury Goods
    "25203010": SubIndustryETF(
        code="25203010",
        name="Apparel, Accessories & Luxury Goods",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",      # SPDR S&P Retail
        alt_etf="RTH",
        index_name="S&P Retail Select Industry Index"
    ),
    "25203020": SubIndustryETF(
        code="25203020",
        name="Footwear",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="RTH",      # VanEck Retail
        alt_etf="XRT",
        index_name="MVIS US Listed Retail 25 Index"
    ),
    "25203030": SubIndustryETF(
        code="25203030",
        name="Textiles",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="VCR",
        alt_etf="XLY",
        index_name="MSCI US IMI Consumer Discretionary 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 253010: Hotels, Restaurants & Leisure
    "25301010": SubIndustryETF(
        code="25301010",
        name="Casinos & Gaming",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="BJK",      # VanEck Gaming - highly specific
        alt_etf="BETZ",
        index_name="MVIS Global Gaming Index"
    ),
    "25301020": SubIndustryETF(
        code="25301020",
        name="Hotels, Resorts & Cruise Lines",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",      # Invesco Dynamic Leisure & Entertainment
        alt_etf="AWAY",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),
    "25301030": SubIndustryETF(
        code="25301030",
        name="Leisure Facilities",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="AWAY",     # ETFMG Travel Tech
        alt_etf="PEJ",
        index_name="Prime Travel Technology Index"
    ),
    "25301040": SubIndustryETF(
        code="25301040",
        name="Restaurants",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PBJ",      # Invesco Dynamic Food & Beverage
        alt_etf="PEJ",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    
    # Industry 253020: Diversified Consumer Services
    "25302010": SubIndustryETF(
        code="25302010",
        name="Education Services",
        industry_code="253020",
        industry_name="Diversified Consumer Services",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="VCR",
        alt_etf="XLY",
        index_name="MSCI US IMI Consumer Discretionary 25/50 Index",
        is_sector_fallback=True
    ),
    "25302020": SubIndustryETF(
        code="25302020",
        name="Specialized Consumer Services",
        industry_code="253020",
        industry_name="Diversified Consumer Services",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="VCR",
        alt_etf="XLY",
        index_name="MSCI US IMI Consumer Discretionary 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 255010: Distributors
    "25501010": SubIndustryETF(
        code="25501010",
        name="Distributors",
        industry_code="255010",
        industry_name="Distributors",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="VCR",
        index_name="S&P Retail Select Industry Index"
    ),
    
    # Industry 255020: Broadline Retail
    "25502010": SubIndustryETF(
        code="25502010",
        name="Broadline Retail",
        industry_code="255020",
        industry_name="Broadline Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="IBUY",     # Amplify Online Retail - highly specific
        alt_etf="ONLN",
        index_name="EQM Online Retail Index"
    ),
    
    # Industry 255030: Specialty Retail
    "25503010": SubIndustryETF(
        code="25503010",
        name="Apparel Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="RTH",
        alt_etf="XRT",
        index_name="MVIS US Listed Retail 25 Index"
    ),
    "25503020": SubIndustryETF(
        code="25503020",
        name="Computer & Electronics Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="ONLN",     # ProShares Online Retail
        alt_etf="XRT",
        index_name="ProShares Online Retail Index"
    ),
    "25503030": SubIndustryETF(
        code="25503030",
        name="Home Improvement Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="ITB",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    "25503040": SubIndustryETF(
        code="25503040",
        name="Other Specialty Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="RTH",
        index_name="S&P Retail Select Industry Index"
    ),
    "25503050": SubIndustryETF(
        code="25503050",
        name="Automotive Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="XRT",
        index_name="NASDAQ OMX Global Automobile Index"
    ),
    "25503060": SubIndustryETF(
        code="25503060",
        name="Home Furnishing Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="XRT",
        index_name="S&P Homebuilders Select Industry Index"
    ),
    
    # =========================================================================
    # SECTOR 30: CONSUMER STAPLES
    # =========================================================================
    
    # Industry 301010: Consumer Staples Distribution & Retail
    "30101010": SubIndustryETF(
        code="30101010",
        name="Drug Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="IHF",      # iShares U.S. Healthcare Providers
        alt_etf="XLP",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    "30101020": SubIndustryETF(
        code="30101020",
        name="Food Distributors",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="IYK",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "30101030": SubIndustryETF(
        code="30101030",
        name="Food Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="IYK",      # iShares U.S. Consumer Staples
        alt_etf="PBJ",
        index_name="Dow Jones U.S. Consumer Goods Index"
    ),
    "30101040": SubIndustryETF(
        code="30101040",
        name="Consumer Staples Merchandise Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="VDC",      # Vanguard Consumer Staples
        alt_etf="XLP",
        index_name="MSCI US IMI Consumer Staples 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 302010: Beverages
    "30201010": SubIndustryETF(
        code="30201010",
        name="Brewers",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="VDC",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "30201020": SubIndustryETF(
        code="30201020",
        name="Distillers & Vintners",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="IYK",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    "30201030": SubIndustryETF(
        code="30201030",
        name="Soft Drinks & Non-alcoholic Beverages",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="VDC",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    
    # Industry 302020: Food Products
    "30202010": SubIndustryETF(
        code="30202010",
        name="Agricultural Products & Services",
        industry_code="302020",
        industry_name="Food Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="VEGI",     # iShares MSCI Global Agriculture Producers
        alt_etf="MOO",
        index_name="MSCI ACWI Select Agriculture Producers IMI"
    ),
    "30202030": SubIndustryETF(
        code="30202030",
        name="Packaged Foods & Meats",
        industry_code="302020",
        industry_name="Food Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="VDC",
        index_name="Dynamic Food & Beverage Intellidex Index"
    ),
    
    # Industry 302030: Tobacco
    "30203010": SubIndustryETF(
        code="30203010",
        name="Tobacco",
        industry_code="302030",
        industry_name="Tobacco",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="VDC",
        alt_etf="XLP",
        index_name="MSCI US IMI Consumer Staples 25/50 Index",
        is_sector_fallback=True
    ),
    
    # Industry 303010: Household Products
    "30301010": SubIndustryETF(
        code="30301010",
        name="Household Products",
        industry_code="303010",
        industry_name="Household Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="IYK",
        alt_etf="VDC",
        index_name="Dow Jones U.S. Consumer Goods Index"
    ),
    
    # Industry 303020: Personal Care Products
    "30302010": SubIndustryETF(
        code="30302010",
        name="Personal Care Products",
        industry_code="303020",
        industry_name="Personal Care Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="IYK",
        alt_etf="VDC",
        index_name="Dow Jones U.S. Consumer Goods Index"
    ),
    
    # =========================================================================
    # SECTOR 35: HEALTH CARE
    # =========================================================================
    
    # Industry 351010: Health Care Equipment & Supplies
    "35101010": SubIndustryETF(
        code="35101010",
        name="Health Care Equipment",
        industry_code="351010",
        industry_name="Health Care Equipment & Supplies",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHI",      # iShares U.S. Medical Devices - highly specific
        alt_etf="XHE",
        index_name="Dow Jones U.S. Select Medical Equipment Index"
    ),
    "35101020": SubIndustryETF(
        code="35101020",
        name="Health Care Supplies",
        industry_code="351010",
        industry_name="Health Care Equipment & Supplies",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XHE",      # SPDR S&P Health Care Equipment
        alt_etf="IHI",
        index_name="S&P Health Care Equipment Select Industry Index"
    ),
    
    # Industry 351020: Health Care Providers & Services
    "35102010": SubIndustryETF(
        code="35102010",
        name="Health Care Distributors",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",      # iShares U.S. Healthcare Providers
        alt_etf="XHS",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    "35102015": SubIndustryETF(
        code="35102015",
        name="Health Care Services",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XHS",      # SPDR S&P Health Care Services
        alt_etf="IHF",
        index_name="S&P Health Care Services Select Industry Index"
    ),
    "35102020": SubIndustryETF(
        code="35102020",
        name="Health Care Facilities",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",
        alt_etf="XHS",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    "35102030": SubIndustryETF(
        code="35102030",
        name="Managed Health Care",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",
        alt_etf="VHT",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    
    # Industry 351030: Health Care Technology
    "35103010": SubIndustryETF(
        code="35103010",
        name="Health Care Technology",
        industry_code="351030",
        industry_name="Health Care Technology",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="EDOC",     # Global X Telemedicine & Digital Health - highly specific
        alt_etf="IHF",
        index_name="Solactive Telemedicine & Digital Health Index"
    ),
    
    # Industry 352010: Biotechnology
    "35201010": SubIndustryETF(
        code="35201010",
        name="Biotechnology",
        industry_code="352010",
        industry_name="Biotechnology",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XBI",      # SPDR S&P Biotech - highly specific
        alt_etf="IBB",
        index_name="S&P Biotechnology Select Industry Index"
    ),
    
    # Industry 352020: Pharmaceuticals
    "35202010": SubIndustryETF(
        code="35202010",
        name="Pharmaceuticals",
        industry_code="352020",
        industry_name="Pharmaceuticals",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XPH",      # SPDR S&P Pharmaceuticals
        alt_etf="IHE",          # iShares U.S. Pharmaceuticals
        index_name="S&P Pharmaceuticals Select Industry Index"
    ),
    
    # Industry 352030: Life Sciences Tools & Services
    "35203010": SubIndustryETF(
        code="35203010",
        name="Life Sciences Tools & Services",
        industry_code="352030",
        industry_name="Life Sciences Tools & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IBB",      # iShares Biotechnology
        alt_etf="XBI",
        index_name="Nasdaq Biotechnology Index"
    ),
    
    # =========================================================================
    # SECTOR 40: FINANCIALS
    # =========================================================================
    
    # Industry 401010: Banks
    "40101010": SubIndustryETF(
        code="40101010",
        name="Diversified Banks",
        industry_code="401010",
        industry_name="Banks",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KBE",      # SPDR S&P Bank - highly specific
        alt_etf="IAT",
        index_name="S&P Banks Select Industry Index"
    ),
    "40101015": SubIndustryETF(
        code="40101015",
        name="Regional Banks",
        industry_code="401010",
        industry_name="Banks",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KRE",      # SPDR S&P Regional Banking - highly specific
        alt_etf="IAT",
        index_name="S&P Regional Banks Select Industry Index"
    ),
    
    # Industry 402010: Diversified Financial Services
    "40201010": SubIndustryETF(
        code="40201010",
        name="Diversified Financial Services",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="VFH",      # Vanguard Financials
        alt_etf="XLF",
        index_name="MSCI US IMI Financials 25/50 Index",
        is_sector_fallback=True
    ),
    "40201020": SubIndustryETF(
        code="40201020",
        name="Multi-Sector Holdings",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="VFH",
        alt_etf="XLF",
        index_name="MSCI US IMI Financials 25/50 Index",
        is_sector_fallback=True
    ),
    "40201030": SubIndustryETF(
        code="40201030",
        name="Specialized Finance",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KBWP",     # Invesco KBW Premium Yield Equity REIT
        alt_etf="VFH",
        index_name="KBW Nasdaq Premium Yield Equity REIT Index"
    ),
    "40201040": SubIndustryETF(
        code="40201040",
        name="Commercial & Residential Mortgage Finance",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="REM",      # iShares Mortgage Real Estate - highly specific
        alt_etf="MORT",
        index_name="FTSE NAREIT All Mortgage Capped Index"
    ),
    "40201050": SubIndustryETF(
        code="40201050",
        name="Transaction & Payment Processing Services",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IPAY",     # ETFMG Prime Mobile Payments - highly specific
        alt_etf="FINX",
        index_name="Prime Mobile Payments Index"
    ),
    
    # Industry 402020: Consumer Finance
    "40202010": SubIndustryETF(
        code="40202010",
        name="Consumer Finance",
        industry_code="402020",
        industry_name="Consumer Finance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="FINX",     # Global X FinTech
        alt_etf="VFH",
        index_name="Indxx Global FinTech Thematic Index"
    ),
    
    # Industry 402030: Capital Markets
    "40203010": SubIndustryETF(
        code="40203010",
        name="Asset Management & Custody Banks",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",      # SPDR S&P Capital Markets
        alt_etf="IAI",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    "40203020": SubIndustryETF(
        code="40203020",
        name="Investment Banking & Brokerage",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IAI",      # iShares U.S. Broker-Dealers & Securities Exchanges
        alt_etf="KCE",
        index_name="Dow Jones U.S. Select Investment Services Index"
    ),
    "40203030": SubIndustryETF(
        code="40203030",
        name="Diversified Capital Markets",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",
        alt_etf="IAI",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    "40203040": SubIndustryETF(
        code="40203040",
        name="Financial Exchanges & Data",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IAI",
        alt_etf="KCE",
        index_name="Dow Jones U.S. Select Investment Services Index"
    ),
    
    # Industry 402040: Mortgage REITs
    "40204010": SubIndustryETF(
        code="40204010",
        name="Mortgage REITs",
        industry_code="402040",
        industry_name="Mortgage Real Estate Investment Trusts (REITs)",
        sector_code="40",
        sector_name="Financials",
        primary_etf="REM",
        alt_etf="MORT",
        index_name="FTSE NAREIT All Mortgage Capped Index"
    ),
    
    # Industry 403010: Insurance
    "40301010": SubIndustryETF(
        code="40301010",
        name="Insurance Brokers",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",      # SPDR S&P Insurance - highly specific
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "40301020": SubIndustryETF(
        code="40301020",
        name="Life & Health Insurance",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IAK",      # iShares U.S. Insurance
        alt_etf="KIE",
        index_name="Dow Jones U.S. Select Insurance Index"
    ),
    "40301030": SubIndustryETF(
        code="40301030",
        name="Multi-line Insurance",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    "40301040": SubIndustryETF(
        code="40301040",
        name="Property & Casualty Insurance",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IAK",
        alt_etf="KIE",
        index_name="Dow Jones U.S. Select Insurance Index"
    ),
    "40301050": SubIndustryETF(
        code="40301050",
        name="Reinsurance",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
    ),
    
    # =========================================================================
    # SECTOR 45: INFORMATION TECHNOLOGY
    # =========================================================================
    
    # Industry 451020: IT Services
    "45102010": SubIndustryETF(
        code="45102010",
        name="IT Consulting & Other Services",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IGV",      # iShares Expanded Tech-Software
        alt_etf="XSW",
        index_name="S&P North American Technology-Software Index"
    ),
    "45102020": SubIndustryETF(
        code="45102020",
        name="Internet Services & Infrastructure",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="FDN",      # First Trust Dow Jones Internet
        alt_etf="XWEB",
        index_name="Dow Jones Internet Composite Index"
    ),
    "45102030": SubIndustryETF(
        code="45102030",
        name="Data Processing & Outsourced Services",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="WCLD",     # WisdomTree Cloud Computing
        alt_etf="SKYY",
        index_name="BVP Nasdaq Emerging Cloud Index"
    ),
    
    # Industry 451030: Software
    "45103010": SubIndustryETF(
        code="45103010",
        name="Application Software",
        industry_code="451030",
        industry_name="Software",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IGV",      # iShares Expanded Tech-Software - highly specific
        alt_etf="XSW",
        index_name="S&P North American Technology-Software Index"
    ),
    "45103020": SubIndustryETF(
        code="45103020",
        name="Systems Software",
        industry_code="451030",
        industry_name="Software",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XSW",      # SPDR S&P Software & Services
        alt_etf="IGV",
        index_name="S&P Software & Services Select Industry Index"
    ),
    
    # Industry 452010: Communications Equipment
    "45201010": SubIndustryETF(
        code="45201010",
        name="Communications Equipment",
        industry_code="452010",
        industry_name="Communications Equipment",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IYZ",      # iShares U.S. Telecommunications
        alt_etf="FCOM",
        index_name="Dow Jones U.S. Select Telecommunications Index"
    ),
    
    # Industry 452020: Technology Hardware, Storage & Peripherals
    "45202010": SubIndustryETF(
        code="45202010",
        name="Technology Hardware, Storage & Peripherals",
        industry_code="452020",
        industry_name="Technology Hardware, Storage & Peripherals",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",      # SPDR S&P Technology Hardware
        alt_etf="QTEC",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    
    # Industry 452030: Electronic Equipment, Instruments & Components
    "45203010": SubIndustryETF(
        code="45203010",
        name="Electronic Equipment & Instruments",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="QTEC",     # First Trust NASDAQ-100 Technology
        alt_etf="XTH",
        index_name="NASDAQ-100 Technology Sector Index"
    ),
    "45203015": SubIndustryETF(
        code="45203015",
        name="Electronic Components",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
        alt_etf="QTEC",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    "45203020": SubIndustryETF(
        code="45203020",
        name="Electronic Manufacturing Services",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="QTEC",
        alt_etf="IYW",
        index_name="NASDAQ-100 Technology Sector Index"
    ),
    "45203030": SubIndustryETF(
        code="45203030",
        name="Technology Distributors",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IYW",      # iShares U.S. Technology
        alt_etf="VGT",
        index_name="Dow Jones U.S. Technology Index"
    ),
    
    # Industry 453010: Semiconductors & Semiconductor Equipment
    "45301010": SubIndustryETF(
        code="45301010",
        name="Semiconductor Materials & Equipment",
        industry_code="453010",
        industry_name="Semiconductors & Semiconductor Equipment",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XSD",      # SPDR S&P Semiconductor
        alt_etf="SMH",
        index_name="S&P Semiconductor Select Industry Index"
    ),
    "45301020": SubIndustryETF(
        code="45301020",
        name="Semiconductors",
        industry_code="453010",
        industry_name="Semiconductors & Semiconductor Equipment",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="SMH",      # VanEck Semiconductor - highly specific
        alt_etf="SOXX",         # iShares Semiconductor
        index_name="MVIS US Listed Semiconductor 25 Index"
    ),
    
    # =========================================================================
    # SECTOR 50: COMMUNICATION SERVICES
    # =========================================================================
    
    # Industry 501010: Diversified Telecommunication Services
    "50101010": SubIndustryETF(
        code="50101010",
        name="Alternative Carriers",
        industry_code="501010",
        industry_name="Diversified Telecommunication Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="IYZ",
        alt_etf="VOX",
        index_name="Dow Jones U.S. Select Telecommunications Index"
    ),
    "50101020": SubIndustryETF(
        code="50101020",
        name="Integrated Telecommunication Services",
        industry_code="501010",
        industry_name="Diversified Telecommunication Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="VOX",      # Vanguard Communication Services
        alt_etf="IYZ",
        index_name="MSCI US IMI Communication Services 25/50 Index"
    ),
    
    # Industry 501020: Wireless Telecommunication Services
    "50102010": SubIndustryETF(
        code="50102010",
        name="Wireless Telecommunication Services",
        industry_code="501020",
        industry_name="Wireless Telecommunication Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="IYZ",
        alt_etf="FCOM",
        index_name="Dow Jones U.S. Select Telecommunications Index"
    ),
    
    # Industry 502010: Media
    "50201010": SubIndustryETF(
        code="50201010",
        name="Advertising",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="PBS",      # Invesco Dynamic Media
        alt_etf="XLC",
        index_name="Dynamic Media Intellidex Index"
    ),
    "50201020": SubIndustryETF(
        code="50201020",
        name="Broadcasting",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="PBS",
        alt_etf="VOX",
        index_name="Dynamic Media Intellidex Index"
    ),
    "50201030": SubIndustryETF(
        code="50201030",
        name="Cable & Satellite",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="VOX",
        alt_etf="XLC",
        index_name="MSCI US IMI Communication Services 25/50 Index",
        is_sector_fallback=True
    ),
    "50201040": SubIndustryETF(
        code="50201040",
        name="Publishing",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="PBS",
        alt_etf="VOX",
        index_name="Dynamic Media Intellidex Index"
    ),
    
    # Industry 502020: Entertainment
    "50202010": SubIndustryETF(
        code="50202010",
        name="Movies & Entertainment",
        industry_code="502020",
        industry_name="Entertainment",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="PEJ",
        alt_etf="PBS",
        index_name="Dynamic Leisure & Entertainment Intellidex Index"
    ),
    "50202020": SubIndustryETF(
        code="50202020",
        name="Interactive Home Entertainment",
        industry_code="502020",
        industry_name="Entertainment",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="ESPO",     # VanEck Video Gaming & eSports - highly specific
        alt_etf="HERO",
        index_name="MVIS Global Video Gaming and eSports Index"
    ),
    
    # Industry 502030: Interactive Media & Services
    "50203010": SubIndustryETF(
        code="50203010",
        name="Interactive Media & Services",
        industry_code="502030",
        industry_name="Interactive Media & Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="SOCL",     # Global X Social Media - highly specific
        alt_etf="FDN",
        index_name="Solactive Social Media Index"
    ),
    
    # =========================================================================
    # SECTOR 55: UTILITIES
    # =========================================================================
    
    # Industry 551010: Electric Utilities
    "55101010": SubIndustryETF(
        code="55101010",
        name="Electric Utilities",
        industry_code="551010",
        industry_name="Electric Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",      # Utilities Select Sector SPDR
        alt_etf="VPU",
        index_name="Utilities Select Sector Index"
    ),
    
    # Industry 551020: Gas Utilities
    "55102010": SubIndustryETF(
        code="55102010",
        name="Gas Utilities",
        industry_code="551020",
        industry_name="Gas Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="FCG",      # First Trust Natural Gas
        alt_etf="XLU",
        index_name="ISE-Revere Natural Gas Index"
    ),
    
    # Industry 551030: Multi-Utilities
    "55103010": SubIndustryETF(
        code="55103010",
        name="Multi-Utilities",
        industry_code="551030",
        industry_name="Multi-Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="VPU",      # Vanguard Utilities
        alt_etf="XLU",
        index_name="MSCI US IMI Utilities 25/50 Index"
    ),
    
    # Industry 551040: Water Utilities
    "55104010": SubIndustryETF(
        code="55104010",
        name="Water Utilities",
        industry_code="551040",
        industry_name="Water Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="PHO",      # Invesco Water Resources - highly specific
        alt_etf="FIW",
        index_name="NASDAQ OMX US Water Index"
    ),
    
    # Industry 551050: Independent Power and Renewable Electricity Producers
    "55105010": SubIndustryETF(
        code="55105010",
        name="Independent Power Producers & Energy Traders",
        industry_code="551050",
        industry_name="Independent Power and Renewable Electricity Producers",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="VPU",
        alt_etf="XLU",
        index_name="MSCI US IMI Utilities 25/50 Index",
        is_sector_fallback=True
    ),
    "55105020": SubIndustryETF(
        code="55105020",
        name="Renewable Electricity",
        industry_code="551050",
        industry_name="Independent Power and Renewable Electricity Producers",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="QCLN",     # First Trust NASDAQ Clean Edge Green Energy
        alt_etf="ICLN",
        index_name="NASDAQ Clean Edge Green Energy Index"
    ),
    
    # =========================================================================
    # SECTOR 60: REAL ESTATE
    # =========================================================================
    
    # Industry 601010: Diversified REITs
    "60101010": SubIndustryETF(
        code="60101010",
        name="Diversified REITs",
        industry_code="601010",
        industry_name="Diversified REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",      # Vanguard Real Estate
        alt_etf="XLRE",
        index_name="MSCI US IMI Real Estate 25/50 Index"
    ),
    
    # Industry 601025: Industrial REITs
    "60102510": SubIndustryETF(
        code="60102510",
        name="Industrial REITs",
        industry_code="601025",
        industry_name="Industrial REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="INDS",     # Pacer Industrial Real Estate - highly specific
        alt_etf="VNQ",
        index_name="Benchmark Industrial Real Estate SCTR Index"
    ),
    
    # Industry 601030: Hotel & Resort REITs
    "60103010": SubIndustryETF(
        code="60103010",
        name="Hotel & Resort REITs",
        industry_code="601030",
        industry_name="Hotel & Resort REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="AWAY",     # ETFMG Travel Tech
        alt_etf="VNQ",
        index_name="Prime Travel Technology Index"
    ),
    
    # Industry 601040: Office REITs
    "60104010": SubIndustryETF(
        code="60104010",
        name="Office REITs",
        industry_code="601040",
        industry_name="Office REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",     # Real Estate Select Sector SPDR
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index"
    ),
    
    # Industry 601050: Health Care REITs
    "60105010": SubIndustryETF(
        code="60105010",
        name="Health Care REITs",
        industry_code="601050",
        industry_name="Health Care REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="REZ",      # iShares Residential and Multisector Real Estate
        alt_etf="VNQ",
        index_name="FTSE NAREIT All Residential Capped Index"
    ),
    
    # Industry 601060: Residential REITs
    "60106010": SubIndustryETF(
        code="60106010",
        name="Multi-Family Residential REITs",
        industry_code="601060",
        industry_name="Residential REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="REZ",
        alt_etf="XLRE",
        index_name="FTSE NAREIT All Residential Capped Index"
    ),
    "60106020": SubIndustryETF(
        code="60106020",
        name="Single-Family Residential REITs",
        industry_code="601060",
        industry_name="Residential REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="REZ",
        alt_etf="VNQ",
        index_name="FTSE NAREIT All Residential Capped Index"
    ),
    
    # Industry 601070: Retail REITs
    "60107010": SubIndustryETF(
        code="60107010",
        name="Retail REITs",
        industry_code="601070",
        industry_name="Retail REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="RTL",      # Invesco S&P 500 Equal Weight Real Estate
        alt_etf="XLRE",
        index_name="S&P 500 Equal Weight Real Estate Index"
    ),
    
    # Industry 601080: Specialized REITs
    "60108010": SubIndustryETF(
        code="60108010",
        name="Data Center REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="SRVR",     # Pacer Data & Infrastructure Real Estate - highly specific
        alt_etf="VNQ",
        index_name="Benchmark Data & Infrastructure Real Estate SCTR Index"
    ),
    "60108020": SubIndustryETF(
        code="60108020",
        name="Infrastructure REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="IGF",      # iShares Global Infrastructure
        alt_etf="PAVE",
        index_name="S&P Global Infrastructure Index"
    ),
    "60108030": SubIndustryETF(
        code="60108030",
        name="Self-Storage REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="XLRE",
        alt_etf="VNQ",
        index_name="Real Estate Select Sector Index"
    ),
    "60108040": SubIndustryETF(
        code="60108040",
        name="Timber REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="WOOD",
        alt_etf="CUT",
        index_name="S&P Global Timber & Forestry Index"
    ),
    "60108050": SubIndustryETF(
        code="60108050",
        name="Other Specialized REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="MSCI US IMI Real Estate 25/50 Index"
    ),
    
    # Industry 602010: Real Estate Management & Development
    "60201010": SubIndustryETF(
        code="60201010",
        name="Diversified Real Estate Activities",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="IYR",
        index_name="MSCI US IMI Real Estate 25/50 Index"
    ),
    "60201020": SubIndustryETF(
        code="60201020",
        name="Real Estate Operating Companies",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="IYR",      # iShares U.S. Real Estate
        alt_etf="VNQ",
        index_name="Dow Jones U.S. Real Estate Index"
    ),
    "60201030": SubIndustryETF(
        code="60201030",
        name="Real Estate Development",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="ITB",      # Home construction related
        alt_etf="VNQ",
        index_name="Dow Jones U.S. Select Home Construction Index"
    ),
    "60201040": SubIndustryETF(
        code="60201040",
        name="Real Estate Services",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="IYR",
        alt_etf="VNQ",
        index_name="Dow Jones U.S. Real Estate Index"
    ),
}


# =============================================================================
# SECTOR ETF FALLBACKS
# Only used when no sub-industry/industry ETF is available
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


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_etf_for_gics_code(gics_code: str) -> str:
    """
    Get the primary ETF for a GICS sub-industry code.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        ETF ticker symbol (primary or sector fallback)
    """
    if gics_code in GICS_SUBINDUSTRY_ETF_MAP:
        return GICS_SUBINDUSTRY_ETF_MAP[gics_code].primary_etf
    
    # Fallback to sector ETF
    sector_code = gics_code[:2] if len(gics_code) >= 2 else "45"
    return SECTOR_ETFS.get(sector_code, "SPY")


def get_alt_etf_for_gics_code(gics_code: str) -> Optional[str]:
    """
    Get the alternative ETF for a GICS sub-industry code.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        Alternative ETF ticker symbol or None
    """
    if gics_code in GICS_SUBINDUSTRY_ETF_MAP:
        return GICS_SUBINDUSTRY_ETF_MAP[gics_code].alt_etf
    return None


def get_subindustry_info(gics_code: str) -> Optional[SubIndustryETF]:
    """
    Get full sub-industry information including ETF mapping.
    
    Args:
        gics_code: 8-digit GICS sub-industry code
    
    Returns:
        SubIndustryETF named tuple or None
    """
    return GICS_SUBINDUSTRY_ETF_MAP.get(gics_code)


def get_etf_for_subindustry_name(name: str) -> str:
    """
    Get ETF for a sub-industry by name (fuzzy matching).
    
    Args:
        name: Sub-industry name
    
    Returns:
        ETF ticker symbol
    """
    normalized_name = name.lower().strip()
    
    # Exact match first
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        if entry.name.lower() == normalized_name:
            return entry.primary_etf
    
    # Partial match
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        if normalized_name in entry.name.lower() or entry.name.lower() in normalized_name:
            return entry.primary_etf
    
    # Default fallback
    return "SPY"


def get_all_subindustries_by_sector(sector_code: str) -> list[SubIndustryETF]:
    """
    Get all sub-industries for a given sector.
    
    Args:
        sector_code: 2-digit sector code
    
    Returns:
        List of SubIndustryETF entries
    """
    return [
        entry for entry in GICS_SUBINDUSTRY_ETF_MAP.values()
        if entry.sector_code == sector_code
    ]


def get_unique_etfs() -> set[str]:
    """
    Get all unique ETF tickers used in the mapping.
    
    Returns:
        Set of ETF ticker symbols
    """
    etfs = set()
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
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
    for entry in GICS_SUBINDUSTRY_ETF_MAP.values():
        etf = entry.primary_etf
        usage[etf] = usage.get(etf, 0) + 1
    return dict(sorted(usage.items(), key=lambda x: x[1], reverse=True))


def get_sector_fallback_count() -> int:
    """
    Get count of sub-industries using sector-level fallback ETFs.
    
    Returns:
        Number of sub-industries marked as sector fallbacks
    """
    return sum(1 for entry in GICS_SUBINDUSTRY_ETF_MAP.values() if entry.is_sector_fallback)
