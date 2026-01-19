"""
Extended list of US stock tickers for database expansion.

This module provides additional ticker symbols beyond S&P 500/400/600 indices.
These are sourced from Russell 3000, Nasdaq listings, and other US exchanges.

Organized by StockCharts industry codes for proper sub-industry assignment.

Code Format: SSIIXX
- SS: Sector code (2 digits)
- II: Industry number within sector (2 digits, 01-99)
- XX: Reserved for sub-industry expansion (00 by default)
"""

from typing import Dict, List

# =============================================================================
# SECTOR 10: ENERGY
# =============================================================================

# 100100 - Coal
INDUSTRY_100100_COAL: List[str] = [
    "ARCH", "HCC", "BTU", "CEIX", "ARLP", "AMR", "METC", "SXC", "HNRG",
]

# 100200 - Oil & Gas - Drilling
INDUSTRY_100200_OIL_GAS_DRILLING: List[str] = [
    "HP", "NBR", "RIG", "VAL", "DO", "NE", "PTEN", "PDS", "BORR", "DRQ", "NINE",
    "USWS", "KLXE", "VTOL",
]

# 100300 - Oil & Gas - E&P
INDUSTRY_100300_OIL_GAS_EP: List[str] = [
    "APA", "DVN", "FANG", "EOG", "PXD", "COP", "OXY", "MRO", "CLR",  # Removed: SU, CVE (Canadian)
    "PR", "MTDR", "CTRA", "CHRD", "OVV", "MGY", "SM", "CRGY", "SBOW", "CNX",
    "AR", "SWN", "EQT", "VTLE", "REPX", "ESTE", "REI", "SD", "AXAS",
    "SNDE", "EPSN", "WTI", "NGAS", "WFRD", "BRY", "SGML", "CIVI", "BKV", "VNOM",
    "CPE", "GPOR", "GRNT", "HPK", "CDEV", "WLL", "NOG", "KOS", "RRC",
    "TELL", "NEXT", "ZN", "LONE",
]

# 100400 - Oil & Gas - Equipment & Services
INDUSTRY_100400_OIL_GAS_EQUIPMENT: List[str] = [
    "SLB", "HAL", "BKR", "NOV", "FTI", "WHD", "WTTR", "OII", "LBRT", "NEX",
    "RES", "HLX", "CLB", "XPRO", "BOOM", "GEL", "TTI", "PUMP", "DWSN",
    "AROC", "SOI", "TDW", "GIFI", "MTRX", "MPLN", "OIS",
]

# 100500 - Oil & Gas - Integrated
INDUSTRY_100500_OIL_GAS_INTEGRATED: List[str] = [
    "XOM", "CVX", "SHEL", "TTE", "BP",  # Removed: ENB, IMO (Canadian)
]

# 100600 - Oil & Gas - Pipelines
INDUSTRY_100600_OIL_GAS_PIPELINES: List[str] = [
    "KMI", "WMB", "OKE", "ET", "MPLX", "EPD", "PAA", "WES", "TRGP", "AM",
    "DCP", "USAC", "SMLP", "NGL", "CEQP", "ENLC", "ETRN", "KNTK", "DTM",
    "GLP", "PAGP", "BSM", "CLNE", "CPLP", "SPH",
]

# 100700 - Oil & Gas - Refining
INDUSTRY_100700_OIL_GAS_REFINING: List[str] = [
    "VLO", "PSX", "MPC", "DK", "PBF", "CVI", "DINO", "CLMT", "CAPL", "HEP",
    "NS", "INT", "PARR", "NTI",
]


# =============================================================================
# SECTOR 15: MATERIALS
# =============================================================================

# 150100 - Aluminum
INDUSTRY_150100_ALUMINUM: List[str] = [
    "AA", "ARNC", "CENX", "KALU", "CSTM",
]

# 150200 - Building Materials
INDUSTRY_150200_BUILDING_MATERIALS: List[str] = [
    "VMC", "MLM", "EXP", "USLM", "SUM", "ROCK", "MDU", "CNHI", "CRH",
    "CMCO", "KNF", "TGLS", "APOG", "ASTE", "PGTI",
]

# 150300 - Chemicals
INDUSTRY_150300_CHEMICALS: List[str] = [
    "DOW", "LYB", "CE", "EMN", "HUN", "WLK", "OLN", "TROX", "KRO", "MEOH",
    "ASIX", "IOSP", "KWR", "NGVT", "FUL", "RPM", "BCPC", "HWKN",
    "APD", "ECL", "SHW", "PPG", "ALB", "IFF", "AVNT", "AXTA", "ASH",
    "CBT", "CC", "FOE", "LTH", "MTX", "LTHM", "LIN",
]

# 150400 - Containers & Packaging
INDUSTRY_150400_CONTAINERS_PACKAGING: List[str] = [
    "IP", "WRK", "PKG", "SON", "SEE", "BLL", "CCK", "ATR", "GEF", "BERY",
    "UFPT", "PACK", "GPK",
]

# 150500 - Copper
INDUSTRY_150500_COPPER: List[str] = [
    "SCCO", "FCX", "HBM", "ERO", "NEXA",  # Removed: TECK (Canadian)
]

# 150600 - Fertilizers
INDUSTRY_150600_FERTILIZERS: List[str] = [
    "CF", "MOS", "FMC", "SMG", "CTVA", "ICL", "IPI", "ADM",  # Removed: NTR (Canadian)
    "AGFY", "GRWG", "APPH", "AVO", "SEED", "LMNR",
]

# 150700 - Gold
INDUSTRY_150700_GOLD: List[str] = [
    "NEM", "GOLD", "KGC", "AU", "RGLD", "FNV", "OR", "SAND",  # Removed: AEM, WPM (Canadian)
    "SSRM", "BTG", "IAG", "HMY", "DRD", "NGD", "GATO", "EGO",
]

# 150800 - Metals & Mining
INDUSTRY_150800_METALS_MINING: List[str] = [
    "NUE", "CLF", "X", "ATI", "RS", "CRS", "WOR", "HAYN",
    "VALE", "RIO", "BHP", "MP", "LAC", "UUUU", "CCJ",
]

# 150900 - Paper & Forest Products
INDUSTRY_150900_PAPER_FOREST: List[str] = [
    "CLW", "LSB", "SWM", "RYN", "WY", "PCH", "UFS", "UFPI", "LPX",
]

# 151000 - Silver
INDUSTRY_151000_SILVER: List[str] = [
    "HL", "PAAS", "AG", "EXK", "CDE", "FSM", "MAG", "SVM", "MUX",
    "SILV", "GPL",
]

# 151100 - Specialty Chemicals
INDUSTRY_151100_SPECIALTY_CHEMICALS: List[str] = [
    "HXL", "NEU", "GPRE", "RYAM",
]

# 151200 - Steel
INDUSTRY_151200_STEEL: List[str] = [
    "TX", "TMST", "SCHN", "RYI", "SXC", "WS", "WIRE",
    "MATV", "CMC", "STLD", "MT", "PKX", "SID",
]


# =============================================================================
# SECTOR 20: INDUSTRIALS
# =============================================================================

# 200100 - Aerospace
INDUSTRY_200100_AEROSPACE: List[str] = [
    "BA", "LMT", "NOC", "GD", "RTX", "HII", "TDG", "LHX", "HWM", "TXT",
    "AXON", "CW", "SPR", "HXL", "DCO", "AIR", "VSEC", "KTOS", "MRCY",
    "AVAV", "BWXT", "LDOS", "CACI", "SAIC", "PSN",
    "SPCE", "ACHR", "JOBY", "LILM", "BLDE", "ASTR", "RKLB", "ASTS",
    "IRDM", "GSAT", "SATS", "VSAT",
]

# 200200 - Air Freight
INDUSTRY_200200_AIR_FREIGHT: List[str] = [
    "FDX", "UPS", "EXPD", "CHRW", "XPO", "GXO", "FWRD",
]

