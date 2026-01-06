"""
Extended list of US stock tickers for database expansion.

This module provides additional ticker symbols beyond S&P 500/400/600 indices.
These are sourced from Russell 3000, Nasdaq listings, and other US exchanges.

Organized by GICS sector for easier prioritization of underrepresented industries.
"""

# =============================================================================
# ADDITIONAL TICKERS BY SECTOR
# =============================================================================

SECTOR_10_ENERGY = [
    # Oil & Gas Drilling
    "HP", "NBR", "RIG", "VAL", "DO", "NE", "PTEN", "PDS", "BORR", "DRQ", "NINE",
    "USWS", "KLXE", "VTOL",
    # Oil & Gas E&P
    "APA", "DVN", "FANG", "EOG", "PXD", "COP", "OXY", "MRO", "CLR", "SU", "CVE",
    "PR", "MTDR", "CTRA", "CHRD", "OVV", "MGY", "SM", "CRGY", "SBOW", "CNX", 
    "AR", "SWN", "EQT", "VTLE", "REPX", "ESTE", "REI", "PARR", "SD", "AXAS",
    "SNDE", "EPSN", "WTI", "NGAS", "WFRD", "BRY", "SGML", "CIVI", "BKV", "VNOM",
    "CPE", "GPOR", "GRNT", "HPK", "CDEV", "WLL", "NOG", "CRZO", "KOS", "RRC",
    "TELL", "NEXT", "ZN", "LONE", "PTR",
    # Oil & Gas Refining
    "VLO", "PSX", "MPC", "DK", "PBF", "CVI", "DINO", "CLMT", "CAPL", "HEP",
    "NS", "HFC", "INT", "CVRR", "NTI", "REGI", "PACD", "GPRK", "AMCF",
    # Oil & Gas Midstream/Storage
    "KMI", "WMB", "OKE", "ET", "MPLX", "EPD", "PAA", "WES", "TRGP", "AM",
    "DCP", "USAC", "SMLP", "NGL", "CEQP", "ENLC", "ETRN", "KNTK", "DTM",
    "GLP", "PAGP", "BSM", "CLNE", "CPLP", "NBLX", "SPH",
    # Oil Services & Equipment
    "SLB", "HAL", "BKR", "NOV", "FTI", "WHD", "WTTR", "OII", "LBRT", "NEX",
    "RES", "HLX", "CLB", "XPRO", "BOOM", "GEL", "TTI", "PUMP", "DWSN",
    "AROC", "SOI", "TDW", "GIFI", "MTRX", "MPLN", "OIS",
]

SECTOR_15_MATERIALS = [
    # Chemicals - Diversified & Specialty
    "DOW", "LYB", "CE", "EMN", "HUN", "WLK", "OLN", "TROX", "KRO", "MEOH",
    "ASIX", "IOSP", "KWR", "NGVT", "FUL", "RPM", "GRA", "BCPC", "HWKN",
    "APD", "ECL", "SHW", "PPG", "ALB", "IFF", "AVNT", "AXTA", "ASH", "GCP",
    "CBT", "CC", "FOE", "LTH", "MTX", "LTHM", "UNVR", "KALM",
    "NVZMY", "HXL", "NEU", "GPRE", "RYAM", "ZEUS", "GLATF", "AREC",
    # Industrial Gases
    "LIN",   # Linde plc
    # Agricultural Chemicals
    "NTR", "CF", "MOS", "FMC", "SMG", "CTVA", "ICL", "IPI", "ADM",
    "AGFY", "GRWG", "APPH", "AVO", "AGRO", "SEED", "LMNR", "SMID",
    # Construction Materials
    "VMC", "MLM", "EXP", "USLM", "SUM", "ROCK", "ITE", "MDU", "CNHI", "CRH",
    "CMCO", "KNF", "TGLS", "APOG", "ASTE", "PGTI",
    # Metals & Mining - Copper
    "SCCO", "TECK", "HBM", "ERO", "NEXA",  # Copper producers
    # Metals & Mining (Gold, Silver, Other)
    "NEM", "FCX", "GOLD", "NUE", "CLF", "X", "AA", "ATI",
    "RS", "CRS", "WOR", "HAYN", "CENX", "KALU", "ARCH", "HCC", "BTU", 
    "CEIX", "ARLP", "AMR", "HL", "PAAS", "AG", "EXK", "CDE", "FSM", "RGLD",
    "WPM", "FNV", "SBSW", "OR", "SAND", "SSRM", "BTG", "IAG", "HMY", "DRD",
    "NGD", "GATO", "GPL", "SILV", "MAG", "SVM", "MUX", "EGO", "USAS",
    # Aluminum
    "ARNC", "CSTM", "NHYDY",  # Aluminum producers
    # Steel
    "TX", "TMST", "SCHN", "RYI", "SXC", "UFAB", "WS", "WIRE", "NMM", "PRLB",
    "MATV", "CMC", "STLD", "MT", "PKX", "SID", "VALE", "RIO", "BHP",
    # Paper & Forest Products
    "IP", "WRK", "PKG", "SON", "SEE", "BLL", "CCK", "ATR", "GEF", "BERY",
    "UFPT", "PACK", "KRT", "CLW", "LSB", "SWM", "TG", "GLT", "RYN", "WY",
    "PCH", "PPC", "SLVM", "GPK", "TRS", "TREC", "CKH", "UFS", "UFPI", "LPX",
]

