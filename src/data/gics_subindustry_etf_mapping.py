"""
GICS Sub-Industry to ETF/Index Mapping.

Official GICS (Global Industry Classification Standard) sub-industry codes
mapped to their most representative ETFs and indexes.

GICS Structure:
- 11 Sectors (2-digit code)
- 25 Industry Groups (4-digit code)
- 74 Industries (6-digit code)
- 163 Sub-Industries (8-digit code)

Sources:
- MSCI/S&P GICS Structure: https://www.msci.com/gics
- SPDR Industry ETFs: https://www.ssga.com
- iShares Sector ETFs: https://www.ishares.com

Last Updated: January 2026
"""

from typing import Dict, NamedTuple, Optional


class SubIndustryETF(NamedTuple):
    """Sub-industry ETF mapping entry."""
    code: str              # 8-digit GICS code
    name: str              # Official sub-industry name
    industry_code: str     # 6-digit industry code
    industry_name: str     # Official industry name
    sector_code: str       # 2-digit sector code
    sector_name: str       # Official sector name
    primary_etf: str       # Primary ETF ticker
    alt_etf: Optional[str] # Alternative ETF (if available)
    index_name: str        # Related index name


# =============================================================================
# GICS SUB-INDUSTRY ETF MAPPINGS
# Organized by Sector -> Industry Group -> Industry -> Sub-Industry
# =============================================================================