# 200300 - Airlines
INDUSTRY_200300_AIRLINES: List[str] = [
    "DAL", "UAL", "LUV", "AAL", "ALK", "JBLU", "SAVE", "ALGT", "SKYW", "ULCC",
    "HA", "MESA", "RYAAY", "AZUL", "GOL",
]

# 200400 - Building Products
INDUSTRY_200400_BUILDING_PRODUCTS: List[str] = [
    "JCI", "CARR", "TT", "LII", "MAS", "FBHS", "AWI", "DOOR", "AZEK", "BLD",
    "APOG", "GFF", "PGTI", "JELD", "TILE", "TREX", "SSD", "BLDR", "BCC",
    "OC", "IBP", "CSWI", "AAON", "NX", "UFPI", "AMWD", "CNR",
]

# 200500 - Business Services
INDUSTRY_200500_BUSINESS_SERVICES: List[str] = [
    "ACN", "VRSK", "FTV", "TRI", "BR", "EEFT", "EFX", "EXPO", "FCN", "FORR",
    "HURN", "INFO", "KFRC", "MAN", "MMS", "TNET", "WST", "RHI", "HSKA", "BAH",
    "CRAI", "ICFI", "GMS", "MANT", "EXLS", "PRGS",
]

# 200600 - Capital Goods
INDUSTRY_200600_CAPITAL_GOODS: List[str] = [
    "MMM", "HON", "ITW", "ROP", "DHR", "IEP",
]

# 200700 - Commercial Vehicles
INDUSTRY_200700_COMMERCIAL_VEHICLES: List[str] = [
    "PCAR", "CMI", "OSK", "NAV", "WABCO",
]

# 200800 - Conglomerates
INDUSTRY_200800_CONGLOMERATES: List[str] = [
    "GE", "ABB",
]

# 200900 - Construction Materials
INDUSTRY_200900_CONSTRUCTION_MATERIALS: List[str] = [
    "ACM", "MTZ", "PWR", "DY", "EME", "FIX", "PRIM", "TPC", "MYRG", "STRL",
    "ORN", "IESC", "GVA", "KBR", "FLR", "AGX", "NVEE", "TTEK", "WSC",
]

# 201000 - Defense
INDUSTRY_201000_DEFENSE: List[str] = [
    "RCAT", "VVX", "PKE", "GILT",
]

# 201100 - Electrical Equipment
INDUSTRY_201100_ELECTRICAL_EQUIPMENT: List[str] = [
    "ETN", "ROK", "EMR", "AME", "RBC", "GNRC", "AZZ", "ATKR", "WCC", "HUBB",
    "POWL", "AYI", "EAF", "WIRE", "NVT", "VRT", "PLUG", "FLUX",
    "FCEL", "BLDP", "HYLN", "BLNK", "CHPT", "EVGO",
]

# 201200 - Engineering & Construction
INDUSTRY_201200_ENGINEERING_CONSTRUCTION: List[str] = [
    "ROAD",
]

# 201300 - Environmental Services
INDUSTRY_201300_ENVIRONMENTAL_SERVICES: List[str] = [
    "WM", "RSG", "WCN", "CWST", "SRCL", "CLH", "ECOL", "HCCI", "NVRI",
]

# 201400 - Farm Machinery
INDUSTRY_201400_FARM_MACHINERY: List[str] = [
    "CAT", "DE", "AGCO", "CNHI", "ALG", "LNN", "TITN",
]

# 201500 - Heavy Machinery
INDUSTRY_201500_HEAVY_MACHINERY: List[str] = [
    "SWK", "TTC", "KMT", "MEC", "NPO", "CFX", "HAYW", "HLIO", "MIDD", "MTW", "SXI",
    "TWI", "WTS", "BMI", "FLOW", "HI", "AIT", "GTLS", "IDEX", "IEX",
    "ITT", "LECO", "PNR", "RXO", "TKR", "WMS", "XYL", "CR", "PH",
    "IR", "FLS", "DOV",
]

# 201600 - Industrial Distribution
INDUSTRY_201600_INDUSTRIAL_DISTRIBUTION: List[str] = [
    "GWW", "FAST", "WSO", "MSM", "SITE", "DXPE", "DNOW", "DXP", "HDSN", "PKOH",
    "SYX", "HDS", "CCMP", "POOL", "EVI", "FELE",
]

# 201700 - Marine Shipping
INDUSTRY_201700_MARINE_SHIPPING: List[str] = [
    "SBLK", "DAC", "ZIM", "INSW", "NMM", "GOGL", "STNG", "EURN", "FLNG", "TNK",
    "CPLP", "SALT", "DSX", "GNK",
]

# 201800 - Packaging
INDUSTRY_201800_PACKAGING: List[str] = [
    "TRS", "TREC", "CKH",
]

# 201900 - Railroads
INDUSTRY_201900_RAILROADS: List[str] = [
    "UNP", "CSX", "NSC", "WAB", "GBX", "TRN",
]

# 202000 - Security Services
INDUSTRY_202000_SECURITY_SERVICES: List[str] = [
    "ALLE", "MSA", "NSSC", "OSIS", "ARLO",
]

# 202100 - Staffing
INDUSTRY_202100_STAFFING: List[str] = [
    "ABM", "CTAS", "ARMK", "BCO", "BRC", "NSIT", "SP", "CPRT",
    "ROLL", "LAUR", "BFAM", "TBI",
]

# 202200 - Trucking
INDUSTRY_202200_TRUCKING: List[str] = [
    "JBHT", "ODFL", "SAIA", "WERN", "LSTR", "HTLD", "KNX", "MRTN", "SNDR",
    "ARCB", "HUBG", "ECHO", "RLGT", "DSKE", "USAK", "USX",
]

# 202300 - Waste Management
INDUSTRY_202300_WASTE_MANAGEMENT: List[str] = [
    "VSE", "ADMS",
]


# =============================================================================
# SECTOR 25: CONSUMER DISCRETIONARY
# =============================================================================

# 250100 - Auto Parts
INDUSTRY_250100_AUTO_PARTS: List[str] = [
    "APTV", "BWA", "LEA", "MGA", "ALV", "ADNT", "AXL", "GNTX", "VC", "DAN",
    "MOD", "PHIN", "SMP", "THRM", "DORM", "FOXF", "LKQ", "SRI",
    "STRT", "SUP", "TEN", "MTOR", "SHYF",
]

# 250200 - Automobiles
INDUSTRY_250200_AUTOMOBILES: List[str] = [
    "F", "GM", "TSLA", "RIVN", "LCID", "FSR", "NIO", "XPEV", "LI",
    "WKHS", "SOLO", "LAZR", "MVIS", "LIDR",
    "OUST", "AEVA", "INVZ", "HOG", "PII", "WGO", "THO", "CWH", "LCII",
]

# 250300 - Casinos & Gaming
INDUSTRY_250300_CASINOS_GAMING: List[str] = [
    "LVS", "WYNN", "MGM", "CZR", "DKNG", "PENN", "BYD", "MLCO", "RRR", "GDEN",
    "IGT", "SGMS", "GAN", "RSI", "BALY", "CHDN", "EVRI",
    "AGS",
]

# 250400 - Consumer Electronics
INDUSTRY_250400_CONSUMER_ELECTRONICS: List[str] = [
    "GPRO", "KOSS", "VUZI", "UEIC", "VOXX", "SONY",
]

# 250500 - Department Stores
INDUSTRY_250500_DEPARTMENT_STORES: List[str] = [
    "M", "JWN", "DDS", "KSS",
]

# 250600 - Footwear
INDUSTRY_250600_FOOTWEAR: List[str] = [
    "NKE", "SKX", "DECK", "CROX", "SHOO", "WWW", "WEYS", "CAL",
]

# 250700 - Furnishings
INDUSTRY_250700_FURNISHINGS: List[str] = [
    "RH", "WSM", "ARHS", "ETH", "LOVE", "SNBR", "PRPL", "CSPR", "TPX", "LEG",
    "HVT", "FLXS", "PATK", "AMWD", "LCUT",
]