SECTOR_20_INDUSTRIALS = [
    # Aerospace & Defense
    "BA", "LMT", "NOC", "GD", "RTX", "HII", "TDG", "LHX", "HWM", "TXT",
    "AXON", "CW", "SPR", "HXL", "DCO", "AIR", "VSEC", "KTOS", "MRCY",
    "AVAV", "RCAT", "BWXT", "LDOS", "CACI", "SAIC", "PSN", "VVX", "PKE",
    "SPCE", "ACHR", "JOBY", "LILM", "BLDE", "RDW", "ASTR", "RKLB", "ASTS",
    "IRDM", "GSAT", "SATS", "VSAT", "GILT", "MANU", "ISDR", "SPIR", "BKSY",
    # Building Products
    "JCI", "CARR", "TT", "LII", "MAS", "FBHS", "AWI", "DOOR", "AZEK", "BLD",
    "APOG", "GFF", "PGTI", "JELD", "TILE", "TREX", "SSD", "BLDR", "BCC",
    "OC", "IBP", "CSWI", "AAON", "NX", "UFPI", "SMG", "AMWD", "CNR",
    # Construction & Engineering
    "ACM", "MTZ", "PWR", "DY", "EME", "FIX", "PRIM", "TPC", "MYRG", "STRL",
    "ORN", "CTO", "IESC", "GVA", "KBR", "FLR", "AGX", "NVEE", "TTEK", "WSC",
    "AAMC", "AGS", "GLT", "ROAD", "CENX", "LPG",
    # Electrical Equipment (incl. Heavy Electrical)
    "ETN", "ROK", "EMR", "AME", "RBC", "GNRC", "AZZ", "ATKR", "WCC", "HUBB",
    "POWL", "AYI", "EAF", "WIRE", "NVT", "VRT", "PLUG", "FLUX", "LTCH",
    "FCEL", "BLDP", "HYLN", "BLNK", "CHPT", "EVGO", "NKLA", "RIDE", "GOEV",
    "ABB", "GE",  # Heavy Electrical Equipment
    # Industrial Conglomerates
    "MMM", "HON", "ITW", "ROP", "DHR", "IEP", "MGRC", "MDC", "GTES", "ESE",
    # Machinery
    "CAT", "DE", "PCAR", "CMI", "SWK", "TTC", "OSK", "AGCO", "CNHI", "ALG",
    "KMT", "MEC", "NPO", "CFX", "HAYW", "HLIO", "LNN", "MIDD", "MTW", "SXI",
    "TWI", "WTS", "BMI", "FLOW", "HI", "AIT", "GTLS", "IDEX", "IEX",
    "ITT", "LECO", "PNR", "RXO", "TKR", "WMS", "XYL", "CR", "PH",
    "IR", "FLS", "DOV",
    # Trading Companies & Distributors
    "GWW", "FAST", "WSO", "MSM", "SITE", "DXPE", "DNOW", "DXP", "HDSN", "PKOH",
    "SYX", "TITN", "HDS", "CCMP", "POOL", "HWKN", "EVI", "FELE",
    # Commercial Printing
    "RRD", "DFIN", "CMPR",  # Commercial printing companies
    # Security & Alarm Services
    "ALLE", "MSA", "NSSC", "PRSP", "OSIS", "ARLO",  # Security services
    # Passenger Ground Transportation
    "LYFT", "UBER", "CAR", "HTZ", "YELL",  # Ground transportation
    # Commercial Services
    "WM", "RSG", "WCN", "CWST", "SRCL", "CLH", "ECOL", "HCCI", "NVRI", "VSE",
    "ABM", "CTAS", "ARMK", "BCO", "BRC", "NSIT", "TISI", "SP", "CPRT", "ADMS",
    "SLQT", "ROLL", "LAUR", "MNST", "BFAM", "BCOV", "HMST", "TBI", "UONE",
    # Professional Services
    "ACN", "VRSK", "FTV", "TRI", "BR", "EEFT", "EFX", "EXPO", "FCN", "FORR",
    "HURN", "INFO", "KFRC", "MAN", "MMS", "TNET", "WST", "RHI", "HSKA", "BAH",
    "CRAI", "ICFI", "GMS", "MANT", "EXLS", "PRGS", "NV", "IIIV", "FRPT", "SSTI",
    # Airlines
    "DAL", "UAL", "LUV", "AAL", "ALK", "JBLU", "SAVE", "ALGT", "SKYW", "ULCC",
    "HA", "MESA", "RYAAY", "AZUL", "GOL", "CEA", "CPA", "ZNH", "SNCY",
    # Transportation - Rail, Trucking, Freight
    "UNP", "CSX", "NSC", "WAB", "GBX", "RAIL", "TRN", "FDX", "UPS", "XPO",
    "JBHT", "ODFL", "SAIA", "WERN", "LSTR", "HTLD", "KNX", "MRTN", "SNDR",
    "ARCB", "CHRW", "EXPD", "HUBG", "ECHO", "GXO", "FWRD", "RLGT", "DSKE",
    "PTVE", "USAK", "USX", "TLRY", "SBLK", "DAC", "ZIM", "INSW", "NMM",
    "GOGL", "STNG", "EURN", "FLNG", "TNK", "CPLP", "SALT", "DSX", "GNK",
]

SECTOR_25_CONSUMER_DISCRETIONARY = [
    # Auto Manufacturers
    "F", "GM", "TSLA", "RIVN", "LCID", "FSR", "NIO", "XPEV", "LI", "GOEV",
    "WKHS", "RIDE", "SOLO", "NKLA", "FFIE", "ARVL", "LAZR", "MVIS", "LIDR",
    "OUST", "VLDR", "CPTN", "AEVA", "INVZ", "AEHR", "OSK", "WGO", "THO", "CWH",
    "LCII", "REV", "CVII", "HYLN", "XL",
    # Auto Parts (removed duplicates from Auto Manufacturers)
    "APTV", "BWA", "LEA", "MGA", "ALV", "ADNT", "AXL", "GNTX", "VC", "DAN",
    "MOD", "PHIN", "SMP", "THRM", "AEY", "DORM", "FOXF", "LKQ", "SRI",
    "STRT", "SUP", "TEN", "MTOR", "CDMO", "SHYF", "GTXMQ", "FRSX", "BSQR",
    # Tires & Rubber
    "GT", "CTB", "ALSN",  # Tire and rubber companies
    # Motorcycle Manufacturers
    "HOG", "PII",  # Motorcycle/powersports
    # Auto Retail
    "AN", "ABG", "GPI", "PAG", "LAD", "SAH", "RUSHA", "KMX", "CVNA", "SFT",
    "CARS", "CARG", "VRM", "CZOO", "LOTZ", "DRVN", "HYRE", "SOS", "FRSH",
    # Home Improvement Retail
    "HD", "LOW", "FND", "LL", "SHC",
    # Homebuilding
    "DHI", "LEN", "PHM", "NVR", "TOL", "KBH", "TMHC", "MDC", "MTH", "MHO",
    "TPH", "SKY", "CCS", "HOV", "BZH", "GRBK", "CVCO", "LGIH", "DFH", "LEGH",
    "UHG", "MERH", "NOAH", "STRW", "MSCI", "CBG", "JLL", "CWK", "RMR",
    # Household Appliances & Durables
    "WHR", "SEB", "IRBT", "NPK", "HBB", "IBP", "SN", "ALTO",
    "SHCAY", "SONY",  # Consumer electronics/appliances
    # Housewares & Specialties
    "COOK",  # Traeger grills
    # Leisure Products & Facilities
    "HAS", "MAT", "POOL", "BC", "PTON", "NLS", "PRKS", "FNKO", "JAKK", "PLNT",
    "PLAY", "TRAK", "VSTO", "YETI", "FIZZ", "NILE", "CLVR", "PRPH",
    "GOLF", "ESGL", "FUN", "SIX", "SEAS", "SUM", "MTN", "SKI", "EPR",
    "XPOF",  # Xponential Fitness
    # Apparel & Luxury
    "NKE", "LULU", "TPR", "VFC", "PVH", "RL", "CPRI", "GIII", "GIL", "COLM",
    "UAA", "CROX", "DECK", "SKX", "SHOO", "WWW", "WEYS", "CATO", "HNST", "GES",
    "LEVI", "GOOS", "HBI", "SCVL", "CAL", "SMRT", "FIGS", "ONON", "HELE",
    "BOOT", "CURV", "DXLG", "CTRN", "EXPR", "AEO", "ANF", "BKE", "ZUMZ",
    # Home Furnishings
    "RH", "WSM", "ARHS", "ETH", "LOVE", "SNBR", "PRPL", "CSPR", "TPX", "LEG",
    "HVT", "FLXS", "PATK", "AMWD", "LCUT", "TILE",
    # Casinos & Gaming
    "LVS", "WYNN", "MGM", "CZR", "DKNG", "PENN", "BYD", "MLCO", "RRR", "GDEN",
    "IGT", "SGMS", "GAN", "RSI", "BALY", "CHDN", "WBET", "GMBL", "SGHC", "EVRI",
    "AGS", "NUVB", "BETZ", "NGMS", "GIG", "PUCK", "LUCK", "WMS",
    # Hotels & Resorts
    "MAR", "HLT", "H", "IHG", "WH", "CHH", "VAC", "TNL", "PLYA", "HGV",
    "BHR", "STAY", "CLDT", "HT", "RHP", "WYNDQ", "SVC", "APTS", "AHT", "DRH",
    "PK", "PEB", "RLJ", "SHO", "XHR", "INN", "SOHO", "HTGC", "ASHF", "HTLD",
    # Restaurants
    "MCD", "SBUX", "DPZ", "CMG", "YUM", "QSR", "WEN", "DNUT", "PZZA", "DRI",
    "TXRH", "BLMN", "EAT", "CAKE", "DIN", "JACK", "TACO", "WING", "SHAK", "BROS",
    "CAVA", "SG", "LOCO", "ARCO", "ARKR", "NDLS", "PBPB", "KRUS", "BJRI", "FAT",
    "RAVE", "RRGB", "RUTH", "BAGR", "KTRA", "RICK", "MSSR", "NATH", "CBRL",
    # Computer & Electronics Retail
    "CONN", "WINA", "RST",  # Electronics retailers
    # Consumer Electronics
    "GPRO", "KOSS", "VUZI", "UEIC", "VOXX",  # Consumer electronics manufacturers
    # Specialty Retail
    "AMZN", "TGT", "COST", "WMT", "DG", "DLTR", "FIVE", "OLLI", "BBY", "GME",
    "CHWY", "W", "ETSY", "EBAY", "WISH", "SHOP", "GRPN", "OPEN", "RENT",
    "BIRD", "TDUP", "REAL", "PRTS", "SSTK", "TCS", "ASO", "DKS", "HIBB", "SPWH",
    "PLCE", "BURL", "ROST", "TJX", "GPS", "AAP",
    "AZO", "ORLY", "GPC", "MNRO", "MPAA", "MOV", "FUL",
    "SIG", "KAR", "CPRT", "SBH", "ULTA", "EYE", "WOOF", "HEAR",
    # Education Services
    "CHGG", "COUR", "DUOL", "LRN", "ATGE", "LOPE", "PRDO", "STRA", "TWOU",
    "UDMY", "LAUR", "LINC", "HLG", "AFYA", "GHC", "MEDP", "UTI", "APEI",
]