GICS_SUBINDUSTRY_ETF_MAP: Dict[str, SubIndustryETF] = {
    
    # =========================================================================
    # SECTOR 10: ENERGY
    # =========================================================================
    
    # Industry Group 1010: Energy
    # Industry 101010: Energy Equipment & Services
    "10101010": SubIndustryETF(
        code="10101010",
        name="Oil & Gas Drilling",
        industry_code="101010",
        industry_name="Energy Equipment & Services",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XES",
        alt_etf="OIH",
        index_name="S&P Oil & Gas Equipment & Services Select Industry Index"
    ),
    "10101020": SubIndustryETF(
        code="10101020",
        name="Oil & Gas Equipment & Services",
        industry_code="101010",
        industry_name="Energy Equipment & Services",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XES",
        alt_etf="OIH",
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
        primary_etf="XLE",
        alt_etf="VDE",
        index_name="Energy Select Sector Index"
    ),
    "10102020": SubIndustryETF(
        code="10102020",
        name="Oil & Gas Exploration & Production",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="XOP",
        alt_etf="FCG",
        index_name="S&P Oil & Gas Exploration & Production Select Industry Index"
    ),
    "10102030": SubIndustryETF(
        code="10102030",
        name="Oil & Gas Refining & Marketing",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="CRAK",
        alt_etf="XLE",
        index_name="VanEck Vectors Oil Refiners ETF Index"
    ),
    "10102040": SubIndustryETF(
        code="10102040",
        name="Oil & Gas Storage & Transportation",
        industry_code="101020",
        industry_name="Oil, Gas & Consumable Fuels",
        sector_code="10",
        sector_name="Energy",
        primary_etf="AMLP",
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
        primary_etf="KOL",
        alt_etf="XLE",
        index_name="VanEck Vectors Coal ETF Index"
    ),
    
    # =========================================================================
    # SECTOR 15: MATERIALS
    # =========================================================================
    
    # Industry Group 1510: Materials
    # Industry 151010: Chemicals
    "15101010": SubIndustryETF(
        code="15101010",
        name="Commodity Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    "15101020": SubIndustryETF(
        code="15101020",
        name="Diversified Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    "15101030": SubIndustryETF(
        code="15101030",
        name="Fertilizers & Agricultural Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="MOO",
        alt_etf="XLB",
        index_name="VanEck Agribusiness ETF Index"
    ),
    "15101040": SubIndustryETF(
        code="15101040",
        name="Industrial Gases",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    "15101050": SubIndustryETF(
        code="15101050",
        name="Specialty Chemicals",
        industry_code="151010",
        industry_name="Chemicals",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    
    # Industry 151020: Construction Materials
    "15102010": SubIndustryETF(
        code="15102010",
        name="Construction Materials",
        industry_code="151020",
        industry_name="Construction Materials",
        sector_code="15",
        sector_name="Materials",
        primary_etf="PKB",
        alt_etf="XLB",
        index_name="Invesco Dynamic Building & Construction ETF Index"
    ),
    
    # Industry 151030: Containers & Packaging
    "15103010": SubIndustryETF(
        code="15103010",
        name="Metal, Glass & Plastic Containers",
        industry_code="151030",
        industry_name="Containers & Packaging",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    "15103020": SubIndustryETF(
        code="15103020",
        name="Paper & Plastic Packaging Products & Materials",
        industry_code="151030",
        industry_name="Containers & Packaging",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XLB",
        alt_etf="VAW",
        index_name="Materials Select Sector Index"
    ),
    
    # Industry 151040: Metals & Mining
    "15104010": SubIndustryETF(
        code="15104010",
        name="Aluminum",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XME",
        alt_etf="PICK",
        index_name="S&P Metals & Mining Select Industry Index"
    ),
    "15104020": SubIndustryETF(
        code="15104020",
        name="Diversified Metals & Mining",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="XME",
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
        primary_etf="COPX",
        alt_etf="XME",
        index_name="Global X Copper Miners ETF Index"
    ),
    "15104030": SubIndustryETF(
        code="15104030",
        name="Gold",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="GDX",
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
        primary_etf="GDX",
        alt_etf="SIL",
        index_name="NYSE Arca Gold Miners Index"
    ),
    "15104045": SubIndustryETF(
        code="15104045",
        name="Silver",
        industry_code="151040",
        industry_name="Metals & Mining",
        sector_code="15",
        sector_name="Materials",
        primary_etf="SIL",
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
        primary_etf="SLX",
        alt_etf="XME",
        index_name="VanEck Vectors Steel ETF Index"
    ),
    
    # Industry 151050: Paper & Forest Products
    "15105010": SubIndustryETF(
        code="15105010",
        name="Forest Products",
        industry_code="151050",
        industry_name="Paper & Forest Products",
        sector_code="15",
        sector_name="Materials",
        primary_etf="WOOD",
        alt_etf="CUT",
        index_name="iShares Global Timber & Forestry ETF Index"
    ),
    "15105020": SubIndustryETF(
        code="15105020",
        name="Paper Products",
        industry_code="151050",
        industry_name="Paper & Forest Products",
        sector_code="15",
        sector_name="Materials",
        primary_etf="WOOD",
        alt_etf="XLB",
        index_name="iShares Global Timber & Forestry ETF Index"
    ),
    
    # =========================================================================
    # SECTOR 20: INDUSTRIALS
    # =========================================================================
    
    # Industry Group 2010: Capital Goods
    # Industry 201010: Aerospace & Defense
    "20101010": SubIndustryETF(
        code="20101010",
        name="Aerospace & Defense",
        industry_code="201010",
        industry_name="Aerospace & Defense",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XAR",
        alt_etf="ITA",
        index_name="S&P Aerospace & Defense Select Industry Index"
    ),
    
    # Industry 201020: Building Products
    "20102010": SubIndustryETF(
        code="20102010",
        name="Building Products",
        industry_code="201020",
        industry_name="Building Products",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="ITB",
        alt_etf="XHB",
        index_name="Dow Jones U.S. Select Home Construction Index"
    ),
    
    # Industry 201030: Construction & Engineering
    "20103010": SubIndustryETF(
        code="20103010",
        name="Construction & Engineering",
        industry_code="201030",
        industry_name="Construction & Engineering",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="PKB",
        alt_etf="XLI",
        index_name="Invesco Dynamic Building & Construction ETF Index"
    ),
    
    # Industry 201040: Electrical Equipment
    "20104010": SubIndustryETF(
        code="20104010",
        name="Electrical Components & Equipment",
        industry_code="201040",
        industry_name="Electrical Equipment",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="GRID",
        alt_etf="XLI",
        index_name="NASDAQ Clean Edge Smart Grid Infrastructure Index"
    ),
    "20104020": SubIndustryETF(
        code="20104020",
        name="Heavy Electrical Equipment",
        industry_code="201040",
        industry_name="Electrical Equipment",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="GRID",
        alt_etf="XLI",
        index_name="NASDAQ Clean Edge Smart Grid Infrastructure Index"
    ),
    
    # Industry 201050: Industrial Conglomerates
    "20105010": SubIndustryETF(
        code="20105010",
        name="Industrial Conglomerates",
        industry_code="201050",
        industry_name="Industrial Conglomerates",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    
    # Industry 201060: Machinery
    "20106010": SubIndustryETF(
        code="20106010",
        name="Construction Machinery & Heavy Transportation Equipment",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20106015": SubIndustryETF(
        code="20106015",
        name="Agricultural & Farm Machinery",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="MOO",
        alt_etf="XLI",
        index_name="VanEck Agribusiness ETF Index"
    ),
    "20106020": SubIndustryETF(
        code="20106020",
        name="Industrial Machinery & Supplies & Components",
        industry_code="201060",
        industry_name="Machinery",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    
    # Industry 201070: Trading Companies & Distributors
    "20107010": SubIndustryETF(
        code="20107010",
        name="Trading Companies & Distributors",
        industry_code="201070",
        industry_name="Trading Companies & Distributors",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    
    # Industry Group 2020: Commercial & Professional Services
    # Industry 202010: Commercial Services & Supplies
    "20201010": SubIndustryETF(
        code="20201010",
        name="Commercial Printing",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20201050": SubIndustryETF(
        code="20201050",
        name="Environmental & Facilities Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="EVX",
        alt_etf="XLI",
        index_name="VanEck Vectors Environmental Services ETF Index"
    ),
    "20201060": SubIndustryETF(
        code="20201060",
        name="Office Services & Supplies",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20201070": SubIndustryETF(
        code="20201070",
        name="Diversified Support Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20201080": SubIndustryETF(
        code="20201080",
        name="Security & Alarm Services",
        industry_code="202010",
        industry_name="Commercial Services & Supplies",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="HACK",
        alt_etf="XLI",
        index_name="ISE Cyber Security Index"
    ),
    
    # Industry 202020: Professional Services
    "20202010": SubIndustryETF(
        code="20202010",
        name="Human Resource & Employment Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20202020": SubIndustryETF(
        code="20202020",
        name="Research & Consulting Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XLI",
        alt_etf="VIS",
        index_name="Industrial Select Sector Index"
    ),
    "20202030": SubIndustryETF(
        code="20202030",
        name="Data Processing & Outsourced Services",
        industry_code="202020",
        industry_name="Professional Services",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SKYY",
        alt_etf="XLI",
        index_name="First Trust Cloud Computing ETF Index"
    ),
    
    # Industry Group 2030: Transportation
    # Industry 203010: Air Freight & Logistics
    "20301010": SubIndustryETF(
        code="20301010",
        name="Air Freight & Logistics",
        industry_code="203010",
        industry_name="Air Freight & Logistics",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",
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
        primary_etf="JETS",
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
        primary_etf="SEA",
        alt_etf="XTN",
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
        primary_etf="XTN",
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    "20304020": SubIndustryETF(
        code="20304020",
        name="Cargo Ground Transportation",
        industry_code="203040",
        industry_name="Ground Transportation",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",
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
        primary_etf="XTN",
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    
    # Industry 203050: Transportation Infrastructure
    "20305010": SubIndustryETF(
        code="20305010",
        name="Airport Services",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    "20305020": SubIndustryETF(
        code="20305020",
        name="Highways & Railtracks",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="XTN",
        alt_etf="IYT",
        index_name="S&P Transportation Select Industry Index"
    ),
    "20305030": SubIndustryETF(
        code="20305030",
        name="Marine Ports & Services",
        industry_code="203050",
        industry_name="Transportation Infrastructure",
        sector_code="20",
        sector_name="Industrials",
        primary_etf="SEA",
        alt_etf="XTN",
        index_name="U.S. Global Sea to Sky Cargo Index"
    ),
    
    # =========================================================================
    # SECTOR 25: CONSUMER DISCRETIONARY
    # =========================================================================
    
    # Industry Group 2510: Automobiles & Components
    # Industry 251010: Automobile Components
    "25101010": SubIndustryETF(
        code="25101010",
        name="Automotive Parts & Equipment",
        industry_code="251010",
        industry_name="Automobile Components",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="XLY",
        index_name="First Trust NASDAQ Global Auto Index"
    ),
    "25101020": SubIndustryETF(
        code="25101020",
        name="Tires & Rubber",
        industry_code="251010",
        industry_name="Automobile Components",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="XLY",
        index_name="First Trust NASDAQ Global Auto Index"
    ),
    
    # Industry 251020: Automobiles
    "25102010": SubIndustryETF(
        code="25102010",
        name="Automobile Manufacturers",
        industry_code="251020",
        industry_name="Automobiles",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="XLY",
        index_name="First Trust NASDAQ Global Auto Index"
    ),
    "25102020": SubIndustryETF(
        code="25102020",
        name="Motorcycle Manufacturers",
        industry_code="251020",
        industry_name="Automobiles",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="CARZ",
        alt_etf="XLY",
        index_name="First Trust NASDAQ Global Auto Index"
    ),
    
    # Industry Group 2520: Consumer Durables & Apparel
    # Industry 252010: Household Durables
    "25201010": SubIndustryETF(
        code="25201010",
        name="Consumer Electronics",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XLY",
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index"
    ),
    "25201020": SubIndustryETF(
        code="25201020",
        name="Home Furnishings",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="XLY",
        index_name="SPDR S&P Homebuilders ETF Index"
    ),
    "25201030": SubIndustryETF(
        code="25201030",
        name="Homebuilding",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="ITB",
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
        primary_etf="XLY",
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index"
    ),
    "25201050": SubIndustryETF(
        code="25201050",
        name="Housewares & Specialties",
        industry_code="252010",
        industry_name="Household Durables",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="XLY",
        index_name="SPDR S&P Homebuilders ETF Index"
    ),
    
    # Industry 252020: Leisure Products
    "25202010": SubIndustryETF(
        code="25202010",
        name="Leisure Products",
        industry_code="252020",
        industry_name="Leisure Products",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",
        alt_etf="XLY",
        index_name="Invesco Dynamic Leisure & Entertainment ETF Index"
    ),
    
    # Industry 252030: Textiles, Apparel & Luxury Goods
    "25203010": SubIndustryETF(
        code="25203010",
        name="Apparel, Accessories & Luxury Goods",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "25203020": SubIndustryETF(
        code="25203020",
        name="Footwear",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "25203030": SubIndustryETF(
        code="25203030",
        name="Textiles",
        industry_code="252030",
        industry_name="Textiles, Apparel & Luxury Goods",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    
    # Industry Group 2530: Consumer Services
    # Industry 253010: Hotels, Restaurants & Leisure
    "25301010": SubIndustryETF(
        code="25301010",
        name="Casinos & Gaming",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="BJK",
        alt_etf="PEJ",
        index_name="VanEck Vectors Gaming ETF Index"
    ),
    "25301020": SubIndustryETF(
        code="25301020",
        name="Hotels, Resorts & Cruise Lines",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",
        alt_etf="XLY",
        index_name="Invesco Dynamic Leisure & Entertainment ETF Index"
    ),
    "25301030": SubIndustryETF(
        code="25301030",
        name="Leisure Facilities",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PEJ",
        alt_etf="XLY",
        index_name="Invesco Dynamic Leisure & Entertainment ETF Index"
    ),
    "25301040": SubIndustryETF(
        code="25301040",
        name="Restaurants",
        industry_code="253010",
        industry_name="Hotels, Restaurants & Leisure",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="PBJ",
        alt_etf="XLY",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    
    # Industry 253020: Diversified Consumer Services
    "25302010": SubIndustryETF(
        code="25302010",
        name="Education Services",
        industry_code="253020",
        industry_name="Diversified Consumer Services",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XLY",
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index"
    ),
    "25302020": SubIndustryETF(
        code="25302020",
        name="Specialized Consumer Services",
        industry_code="253020",
        industry_name="Diversified Consumer Services",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XLY",
        alt_etf="VCR",
        index_name="Consumer Discretionary Select Sector Index"
    ),
    
    # Industry Group 2550: Consumer Discretionary Distribution & Retail
    # Industry 255010: Distributors
    "25501010": SubIndustryETF(
        code="25501010",
        name="Distributors",
        industry_code="255010",
        industry_name="Distributors",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
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
        primary_etf="IBUY",
        alt_etf="XRT",
        index_name="Amplify Online Retail ETF Index"
    ),
    
    # Industry 255030: Specialty Retail
    "25503010": SubIndustryETF(
        code="25503010",
        name="Apparel Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "25503020": SubIndustryETF(
        code="25503020",
        name="Computer & Electronics Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
        index_name="S&P Retail Select Industry Index"
    ),
    "25503030": SubIndustryETF(
        code="25503030",
        name="Home Improvement Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XHB",
        alt_etf="XRT",
        index_name="SPDR S&P Homebuilders ETF Index"
    ),
    "25503040": SubIndustryETF(
        code="25503040",
        name="Other Specialty Retail",
        industry_code="255030",
        industry_name="Specialty Retail",
        sector_code="25",
        sector_name="Consumer Discretionary",
        primary_etf="XRT",
        alt_etf="XLY",
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
        index_name="First Trust NASDAQ Global Auto Index"
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
        index_name="SPDR S&P Homebuilders ETF Index"
    ),
    
    # =========================================================================
    # SECTOR 30: CONSUMER STAPLES
    # =========================================================================
    
    # Industry Group 3010: Consumer Staples Distribution & Retail
    # Industry 301010: Consumer Staples Distribution & Retail
    "30101010": SubIndustryETF(
        code="30101010",
        name="Drug Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index"
    ),
    "30101020": SubIndustryETF(
        code="30101020",
        name="Food Distributors",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    "30101030": SubIndustryETF(
        code="30101030",
        name="Food Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    "30101040": SubIndustryETF(
        code="30101040",
        name="Consumer Staples Merchandise Retail",
        industry_code="301010",
        industry_name="Consumer Staples Distribution & Retail",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index"
    ),
    
    # Industry Group 3020: Food, Beverage & Tobacco
    # Industry 302010: Beverages
    "30201010": SubIndustryETF(
        code="30201010",
        name="Brewers",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    "30201020": SubIndustryETF(
        code="30201020",
        name="Distillers & Vintners",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    "30201030": SubIndustryETF(
        code="30201030",
        name="Soft Drinks & Non-alcoholic Beverages",
        industry_code="302010",
        industry_name="Beverages",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    
    # Industry 302020: Food Products
    "30202010": SubIndustryETF(
        code="30202010",
        name="Agricultural Products & Services",
        industry_code="302020",
        industry_name="Food Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="MOO",
        alt_etf="XLP",
        index_name="VanEck Agribusiness ETF Index"
    ),
    "30202030": SubIndustryETF(
        code="30202030",
        name="Packaged Foods & Meats",
        industry_code="302020",
        industry_name="Food Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="PBJ",
        alt_etf="XLP",
        index_name="Invesco Dynamic Food & Beverage ETF Index"
    ),
    
    # Industry 302030: Tobacco
    "30203010": SubIndustryETF(
        code="30203010",
        name="Tobacco",
        industry_code="302030",
        industry_name="Tobacco",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index"
    ),
    
    # Industry Group 3030: Household & Personal Products
    # Industry 303010: Household Products
    "30301010": SubIndustryETF(
        code="30301010",
        name="Household Products",
        industry_code="303010",
        industry_name="Household Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index"
    ),
    
    # Industry 303020: Personal Care Products
    "30302010": SubIndustryETF(
        code="30302010",
        name="Personal Care Products",
        industry_code="303020",
        industry_name="Personal Care Products",
        sector_code="30",
        sector_name="Consumer Staples",
        primary_etf="XLP",
        alt_etf="VDC",
        index_name="Consumer Staples Select Sector Index"
    ),
    
    # =========================================================================
    # SECTOR 35: HEALTH CARE
    # =========================================================================
    
    # Industry Group 3510: Health Care Equipment & Services
    # Industry 351010: Health Care Equipment & Supplies
    "35101010": SubIndustryETF(
        code="35101010",
        name="Health Care Equipment",
        industry_code="351010",
        industry_name="Health Care Equipment & Supplies",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHI",
        alt_etf="XLV",
        index_name="Dow Jones U.S. Select Medical Equipment Index"
    ),
    "35101020": SubIndustryETF(
        code="35101020",
        name="Health Care Supplies",
        industry_code="351010",
        industry_name="Health Care Equipment & Supplies",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHI",
        alt_etf="XLV",
        index_name="Dow Jones U.S. Select Medical Equipment Index"
    ),
    
    # Industry 351020: Health Care Providers & Services
    "35102010": SubIndustryETF(
        code="35102010",
        name="Health Care Distributors",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",
        alt_etf="XLV",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    "35102015": SubIndustryETF(
        code="35102015",
        name="Health Care Services",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",
        alt_etf="XLV",
        index_name="Dow Jones U.S. Select Health Care Providers Index"
    ),
    "35102020": SubIndustryETF(
        code="35102020",
        name="Health Care Facilities",
        industry_code="351020",
        industry_name="Health Care Providers & Services",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="IHF",
        alt_etf="XLV",
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
        alt_etf="XLV",
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
        primary_etf="EDOC",
        alt_etf="XLV",
        index_name="Global X Telemedicine & Digital Health ETF Index"
    ),
    
    # Industry Group 3520: Pharmaceuticals, Biotechnology & Life Sciences
    # Industry 352010: Biotechnology
    "35201010": SubIndustryETF(
        code="35201010",
        name="Biotechnology",
        industry_code="352010",
        industry_name="Biotechnology",
        sector_code="35",
        sector_name="Health Care",
        primary_etf="XBI",
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
        primary_etf="XPH",
        alt_etf="IHE",
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
        primary_etf="XBI",
        alt_etf="XLV",
        index_name="S&P Biotechnology Select Industry Index"
    ),
    
    # =========================================================================
    # SECTOR 40: FINANCIALS
    # =========================================================================
    
    # Industry Group 4010: Banks
    # Industry 401010: Banks
    "40101010": SubIndustryETF(
        code="40101010",
        name="Diversified Banks",
        industry_code="401010",
        industry_name="Banks",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KBE",
        alt_etf="XLF",
        index_name="S&P Banks Select Industry Index"
    ),
    "40101015": SubIndustryETF(
        code="40101015",
        name="Regional Banks",
        industry_code="401010",
        industry_name="Banks",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KRE",
        alt_etf="KBE",
        index_name="S&P Regional Banks Select Industry Index"
    ),
    
    # Industry Group 4020: Financial Services
    # Industry 402010: Diversified Financial Services
    "40201010": SubIndustryETF(
        code="40201010",
        name="Diversified Financial Services",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",
        alt_etf="VFH",
        index_name="Financial Select Sector Index"
    ),
    "40201020": SubIndustryETF(
        code="40201020",
        name="Multi-Sector Holdings",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",
        alt_etf="VFH",
        index_name="Financial Select Sector Index"
    ),
    "40201030": SubIndustryETF(
        code="40201030",
        name="Specialized Finance",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",
        alt_etf="VFH",
        index_name="Financial Select Sector Index"
    ),
    "40201040": SubIndustryETF(
        code="40201040",
        name="Commercial & Residential Mortgage Finance",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="REM",
        alt_etf="XLF",
        index_name="FTSE NAREIT All Mortgage Capped Index"
    ),
    "40201050": SubIndustryETF(
        code="40201050",
        name="Transaction & Payment Processing Services",
        industry_code="402010",
        industry_name="Diversified Financial Services",
        sector_code="40",
        sector_name="Financials",
        primary_etf="IPAY",
        alt_etf="XLF",
        index_name="NASDAQ CTA Global Digital Payments Index"
    ),
    
    # Industry 402020: Consumer Finance
    "40202010": SubIndustryETF(
        code="40202010",
        name="Consumer Finance",
        industry_code="402020",
        industry_name="Consumer Finance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="XLF",
        alt_etf="VFH",
        index_name="Financial Select Sector Index"
    ),
    
    # Industry 402030: Capital Markets
    "40203010": SubIndustryETF(
        code="40203010",
        name="Asset Management & Custody Banks",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",
        alt_etf="XLF",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    "40203020": SubIndustryETF(
        code="40203020",
        name="Investment Banking & Brokerage",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",
        alt_etf="XLF",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    "40203030": SubIndustryETF(
        code="40203030",
        name="Diversified Capital Markets",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",
        alt_etf="XLF",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    "40203040": SubIndustryETF(
        code="40203040",
        name="Financial Exchanges & Data",
        industry_code="402030",
        industry_name="Capital Markets",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KCE",
        alt_etf="XLF",
        index_name="S&P Capital Markets Select Industry Index"
    ),
    
    # Industry 402040: Mortgage Real Estate Investment Trusts (REITs)
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
    
    # Industry Group 4030: Insurance
    # Industry 403010: Insurance
    "40301010": SubIndustryETF(
        code="40301010",
        name="Insurance Brokers",
        industry_code="403010",
        industry_name="Insurance",
        sector_code="40",
        sector_name="Financials",
        primary_etf="KIE",
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
        primary_etf="KIE",
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
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
        primary_etf="KIE",
        alt_etf="IAK",
        index_name="S&P Insurance Select Industry Index"
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
    
    # Industry Group 4510: Software & Services
    # Industry 451020: IT Services
    "45102010": SubIndustryETF(
        code="45102010",
        name="IT Consulting & Other Services",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IGV",
        alt_etf="XLK",
        index_name="iShares Expanded Tech-Software Sector ETF Index"
    ),
    "45102020": SubIndustryETF(
        code="45102020",
        name="Internet Services & Infrastructure",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XWEB",
        alt_etf="SKYY",
        index_name="SPDR S&P Internet ETF Index"
    ),
    "45102030": SubIndustryETF(
        code="45102030",
        name="Data Processing & Outsourced Services",
        industry_code="451020",
        industry_name="IT Services",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="SKYY",
        alt_etf="XLK",
        index_name="First Trust Cloud Computing ETF Index"
    ),
    
    # Industry 451030: Software
    "45103010": SubIndustryETF(
        code="45103010",
        name="Application Software",
        industry_code="451030",
        industry_name="Software",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IGV",
        alt_etf="XSW",
        index_name="iShares Expanded Tech-Software Sector ETF Index"
    ),
    "45103020": SubIndustryETF(
        code="45103020",
        name="Systems Software",
        industry_code="451030",
        industry_name="Software",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="IGV",
        alt_etf="XSW",
        index_name="iShares Expanded Tech-Software Sector ETF Index"
    ),
    
    # Industry Group 4520: Technology Hardware & Equipment
    # Industry 452010: Communications Equipment
    "45201010": SubIndustryETF(
        code="45201010",
        name="Communications Equipment",
        industry_code="452010",
        industry_name="Communications Equipment",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
        alt_etf="XLK",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    
    # Industry 452020: Technology Hardware, Storage & Peripherals
    "45202010": SubIndustryETF(
        code="45202010",
        name="Technology Hardware, Storage & Peripherals",
        industry_code="452020",
        industry_name="Technology Hardware, Storage & Peripherals",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
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
        primary_etf="XTH",
        alt_etf="XLK",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    "45203015": SubIndustryETF(
        code="45203015",
        name="Electronic Components",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
        alt_etf="XLK",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    "45203020": SubIndustryETF(
        code="45203020",
        name="Electronic Manufacturing Services",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
        alt_etf="XLK",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    "45203030": SubIndustryETF(
        code="45203030",
        name="Technology Distributors",
        industry_code="452030",
        industry_name="Electronic Equipment, Instruments & Components",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XTH",
        alt_etf="XLK",
        index_name="S&P Technology Hardware Select Industry Index"
    ),
    
    # Industry Group 4530: Semiconductors & Semiconductor Equipment
    # Industry 453010: Semiconductors & Semiconductor Equipment
    "45301010": SubIndustryETF(
        code="45301010",
        name="Semiconductor Materials & Equipment",
        industry_code="453010",
        industry_name="Semiconductors & Semiconductor Equipment",
        sector_code="45",
        sector_name="Information Technology",
        primary_etf="XSD",
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
        primary_etf="SMH",
        alt_etf="XSD",
        index_name="VanEck Semiconductor ETF Index (MVIS US Listed Semiconductor 25 Index)"
    ),
    
    # =========================================================================
    # SECTOR 50: COMMUNICATION SERVICES
    # =========================================================================
    
    # Industry Group 5010: Telecommunication Services
    # Industry 501010: Diversified Telecommunication Services
    "50101010": SubIndustryETF(
        code="50101010",
        name="Alternative Carriers",
        industry_code="501010",
        industry_name="Diversified Telecommunication Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="IYZ",
        alt_etf="XLC",
        index_name="iShares U.S. Telecommunications ETF Index"
    ),
    "50101020": SubIndustryETF(
        code="50101020",
        name="Integrated Telecommunication Services",
        industry_code="501010",
        industry_name="Diversified Telecommunication Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="IYZ",
        alt_etf="VOX",
        index_name="iShares U.S. Telecommunications ETF Index"
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
        alt_etf="VOX",
        index_name="iShares U.S. Telecommunications ETF Index"
    ),
    
    # Industry Group 5020: Media & Entertainment
    # Industry 502010: Media
    "50201010": SubIndustryETF(
        code="50201010",
        name="Advertising",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index"
    ),
    "50201020": SubIndustryETF(
        code="50201020",
        name="Broadcasting",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index"
    ),
    "50201030": SubIndustryETF(
        code="50201030",
        name="Cable & Satellite",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index"
    ),
    "50201040": SubIndustryETF(
        code="50201040",
        name="Publishing",
        industry_code="502010",
        industry_name="Media",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="XLC",
        alt_etf="VOX",
        index_name="Communication Services Select Sector Index"
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
        alt_etf="XLC",
        index_name="Invesco Dynamic Leisure & Entertainment ETF Index"
    ),
    "50202020": SubIndustryETF(
        code="50202020",
        name="Interactive Home Entertainment",
        industry_code="502020",
        industry_name="Entertainment",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="ESPO",
        alt_etf="HERO",
        index_name="VanEck Video Gaming and eSports ETF Index"
    ),
    
    # Industry 502030: Interactive Media & Services
    "50203010": SubIndustryETF(
        code="50203010",
        name="Interactive Media & Services",
        industry_code="502030",
        industry_name="Interactive Media & Services",
        sector_code="50",
        sector_name="Communication Services",
        primary_etf="SOCL",
        alt_etf="XLC",
        index_name="Global X Social Media ETF Index"
    ),
    
    # =========================================================================
    # SECTOR 55: UTILITIES
    # =========================================================================
    
    # Industry Group 5510: Utilities
    # Industry 551010: Electric Utilities
    "55101010": SubIndustryETF(
        code="55101010",
        name="Electric Utilities",
        industry_code="551010",
        industry_name="Electric Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",
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
        primary_etf="XLU",
        alt_etf="VPU",
        index_name="Utilities Select Sector Index"
    ),
    
    # Industry 551030: Multi-Utilities
    "55103010": SubIndustryETF(
        code="55103010",
        name="Multi-Utilities",
        industry_code="551030",
        industry_name="Multi-Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="XLU",
        alt_etf="VPU",
        index_name="Utilities Select Sector Index"
    ),
    
    # Industry 551040: Water Utilities
    "55104010": SubIndustryETF(
        code="55104010",
        name="Water Utilities",
        industry_code="551040",
        industry_name="Water Utilities",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="PHO",
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
        primary_etf="XLU",
        alt_etf="VPU",
        index_name="Utilities Select Sector Index"
    ),
    "55105020": SubIndustryETF(
        code="55105020",
        name="Renewable Electricity",
        industry_code="551050",
        industry_name="Independent Power and Renewable Electricity Producers",
        sector_code="55",
        sector_name="Utilities",
        primary_etf="QCLN",
        alt_etf="ICLN",
        index_name="NASDAQ Clean Edge Green Energy Index"
    ),
    
    # =========================================================================
    # SECTOR 60: REAL ESTATE
    # =========================================================================
    
    # Industry Group 6010: Equity Real Estate Investment Trusts (REITs)
    # Industry 601010: Diversified REITs
    "60101010": SubIndustryETF(
        code="60101010",
        name="Diversified REITs",
        industry_code="601010",
        industry_name="Diversified REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    
    # Industry 601025: Industrial REITs
    "60102510": SubIndustryETF(
        code="60102510",
        name="Industrial REITs",
        industry_code="601025",
        industry_name="Industrial REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="INDS",
        alt_etf="VNQ",
        index_name="Pacer Benchmark Industrial Real Estate ETF Index"
    ),
    
    # Industry 601030: Hotel & Resort REITs
    "60103010": SubIndustryETF(
        code="60103010",
        name="Hotel & Resort REITs",
        industry_code="601030",
        industry_name="Hotel & Resort REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="PEJ",
        alt_etf="VNQ",
        index_name="Invesco Dynamic Leisure & Entertainment ETF Index"
    ),
    
    # Industry 601040: Office REITs
    "60104010": SubIndustryETF(
        code="60104010",
        name="Office REITs",
        industry_code="601040",
        industry_name="Office REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    
    # Industry 601050: Health Care REITs
    "60105010": SubIndustryETF(
        code="60105010",
        name="Health Care REITs",
        industry_code="601050",
        industry_name="Health Care REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
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
        alt_etf="VNQ",
        index_name="iShares Residential and Multisector Real Estate ETF Index"
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
        index_name="iShares Residential and Multisector Real Estate ETF Index"
    ),
    
    # Industry 601070: Retail REITs
    "60107010": SubIndustryETF(
        code="60107010",
        name="Retail REITs",
        industry_code="601070",
        industry_name="Retail REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="RTL",
        alt_etf="VNQ",
        index_name="Invesco S&P 500 Equal Weight Real Estate ETF Index"
    ),
    
    # Industry 601080: Specialized REITs
    "60108010": SubIndustryETF(
        code="60108010",
        name="Data Center REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="SRVR",
        alt_etf="VNQ",
        index_name="Pacer Benchmark Data & Infrastructure Real Estate ETF Index"
    ),
    "60108020": SubIndustryETF(
        code="60108020",
        name="Infrastructure REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    "60108030": SubIndustryETF(
        code="60108030",
        name="Self-Storage REITs",
        industry_code="601080",
        industry_name="Specialized REITs",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
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
        index_name="iShares Global Timber & Forestry ETF Index"
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
        index_name="Vanguard Real Estate ETF Index"
    ),
    
    # Industry Group 6020: Real Estate Management & Development
    # Industry 602010: Real Estate Management & Development
    "60201010": SubIndustryETF(
        code="60201010",
        name="Diversified Real Estate Activities",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    "60201020": SubIndustryETF(
        code="60201020",
        name="Real Estate Operating Companies",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    "60201030": SubIndustryETF(
        code="60201030",
        name="Real Estate Development",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
    "60201040": SubIndustryETF(
        code="60201040",
        name="Real Estate Services",
        industry_code="602010",
        industry_name="Real Estate Management & Development",
        sector_code="60",
        sector_name="Real Estate",
        primary_etf="VNQ",
        alt_etf="XLRE",
        index_name="Vanguard Real Estate ETF Index"
    ),
}


# =============================================================================
# SECTOR ETF FALLBACKS
# Used when no specific sub-industry ETF is available
# =============================================================================

SECTOR_ETFS: Dict[str, str] = {
    "10": "XLE",   # Energy
    "15": "XLB",   # Materials
    "20": "XLI",   # Industrials
    "25": "XLY",   # Consumer Discretionary
    "30": "XLP",   # Consumer Staples
    "35": "XLV",   # Health Care
    "40": "XLF",   # Financials
    "45": "XLK",   # Information Technology
    "50": "XLC",   # Communication Services
    "55": "XLU",   # Utilities
    "60": "XLRE",  # Real Estate
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