# 250800 - General Merchandise
INDUSTRY_250800_GENERAL_MERCHANDISE: List[str] = [
    "WMT", "TGT", "COST", "DG", "DLTR", "FIVE", "OLLI", "BIG",
]

# 250900 - Home Improvement
INDUSTRY_250900_HOME_IMPROVEMENT: List[str] = [
    "HD", "LOW", "FND", "LL", "SHC",
]

# 251000 - Homebuilders
INDUSTRY_251000_HOMEBUILDERS: List[str] = [
    "DHI", "LEN", "PHM", "NVR", "TOL", "KBH", "TMHC", "MDC", "MTH", "MHO",
    "TPH", "SKY", "CCS", "HOV", "BZH", "GRBK", "CVCO", "LGIH", "DFH", "LEGH",
    "UHG", "NOAH",
]

# 251100 - Hotels & Motels
INDUSTRY_251100_HOTELS_MOTELS: List[str] = [
    "MAR", "HLT", "H", "IHG", "WH", "CHH", "VAC", "TNL", "PLYA", "HGV",
    "BHR", "STAY", "CLDT", "HT", "RHP", "SVC", "AHT", "DRH",
    "PK", "PEB", "RLJ", "SHO", "XHR", "INN", "SOHO",
]

# 251200 - Housewares
INDUSTRY_251200_HOUSEWARES: List[str] = [
    "WHR", "IRBT", "HBB",
]

# 251300 - Leisure Products
INDUSTRY_251300_LEISURE_PRODUCTS: List[str] = [
    "HAS", "MAT", "POOL", "BC", "PTON", "NLS", "FNKO", "JAKK", "PLNT",
    "PLAY", "VSTO", "YETI", "FIZZ",
    "GOLF", "FUN", "SIX", "SEAS", "MTN",
]

# 251400 - Recreational Services
INDUSTRY_251400_RECREATIONAL_SERVICES: List[str] = [
    "XPOF",
]

# 251500 - Recreational Vehicles
INDUSTRY_251500_RECREATIONAL_VEHICLES: List[str] = [
    "LCII", "REV",
]

# 251600 - Restaurants
INDUSTRY_251600_RESTAURANTS: List[str] = [
    "MCD", "SBUX", "DPZ", "CMG", "YUM", "QSR", "WEN", "DNUT", "PZZA", "DRI",
    "TXRH", "BLMN", "EAT", "CAKE", "DIN", "JACK", "TACO", "WING", "SHAK", "BROS",
    "CAVA", "SG", "LOCO", "ARCO", "NDLS", "PBPB", "KRUS", "BJRI", "FAT",
    "RAVE", "RRGB", "RUTH", "NATH", "CBRL",
]

# 251700 - Retail Apparel
INDUSTRY_251700_RETAIL_APPAREL: List[str] = [
    "TPR", "VFC", "PVH", "RL", "CPRI", "GIII", "GIL", "COLM",  # Removed: LULU (Canadian)
    "UAA", "GES", "LEVI", "HBI", "SCVL", "FIGS", "ONON", "HELE",  # Removed: GOOS (Canadian)
    "BOOT", "CURV", "DXLG", "CTRN", "EXPR", "AEO", "ANF", "BKE", "ZUMZ",
]

# 251800 - Specialty Retail
INDUSTRY_251800_SPECIALTY_RETAIL: List[str] = [
    "AMZN", "BBY", "GME", "CHWY", "W", "ETSY", "EBAY", "WISH",  # Removed: SHOP (Canadian)
    "TDUP", "REAL", "PRTS", "TCS", "ASO", "DKS", "HIBB", "SPWH",
    "PLCE", "BURL", "ROST", "TJX", "GPS", "AAP",
    "AZO", "ORLY", "GPC", "MNRO", "MPAA", "MOV",
    "SIG", "KAR", "CPRT", "SBH", "ULTA", "EYE", "WOOF",
]

# 251900 - Textiles & Apparel
INDUSTRY_251900_TEXTILES_APPAREL: List[str] = [
    "CATO", "HNST",
]

# 252000 - Tires
INDUSTRY_252000_TIRES: List[str] = [
    "GT", "CTB", "ALSN",
]

# 252100 - Toys
INDUSTRY_252100_TOYS: List[str] = [
    # Merged into Leisure Products (HAS, MAT already there)
]


# =============================================================================
# SECTOR 30: CONSUMER STAPLES
# =============================================================================

# 300100 - Beverages: Alcoholic
INDUSTRY_300100_BEVERAGES_ALCOHOLIC: List[str] = [
    "BUD", "TAP", "SAM", "STZ", "DEO", "ABEV", "CCU",
    "NAPA", "WVVI",
]

# 300200 - Beverages: Non-Alcoholic
INDUSTRY_300200_BEVERAGES_NON_ALCOHOLIC: List[str] = [
    "PEP", "KO", "COKE", "CCEP", "MNST", "CELH", "FIZZ", "ZVIA", "REED",
]

# 300300 - Drug Retailers
INDUSTRY_300300_DRUG_RETAILERS: List[str] = [
    "WBA", "CVS", "RAD",
]

# 300400 - Food Products
INDUSTRY_300400_FOOD_PRODUCTS: List[str] = [
    "MDLZ", "KHC", "GIS", "K", "CAG", "CPB", "SJM", "HRL",
    "TSN", "JJSF", "LANC", "INGR", "DAR", "CALM", "HAIN", "SMPL", "THS",
    "BRBR", "USFD", "DOLE", "FARM", "LNDC", "SFD", "CVGW", "STKL",
    "MGPI", "PSMT", "VFF", "BWMN",
]

# 300500 - Food Retailers
INDUSTRY_300500_FOOD_RETAILERS: List[str] = [
    "KR", "ACI", "SFM", "IMKTA", "BGS", "GO", "CASY", "VLGEA", "WMK",
    "NGVC", "CHEF", "PFGC", "UNFI", "SPTN", "FWRG",
]

# 300600 - Household Products
INDUSTRY_300600_HOUSEHOLD_PRODUCTS: List[str] = [
    "PG", "CL", "CHD", "CLX", "KMB", "SPB", "EPC", "ELF", "IPAR",
    "CENT", "NUS", "USNA", "ENR", "REV", "COTY", "SKIN", "OLPX",
    "GROV", "NWL", "SBH",
]

# 300700 - Personal Products
INDUSTRY_300700_PERSONAL_PRODUCTS: List[str] = [
    "EL", "PRGO", "HNST", "OMI",
]

# 300800 - Tobacco
INDUSTRY_300800_TOBACCO: List[str] = [
    "PM", "MO", "BTI", "TPB", "VGR", "UVV",
]


# =============================================================================
# SECTOR 35: HEALTH CARE
# =============================================================================

# 350100 - Biotechnology
INDUSTRY_350100_BIOTECHNOLOGY: List[str] = [
    "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "BNTX", "SGEN", "ALNY",
    "INCY", "BMRN", "EXEL", "IONS", "UTHR", "RARE", "NBIX", "SRPT", "BLUE",
    "SGMO", "EDIT", "CRSP", "NTLA", "BEAM", "VERV", "TWST", "DNA", "ALLO",
    "RXRX", "KRYS", "ARWR", "FOLD", "DNLI", "KYMR", "KROS", "BCRX", "ARQT",
    "DRNA", "MYOV", "BGNE", "LEGN", "RPRX", "ROIV", "JANX", "VERA", "IDYA",
    "RCUS", "NVAX", "VXRT", "INO", "MRVI", "CRBU", "ATAI", "MNMD", "CMPS",
    "IMVT", "PRTA", "SRRK", "SANA", "VIR", "ABCL", "PTGX", "MORF",
    "XNCR", "APLS", "RXDX", "TNGX", "ETNB", "SWTX", "AVXL", "LXRX",
    "CGEM", "VRDN", "DAWN", "ACAD", "GERN", "REPL", "ALLK",
    "BOLT", "MLYS", "TARS", "ARDX", "AKRO", "CRMD", "KRON", "BCAB",
]