SECTOR_30_CONSUMER_STAPLES = [
    # Food & Beverage
    "PEP", "KO", "MDLZ", "KHC", "GIS", "K", "CAG", "CPB", "SJM", "HRL",
    "TSN", "PPC", "JJSF", "LANC", "INGR", "DAR", "CALM", "HAIN", "SMPL", "THS",
    "BRBR", "SENEA", "USFD", "DOLE", "CELH", "FIZZ", "MNST",
    "ZVIA", "FRPT", "FREE", "FARM", "LNDC", "SFD", "CVGW", "STKL", "BERY",
    "MGPI", "PSMT", "CSWI", "SEB", "BRCC", "VFF", "SFIX", "BWMN",
    # Beverages
    "BUD", "TAP", "SAM", "STZ", "DEO", "ABEV", "CCU", "PRMW", "WVVI", "COCO",
    "NAPA", "NBEV", "WEYS", "COKE", "CCEP", "REED",
    # Tobacco
    "PM", "MO", "BTI", "TPB", "VGR", "UVV", "CRLBF", "GRNH", "CURLF", "AYRWF",
    "TCNNF", "GTBIF", "CCHWF", "TRSSF", "JUSHF", "MSOS", "MJ", "POTX",
    # Household Products
    "PG", "CL", "CHD", "CLX", "KMB", "SPB", "EPC", "ELF", "IPAR",
    "CENT", "NUS", "USNA", "ENR", "REV", "COTY", "SKIN", "OLPX",
    "GROV", "HLF", "NU", "HIMS", "HYFM", "NATR", "CMBM", "NWL", "SBH", "REVG",
    # Personal Products
    "EL", "PRGO", "HNST", "MAMA", "OMI", "TREE", "BNED",
    # Retail - Grocery
    "KR", "ACI", "SFM", "IMKTA", "BGS", "GO", "NDLS", "CASY", "VLGEA", "WMK",
    "NGVC", "CHEF", "PFGC", "UNFI", "SPTN", "OLLI", "FWRG",
]

