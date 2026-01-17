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
        "WY",    # Weyerhaeuser Company - timber REIT
        "RYN",   # Rayonier Inc - timber REIT
        "PCH",   # PotlatchDeltic Corporation - timber REIT
        "CUT",   # Invesco MSCI Global Timber ETF
        "PLTK",  # Pope Resources - timber
    ],
    
    # === NEW SUB-INDUSTRIES FROM STOCKCHARTS DRILL-DOWN ===
    
    # Energy Sector Sub-Industries
    "Integrated Oil & Gas": [
        "XOM",   # Exxon Mobil Corporation
        "CVX",   # Chevron Corporation
        "COP",   # ConocoPhillips
        "OXY",   # Occidental Petroleum
        "HES",   # Hess Corporation
        "MPC",   # Marathon Petroleum
        "VLO",   # Valero Energy
        "PSX",   # Phillips 66
    ],
    
    "Oil & Gas Exploration & Production": [
        "EOG",   # EOG Resources
        "PXD",   # Pioneer Natural Resources
        "DVN",   # Devon Energy
        "FANG",  # Diamondback Energy
        "APA",   # APA Corporation
        "CTRA",  # Coterra Energy
        "MRO",   # Marathon Oil
        "EQT",   # EQT Corporation
        "OVV",   # Ovintiv Inc
        "CHRD",  # Chord Energy
        "MTDR",  # Matador Resources
        "PR",    # Permian Resources
        "TPL",   # Texas Pacific Land
        "MGY",   # Magnolia Oil & Gas
        "SM",    # SM Energy
    ],
    
    "Oil & Gas Refining & Marketing": [
        "VLO",   # Valero Energy
        "MPC",   # Marathon Petroleum
        "PSX",   # Phillips 66
        "DK",    # Delek US Holdings
        "PBF",   # PBF Energy
        "HFC",   # HollyFrontier
        "CVI",   # CVR Energy
        "DINO",  # HF Sinclair
        "PARR",  # Par Pacific Holdings
    ],
    
    "Oil & Gas Storage & Transportation": [
        "WMB",   # Williams Companies
        "KMI",   # Kinder Morgan
        "OKE",   # ONEOK Inc
        "TRGP",  # Targa Resources
        "ET",    # Energy Transfer
        "EPD",   # Enterprise Products Partners
        "MPLX",  # MPLX LP
        "PAA",   # Plains All American
        "LNG",   # Cheniere Energy
        "DTM",   # DT Midstream
    ],
    
    "Oil & Gas Equipment & Services": [
        "SLB",   # Schlumberger
        "HAL",   # Halliburton
        "BKR",   # Baker Hughes
        "NOV",   # NOV Inc
        "FTI",   # TechnipFMC
        "CHX",   # ChampionX Corporation
        "WHD",   # Cactus Inc
        "LBRT",  # Liberty Energy
        "HP",    # Helmerich & Payne
        "RIG",   # Transocean
    ],
    
    # Materials Sector Sub-Industries
    "Construction Materials": [
        "VMC",   # Vulcan Materials
        "MLM",   # Martin Marietta Materials
        "CRH",   # CRH plc
        "EXP",   # Eagle Materials
        "SUM",   # Summit Materials
        "USLM",  # United States Lime
    ],
    
    "Diversified Chemicals": [
        "DD",    # DuPont de Nemours
        "EMN",   # Eastman Chemical
        "CE",    # Celanese
        "HUN",   # Huntsman Corporation
        "AXTA",  # Axalta Coating Systems
        "AVNT",  # Avient Corporation
    ],
    
    "Specialty Chemicals": [
        "SHW",   # Sherwin-Williams
        "ECL",   # Ecolab
        "PPG",   # PPG Industries
        "IFF",   # International Flavors & Fragrances
        "ALB",   # Albemarle Corporation
        "RPM",   # RPM International
        "FUL",   # H.B. Fuller
        "ASH",   # Ashland Global Holdings
    ],
    
    "Fertilizers & Agricultural Chemicals": [
        "NTR",   # Nutrien Ltd
        "CF",    # CF Industries
        "MOS",   # The Mosaic Company
        "FMC",   # FMC Corporation
        "CTVA",  # Corteva Inc
        "SMG",   # The Scotts Miracle-Gro
        "ICL",   # ICL Group
    ],
    
    "Diversified Metals & Mining": [
        "FCX",   # Freeport-McMoRan
        "NUE",   # Nucor Corporation
        "CLF",   # Cleveland-Cliffs
        "STLD",  # Steel Dynamics
        "RS",    # Reliance Steel
        "CMC",   # Commercial Metals
        "ATI",   # ATI Inc
        "X",     # United States Steel
    ],
    
    "Gold": [
        "NEM",   # Newmont Corporation
        "GOLD",  # Barrick Gold
        "FNV",   # Franco-Nevada
        "WPM",   # Wheaton Precious Metals
        "RGLD",  # Royal Gold
        "AEM",   # Agnico Eagle Mines
        "KGC",   # Kinross Gold
    ],
    
    "Metal, Glass & Plastic Containers": [
        "BLL",   # Ball Corporation
        "CCK",   # Crown Holdings
        "AMCR",  # Amcor plc
        "BERY",  # Berry Global
        "SEE",   # Sealed Air Corporation
        "ATR",   # AptarGroup
        "SON",   # Sonoco Products
    ],
    
    # Industrials Sector Sub-Industries
    "Aerospace & Defense": [
        "RTX",   # RTX Corporation
        "BA",    # Boeing Company
        "LMT",   # Lockheed Martin
        "NOC",   # Northrop Grumman
        "GD",    # General Dynamics
        "LHX",   # L3Harris Technologies
        "TDG",   # TransDigm Group
        "HWM",   # Howmet Aerospace
        "TXT",   # Textron
        "HII",   # Huntington Ingalls
        "AXON",  # Axon Enterprise
    ],
    
    "Building Products": [
        "JCI",   # Johnson Controls
        "TT",    # Trane Technologies
        "CARR",  # Carrier Global
        "MAS",   # Masco Corporation
        "LII",   # Lennox International
        "AOS",   # A. O. Smith
        "FBHS",  # Fortune Brands
        "AWI",   # Armstrong World Industries
    ],
    
    "Construction & Engineering": [
        "ACM",   # AECOM
        "PWR",   # Quanta Services
        "EME",   # EMCOR Group
        "FLR",   # Fluor Corporation
        "MTZ",   # MasTec Inc
        "J",     # Jacobs Solutions
        "DY",    # Dycom Industries
        "STRL",  # Sterling Infrastructure
    ],
    
    "Electrical Components & Equipment": [
        "ETN",   # Eaton Corporation
        "EMR",   # Emerson Electric
        "GNRC",  # Generac Holdings
        "HUBB",  # Hubbell Incorporated
        "AYI",   # Acuity Brands
        "NVT",   # nVent Electric
        "VRT",   # Vertiv Holdings
    ],
    
    "Industrial Conglomerates": [
        "HON",   # Honeywell International
        "MMM",   # 3M Company
        "GE",    # GE Aerospace
        "ROP",   # Roper Technologies
        "ITW",   # Illinois Tool Works
    ],
    
    "Construction Machinery & Heavy Transportation Equipment": [
        "CAT",   # Caterpillar
        "DE",    # Deere & Company
        "PCAR",  # PACCAR
        "CMI",   # Cummins Inc
        "OSK",   # Oshkosh Corporation
        "TEX",   # Terex Corporation
    ],
    
    "Industrial Machinery & Supplies & Components": [
        "DOV",   # Dover Corporation
        "ITT",   # ITT Inc
        "PH",    # Parker-Hannifin
        "IR",    # Ingersoll Rand
        "XYL",   # Xylem Inc
        "IEX",   # IDEX Corporation
        "NDSN",  # Nordson Corporation
        "FLS",   # Flowserve Corporation
    ],
    
    "Trading Companies & Distributors": [
        "FAST",  # Fastenal Company
        "GWW",   # W.W. Grainger
        "WSO",   # Watsco Inc
        "SITE",  # SiteOne Landscape
        "MSM",   # MSC Industrial Direct
        "AIT",   # Applied Industrial Technologies
    ],
    
    "Environmental & Facilities Services": [
        "WM",    # Waste Management
        "RSG",   # Republic Services
        "WCN",   # Waste Connections
        "CTAS",  # Cintas Corporation
        "CLH",   # Clean Harbors
        "CWST",  # Casella Waste Systems
        "ABM",   # ABM Industries
    ],
    
    "Human Resource & Employment Services": [
        "ADP",   # Automatic Data Processing
        "PAYX",  # Paychex
        "DAY",   # Dayforce Inc
        "RHI",   # Robert Half
        "MAN",   # ManpowerGroup
        "KFRC",  # Kforce Inc
        "TBI",   # TrueBlue Inc
    ],
    
    "Research & Consulting Services": [
        "VRSK",  # Verisk Analytics
        "INFO",  # IHS Markit
        "FTV",   # Fortive Corporation
        "BR",    # Broadridge Financial
        "EXPO",  # Exponent Inc
        "FCN",   # FTI Consulting
        "HURN",  # Huron Consulting
    ],
    
    "Air Freight & Logistics": [
        "FDX",   # FedEx Corporation
        "UPS",   # United Parcel Service
        "EXPD",  # Expeditors International
        "CHRW",  # C.H. Robinson
        "XPO",   # XPO Inc
        "GXO",   # GXO Logistics
    ],
    
    "Passenger Airlines": [
        "DAL",   # Delta Air Lines
        "UAL",   # United Airlines
        "LUV",   # Southwest Airlines
        "AAL",   # American Airlines
        "ALK",   # Alaska Air Group
        "JBLU",  # JetBlue Airways
    ],
    
    "Rail Transportation": [
        "UNP",   # Union Pacific
        "CSX",   # CSX Corporation
        "NSC",   # Norfolk Southern
        "CP",    # Canadian Pacific
        "CNI",   # Canadian National Railway
    ],
    
    "Cargo Ground Transportation": [
        "ODFL",  # Old Dominion Freight Line
        "JBHT",  # J.B. Hunt Transport
        "SAIA",  # Saia Inc
        "WERN",  # Werner Enterprises
        "SNDR",  # Schneider National
        "KNX",   # Knight-Swift
        "LSTR",  # Landstar System
    ],
    
    # Consumer Discretionary Sub-Industries
    "Automobile Manufacturers": [
        "TSLA",  # Tesla Inc
        "GM",    # General Motors
        "F",     # Ford Motor
        "RIVN",  # Rivian Automotive
        "LCID",  # Lucid Group
        "NIO",   # NIO Inc
    ],
    
    "Automotive Parts & Equipment": [
        "APTV",  # Aptiv PLC
        "BWA",   # BorgWarner
        "LEA",   # Lear Corporation
        "MGA",   # Magna International
        "ALV",   # Autoliv Inc
        "GNTX",  # Gentex Corporation
        "VC",    # Visteon Corporation
    ],
    
    "Homebuilding": [
        "DHI",   # D.R. Horton
        "LEN",   # Lennar Corporation
        "PHM",   # PulteGroup
        "NVR",   # NVR Inc
        "TOL",   # Toll Brothers
        "KBH",   # KB Home
        "TMHC",  # Taylor Morrison
        "MHO",   # M/I Homes
        "MTH",   # Meritage Homes
    ],
    
    "Home Furnishings": [
        "WSM",   # Williams-Sonoma
        "MHK",   # Mohawk Industries
        "LEG",   # Leggett & Platt
        "SNBR",  # Sleep Number
        "TPX",   # Tempur Sealy
        "LOVE",  # Lovesac Company
        "ARHS",  # Arhaus Inc
    ],
    
    "Leisure Products": [
        "HAS",   # Hasbro
        "POOL",  # Pool Corporation
        "YETI",  # YETI Holdings
        "BC",    # Brunswick Corporation
        "PTON",  # Peloton Interactive
        "MAT",   # Mattel
    ],
    
    "Apparel, Accessories & Luxury Goods": [
        "NKE",   # Nike Inc
        "LULU",  # Lululemon Athletica
        "TPR",   # Tapestry Inc
        "VFC",   # VF Corporation
        "PVH",   # PVH Corp
        "RL",    # Ralph Lauren
        "CPRI",  # Capri Holdings
        "HBI",   # Hanesbrands
    ],
    
    "Footwear": [
        # NKE removed - primary classification is Apparel, Accessories & Luxury Goods
        "DECK",  # Deckers Outdoor
        "CROX",  # Crocs Inc
        "SKX",   # Skechers USA
        "ONON",  # On Holding
        "SHOO",  # Steven Madden
        "WWW",   # Wolverine World Wide
    ],
    
    "Casinos & Gaming": [
        "LVS",   # Las Vegas Sands
        "WYNN",  # Wynn Resorts
        "MGM",   # MGM Resorts
        "CZR",   # Caesars Entertainment
        "PENN",  # Penn Entertainment
        "DKNG",  # DraftKings
        "BYD",   # Boyd Gaming
        "MLCO",  # Melco Resorts
    ],
    
    "Hotels, Resorts & Cruise Lines": [
        "MAR",   # Marriott International
        "HLT",   # Hilton Worldwide
        "H",     # Hyatt Hotels
        "WH",    # Wyndham Hotels
        "CCL",   # Carnival Corporation
        "RCL",   # Royal Caribbean
        "NCLH",  # Norwegian Cruise Line
        "ABNB",  # Airbnb Inc
        "BKNG",  # Booking Holdings
    ],
    
    "Restaurants": [
        "MCD",   # McDonald's
        "SBUX",  # Starbucks
        "CMG",   # Chipotle Mexican Grill
        "YUM",   # Yum! Brands
        "DPZ",   # Domino's Pizza
        "DRI",   # Darden Restaurants
        "TXRH",  # Texas Roadhouse
        "WING",  # Wingstop
        "CAVA",  # CAVA Group
    ],
    
    "Education Services": [
        "LOPE",  # Grand Canyon Education
        "LRN",   # Stride Inc
        "DUOL",  # Duolingo
        "CHGG",  # Chegg Inc
        "COUR",  # Coursera
        "UDMY",  # Udemy Inc
        "STRA",  # Strategic Education
    ],
    
    "Specialized Consumer Services": [
        "DASH",  # DoorDash
        "UBER",  # Uber Technologies
        "LYFT",  # Lyft Inc
        # ABNB removed - primary classification is Hotels, Resorts & Cruise Lines
        "EXPE",  # Expedia Group
        # BKNG removed - primary classification is Hotels, Resorts & Cruise Lines
    ],
    
    "Broadline Retail": [
        "AMZN",  # Amazon.com
        "EBAY",  # eBay Inc
        "ETSY",  # Etsy Inc
        "W",     # Wayfair
        "SHOP",  # Shopify
    ],
    
    "Apparel Retail": [
        "TJX",   # TJX Companies
        "ROST",  # Ross Stores
        "BURL",  # Burlington Stores
        "GPS",   # Gap Inc
        "AEO",   # American Eagle
        "ANF",   # Abercrombie & Fitch
    ],
    
    "Home Improvement Retail": [
        "HD",    # Home Depot
        "LOW",   # Lowe's Companies
        "FND",   # Floor & Decor
        "TSCO",  # Tractor Supply
    ],
    
    "Automotive Retail": [
        "AZO",   # AutoZone
        "ORLY",  # O'Reilly Automotive
        "GPC",   # Genuine Parts
        "AAP",   # Advance Auto Parts
        "KMX",   # CarMax
        "AN",    # AutoNation
        "LAD",   # Lithia Motors
        "CVNA",  # Carvana
    ],
    
    "Other Specialty Retail": [
        "ULTA",  # Ulta Beauty
        "BBY",   # Best Buy
        "DKS",   # Dick's Sporting Goods
        "FIVE",  # Five Below
        "OLLI",  # Ollie's Bargain Outlet
        # WSM removed - primary classification is Home Furnishings
        "RH",    # RH (Restoration Hardware)
    ],
    
    "Distributors": [
        # GPC removed - primary classification is Automotive Retail
        # POOL removed - primary classification is Leisure Products
        "LKQ",   # LKQ Corporation
        # SITE removed - primary classification is Trading Companies & Distributors
        # FAST removed - primary classification is Trading Companies & Distributors
        "WESCO", # WESCO International
        "DNOW",  # DNOW Inc
    ],
    
    # Consumer Staples Sub-Industries
    "Packaged Foods & Meats": [
        "GIS",   # General Mills
        "K",     # Kellanova
        "CAG",   # Conagra Brands
        "SJM",   # J.M. Smucker
        "CPB",   # Campbell Soup
        "HRL",   # Hormel Foods
        "TSN",   # Tyson Foods
        "KHC",   # Kraft Heinz
        "HSY",   # Hershey Company
        "MKC",   # McCormick & Company
        "MDLZ",  # Mondelez International
    ],
    
    "Soft Drinks & Non-alcoholic Beverages": [
        "KO",    # Coca-Cola Company
        "PEP",   # PepsiCo Inc
        "MNST",  # Monster Beverage
        "KDP",   # Keurig Dr Pepper
        "CELH",  # Celsius Holdings
    ],
    
    "Distillers & Vintners": [
        "STZ",   # Constellation Brands
        "BF.B",  # Brown-Forman
        "DEO",   # Diageo plc
        "SAM",   # Boston Beer Company
        "TAP",   # Molson Coors Beverage
        "BUD",   # Anheuser-Busch InBev
    ],
    
    "Agricultural Products & Services": [
        "ADM",   # Archer-Daniels-Midland
        "BG",    # Bunge Global
        "INGR",  # Ingredion
        "DAR",   # Darling Ingredients
        "CALM",  # Cal-Maine Foods
    ],
    
    "Household Products": [
        "PG",    # Procter & Gamble
        "CL",    # Colgate-Palmolive
        "CHD",   # Church & Dwight
        "CLX",   # Clorox Company
        "KMB",   # Kimberly-Clark
        "SPB",   # Spectrum Brands
        "ENR",   # Energizer Holdings
    ],
    
    "Personal Care Products": [
        "EL",    # Estee Lauder
        "COTY",  # Coty Inc
        "ELF",   # e.l.f. Beauty
        "ULTA",  # Ulta Beauty
        "OLPX",  # Olaplex Holdings
    ],
    
    "Tobacco": [
        "PM",    # Philip Morris International
        "MO",    # Altria Group
        "BTI",   # British American Tobacco
        "TPB",   # Turning Point Brands
    ],
    
    "Consumer Staples Merchandise Retail": [
        "WMT",   # Walmart
        "COST",  # Costco Wholesale
        "TGT",   # Target Corporation
        "DG",    # Dollar General
        "DLTR",  # Dollar Tree
        "BJ",    # BJ's Wholesale Club
    ],
    
    "Drug Retail": [
        "WBA",   # Walgreens Boots Alliance
        "CVS",   # CVS Health
        "RAD",   # Rite Aid
    ],
    
    "Food Retail": [
        "KR",    # Kroger Company
        "ACI",   # Albertsons Companies
        "SFM",   # Sprouts Farmers Market
        "GO",    # Grocery Outlet
    ],
    
    "Food Distributors": [
        "SYY",   # Sysco Corporation
        "USFD",  # US Foods Holding
        "PFGC",  # Performance Food Group
        "UNFI",  # United Natural Foods
        "SPTN",  # SpartanNash
    ],
    
    # Health Care Sub-Industries  
    "Biotechnology": [
        "ABBV",  # AbbVie Inc
        "AMGN",  # Amgen Inc
        "GILD",  # Gilead Sciences
        "VRTX",  # Vertex Pharmaceuticals
        "REGN",  # Regeneron Pharmaceuticals
        "BIIB",  # Biogen Inc
        "MRNA",  # Moderna Inc
        "ALNY",  # Alnylam Pharmaceuticals
        "SGEN",  # Seagen Inc
        "INCY",  # Incyte Corporation
        "BMRN",  # BioMarin Pharmaceutical
    ],
    
    "Pharmaceuticals": [
        "JNJ",   # Johnson & Johnson
        "PFE",   # Pfizer Inc
        "LLY",   # Eli Lilly
        "MRK",   # Merck & Co
        "BMY",   # Bristol-Myers Squibb
        "ZTS",   # Zoetis Inc
        "VTRS",  # Viatris Inc
        "TEVA",  # Teva Pharmaceutical
        "CTLT",  # Catalent Inc
    ],
    
    "Health Care Equipment": [
        "ABT",   # Abbott Laboratories
        "MDT",   # Medtronic
        "SYK",   # Stryker Corporation
        "BSX",   # Boston Scientific
        "ISRG",  # Intuitive Surgical
        "EW",    # Edwards Lifesciences
        "ZBH",   # Zimmer Biomet
        "DXCM",  # Dexcom Inc
        "ALGN",  # Align Technology
        "RMD",   # ResMed Inc
        "HOLX",  # Hologic Inc
        "TFX",   # Teleflex
        "PODD",  # Insulet Corporation
    ],
    
    "Health Care Supplies": [
        "COO",   # Cooper Companies
        "WST",   # West Pharmaceutical
        "BIO",   # Bio-Rad Laboratories
        "HSIC",  # Henry Schein
    ],
    
    "Health Care Distributors": [
        "MCK",   # McKesson Corporation
        "CAH",   # Cardinal Health
        "COR",   # Cencora Inc
        "HSIC",  # Henry Schein
    ],
    
    "Health Care Services": [
        "CVS",   # CVS Health
        "CI",    # The Cigna Group
        "DGX",   # Quest Diagnostics
        "LH",    # Labcorp Holdings
        "DVA",   # DaVita Inc
        "GEHC",  # GE HealthCare
    ],
    
    "Health Care Facilities": [
        "HCA",   # HCA Healthcare
        "UHS",   # Universal Health Services
        "THC",   # Tenet Healthcare
        "ACHC",  # Acadia Healthcare
        "SEM",   # Select Medical Holdings
    ],
    
    "Managed Health Care": [
        "UNH",   # UnitedHealth Group
        "ELV",   # Elevance Health
        "HUM",   # Humana Inc
        "CNC",   # Centene Corporation
        "MOH",   # Molina Healthcare
        "CI",    # The Cigna Group
    ],
    
    "Life Sciences Tools & Services": [
        "TMO",   # Thermo Fisher Scientific
        "DHR",   # Danaher Corporation
        "A",     # Agilent Technologies
        "IQV",   # IQVIA Holdings
        "MTD",   # Mettler-Toledo
        "WAT",   # Waters Corporation
        "CRL",   # Charles River Laboratories
        "PKI",   # Revvity Inc
        "TECH",  # Bio-Techne
        "ILMN",  # Illumina Inc
    ],
    
    "Health Care Technology": [
        "VEEV",  # Veeva Systems
        "HCAT",  # Health Catalyst
        "DOCS",  # Doximity Inc
        "TDOC",  # Teladoc Health
        "AMWL",  # Amwell
        "GDRX",  # GoodRx Holdings
    ],
    
    # Financials Sub-Industries
    "Diversified Banks": [
        "JPM",   # JPMorgan Chase
        "BAC",   # Bank of America
        "WFC",   # Wells Fargo
        "C",     # Citigroup
        "USB",   # U.S. Bancorp
        "PNC",   # PNC Financial
        "TFC",   # Truist Financial
        "MTB",   # M&T Bank
    ],
    
    "Regional Banks": [
        "FITB",  # Fifth Third Bancorp
        "RF",    # Regions Financial
        "HBAN",  # Huntington Bancshares
        "CFG",   # Citizens Financial
        "KEY",   # KeyCorp
        "CMA",   # Comerica
        "ZION",  # Zions Bancorporation
        "FHN",   # First Horizon
        "EWBC",  # East West Bancorp
        "WAL",   # Western Alliance
        "FCNCA", # First Citizens BancShares
    ],
    
    "Investment Banking & Brokerage": [
        "GS",    # Goldman Sachs
        "MS",    # Morgan Stanley
        "SCHW",  # Charles Schwab
        "RJF",   # Raymond James
        "IBKR",  # Interactive Brokers
        "JEF",   # Jefferies Financial
        "LPL",   # LPL Financial
        "LPLA",  # LPL Financial Holdings
    ],
    
    "Asset Management & Custody Banks": [
        "BLK",   # BlackRock
        "TROW",  # T. Rowe Price
        "BEN",   # Franklin Resources
        "IVZ",   # Invesco Ltd
        "BK",    # Bank of New York Mellon
        "STT",   # State Street
        "NTRS",  # Northern Trust
        "SEIC",  # SEI Investments
        "AMG",   # Affiliated Managers
    ],
    
    "Financial Exchanges & Data": [
        "CME",   # CME Group
        "ICE",   # Intercontinental Exchange
        "NDAQ",  # Nasdaq Inc
        "CBOE",  # Cboe Global Markets
        "SPGI",  # S&P Global
        "MSCI",  # MSCI Inc
        "MCO",   # Moody's Corporation
        "MKTX",  # MarketAxess
        "FDS",   # FactSet Research
    ],
    
    "Consumer Finance": [
        "COF",   # Capital One
        "AXP",   # American Express
        "DFS",   # Discover Financial
        "SYF",   # Synchrony Financial
        "ALLY",  # Ally Financial
        "OMF",   # OneMain Holdings
        "SLM",   # SLM Corporation
    ],
    
    "Transaction & Payment Processing Services": [
        "V",     # Visa Inc
        "MA",    # Mastercard
        "PYPL",  # PayPal Holdings
        "FIS",   # Fidelity National
        "FISV",  # Fiserv Inc
        "GPN",   # Global Payments
        "SQ",    # Block Inc
        "AFRM",  # Affirm Holdings
    ],
    
    "Property & Casualty Insurance": [
        "PGR",   # Progressive Corporation
        "ALL",   # Allstate Corporation
        "TRV",   # Travelers Companies
        "CB",    # Chubb Limited
        "AIG",   # American International Group
        "WRB",   # W. R. Berkley
        "CNA",   # CNA Financial
        "CINF",  # Cincinnati Financial
    ],
    
    "Life & Health Insurance": [
        "AFL",   # Aflac
        "MET",   # MetLife
        "PRU",   # Prudential Financial
        "LNC",   # Lincoln National
        "PFG",   # Principal Financial
        "GL",    # Globe Life
        "VOYA",  # Voya Financial
    ],
    
    "Insurance Brokers": [
        "MMC",   # Marsh & McLennan
        "AON",   # Aon plc
        "WTW",   # Willis Towers Watson
        "AJG",   # Arthur J. Gallagher
        "BRO",   # Brown & Brown
        "RYAN",  # Ryan Specialty
    ],
    
    "Reinsurance": [
        "RNR",   # RenaissanceRe Holdings
        "ACGL",  # Arch Capital Group
        "EG",    # Everest Group
        "RE",    # Everest Re Group
    ],
    
    # Information Technology Sub-Industries
    "Application Software": [
        "MSFT",  # Microsoft
        "CRM",   # Salesforce
        "ADBE",  # Adobe Inc
        "INTU",  # Intuit Inc
        "NOW",   # ServiceNow
        "WDAY",  # Workday
        "TEAM",  # Atlassian
        "HUBS",  # HubSpot
        "DDOG",  # Datadog
        "ZS",    # Zscaler
        "CRWD",  # CrowdStrike
        "SNOW",  # Snowflake
        "PLTR",  # Palantir Technologies
        "MDB",   # MongoDB
    ],
    
    "Systems Software": [
        "ORCL",  # Oracle Corporation
        "PANW",  # Palo Alto Networks
        "FTNT",  # Fortinet
        "GEN",   # Gen Digital
        "VMW",   # VMware
        "KEYS",  # Keysight Technologies
        "ANSS",  # ANSYS Inc
        "SNPS",  # Synopsys
        "CDNS",  # Cadence Design Systems
    ],
    
    "IT Consulting & Other Services": [
        "ACN",   # Accenture
        "IBM",   # IBM Corporation
        "CTSH",  # Cognizant Technology
        "IT",    # Gartner Inc
        "EPAM",  # EPAM Systems
        "GLOB",  # Globant
        "GDYN",  # Grid Dynamics
        "DXC",   # DXC Technology
    ],
    
    "Internet Services & Infrastructure": [
        "GOOGL", # Alphabet Inc
        "META",  # Meta Platforms
        "AKAM",  # Akamai Technologies
        "NET",   # Cloudflare
        "FSLY",  # Fastly
        "CDN",   # CDN Technologies
        "FFIV",  # F5 Inc
    ],
    
    "Data Processing & Outsourced Services": [
        "V",     # Visa Inc
        "MA",    # Mastercard
        "PYPL",  # PayPal Holdings
        "ADP",   # Automatic Data Processing
        "PAYX",  # Paychex
        "FIS",   # Fidelity National
        "FISV",  # Fiserv
        "GPN",   # Global Payments
        "JKHY",  # Jack Henry & Associates
        "BR",    # Broadridge Financial
    ],
    
    "Communications Equipment": [
        "CSCO",  # Cisco Systems
        "MSI",   # Motorola Solutions
        "JNPR",  # Juniper Networks
        "HPE",   # Hewlett Packard Enterprise
        "ANET",  # Arista Networks
        "CIEN",  # Ciena Corporation
        "UI",    # Ubiquiti Inc
    ],
    
    "Technology Hardware, Storage & Peripherals": [
        "AAPL",  # Apple Inc
        "DELL",  # Dell Technologies
        "HPQ",   # HP Inc
        "STX",   # Seagate Technology
        "WDC",   # Western Digital
        "NTAP",  # NetApp
        "PSTG",  # Pure Storage
        "LOGI",  # Logitech International
        "ZBRA",  # Zebra Technologies
    ],
    
    "Electronic Equipment & Instruments": [
        "KEYS",  # Keysight Technologies
        "TDY",   # Teledyne Technologies
        "FTV",   # Fortive Corporation
        "GRMN",  # Garmin Ltd
        "ZBRA",  # Zebra Technologies
        "TER",   # Teradyne
        "COHR",  # Coherent Corp
    ],
    
    "Electronic Components": [
        "APH",   # Amphenol Corporation
        "TEL",   # TE Connectivity
        "GLW",   # Corning Incorporated
        "FLEX",  # Flex Ltd
        "JBL",   # Jabil Inc
        "CLS",   # Celestica Inc
    ],
    
    "Electronic Manufacturing Services": [
        "FLEX",  # Flex Ltd
        "JBL",   # Jabil Inc
        "PLXS",  # Plexus Corp
        "SANM",  # Sanmina Corporation
        "BHE",   # Benchmark Electronics
    ],
    
    "Semiconductors": [
        "NVDA",  # NVIDIA Corporation
        "AMD",   # Advanced Micro Devices
        "AVGO",  # Broadcom Inc
        "INTC",  # Intel Corporation
        "QCOM",  # Qualcomm
        "TXN",   # Texas Instruments
        "ADI",   # Analog Devices
        "MU",    # Micron Technology
        "NXPI",  # NXP Semiconductors
        "MCHP",  # Microchip Technology
        "MRVL",  # Marvell Technology
        "ON",    # ON Semiconductor
        "SWKS",  # Skyworks Solutions
        "QRVO",  # Qorvo
        "MPWR",  # Monolithic Power
    ],
    
    "Semiconductor Materials & Equipment": [
        "AMAT",  # Applied Materials
        "LRCX",  # Lam Research
        "KLAC",  # KLA Corporation
        "ASML",  # ASML Holding
        "TER",   # Teradyne
        "ENTG",  # Entegris
        "MKSI",  # MKS Instruments
        "ONTO",  # Onto Innovation
        "UCTT",  # Ultra Clean Holdings
    ],
    
    # Communication Services Sub-Industries
    "Interactive Media & Services": [
        "GOOGL", # Alphabet Inc
        "META",  # Meta Platforms
        "SNAP",  # Snap Inc
        "PINS",  # Pinterest
        "MTCH",  # Match Group
        "IAC",   # IAC Inc
        "ZG",    # Zillow Group
        "YELP",  # Yelp Inc
        "TTD",   # The Trade Desk
    ],
    
    "Movies & Entertainment": [
        "DIS",   # Walt Disney
        "NFLX",  # Netflix
        "WBD",   # Warner Bros. Discovery
        "PARA",  # Paramount Global
        "LYV",   # Live Nation Entertainment
        "IMAX",  # IMAX Corporation
        "WMG",   # Warner Music Group
    ],
    
    "Interactive Home Entertainment": [
        "EA",    # Electronic Arts
        "TTWO",  # Take-Two Interactive
        "ATVI",  # Activision Blizzard
        "RBLX",  # Roblox Corporation
        "U",     # Unity Software
        "PLTK",  # Playtika Holding
    ],
    
    "Broadcasting": [
        "FOX",   # Fox Corporation
        "FOXA",  # Fox Corporation Class A
        "NWS",   # News Corp
        "NWSA",  # News Corp Class A
        "PARA",  # Paramount Global
        "TGNA",  # TEGNA Inc
        "NXST",  # Nexstar Media
        "GTN",   # Gray Television
    ],
    
    "Cable & Satellite": [
        "CMCSA", # Comcast Corporation
        "CHTR",  # Charter Communications
        "CABO",  # Cable One
        "SIRI",  # Sirius XM
        "DISH",  # DISH Network
        "LBRDK", # Liberty Broadband
    ],
    
    "Publishing": [
        "NWSA",  # News Corp
        "NYT",   # New York Times
        "GCI",   # Gannett Co
        "SCHL",  # Scholastic
    ],
    
    "Advertising": [
        "OMC",   # Omnicom Group
        "IPG",   # Interpublic Group
        "MGNI",  # Magnite Inc
        "PUBM",  # PubMatic
        "TTD",   # The Trade Desk
        "TBLA",  # Taboola.com
        "DSP",   # Viant Technology
        "IAS",   # Integral Ad Science
    ],
    
    "Integrated Telecommunication Services": [
        "T",     # AT&T Inc
        "VZ",    # Verizon Communications
        "LUMN",  # Lumen Technologies
        "FTR",   # Frontier Communications
    ],
    
    "Wireless Telecommunication Services": [
        "TMUS",  # T-Mobile US
        "USM",   # United States Cellular
        "SHEN",  # Shenandoah Telecommunications
    ],
    
    "Alternative Carriers": [
        "LUMN",  # Lumen Technologies
        "CCOI",  # Cogent Communications
        "BAND",  # Bandwidth Inc
        "CIEN",  # Ciena Corporation
    ],
    
    # Utilities Sub-Industries
    "Electric Utilities": [
        "NEE",   # NextEra Energy
        "DUK",   # Duke Energy
        "SO",    # Southern Company
        "AEP",   # American Electric Power
        "EXC",   # Exelon Corporation
        "SRE",   # Sempra
        "XEL",   # Xcel Energy
        "ED",    # Consolidated Edison
        "EIX",   # Edison International
        "WEC",   # WEC Energy Group
        "ES",    # Eversource Energy
        "DTE",   # DTE Energy
        "PCG",   # PG&E Corporation
        "FE",    # FirstEnergy
        "PPL",   # PPL Corporation
        "PEG",   # Public Service Enterprise
    ],
    
    "Gas Utilities": [
        "ATO",   # Atmos Energy
        "NJR",   # New Jersey Resources
        "SWX",   # Southwest Gas
        "UGI",   # UGI Corporation
        "NFG",   # National Fuel Gas
        "NI",    # NiSource Inc
        "OGS",   # ONE Gas
        "SR",    # Spire Inc
    ],
    
    "Multi-Utilities": [
        "D",     # Dominion Energy
        "CNP",   # CenterPoint Energy
        "AEE",   # Ameren Corporation
        "CMS",   # CMS Energy
        "NI",    # NiSource
        "LNT",   # Alliant Energy
        "EVRG",  # Evergy Inc
        "PNW",   # Pinnacle West Capital
    ],
    
    "Water Utilities": [
        "AWK",   # American Water Works
        "WTRG",  # Essential Utilities
        "CWT",   # California Water Service
        "SJW",   # SJW Group
        "AWR",   # American States Water
        "MSEX",  # Middlesex Water
        "YORW",  # York Water Company
    ],
    
    "Independent Power Producers & Energy Traders": [
        "AES",   # AES Corporation
        "NRG",   # NRG Energy
        "VST",   # Vistra Corp
        "CWEN",  # Clearway Energy
        "TAL",   # TAL Education Group
    ],
    
    "Renewable Electricity": [
        "NEP",   # NextEra Energy Partners
        "BEP",   # Brookfield Renewable
        "ENPH",  # Enphase Energy
        "FSLR",  # First Solar
        "SEDG",  # SolarEdge Technologies
        "RUN",   # Sunrun Inc
        "NOVA",  # Sunnova Energy
        "ARRY",  # Array Technologies
    ],
    
    # Real Estate Sub-Industries
    "Industrial REITs": [
        "PLD",   # Prologis
        "DRE",   # Duke Realty
        "REXR",  # Rexford Industrial
        "STAG",  # STAG Industrial
        "FR",    # First Industrial Realty
        "EGP",   # EastGroup Properties
        "TRNO",  # Terreno Realty
    ],
    
    "Office REITs": [
        "BXP",   # Boston Properties
        "ARE",   # Alexandria Real Estate
        "KRC",   # Kilroy Realty
        "VNO",   # Vornado Realty
        "SLG",   # SL Green Realty
        "HIW",   # Highwoods Properties
        "DEI",   # Douglas Emmett
        "CUZ",   # Cousins Properties
    ],
    
    "Retail REITs": [
        "SPG",   # Simon Property Group
        "REG",   # Regency Centers
        "FRT",   # Federal Realty
        "KIM",   # Kimco Realty
        "O",     # Realty Income
        "NNN",   # NNN REIT
        "BRX",   # Brixmor Property
        "SITC",  # SITE Centers
    ],
    
    "Multi-Family Residential REITs": [
        "EQR",   # Equity Residential
        "AVB",   # AvalonBay Communities
        "ESS",   # Essex Property Trust
        "UDR",   # UDR Inc
        "MAA",   # Mid-America Apartment
        "CPT",   # Camden Property Trust
        "INVH",  # Invitation Homes
        "AMH",   # American Homes 4 Rent
    ],
    
    "Single-Family Residential REITs": [
        "INVH",  # Invitation Homes
        "AMH",   # American Homes 4 Rent
        "RESI",  # Front Yard Residential
    ],
    
    "Health Care REITs": [
        "WELL",  # Welltower
        "VTR",   # Ventas
        "PEAK",  # Healthpeak Properties
        "OHI",   # Omega Healthcare
        "HR",    # Healthcare Realty
        "DOC",   # Physicians Realty Trust
        "LTC",   # LTC Properties
        "NHI",   # National Health Investors
        "SBRA",  # Sabra Health Care
        "MPW",   # Medical Properties Trust
    ],
    
    "Hotel & Resort REITs": [
        "HST",   # Host Hotels & Resorts
        "VICI",  # VICI Properties
        "PK",    # Park Hotels & Resorts
        "RHP",   # Ryman Hospitality
        "SHO",   # Sunstone Hotel
        "PEB",   # Pebblebrook Hotel
        "XHR",   # Xenia Hotels
        "DRH",   # DiamondRock Hospitality
    ],
    
    "Diversified REITs": [
        "VNQ",   # Vanguard Real Estate ETF
        "WPC",   # W. P. Carey
        "STOR",  # STORE Capital
        "IRM",   # Iron Mountain
        "GLPI",  # Gaming and Leisure Properties
    ],
    
    "Infrastructure REITs": [
        "AMT",   # American Tower
        "CCI",   # Crown Castle
        "SBAC",  # SBA Communications
        "UNIT",  # Uniti Group
    ],
    
    "Real Estate Services": [
        "CBRE",  # CBRE Group
        "JLL",   # Jones Lang LaSalle
        "CWK",   # Cushman & Wakefield
        "NMRK",  # Newmark Group
        "EXPI",  # eXp World Holdings
        "RDFN",  # Redfin
        "ZG",    # Zillow Group
        "OPEN",  # Opendoor Technologies
        "COMP",  # Compass Inc
    ],
    
    "Real Estate Operating Companies": [
        "CSGP",  # CoStar Group
        "HHH",   # Howard Hughes
        "JOE",   # St. Joe Company
        "FOR",   # Forestar Group
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