# 350200 - Diagnostics & Research
INDUSTRY_350200_DIAGNOSTICS_RESEARCH: List[str] = [
    "TMO", "DHR", "A", "BIO", "ILMN", "MTD", "WAT", "PKI", "TECH", "CRL",
    "ICLR", "MEDP", "RVTY", "CDNA", "EXAS", "VCYT", "NVTA", "ME", "VEEV",
    "MYGN", "NTRA", "PACB", "TXG", "FLGT", "NEO", "MXCT",
]

# 350300 - Healthcare Distributors
INDUSTRY_350300_HEALTHCARE_DISTRIBUTORS: List[str] = [
    "MCK", "ABC", "CAH", "HSIC", "PDCO",
]

# 350400 - Healthcare Facilities
INDUSTRY_350400_HEALTHCARE_FACILITIES: List[str] = [
    "HCA", "UHS", "THC", "ACHC", "DVA", "ADUS", "ENSG", "PNTG", "SEM", "NHC",
    "SGRY", "OPCH", "ALHC", "HCSG", "BKD",
]

# 350500 - Healthcare Plans
INDUSTRY_350500_HEALTHCARE_PLANS: List[str] = [
    "UNH", "ELV", "HUM", "CI", "CNC", "MOH",
]

# 350600 - Healthcare Services
INDUSTRY_350600_HEALTHCARE_SERVICES: List[str] = [
    "CCRN", "EVH", "GH", "PRVB", "EHAB", "DOCS", "PHR", "TALK", "AMWL",
    "TDOC", "HIMS", "PGNY", "OSCR",
]

# 350700 - Medical Devices
INDUSTRY_350700_MEDICAL_DEVICES: List[str] = [
    "ABT", "MDT", "SYK", "BSX", "ISRG", "EW", "ZBH", "DXCM", "HOLX", "ALGN",
    "RMD", "TFX", "NVST", "SWAV", "PEN", "GMED", "RGEN", "PODD", "INSP",
    "TNDM", "GKOS", "LIVN", "STAA", "ATRC", "MMSI", "IRTC", "OFIX", "CNMD",
    "NARI", "LMAT", "NUVA", "NVCR", "MASI", "HAE", "ESTA", "ATEC", "AXGN",
]

# 350800 - Medical Instruments
INDUSTRY_350800_MEDICAL_INSTRUMENTS: List[str] = [
    "INGN", "LUNG", "ICAD", "SILK", "OPRX", "PROC",
    "STIM", "NNOX", "AXNX", "CUTR", "GHDX", "SRDX",
]

# 350900 - Pharmaceuticals
INDUSTRY_350900_PHARMACEUTICALS: List[str] = [
    "JNJ", "PFE", "LLY", "MRK", "ABBV", "BMY", "ZTS", "VTRS", "TEVA", "PRGO",
    "HLN", "ELAN", "SUPN", "CTLT", "JAZZ", "PCRX", "IRWD", "PAHC", "RVNC",
    "SLNO", "AKBA", "ITCI", "AMPH", "ANI", "CORT", "CPRX", "DRRX", "EOLS",
    "ENTA", "GHRS", "GTHX", "HRTX", "KMPH", "LBPH", "ORGO",
    "PLRX", "PRTX", "RETA", "SIGA", "USPH", "VNDA", "XERS", "ZLAB",
]


# =============================================================================
# SECTOR 40: FINANCIALS
# =============================================================================

# 400100 - Asset Management
INDUSTRY_400100_ASSET_MANAGEMENT: List[str] = [
    "BLK", "BX", "KKR", "APO", "ARES", "OWL", "CG", "TPG", "TROW", "IVZ",
    "BEN", "FHI", "VCTR", "PZN", "GHL", "PJT", "MC", "LPLA",
    "EVR", "HLI", "JEF", "RJF", "SF", "PIPR", "SNEX", "COWN",
    "SCU", "STEP", "WETF", "WDR",
]

# 400200 - Banks: Diversified
INDUSTRY_400200_BANKS_DIVERSIFIED: List[str] = [
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BK", "STT",
]

# 400300 - Banks: Regional
INDUSTRY_400300_BANKS_REGIONAL: List[str] = [
    "PNC", "TFC", "USB", "SCHW", "HBAN", "KEY", "RF",
    "CFG", "FITB", "MTB", "ZION", "CMA", "PACW", "WAL", "FHN",
    "BOKF", "SNV", "VLY", "WBS", "EWBC", "GBCI", "ONB", "PNFP",
    "SBCF", "SEIC", "TOWN", "UBSI", "WAFD", "WSFS", "ASB", "FBK",
    "FFIN", "FULT", "IBOC", "NBTB", "TBBK", "TCBI", "UCBI", "COLB",
    "CATY", "CVBF", "DCOM", "EFSC", "FMBI", "FRME", "GABC", "HWC", "INDB",
    "IBTX", "OFG", "PRK", "RNST", "SBSI", "SFBS", "STBA", "NYCB",
    "BPOP", "FBP", "BANC", "CPF", "LBAI", "MBFI", "SASR",
    "SMBC", "SYBT", "THFF", "UVSP",
]

# 400400 - Brokers & Exchanges
INDUSTRY_400400_BROKERS_EXCHANGES: List[str] = [
    "MKTX", "CBOE", "CME", "ICE", "NDAQ", "COIN", "HOOD", "IBKR",
    "VIRT",
]

# 400500 - Consumer Finance
INDUSTRY_400500_CONSUMER_FINANCE: List[str] = [
    "COF", "AXP", "DFS", "SYF", "ALLY", "NAVI", "SLM",
    "CACC", "ELVT", "OMF", "CURO", "ENVA", "FCFS",
]

# 400600 - Financial Services
INDUSTRY_400600_FINANCIAL_SERVICES: List[str] = [
    "V", "MA", "PYPL", "SQ", "FIS", "FISV", "GPN", "AFRM", "UPST", "SOFI",
    "OPEN", "BILL", "PAYO", "MQ", "TOST",
    "ESNT", "MTG", "RDFN", "UWMC", "RKT", "TREE",
    "OZK", "PFSI", "PRAA", "QFIN", "RELY", "WRLD",
    "GSKY", "LPRO", "MGNI", "MOGO", "MSCI",
    "RPAY", "STNE", "XP",
]

# 400700 - Insurance: Brokers
INDUSTRY_400700_INSURANCE_BROKERS: List[str] = [
    "AJG", "MMC", "AON", "WTW", "BRO",
]

# 400800 - Insurance: Life
INDUSTRY_400800_INSURANCE_LIFE: List[str] = [
    "MET", "PRU", "AFL", "LNC", "PFG", "RGA", "CNO", "GL",  # Removed: SLF (Canadian)
]

# 400900 - Insurance_PC: List[str] = [
INDUSTRY_400900_INSURANCE_PC: List[str] = [
    "PGR", "ALL", "TRV", "CB", "AIG", "ERIE", "CNA", "Y", "RNR", "THG",
    "WRB", "AIZ", "FAF", "FNF", "HIG", "KMPR", "L",
    "ORI", "PLMR", "RDN", "SIGI", "CINF", "KNSL",
    "MCY", "NMIH", "RYAN", "ROOT", "ACGL", "AFG", "AGO", "ANAT",
    "AXS", "LMND", "STC", "STFC",
]

# 401000 - Insurance: Specialty
INDUSTRY_401000_INSURANCE_SPECIALTY: List[str] = [
    "GNW", "HMN", "JRVR", "KREF", "MHLD", "NWLI", "OSCR",
]

# 401100 - Mortgage Finance
INDUSTRY_401100_MORTGAGE_FINANCE: List[str] = [
    "GHLD", "IMXI",
]

# 401200 - Savings & Loans
INDUSTRY_401200_SAVINGS_LOANS: List[str] = [
    "BHLB", "BOCH", "CFFI", "CHCO", "CHMG",
    "CNOB", "EQBK", "FBIZ", "FCBC", "FMBH", "HNVR", "HOMB", "HTBK", "HTLF",
    "IBCP", "LCNB", "MBWM", "MNSB", "MOFG", "NBHC", "NRIM", "OPBK", "OSBC",
    "PKBK", "PLBC", "RBCAA", "SFNC", "SRCE", "SSB", "TRMK", "WABC", "WSBC",
]