SECTOR_35_HEALTHCARE = [
    # Biotechnology
    "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "BNTX", "SGEN", "ALNY",
    "INCY", "BMRN", "EXEL", "IONS", "UTHR", "RARE", "NBIX", "SRPT", "BLUE",
    "SGMO", "EDIT", "CRSP", "NTLA", "BEAM", "VERV", "TWST", "DNA", "ALLO",
    "RXRX", "KRYS", "ARWR", "FOLD", "DNLI", "KYMR", "KROS", "BCRX", "ARQT",
    "DRNA", "MYOV", "BGNE", "LEGN", "RPRX", "ROIV", "JANX", "VERA", "IDYA",
    "RCUS", "NVAX", "VXRT", "INO", "MRVI", "CRBU", "ATAI", "MNMD", "CMPS",
    "IMVT", "PRTA", "SRRK", "SANA", "VIR", "ABCL", "PTGX", "MORF", "CCCC",
    "XNCR", "APLS", "RXDX", "TNGX", "ETNB", "SWTX", "AVXL", "LXRX",
    "CGEM", "VRDN", "DAWN", "ACAD", "ANNX", "GERN", "REPL", "ALLK",
    "BOLT", "MLYS", "TARS", "ARDX", "AKRO", "CRMD", "KRON", "BCAB",
    "IMMP", "LYRA", "NRIX", "OLMA", "PRTC", "ZYME", "DCPH", "FGEN", "CMRX",
    "ADVM", "BLCM", "ELVN", "FATE", "FULC", "ORIC", "PHVS", "RVMD", "SPRO",
    # Pharmaceuticals
    "JNJ", "PFE", "LLY", "MRK", "ABBV", "BMY", "ZTS", "VTRS", "TEVA", "PRGO",
    "HLN", "ELAN", "SUPN", "CTLT", "JAZZ", "PCRX", "IRWD", "PAHC", "RVNC",
    "SLNO", "AKBA", "ITCI", "AMPH", "ANI", "CORT", "CPRX", "DRRX", "EOLS",
    "ENTA", "GHRS", "GTHX", "HRTX", "KMPH", "LBPH", "MNOV", "ORGO", "PDCO",
    "PLRX", "PRTX", "RETA", "SIGA", "THTX", "USPH", "VNDA", "XERS", "ZLAB",
    # Medical Devices
    "ABT", "MDT", "SYK", "BSX", "ISRG", "EW", "ZBH", "DXCM", "HOLX", "ALGN",
    "RMD", "TFX", "NVST", "SWAV", "PEN", "GMED", "RGEN", "PODD", "INSP",
    "TNDM", "GKOS", "LIVN", "STAA", "ATRC", "MMSI", "IRTC", "OFIX", "CNMD",
    "NARI", "LMAT", "NUVA", "NVCR", "MASI", "HAE", "ESTA", "ATEC", "AXGN",
    "INGN", "LUNG", "ICAD", "SIBN", "SILK", "OPRX", "PROC", "PRPH", "KIDS",
    "STIM", "NNOX", "NURO", "BTCY", "OSH", "AXNX", "CUTR", "GHDX", "SRDX",
    # Health Care Facilities & Services
    "UNH", "ELV", "HUM", "CI", "CNC", "MOH", "UHS", "THC", "ACHC", "HCA",
    "DVA", "ADUS", "ENSG", "PNTG", "SEM", "NHC", "CCRN", "SGRY",
    "OPCH", "ALHC", "HCSG", "BKD", "AFMD", "EVH", "GH", "ONEM", "PRVA",
    "EHAB", "DOCS", "PHR", "TALK", "AMWL", "TDOC", "HIMS", "HURN", "PGNY",
    "OSCR", "LFST", "CLVR", "SHCR", "ACCD", "SOPH", "HLAH", "PHAR", "CMAX",
    # Life Sciences Tools
    "TMO", "DHR", "A", "BIO", "ILMN", "MTD", "WAT", "PKI", "TECH", "CRL",
    "ICLR", "MEDP", "RVTY", "CDNA", "EXAS", "VCYT", "NVTA", "ME", "VEEV",
    "MYGN", "NTRA", "PACB", "TXG", "FLGT", "NEO", "MXCT",
    "CSTL", "NGMS", "PSNL", "RDNT", "SDGR", "SEER", "CHRS", "HCAT", "MTSI",
]

SECTOR_40_FINANCIALS = [
    # Banks - Diversified & Regional
    "JPM", "BAC", "WFC", "C", "GS", "MS", "SCHW", "BK", "STT", "PNC",
    "TFC", "USB", "COF", "AXP", "DFS", "SYF", "ALLY", "HBAN", "KEY", "RF",
    "CFG", "FITB", "MTB", "ZION", "CMA", "SIVB", "PACW", "WAL", "FHN",
    "BOKF", "SNV", "VLY", "WBS", "EWBC", "GBCI", "ONB", "PNFP",
    "SBCF", "SEIC", "TOWN", "UBSI", "WAFD", "WSFS", "ASB", "BHF", "FBK",
    "FFIN", "FULT", "IBOC", "NBTB", "SBNY", "TBBK", "TCBI", "UCBI", "COLB",
    "CATY", "CVBF", "DCOM", "EFSC", "FMBI", "FRME", "GABC", "HWC", "INDB",
    "IBTX", "OFG", "PRK", "RNST", "SBSI", "SFBS", "STBA", "NYCB",
    "BPOP", "FBP", "BANC", "CPF", "LBAI", "MBFI", "ORRF", "PVBC", "SASR",
    "SMBC", "SYBT", "THFF", "UVSP", "BHLB", "BOCH", "CFFI", "CHCO", "CHMG",
    "CNOB", "EQBK", "FBIZ", "FCBC", "FMBH", "HNVR", "HOMB", "HTBK", "HTLF",
    "IBCP", "LCNB", "MBWM", "MNSB", "MOFG", "NBHC", "NRIM", "OPBK", "OSBC",
    "PKBK", "PLBC", "RBCAA", "SFNC", "SRCE", "SSB", "TRMK", "WABC", "WSBC",
    # Asset Management & Investment Banking
    "BLK", "BX", "KKR", "APO", "ARES", "OWL", "CG", "TPG", "TROW", "IVZ",
    "BEN", "FHI", "VCTR", "PZN", "GHL", "PJT", "MC", "MKTX", "LPLA", "CBOE",
    "CME", "ICE", "NDAQ", "COIN", "HOOD", "IBKR", "ETFC",
    "VIRT", "EVR", "HLI", "JEF", "LPL", "RJF", "SF", "PIPR", "SNEX", "COWN",
    "OPCH", "SCU", "STEP", "TWST", "WETF", "WDR", "DHF", "DSL", "EXG",
    # Insurance
    "BRK.A", "BRK.B", "PGR", "ALL", "TRV", "CB", "AIG", "MET", "PRU", "AFL",
    "AJG", "MMC", "AON", "WTW", "BRO", "ERIE", "CNA", "Y", "RNR", "THG",
    "WRB", "AIZ", "CNO", "FAF", "FNF", "GL", "HIG", "KMPR", "L", "LNC",
    "ORI", "PFG", "PLMR", "RDN", "RGA", "SLF", "SIGI", "CINF", "KNSL",
    "MCY", "MGRC", "NMIH", "RYAN", "ROOT", "ACGL", "AFG", "AGO", "ANAT",
    "AXS", "BCRH", "GNW", "HMN", "JRVR", "KREF", "LMND", "LTPZ", "MHLD",
    "NWLI", "OSCR", "PRIM", "RILY", "STC", "STFC",
    # Multi-Sector Holdings
    "FWONA", "SPLP", "LORL", "LTRPA", "GNE",  # Diversified holding companies
    # Financial Services
    "V", "MA", "PYPL", "SQ", "FIS", "FISV", "GPN", "AFRM", "UPST", "SOFI",
    "OPEN", "BILL", "PAYO", "MQ", "TOST", "NAVI", "SLM",
    "ESNT", "MTG", "RDFN", "UWMC", "RKT", "GHLD", "CURO", "ENVA", "TREE",
    "OMF", "OZK", "PFSI", "PRAA", "QFIN", "RELY", "WRLD", "CACC", "ELVT",
    "FCFS", "GSKY", "LPRO", "MGNI", "MOGO", "MSCI",
    "RPAY", "STNE", "VNT", "XP", "LSCC", "FRHC", "IMXI", "CNNE",
]

SECTOR_45_INFORMATION_TECHNOLOGY = [
    # Software - Application
    "MSFT", "ORCL", "CRM", "ADBE", "INTU", "NOW", "WDAY", "PANW", "ZS",
    "CRWD", "NET", "DDOG", "ZM", "SNOW", "PLTR", "TEAM", "SPLK", "OKTA",
    "HUBS", "MDB", "TWLO", "U", "PATH", "CFLT", "BILL", "DOCU", "ASAN",
    "APPF", "APPS", "AVLR", "BLKB", "BSY", "CDNS", "CHKP", "CLDR", "COUP",
    "CRTO", "DCT", "DOMO", "ESTC", "EVBG", "FIVN", "FROG", "FSLY", "GTLB",
    "JAMF", "MANH", "MSTR", "NCNO", "NICE", "OOMA", "PD", "PING", "PLAN",
    "PS", "PYCR", "QTWO", "RAMP", "RNG", "RPD", "SAIL", "SITM", "SMAR",
    "SPT", "SUMO", "TYL", "VEEV", "WIX", "WKME", "ZEN", "ZI", "ZUO", "BOX",
    "CCCS", "CLVT", "COMM", "CSGP", "DOCN", "DT", "ECOM", "ENVX", "EVCM",
    "EVOP", "FRSH", "GENI", "GWRE", "INFA", "KNBE", "LSPD", "MCFE",
    "MGNI", "MNDY", "NEWR", "OPAD", "QLYS", "REKR", "S", "SCWX",
    "SNCR", "SPNS", "SQSP", "SVMK", "TASK", "TBIO", "UPST", "WK",
    "WOLF", "XMTR", "YEXT", "YOU", "ZUORA", "ATVI", "EA", "TTWO",
    # Software - Infrastructure
    "IBM", "VMW", "FTNT", "SNPS", "KEYS", "AKAM", "FFIV", "GEN",
    "TENB", "VRNS", "VRNT", "RDWR", "NLOK", "MIME", "LDOS",
    "CTXS", "ANSS", "SYNC", "NTNX", "PSTG", "NATI", "CDK",
    # Semiconductors
    "NVDA", "AMD", "INTC", "TXN", "AVGO", "QCOM", "MU", "ADI", "NXPI",
    "MCHP", "LRCX", "AMAT", "KLAC", "MRVL", "ON", "SWKS", "QRVO", "MPWR",
    "SLAB", "DIOD", "RMBS", "CRUS", "FORM", "HIMX", "IMOS", "LSCC", "MTSI",
    "POWI", "SIMO", "SMTC", "ENTG", "KLIC", "MKSI", "ONTO", "UCTT",
    "ACMR", "AMKR", "AOSL", "ASML", "COHU", "LEDS", "NVMI", "PLAB", "SMCI",
    "TSM", "UMC", "AEHR", "ALGM", "AMBA", "AXTI", "CCMP", "CEVA", "CRDO",
    "GFS", "GSIT", "ICHR", "MXIM", "OLED", "PDFS",
    "SGH", "SYNA", "TER", "TSEM", "UTSI",
    # IT Services
    "ACN", "CTSH", "FIS", "FISV", "IT", "WIT", "EPAM", "GLOB", "GDYN",
    "EXLS", "PEGA", "PRFT", "SSNC", "TTEC", "VNET", "WEX", "BR", "CACI",
    "CNXC", "DXC", "FAF", "FOUR", "G", "GIB", "JKHY", "KD",
    "LPSN", "MANT", "MAXN", "SAIC", "SSTI", "TLRY", "UPWK",
    # Hardware
    "AAPL", "HPQ", "HPE", "DELL", "NTAP", "WDC", "STX", "LOGI",
    "CRSR", "DGII", "DSGX", "HEAR", "IMMR", "NTGR", "SSYS", "ZBRA",
    "LQDT", "VIAV", "GLW", "APH", "TEL", "CDW", "NSIT", "SNX", "ATEN",
    "CLFD", "INSG", "SILC", "TRMB", "VICR",
    # Communications Equipment
    "CSCO", "MSI", "JNPR", "UI", "CIEN", "LITE", "CALX", "HLIT",
    "INFN", "IRDM", "CASA", "DZSI", "IDCC", "VCNX",
]

SECTOR_50_COMMUNICATION_SERVICES = [
    # Cable & Satellite
    "CABO", "DISH", "WOW",  # Cable/satellite operators
    # Interactive Media & Services
    "GOOGL", "META", "SNAP", "PINS", "MTCH", "BMBL", "IAC", "ZG", "YELP",
    "GRPN", "ANGI", "TTD", "MGNI", "PUBM", "CARG", "CARS", "EVER",
    "QNST", "DHC", "SPOT", "SONO", "SSTK", "EDIT", "VNET", "WB", "LZ",
    # Entertainment
    "DIS", "NFLX", "CMCSA", "CHTR", "WBD", "AMC", "CNK", "IMAX", "ROKU",
    "SIRI", "TME", "WMG", "MSGS", "MSGE", "LYV", "FOX",
    "FOXA", "NWS", "NWSA", "VIAC", "DISCB", "DISCK", "DISCA", "GTN", "SSP",
    "IHRT", "CTO", "EVC", "GCI", "GME", "ISIG", "KNSL", "LBTYB", "LBTYK",
    "LSXMA", "LSXMB", "LSXMK", "NRDY", "PARA", "SCHL", "TGNA", "TRIP",
    # Gaming
    "RBLX", "DKNG", "GOGO", "GLBE", "HUYA", "BILI", "DDL",
    "DOYU", "GRVY", "PLTK", "SKLZ", "SOHU", "AGFY", "PERI", "ZNGA",
    "SRAD", "TSQ", "FUBO", "MYPS", "NCTY", "SLGG", "ESPO", "HERO", "NERD",
    # Telecom
    "T", "VZ", "TMUS", "LUMN", "USM", "TDS", "SHEN", "LBRDA",
    "LBRDK", "SBAC", "CCI", "AMT", "EQIX", "DLR", "UNIT", "CCOI", "GDS",
    "CORD", "OOMA", "BAND", "LNTH", "CMTL", "CNSL", "IRDM",
    # Advertising & Media
    "OMC", "IPG", "DLX", "ZETA", "MGID", "ADT",
    "SCOR", "DSP", "IAS", "NCMI", "NEXS", "QUAD", "STCN",
    "TBLA", "VERX", "ADV", "BIGC", "BKNG", "EXPE", "SABR",
]