# =============================================================================
# SECTOR 45: TECHNOLOGY
# =============================================================================

# 450100 - Application Software
INDUSTRY_450100_APPLICATION_SOFTWARE: List[str] = [
    "CRM", "ORCL", "SAP", "ADBE", "NOW", "INTU", "WDAY", "TEAM", "SNOW",
    "DDOG", "ZS", "PANW", "CRWD", "OKTA", "MDB", "ZM", "DOCU", "HUBS",
    "SPLK", "ZEN", "SMAR", "APPN", "FROG", "CFLT", "ESTC", "GTLB",
    "PTC", "ANSS", "CDNS", "SNPS", "ADSK", "TYL", "GWRE", "PAYC", "PCTY",
]

# 450200 - Cloud Computing
INDUSTRY_450200_CLOUD_COMPUTING: List[str] = [
    "NET", "DDOG", "SNOW", "CFLT", "ESTC", "DBX", "BOX",
]

# 450300 - Communication Equipment
INDUSTRY_450300_COMMUNICATION_EQUIPMENT: List[str] = [
    "CSCO", "JNPR", "ANET", "CIEN", "VIAV", "COMM", "CLFD", "LITE", "INFN",
    "CALX", "CASA", "CMTL", "DGII", "NTGR", "SLAB", "SMTC", "VIAVI",
]

# 450400 - Computer Hardware
INDUSTRY_450400_COMPUTER_HARDWARE: List[str] = [
    "AAPL", "HPQ", "HPE", "DELL", "WDC", "STX", "NTAP", "PSTG", "SMCI",
    "LOGI", "SSYS", "DDD",
]

# 450500 - Computer Services
INDUSTRY_450500_COMPUTER_SERVICES: List[str] = [
    "IBM", "ACN", "CTSH", "INFY", "WIT", "EPAM", "GLOB", "EXLS", "GDS",
]

# 450600 - Cybersecurity
INDUSTRY_450600_CYBERSECURITY: List[str] = [
    "PANW", "CRWD", "ZS", "FTNT", "OKTA", "QLYS", "TENB", "CYBR", "RPD",
    "VRNS", "SAIL", "SCWX", "NLOK", "FEYE", "PFPT",  # Removed: BB (Canadian)
]

# 450700 - Data Processing
INDUSTRY_450700_DATA_PROCESSING: List[str] = [
    "V", "MA", "PYPL", "FIS", "FISV", "GPN", "ADP", "PAYX", "JKHY", "EVTC",
    "WEX", "GDOT", "FOUR", "PAY", "QTWO",
]

# 450800 - Electronic Components
INDUSTRY_450800_ELECTRONIC_COMPONENTS: List[str] = [
    "APH", "TEL", "FLEX", "JBL", "SANM", "CLS", "PLXS", "TTMI", "BHE",
    "BELFA", "LFUS", "NOVT", "OLED", "VICR",
]

# 450900 - IT Consulting
INDUSTRY_450900_IT_CONSULTING: List[str] = [
    "ACN", "CTSH", "INFY", "WIT", "EPAM", "GLOB",
]

# 451000 - Scientific Instruments
INDUSTRY_451000_SCIENTIFIC_INSTRUMENTS: List[str] = [
    "KEYS", "TDY", "GRMN", "TRMB", "COHR", "MKSI", "IDXX", "NOVT",
    "CGNX", "ITRI", "MLAB", "NEOG", "OLED", "ST", "FTV",
]

# 451100 - Semiconductor Equipment
INDUSTRY_451100_SEMICONDUCTOR_EQUIPMENT: List[str] = [
    "ASML", "LRCX", "KLAC", "AMAT", "TER", "ENTG", "ONTO", "ACLS", "COHU",
    "ICHR", "MKSI", "UCTT", "FORM", "OLED", "KLIC", "BRKS",
]

# 451200 - Semiconductors
INDUSTRY_451200_SEMICONDUCTORS: List[str] = [
    "NVDA", "AMD", "INTC", "AVGO", "QCOM", "TXN", "MU", "ADI", "NXPI",
    "MRVL", "ON", "SWKS", "QRVO", "MCHP", "MPWR", "WOLF", "GFS", "ALGM",
    "CRUS", "DIOD", "FORM", "HIMX", "LSCC", "SIMO", "SITM", "SMTC",
    "MTSI", "POWI", "RMBS", "SLAB", "STM", "TSM", "UMC",
]

# 451300 - Software Infrastructure
INDUSTRY_451300_SOFTWARE_INFRASTRUCTURE: List[str] = [
    "MSFT", "GOOG", "GOOGL", "META", "AMZN", "PLTR", "PATH", "AI", "BBAI",
    "VMW", "RHT", "RBLX", "U", "TTWO", "EA", "ATVI", "ZNGA",
]


# =============================================================================
# SECTOR 50: COMMUNICATION SERVICES
# =============================================================================

# 500100 - Advertising
INDUSTRY_500100_ADVERTISING: List[str] = [
    "OMC", "IPG", "MGID", "PUBM", "TTD", "APPS", "DV", "IAS",
]

# 500200 - Broadcasting
INDUSTRY_500200_BROADCASTING: List[str] = [
    "CMCSA", "FOX", "FOXA", "PARA", "WBD", "NXST", "SBGI", "GTN", "TGNA",
    "SSP", "GCI", "IHRT", "TRCO", "SALM",
]

# 500300 - Cable & Satellite
INDUSTRY_500300_CABLE_SATELLITE: List[str] = [
    "CHTR", "CABO", "LBRDA", "LBRDK", "SIRI", "DISH",
]

# 500400 - Entertainment
INDUSTRY_500400_ENTERTAINMENT: List[str] = [
    "DIS", "NFLX", "ROKU", "SPOT", "LYV", "WMG", "MSGS", "EDR", "LGF.A",
    "IMAX", "CNK", "AMC", "CINE", "NCMI",
]

# 500500 - Internet
INDUSTRY_500500_INTERNET: List[str] = [
    "GOOG", "GOOGL", "META", "SNAP", "PINS", "TWTR", "MTCH", "BMBL",
    "ZG", "Z", "YELP", "IAC", "ANGI", "CARG", "GRPN", "TRIP", "EXPE", "BKNG",
]

# 500600 - Publishing
INDUSTRY_500600_PUBLISHING: List[str] = [
    "NYT", "NWSA", "NWS", "GCI", "TGNA", "LEE", "MNI",
]

# 500700 - Telecom Equipment
INDUSTRY_500700_TELECOM_EQUIPMENT: List[str] = [
    "ERIC", "NOK", "UI", "COMM", "CLFD", "VIAV",
]

# 500800 - Telecom Services
INDUSTRY_500800_TELECOM_SERVICES: List[str] = [
    "T", "VZ", "TMUS", "LUMN", "FTR", "USM", "TDS", "ATUS", "LILA", "LILAK",
]


# =============================================================================
# SECTOR 55: UTILITIES
# =============================================================================

# 550100 - Electric Utilities
INDUSTRY_550100_ELECTRIC_UTILITIES: List[str] = [
    "NEE", "DUK", "SO", "D", "AEP", "XEL", "EXC", "SRE", "WEC", "ES",
    "ED", "DTE", "PPL", "ETR", "FE", "AEE", "CMS", "EIX", "EVRG", "CNP",
    "NI", "PNW", "OGE", "AVA", "IDA", "HE", "POR", "BKH", "NWE", "OGS",
]

# 550200 - Gas Utilities
INDUSTRY_550200_GAS_UTILITIES: List[str] = [
    "NJR", "SWX", "ATO", "SPH", "OGS", "NWN", "SR", "UTL",
]

# 550300 - Independent Power
INDUSTRY_550300_INDEPENDENT_POWER: List[str] = [
    "NRG", "VST", "ORA", "CWEN", "AES", "TAC",
]