SECTOR_55_UTILITIES = [
    # Electric Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "ED", "PCG",
    "EIX", "WEC", "ES", "DTE", "AEE", "ETR", "FE", "PPL", "CMS", "EVRG",
    "PNW", "AES", "LNT", "OGE", "NWE", "NRG", "POR", "IDA", "AVA", "EE",
    "BKH", "NWN", "PNM", "UTL", "AWA", "AQN", "AGR",
    "AEG", "AMPS", "ATO", "BIPC", "BIP", "CWEN", "CNP", "CPK", "CWENA",
    "DUKB", "EMRAF", "ENPH", "FSLR", "GPJA", "GPRK", "HE", "HIFR", "MGEE",
    "NFG", "NI", "NJR", "OGS", "OTTR", "PEGI", "PEG", "SBS",
    # Gas Utilities
    "SR", "SWX", "UGI", "ONE", "SJI",
    "RGCO", "SMLP", "SPH", "APU",
    # Multi-Utilities & Water
    "AWK", "WTRG", "CWT", "SJW", "YORW", "MSEX", "AWR", "ARTNA", "CWCO",
    "GWRS", "PNR", "WTR", "XYL", "RXN", "AQUA", "TTC", "BMI", "FELE",
    # Renewable Energy
    "NEP", "BEP", "HASI", "ORA", "RUN", "SPWR", "NOVA",
    "SEDG", "JKS", "ARRY", "CSIQ", "MAXN", "SHLS", "STEM",
    "OPAL", "PLUG", "BLDP", "FCEL", "BE", "CLNE", "EVGO", "CHPT", "BLNK",
    "DCFC", "PTRA", "PSNY", "RIVN", "LCID", "FSR", "GOEV", "NKLA", "WKHS",
]

SECTOR_60_REAL_ESTATE = [
    # Real Estate Development
    "FOR", "HHH", "JOE", "STRS", "BRG",  # Real estate development
    # REITs - Diversified
    "SPG", "O", "VICI", "WPC", "STOR", "NNN", "GTY", "GOOD", "AAT",
    "ALX", "BDN", "BRX", "CDP", "CDR", "CERS",
    # REITs - Industrial
    "PLD", "DRE", "REXR", "STAG", "TRNO", "FR", "EGP", "COLD", "IIPR", "LAND",
    "MNR", "PSTL", "PLYM", "GMRE", "ILPT", "INDT", "LXP", "NLCP",
    # REITs - Office
    "BXP", "KRC", "SLG", "VNO", "HIW", "CUZ", "PGRE", "JBGS", "DEI", "PDM",
    "OFC", "ESRT", "CLI", "FSP", "ALEX", "CIO", "CXP",
    "EQC", "ARE", "CADE", "CCIT", "COR", "DEA", "HPP", "NLY",
    # REITs - Residential
    "EQR", "AVB", "ESS", "UDR", "CPT", "MAA", "AIV", "IRT", "NXRT", "ELME",
    "VRE", "CSR", "AHH", "IRET", "NEN", "SAFE", "STAR", "UMH", "VERIS",
    # REITs - Retail
    "REG", "FRT", "KIM", "SITC", "ROIC", "UE", "AKR", "KRG", "MAC",
    "PEI", "CBL", "WRI", "WSR", "BFS", "FCPT", "IVT", "KITE",
    "OLP", "PECO", "RPT", "SKT", "STON", "UBA", "URG", "WHLR",
    # REITs - Healthcare
    "WELL", "VTR", "PEAK", "HR", "OHI", "LTC", "NHI", "SBRA", "CTRE", "CHCT",
    "MPW", "DOC", "GHC", "CMCT", "CTR", "HASI",
    # REITs - Self Storage
    "PSA", "EXR", "CUBE", "LSI", "NSA", "JCAP", "SELF", "SSS",  # Self-storage REITs
    # REITs - Data Center & Infrastructure
    "EQIX", "DLR", "AMT", "CCI", "SBAC", "UNIT", "CCOI", "CONE", "CORZ", "QTS",
    "LADR", "LMRK", "SATS", "SBA", "VNET", "WIFI", "ZAYO",
    "INXN", "SIFY",  # Data center REITs
    # REITs - Timber
    "CUT",  # Timber REIT/ETF
    # REITs - Hotel
    "HST", "PK", "RHP", "PEB", "SHO", "DRH", "XHR", "INN", "CLDT", "AHT",
    "APLE", "BHR", "CHSP", "CPLG", "CRLBF", "FCH", "HT", "RLJ", "SOHO",
    # Real Estate Services
    "CBRE", "JLL", "CWK", "NMRK", "RMR", "FSV", "EXPI", "CIGI", "HF", "RMAX",
    "COMP", "OPEN", "RDFN", "RLGY", "CSGP", "REAL", "ZG", "IMXI",
]

# =============================================================================
# TARGETED STOCKS FOR UNDERREPRESENTED SUB-INDUSTRIES
# These are specifically chosen to fill sub-industries with fewer than 4 stocks
# =============================================================================