# 550400 - Multi-Utilities
INDUSTRY_550400_MULTI_UTILITIES: List[str] = [
    "PCG", "EXC", "WEC", "ES", "ED", "DTE", "CMS", "NI", "PEG", "AGR",
]

# 550500 - Renewable Energy
INDUSTRY_550500_RENEWABLE_ENERGY: List[str] = [
    "ENPH", "SEDG", "FSLR", "RUN", "NOVA", "SPWR", "JKS", "ARRY",  # Removed: CSIQ (Canadian)
    "SHLS", "MAXN", "AMPS", "NEP", "CWEN", "BEPC", "BEP", "TAN",
]

# 550600 - Water Utilities
INDUSTRY_550600_WATER_UTILITIES: List[str] = [
    "AWK", "WTR", "WTRG", "CWT", "SJW", "AWR", "MSEX", "YORW", "ARTNA",
]


# =============================================================================
# SECTOR 60: REAL ESTATE
# =============================================================================

# 600100 - REITs - Diversified
INDUSTRY_600100_REITS_DIVERSIFIED: List[str] = [
    "PLD", "AMT", "CCI", "EQIX", "PSA", "DLR", "SPG", "WELL", "O", "AVB",
    "WY", "EQR", "VTR", "ARE", "DRE", "BXP", "VNO", "SLG", "ESRT", "PGRE",
]

# 600200 - REITs - Healthcare
INDUSTRY_600200_REITS_HEALTHCARE: List[str] = [
    "WELL", "VTR", "PEAK", "OHI", "HR", "DOC", "SBRA", "LTC", "NHI", "CTRE",
    "MPW", "GMRE", "GH", "CHC",
]

# 600300 - REITs - Hotel & Motel
INDUSTRY_600300_REITS_HOTEL_MOTEL: List[str] = [
    "HST", "PK", "RHP", "SHO", "DRH", "PEB", "RLJ", "INN", "XHR", "APTS",
    "BHR", "CLDT", "HT", "AHT",
]

# 600400 - REITs - Industrial
INDUSTRY_600400_REITS_INDUSTRIAL: List[str] = [
    "PLD", "DRE", "FR", "EGP", "STAG", "TRNO", "REXR", "IIPR", "LXP", "COLD",
    "GTY", "PLYM", "ILPT", "PINE",
]

# 600500 - REITs - Mortgage
INDUSTRY_600500_REITS_MORTGAGE: List[str] = [
    "AGNC", "NLY", "STWD", "BXMT", "LADR", "TWO", "MFA", "RWT", "KREF",
    "ABR", "NYMT", "ARI", "GPMT", "DX", "IVR", "NRZ", "PMT", "ACRE",
    "RC", "RITM", "CIM", "TRTX", "NREF", "FBRT",
]

# 600600 - REITs - Office
INDUSTRY_600600_REITS_OFFICE: List[str] = [
    "BXP", "VNO", "SLG", "ESRT", "PGRE", "HIW", "CUZ", "OFC", "KRC", "PDM",
    "DEI", "HPP", "JBGS", "FSP", "EQC", "ONL", "WRE",
]

# 600700 - REITs - Residential
INDUSTRY_600700_REITS_RESIDENTIAL: List[str] = [
    "AVB", "EQR", "MAA", "ESS", "UDR", "CPT", "AIV", "NXRT", "IRT", "ELME",
    "INVH", "AMH", "REXR", "SUI", "ELS",
]

# 600800 - REITs - Retail
INDUSTRY_600800_REITS_RETAIL: List[str] = [
    "SPG", "O", "REG", "KIM", "FRT", "BRX", "KRG", "ROIC", "SITE", "AKR",
    "RPAI", "RPT", "UE", "SKT", "MAC", "CBL", "PEI", "WPG", "STAR",
]

# 600900 - REITs - Specialty
INDUSTRY_600900_REITS_SPECIALTY: List[str] = [
    "AMT", "CCI", "EQIX", "DLR", "PSA", "EXR", "CUBE", "LSI", "NSA", "REXR",
    "SRC", "FCPT", "STOR", "ADC", "LAND", "EPRT", "NNN", "WPC", "GLPI",
    "VICI", "RYN", "PCH", "CTO", "SAFE", "SBAC", "IRM", "MPW",
]

# 601000 - Real Estate Development
INDUSTRY_601000_REAL_ESTATE_DEVELOPMENT: List[str] = [
    "HHC", "FPH", "FOR", "UMH", "SNPR",
]

# 601100 - Real Estate Services
INDUSTRY_601100_REAL_ESTATE_SERVICES: List[str] = [
    "CBRE", "JLL", "CWK", "RMR", "NMRK", "MMI", "DOUG", "HOUS",
]


# =============================================================================
# COMBINED EXPORTS - ALL TICKERS BY INDUSTRY
# =============================================================================