# Maps GICS sub-industry name to specific tickers that belong to it
# DEDUPLICATED - each ticker appears in only ONE sub-industry (most appropriate fit)
TARGETED_SUBINDUSTRY_STOCKS = {
    # === MATERIALS (Sector 15) - Industries with <4 stocks ===
    
    "Forest Products": [
        # Note: WY, RYN, PCH are REITs → moved to Timber REITs
        "LPX",   # Louisiana-Pacific Corporation - building products (not REIT)
        "UFPI",  # UFP Industries Inc - wood products manufacturer
        "BCC",   # Boise Cascade Company - wood products (not REIT)
        "JELD",  # JELD-WEN Holding - windows/doors (wood)
        "AWI",   # Armstrong World Industries - wood flooring
        "TREX",  # Trex Company - composite decking
    ],
    
    "Copper": [
        "FCX",   # Freeport-McMoRan - largest copper producer
        "SCCO",  # Southern Copper Corporation
        "TECK",  # Teck Resources Limited
        "RIO",   # Rio Tinto Group (copper exposure)
        "BHP",   # BHP Group Limited (copper exposure)
        "HBM",   # Hudbay Minerals Inc
        "ERO",   # Ero Copper Corp
        "NEXA",  # Nexa Resources S.A.
    ],
    
    "Paper Products": [
        "IP",    # International Paper Company
        "WRK",   # WestRock Company
        "PKG",   # Packaging Corporation of America
        "SON",   # Sonoco Products Company
        "GPK",   # Graphic Packaging Holding Company
        "SEE",   # Sealed Air Corporation
        "GEF",   # Greif Inc
        "CLW",   # Clearwater Paper Corporation
        "SLVM",  # Sylvamo Corporation
        "UFS",   # Domtar Corporation
    ],
    
    "Commodity Chemicals": [
        "DOW",   # Dow Inc
        "LYB",   # LyondellBasell Industries N.V.
        "WLK",   # Westlake Corporation
        "OLN",   # Olin Corporation
        "TROX",  # Tronox Holdings plc
        "KRO",   # Kronos Worldwide Inc
        "CC",    # Chemours Company
        "HUN",   # Huntsman Corporation
        "MEOH",  # Methanex Corporation
        "IOSP",  # Innospec Inc
    ],
    
    "Aluminum": [
        "AA",    # Alcoa Corporation
        "CENX",  # Century Aluminum Company
        "ARNC",  # Arconic Corporation
        "KALU",  # Kaiser Aluminum Corporation
        "CSTM",  # Constellium SE
        "NHYDY", # Norsk Hydro ASA
    ],
    
    "Industrial Gases": [
        "APD",   # Air Products and Chemicals Inc
        "LIN",   # Linde plc
        "INGR",  # Ingredion Incorporated
        "MTX",   # Minerals Technologies Inc
        "HWKN",  # Hawkins Inc
    ],
    
    # === INDUSTRIALS (Sector 20) - Industries with <4 stocks ===
    
    "Heavy Electrical Equipment": [
        "ETN",   # Eaton Corporation plc
        "EMR",   # Emerson Electric Co
        "ROK",   # Rockwell Automation Inc
        "ABB",   # ABB Ltd
        "GE",    # General Electric Company
        "GNRC",  # Generac Holdings Inc
        "VRT",   # Vertiv Holdings
        "NVT",   # nVent Electric plc
        "HUBB",  # Hubbell Incorporated
        "AYI",   # Acuity Brands Inc
        "POWL",  # Powell Industries Inc
    ],
    
    "Commercial Printing": [
        "RRD",   # R.R. Donnelley & Sons Company
        "QUAD",  # Quad/Graphics Inc
        "DFIN",  # Donnelley Financial Solutions Inc
        "CMPR",  # Cimpress plc
        "SSP",   # E.W. Scripps Company
        "DLX",   # Deluxe Corporation
        "SCHL",  # Scholastic Corporation
        "BNED",  # Barnes & Noble Education
    ],
    
    "Security & Alarm Services": [
        "ADT",   # ADT Inc
        "ALLE",  # Allegion plc
        "BCO",   # The Brink's Company
        "MSA",   # MSA Safety Incorporated
        "NSSC",  # NAPCO Security Technologies Inc
        "DGII",  # Digi International Inc
        "PRSP",  # Perspecta Inc
        "OSIS",  # OSI Systems Inc
        "ARLO",  # Arlo Technologies Inc
    ],
    
    "Passenger Ground Transportation": [
        "LYFT",  # Lyft Inc
        "UBER",  # Uber Technologies Inc
        "CAR",   # Avis Budget Group Inc
        "HTZ",   # Hertz Global Holdings Inc
        "DSKE",  # Daseke Inc
        "YELL",  # Yellow Corporation
        "ARCB",  # ArcBest Corporation
    ],
    
    # === CONSUMER DISCRETIONARY (Sector 25) - Industries with <4 stocks ===
    
    "Housewares & Specialties": [
        # Manufacturers of housewares, kitchen products, bedding
        "NWL",   # Newell Brands Inc - housewares conglomerate
        "TPX",   # Tempur Sealy International Inc - mattress manufacturer
        "HELE",  # Helen of Troy Limited - housewares & beauty
        "COOK",  # Traeger Inc - grills
        "LCUT",  # Lifetime Brands Inc - kitchenware manufacturer
        "PRPL",  # Purple Innovation Inc - mattress manufacturer
        "CSPR",  # Casper Sleep Inc - mattress manufacturer
    ],
    
    "Motorcycle Manufacturers": [
        # Note: Removed MRVL (Marvell Technology is semiconductors, not motorcycles)
        "HOG",   # Harley-Davidson Inc - motorcycles
        "PII",   # Polaris Inc - powersports vehicles
        "BC",    # Brunswick Corporation - marine/rec vehicles
        "THO",   # Thor Industries Inc - RVs
        "WGO",   # Winnebago Industries Inc - RVs
        "LCII",  # LCI Industries - RV components
        "CWH",   # Camping World Holdings Inc - RV retailer
        "FOXF",  # Fox Factory Holding - suspension systems
    ],
    
    "Tires & Rubber": [
        # Note: Removed PZZA (Papa John's is pizza, not tires!)
        "GT",    # The Goodyear Tire & Rubber Company
        "CTB",   # Cooper Tire & Rubber Company
        "GNTX",  # Gentex Corporation - auto mirrors
        "SRI",   # Stoneridge Inc - auto electronics
        "ALSN",  # Allison Transmission Holdings
        "MOD",   # Modine Manufacturing Company - thermal mgmt
        "DORM",  # Dorman Products Inc - auto parts
        "THRM",  # Gentherm Inc - thermal comfort
    ],
    
    "Household Appliances": [
        # Note: Removed duplicates (LCUT, HELE, PRPL, SNBR) → other categories
        "WHR",   # Whirlpool Corporation - major appliances
        "IRBT",  # iRobot Corporation - robotic vacuums
        "NPK",   # National Presto Industries Inc - small appliances
        "HBB",   # Hamilton Beach Brands - small kitchen appliances
        "SEB",   # Seaboard Corporation
        "SHCAY", # Sharp Corporation - electronics/appliances
        "SONY",  # Sony Group Corporation - electronics
    ],
    
    "Homefurnishing Retail": [
        # Retailers of home furnishings
        "WSM",   # Williams-Sonoma Inc - kitchenware retail
        "RH",    # Restoration Hardware Holdings Inc - luxury furniture
        "ARHS",  # Arhaus Inc - furniture retailer
        "ETH",   # Ethan Allen Interiors Inc - furniture retail
        "SNBR",  # Sleep Number Corporation - mattress retail (has stores)
        "LOVE",  # The Lovesac Company - furniture retail
        "FND",   # Floor & Decor Holdings - flooring retail
        "LL",    # LL Flooring Holdings - flooring retail
        "TILE",  # Interface Inc - flooring
        "HVT",   # Haverty Furniture Companies - furniture retail
    ],
    
    "Leisure Facilities": [
        "SIX",   # Six Flags Entertainment Corporation
        "FUN",   # Cedar Fair L.P.
        "SEAS",  # SeaWorld Entertainment Inc
        "PLNT",  # Planet Fitness Inc
        "XPOF",  # Xponential Fitness Inc
        "PTON",  # Peloton Interactive
        "MTN",   # Vail Resorts Inc
        "SKI",   # Peak Resorts
        "EPR",   # EPR Properties (entertainment REIT)
        "CNK",   # Cinemark Holdings
    ],
    
    "Computer & Electronics Retail": [
        # Note: Removed HEAR, CRSR, LOGI → Consumer Electronics (manufacturers)
        "BBY",   # Best Buy Co Inc - electronics retailer
        "GME",   # GameStop Corp - gaming retailer
        "CONN",  # Conn's Inc - electronics/appliance retail
        "WINA",  # Winmark Corporation - resale retail
        "RST",   # Rosetta Stone Inc - software retail
        "COST",  # Costco (has electronics section)
        "TGT",   # Target (has electronics section)
    ],
    
    "Consumer Electronics": [
        # Manufacturers of consumer electronics
        "AAPL",  # Apple Inc - consumer electronics
        "SONO",  # Sonos Inc - speakers
        "GPRO",  # GoPro Inc - cameras
        "HEAR",  # Turtle Beach Corporation - gaming headsets
        "KOSS",  # Koss Corporation - headphones
        "VUZI",  # Vuzix Corporation - smart glasses
        "CRSR",  # Corsair Gaming Inc - gaming peripherals
        "LOGI",  # Logitech International S.A. - peripherals
        "UEIC",  # Universal Electronics Inc - remote controls
        "VOXX",  # VOXX International Corporation - audio
    ],
    
    # === FINANCIALS (Sector 40) - Industries with <4 stocks ===
    
    "Specialized Finance": [
        "CACC",  # Credit Acceptance Corporation
        "WRLD",  # World Acceptance Corporation
        "ENVA",  # Enova International Inc
        "TREE",  # LendingTree Inc
        "QFIN",  # 360 Finance Inc
        "LPRO",  # Open Lending Corporation
        "ELVT",  # Elevate Credit Inc
        "OMF",   # OneMain Holdings Inc
        "SLM",   # SLM Corporation (Sallie Mae)
        "NAVI",  # Navient Corporation
    ],
    
    "Multi-Sector Holdings": [
        # Note: Removed LBRDK → Cable & Satellite (Liberty Broadband's main business)
        "BRK.B", # Berkshire Hathaway Inc
        "FWONA", # Liberty Media Formula One
        "JEF",   # Jefferies Financial Group Inc
        "SPLP",  # Steel Partners Holdings
        "IEP",   # Icahn Enterprises L.P.
        "LORL",  # Loral Space & Communications
        "LTRPA", # Liberty TripAdvisor Holdings
        "GNE",   # Genie Energy Ltd
    ],
    
    # === COMMUNICATION SERVICES (Sector 50) - Industries with <4 stocks ===
    
    "Cable & Satellite": [
        "CMCSA", # Comcast Corporation
        "CHTR",  # Charter Communications Inc
        "CABO",  # Cable One Inc
        "SIRI",  # Sirius XM Holdings Inc
        "DISH",  # DISH Network Corporation
        "WOW",   # WideOpenWest Inc
        "LBRDA", # Liberty Broadband Corporation Class A
        "LBRDK", # Liberty Broadband Corporation Class C
        "TGNA",  # TEGNA Inc
        "GTN",   # Gray Television Inc
    ],
    
    # === REAL ESTATE (Sector 60) - Industries with <4 stocks ===
    
    "Real Estate Development": [
        "FOR",   # Forestar Group Inc
        "HHH",   # Howard Hughes Corporation
        "JOE",   # St. Joe Company
        "STRS",  # Stratus Properties Inc
        "AHH",   # Armada Hoffler Properties Inc
        "SAFE",  # Safehold Inc
        "AIV",   # Apartment Investment and Management
        "AVB",   # AvalonBay Communities
        "BRG",   # Bluerock Residential Growth
    ],
    
    "Data Center REITs": [
        # Note: Removed AMT, CCI, SBAC, UNIT → Telecom Tower REITs (primary business)
        "EQIX",  # Equinix Inc - data centers
        "DLR",   # Digital Realty Trust Inc - data centers
        "QTS",   # QTS Realty Trust - data centers
        "CONE",  # CyrusOne Inc - data centers
        "CCOI",  # Cogent Communications Holdings
        "INXN",  # InterXion Holding - data centers
        "SIFY",  # Sify Technologies - data centers
    ],
    
    "Self-Storage REITs": [
        "PSA",   # Public Storage
        "EXR",   # Extra Space Storage Inc
        "CUBE",  # CubeSmart
        "LSI",   # Life Storage Inc
        "NSA",   # National Storage Affiliates Trust
        "SELF",  # Global Self Storage Inc
        "SSS",   # Sovran Self Storage
    ],
    
    "Telecom Tower REITs": [
        # Primary telecom tower/infrastructure companies
        "AMT",   # American Tower Corporation - telecom towers
        "CCI",   # Crown Castle Inc - telecom towers
        "SBAC",  # SBA Communications Corporation - telecom towers
        "UNIT",  # Uniti Group Inc - fiber infrastructure
        "LMRK",  # Landmark Infrastructure Partners
        "SATS",  # EchoStar Corporation
        "IRDM",  # Iridium Communications Inc
        "GSAT",  # Globalstar Inc
    ],
    
    "Timber REITs": [
        # Note: Removed LPX, BCC → Forest Products (manufacturers, not REITs)
        "WY",    # Weyerhaeuser Company - timber REIT
        "RYN",   # Rayonier Inc - timber REIT
        "PCH",   # PotlatchDeltic Corporation - timber REIT
        "CUT",   # Invesco MSCI Global Timber ETF
        "PLTK",  # Pope Resources - timber
    ],
}