INDUSTRY_TICKERS: Dict[str, List[str]] = {
    # Energy
    "100100": INDUSTRY_100100_COAL,
    "100200": INDUSTRY_100200_OIL_GAS_DRILLING,
    "100300": INDUSTRY_100300_OIL_GAS_EP,
    "100400": INDUSTRY_100400_OIL_GAS_EQUIPMENT,
    "100500": INDUSTRY_100500_OIL_GAS_INTEGRATED,
    "100600": INDUSTRY_100600_OIL_GAS_PIPELINES,
    "100700": INDUSTRY_100700_OIL_GAS_REFINING,
    # Materials
    "150100": INDUSTRY_150100_ALUMINUM,
    "150200": INDUSTRY_150200_BUILDING_MATERIALS,
    "150300": INDUSTRY_150300_CHEMICALS,
    "150400": INDUSTRY_150400_CONTAINERS_PACKAGING,
    "150500": INDUSTRY_150500_COPPER,
    "150600": INDUSTRY_150600_FERTILIZERS,
    "150700": INDUSTRY_150700_GOLD,
    "150800": INDUSTRY_150800_METALS_MINING,
    "150900": INDUSTRY_150900_PAPER_FOREST,
    "151000": INDUSTRY_151000_SILVER,
    "151100": INDUSTRY_151100_SPECIALTY_CHEMICALS,
    "151200": INDUSTRY_151200_STEEL,
    # Industrials
    "200100": INDUSTRY_200100_AEROSPACE,
    "200200": INDUSTRY_200200_AIR_FREIGHT,
    "200300": INDUSTRY_200300_AIRLINES,
    "200400": INDUSTRY_200400_BUILDING_PRODUCTS,
    "200500": INDUSTRY_200500_BUSINESS_SERVICES,
    "200600": INDUSTRY_200600_CAPITAL_GOODS,
    "200700": INDUSTRY_200700_COMMERCIAL_VEHICLES,
    "200800": INDUSTRY_200800_CONGLOMERATES,
    "200900": INDUSTRY_200900_CONSTRUCTION_MATERIALS,
    "201000": INDUSTRY_201000_DEFENSE,
    "201100": INDUSTRY_201100_ELECTRICAL_EQUIPMENT,
    "201200": INDUSTRY_201200_ENGINEERING_CONSTRUCTION,
    "201300": INDUSTRY_201300_ENVIRONMENTAL_SERVICES,
    "201400": INDUSTRY_201400_FARM_MACHINERY,
    "201500": INDUSTRY_201500_HEAVY_MACHINERY,
    "201600": INDUSTRY_201600_INDUSTRIAL_DISTRIBUTION,
    "201700": INDUSTRY_201700_MARINE_SHIPPING,
    "201800": INDUSTRY_201800_PACKAGING,
    "201900": INDUSTRY_201900_RAILROADS,
    "202000": INDUSTRY_202000_SECURITY_SERVICES,
    "202100": INDUSTRY_202100_STAFFING,
    "202200": INDUSTRY_202200_TRUCKING,
    "202300": INDUSTRY_202300_WASTE_MANAGEMENT,
    # Consumer Discretionary
    "250100": INDUSTRY_250100_AUTO_PARTS,
    "250200": INDUSTRY_250200_AUTOMOBILES,
    "250300": INDUSTRY_250300_CASINOS_GAMING,
    "250400": INDUSTRY_250400_CONSUMER_ELECTRONICS,
    "250500": INDUSTRY_250500_DEPARTMENT_STORES,
    "250600": INDUSTRY_250600_FOOTWEAR,
    "250700": INDUSTRY_250700_FURNISHINGS,
    "250800": INDUSTRY_250800_GENERAL_MERCHANDISE,
    "250900": INDUSTRY_250900_HOME_IMPROVEMENT,
    "251000": INDUSTRY_251000_HOMEBUILDERS,
    "251100": INDUSTRY_251100_HOTELS_MOTELS,
    "251200": INDUSTRY_251200_HOUSEWARES,
    "251300": INDUSTRY_251300_LEISURE_PRODUCTS,
    "251400": INDUSTRY_251400_RECREATIONAL_SERVICES,
    "251500": INDUSTRY_251500_RECREATIONAL_VEHICLES,
    "251600": INDUSTRY_251600_RESTAURANTS,
    "251700": INDUSTRY_251700_RETAIL_APPAREL,
    "251800": INDUSTRY_251800_SPECIALTY_RETAIL,
    "251900": INDUSTRY_251900_TEXTILES_APPAREL,
    "252000": INDUSTRY_252000_TIRES,
    "252100": INDUSTRY_252100_TOYS,
    # Consumer Staples
    "300100": INDUSTRY_300100_BEVERAGES_ALCOHOLIC,
    "300200": INDUSTRY_300200_BEVERAGES_NON_ALCOHOLIC,
    "300300": INDUSTRY_300300_DRUG_RETAILERS,
    "300400": INDUSTRY_300400_FOOD_PRODUCTS,
    "300500": INDUSTRY_300500_FOOD_RETAILERS,
    "300600": INDUSTRY_300600_HOUSEHOLD_PRODUCTS,
    "300700": INDUSTRY_300700_PERSONAL_PRODUCTS,
    "300800": INDUSTRY_300800_TOBACCO,
    # Health Care
    "350100": INDUSTRY_350100_BIOTECHNOLOGY,
    "350200": INDUSTRY_350200_DIAGNOSTICS_RESEARCH,
    "350300": INDUSTRY_350300_HEALTHCARE_DISTRIBUTORS,
    "350400": INDUSTRY_350400_HEALTHCARE_FACILITIES,
    "350500": INDUSTRY_350500_HEALTHCARE_PLANS,
    "350600": INDUSTRY_350600_HEALTHCARE_SERVICES,
    "350700": INDUSTRY_350700_MEDICAL_DEVICES,
    "350800": INDUSTRY_350800_MEDICAL_INSTRUMENTS,
    "350900": INDUSTRY_350900_PHARMACEUTICALS,
    # Financials
    "400100": INDUSTRY_400100_ASSET_MANAGEMENT,
    "400200": INDUSTRY_400200_BANKS_DIVERSIFIED,
    "400300": INDUSTRY_400300_BANKS_REGIONAL,
    "400400": INDUSTRY_400400_BROKERS_EXCHANGES,
    "400500": INDUSTRY_400500_CONSUMER_FINANCE,
    "400600": INDUSTRY_400600_FINANCIAL_SERVICES,
    "400700": INDUSTRY_400700_INSURANCE_BROKERS,
    "400800": INDUSTRY_400800_INSURANCE_LIFE,
    "400900": INDUSTRY_400900_INSURANCE_PC,
    "401000": INDUSTRY_401000_INSURANCE_SPECIALTY,
    "401100": INDUSTRY_401100_MORTGAGE_FINANCE,
    "401200": INDUSTRY_401200_SAVINGS_LOANS,
    # Technology
    "450100": INDUSTRY_450100_APPLICATION_SOFTWARE,
    "450200": INDUSTRY_450200_CLOUD_COMPUTING,
    "450300": INDUSTRY_450300_COMMUNICATION_EQUIPMENT,
    "450400": INDUSTRY_450400_COMPUTER_HARDWARE,
    "450500": INDUSTRY_450500_COMPUTER_SERVICES,
    "450600": INDUSTRY_450600_CYBERSECURITY,
    "450700": INDUSTRY_450700_DATA_PROCESSING,
    "450800": INDUSTRY_450800_ELECTRONIC_COMPONENTS,
    "450900": INDUSTRY_450900_IT_CONSULTING,
    "451000": INDUSTRY_451000_SCIENTIFIC_INSTRUMENTS,
    "451100": INDUSTRY_451100_SEMICONDUCTOR_EQUIPMENT,
    "451200": INDUSTRY_451200_SEMICONDUCTORS,
    "451300": INDUSTRY_451300_SOFTWARE_INFRASTRUCTURE,
    # Communication Services
    "500100": INDUSTRY_500100_ADVERTISING,
    "500200": INDUSTRY_500200_BROADCASTING,
    "500300": INDUSTRY_500300_CABLE_SATELLITE,
    "500400": INDUSTRY_500400_ENTERTAINMENT,
    "500500": INDUSTRY_500500_INTERNET,
    "500600": INDUSTRY_500600_PUBLISHING,
    "500700": INDUSTRY_500700_TELECOM_EQUIPMENT,
    "500800": INDUSTRY_500800_TELECOM_SERVICES,
    # Utilities
    "550100": INDUSTRY_550100_ELECTRIC_UTILITIES,
    "550200": INDUSTRY_550200_GAS_UTILITIES,
    "550300": INDUSTRY_550300_INDEPENDENT_POWER,
    "550400": INDUSTRY_550400_MULTI_UTILITIES,
    "550500": INDUSTRY_550500_RENEWABLE_ENERGY,
    "550600": INDUSTRY_550600_WATER_UTILITIES,
    # Real Estate
    "600100": INDUSTRY_600100_REITS_DIVERSIFIED,
    "600200": INDUSTRY_600200_REITS_HEALTHCARE,
    "600300": INDUSTRY_600300_REITS_HOTEL_MOTEL,
    "600400": INDUSTRY_600400_REITS_INDUSTRIAL,
    "600500": INDUSTRY_600500_REITS_MORTGAGE,
    "600600": INDUSTRY_600600_REITS_OFFICE,
    "600700": INDUSTRY_600700_REITS_RESIDENTIAL,
    "600800": INDUSTRY_600800_REITS_RETAIL,
    "600900": INDUSTRY_600900_REITS_SPECIALTY,
    "601000": INDUSTRY_601000_REAL_ESTATE_DEVELOPMENT,
    "601100": INDUSTRY_601100_REAL_ESTATE_SERVICES,
}


def get_all_additional_tickers() -> List[str]:
    """Get all additional tickers as a flat list."""
    all_tickers = []
    for tickers in INDUSTRY_TICKERS.values():
        all_tickers.extend(tickers)
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for t in all_tickers:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def get_tickers_for_industry(industry_code: str) -> List[str]:
    """Get additional tickers for a specific industry code."""
    return INDUSTRY_TICKERS.get(industry_code, [])


def get_industry_code_for_ticker(ticker: str) -> str:
    """Find the industry code for a given ticker."""
    for code, tickers in INDUSTRY_TICKERS.items():
        if ticker in tickers:
            return code
    return ""


# Backward compatibility - sector-based exports
SECTOR_10_ENERGY = (
    INDUSTRY_100100_COAL +
    INDUSTRY_100200_OIL_GAS_DRILLING +
    INDUSTRY_100300_OIL_GAS_EP +
    INDUSTRY_100400_OIL_GAS_EQUIPMENT +
    INDUSTRY_100500_OIL_GAS_INTEGRATED +
    INDUSTRY_100600_OIL_GAS_PIPELINES +
    INDUSTRY_100700_OIL_GAS_REFINING
)

SECTOR_15_MATERIALS = (
    INDUSTRY_150100_ALUMINUM +
    INDUSTRY_150200_BUILDING_MATERIALS +
    INDUSTRY_150300_CHEMICALS +
    INDUSTRY_150400_CONTAINERS_PACKAGING +
    INDUSTRY_150500_COPPER +
    INDUSTRY_150600_FERTILIZERS +
    INDUSTRY_150700_GOLD +
    INDUSTRY_150800_METALS_MINING +
    INDUSTRY_150900_PAPER_FOREST +
    INDUSTRY_151000_SILVER +
    INDUSTRY_151100_SPECIALTY_CHEMICALS +
    INDUSTRY_151200_STEEL
)

SECTOR_20_INDUSTRIALS = (
    INDUSTRY_200100_AEROSPACE +
    INDUSTRY_200200_AIR_FREIGHT +
    INDUSTRY_200300_AIRLINES +
    INDUSTRY_200400_BUILDING_PRODUCTS +
    INDUSTRY_200500_BUSINESS_SERVICES +
    INDUSTRY_200600_CAPITAL_GOODS +
    INDUSTRY_200700_COMMERCIAL_VEHICLES +
    INDUSTRY_200800_CONGLOMERATES +
    INDUSTRY_200900_CONSTRUCTION_MATERIALS +
    INDUSTRY_201000_DEFENSE +
    INDUSTRY_201100_ELECTRICAL_EQUIPMENT +
    INDUSTRY_201200_ENGINEERING_CONSTRUCTION +
    INDUSTRY_201300_ENVIRONMENTAL_SERVICES +
    INDUSTRY_201400_FARM_MACHINERY +
    INDUSTRY_201500_HEAVY_MACHINERY +
    INDUSTRY_201600_INDUSTRIAL_DISTRIBUTION +
    INDUSTRY_201700_MARINE_SHIPPING +
    INDUSTRY_201800_PACKAGING +
    INDUSTRY_201900_RAILROADS +
    INDUSTRY_202000_SECURITY_SERVICES +
    INDUSTRY_202100_STAFFING +
    INDUSTRY_202200_TRUCKING +
    INDUSTRY_202300_WASTE_MANAGEMENT
)

SECTOR_25_CONSUMER_DISCRETIONARY = (
    INDUSTRY_250100_AUTO_PARTS +
    INDUSTRY_250200_AUTOMOBILES +
    INDUSTRY_250300_CASINOS_GAMING +
    INDUSTRY_250400_CONSUMER_ELECTRONICS +
    INDUSTRY_250500_DEPARTMENT_STORES +
    INDUSTRY_250600_FOOTWEAR +
    INDUSTRY_250700_FURNISHINGS +
    INDUSTRY_250800_GENERAL_MERCHANDISE +
    INDUSTRY_250900_HOME_IMPROVEMENT +
    INDUSTRY_251000_HOMEBUILDERS +
    INDUSTRY_251100_HOTELS_MOTELS +
    INDUSTRY_251200_HOUSEWARES +
    INDUSTRY_251300_LEISURE_PRODUCTS +
    INDUSTRY_251400_RECREATIONAL_SERVICES +
    INDUSTRY_251500_RECREATIONAL_VEHICLES +
    INDUSTRY_251600_RESTAURANTS +
    INDUSTRY_251700_RETAIL_APPAREL +
    INDUSTRY_251800_SPECIALTY_RETAIL +
    INDUSTRY_251900_TEXTILES_APPAREL +
    INDUSTRY_252000_TIRES +
    INDUSTRY_252100_TOYS
)

SECTOR_30_CONSUMER_STAPLES = (
    INDUSTRY_300100_BEVERAGES_ALCOHOLIC +
    INDUSTRY_300200_BEVERAGES_NON_ALCOHOLIC +
    INDUSTRY_300300_DRUG_RETAILERS +
    INDUSTRY_300400_FOOD_PRODUCTS +
    INDUSTRY_300500_FOOD_RETAILERS +
    INDUSTRY_300600_HOUSEHOLD_PRODUCTS +
    INDUSTRY_300700_PERSONAL_PRODUCTS +
    INDUSTRY_300800_TOBACCO
)

SECTOR_35_HEALTHCARE = (
    INDUSTRY_350100_BIOTECHNOLOGY +
    INDUSTRY_350200_DIAGNOSTICS_RESEARCH +
    INDUSTRY_350300_HEALTHCARE_DISTRIBUTORS +
    INDUSTRY_350400_HEALTHCARE_FACILITIES +
    INDUSTRY_350500_HEALTHCARE_PLANS +
    INDUSTRY_350600_HEALTHCARE_SERVICES +
    INDUSTRY_350700_MEDICAL_DEVICES +
    INDUSTRY_350800_MEDICAL_INSTRUMENTS +
    INDUSTRY_350900_PHARMACEUTICALS
)

SECTOR_40_FINANCIALS = (
    INDUSTRY_400100_ASSET_MANAGEMENT +
    INDUSTRY_400200_BANKS_DIVERSIFIED +
    INDUSTRY_400300_BANKS_REGIONAL +
    INDUSTRY_400400_BROKERS_EXCHANGES +
    INDUSTRY_400500_CONSUMER_FINANCE +
    INDUSTRY_400600_FINANCIAL_SERVICES +
    INDUSTRY_400700_INSURANCE_BROKERS +
    INDUSTRY_400800_INSURANCE_LIFE +
    INDUSTRY_400900_INSURANCE_PC +
    INDUSTRY_401000_INSURANCE_SPECIALTY +
    INDUSTRY_401100_MORTGAGE_FINANCE +
    INDUSTRY_401200_SAVINGS_LOANS
)

SECTOR_45_TECHNOLOGY = (
    INDUSTRY_450100_APPLICATION_SOFTWARE +
    INDUSTRY_450200_CLOUD_COMPUTING +
    INDUSTRY_450300_COMMUNICATION_EQUIPMENT +
    INDUSTRY_450400_COMPUTER_HARDWARE +
    INDUSTRY_450500_COMPUTER_SERVICES +
    INDUSTRY_450600_CYBERSECURITY +
    INDUSTRY_450700_DATA_PROCESSING +
    INDUSTRY_450800_ELECTRONIC_COMPONENTS +
    INDUSTRY_450900_IT_CONSULTING +
    INDUSTRY_451000_SCIENTIFIC_INSTRUMENTS +
    INDUSTRY_451100_SEMICONDUCTOR_EQUIPMENT +
    INDUSTRY_451200_SEMICONDUCTORS +
    INDUSTRY_451300_SOFTWARE_INFRASTRUCTURE
)

SECTOR_50_COMMUNICATION_SERVICES = (
    INDUSTRY_500100_ADVERTISING +
    INDUSTRY_500200_BROADCASTING +
    INDUSTRY_500300_CABLE_SATELLITE +
    INDUSTRY_500400_ENTERTAINMENT +
    INDUSTRY_500500_INTERNET +
    INDUSTRY_500600_PUBLISHING +
    INDUSTRY_500700_TELECOM_EQUIPMENT +
    INDUSTRY_500800_TELECOM_SERVICES
)

SECTOR_55_UTILITIES = (
    INDUSTRY_550100_ELECTRIC_UTILITIES +
    INDUSTRY_550200_GAS_UTILITIES +
    INDUSTRY_550300_INDEPENDENT_POWER +
    INDUSTRY_550400_MULTI_UTILITIES +
    INDUSTRY_550500_RENEWABLE_ENERGY +
    INDUSTRY_550600_WATER_UTILITIES
)

SECTOR_60_REAL_ESTATE = (
    INDUSTRY_600100_REITS_DIVERSIFIED +
    INDUSTRY_600200_REITS_HEALTHCARE +
    INDUSTRY_600300_REITS_HOTEL_MOTEL +
    INDUSTRY_600400_REITS_INDUSTRIAL +
    INDUSTRY_600500_REITS_MORTGAGE +
    INDUSTRY_600600_REITS_OFFICE +
    INDUSTRY_600700_REITS_RESIDENTIAL +
    INDUSTRY_600800_REITS_RETAIL +
    INDUSTRY_600900_REITS_SPECIALTY +
    INDUSTRY_601000_REAL_ESTATE_DEVELOPMENT +
    INDUSTRY_601100_REAL_ESTATE_SERVICES
)