def get_targeted_subindustry_tickers() -> dict:
    """Get tickers organized by targeted sub-industry name."""
    return TARGETED_SUBINDUSTRY_STOCKS.copy()


def get_all_targeted_tickers() -> list:
    """Get all tickers from targeted sub-industries as a flat list."""
    all_tickers = []
    for tickers in TARGETED_SUBINDUSTRY_STOCKS.values():
        all_tickers.extend(tickers)
    # Remove duplicates
    return list(set(all_tickers))


# =============================================================================
# COMBINED LIST
# =============================================================================

def get_all_additional_tickers() -> list:
    """Get all additional tickers from all sectors."""
    all_tickers = []
    all_tickers.extend(SECTOR_10_ENERGY)
    all_tickers.extend(SECTOR_15_MATERIALS)
    all_tickers.extend(SECTOR_20_INDUSTRIALS)
    all_tickers.extend(SECTOR_25_CONSUMER_DISCRETIONARY)
    all_tickers.extend(SECTOR_30_CONSUMER_STAPLES)
    all_tickers.extend(SECTOR_35_HEALTHCARE)
    all_tickers.extend(SECTOR_40_FINANCIALS)
    all_tickers.extend(SECTOR_45_INFORMATION_TECHNOLOGY)
    all_tickers.extend(SECTOR_50_COMMUNICATION_SERVICES)
    all_tickers.extend(SECTOR_55_UTILITIES)
    all_tickers.extend(SECTOR_60_REAL_ESTATE)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tickers = []
    for ticker in all_tickers:
        if ticker not in seen:
            seen.add(ticker)
            unique_tickers.append(ticker)
    
    return unique_tickers


def get_tickers_by_sector() -> dict:
    """Get tickers organized by sector code."""
    return {
        "10": SECTOR_10_ENERGY,
        "15": SECTOR_15_MATERIALS,
        "20": SECTOR_20_INDUSTRIALS,
        "25": SECTOR_25_CONSUMER_DISCRETIONARY,
        "30": SECTOR_30_CONSUMER_STAPLES,
        "35": SECTOR_35_HEALTHCARE,
        "40": SECTOR_40_FINANCIALS,
        "45": SECTOR_45_INFORMATION_TECHNOLOGY,
        "50": SECTOR_50_COMMUNICATION_SERVICES,
        "55": SECTOR_55_UTILITIES,
        "60": SECTOR_60_REAL_ESTATE,
    }

