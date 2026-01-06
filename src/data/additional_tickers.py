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
    "USWS", "KLXE", "PTR", "RRC", "TELL", "NEXT", "ZN", "LONE", "VTOL",
    # Oil & Gas E&P
    "APA", "DVN", "FANG", "EOG", "PXD", "COP", "OXY", "MRO", "CLR", "SU", "CVE",
    "PR", "MTDR", "CTRA", "CHRD", "OVV", "MGY", "SM", "CRGY", "SBOW", "CNX", 
    "AR", "SWN", "EQT", "VTLE", "REPX", "ESTE", "REI", "PARR", "SD", "AXAS",
    "SNDE", "EPSN", "WTI", "NGAS", "WFRD", "BRY", "SGML", "CIVI", "BKV", "VNOM",
    "CPE", "GPOR", "GRNT", "HPK", "CDEV", "WLL", "NOG", "CRZO", "KOS", "TDW",
    # Oil & Gas Refining
    "VLO", "PSX", "MPC", "DK", "PBF", "CVI", "DINO", "CLMT", "CAPL", "HEP",
    "NS", "HFC", "INT", "CVRR", "NTI", "REGI", "PACD", "GPRK", "AMCF",
    # Oil & Gas Midstream/Storage
    "KMI", "WMB", "OKE", "ET", "MPLX", "EPD", "PAA", "WES", "TRGP", "AM",
    "DCP", "USAC", "SMLP", "NGL", "CEQP", "ENLC", "ETRN", "KNTK", "DTM",
    "GLP", "PAGP", "HEP", "BSM", "SMLP", "CLNE", "CPLP", "NBLX", "SPH",
    # Oil Services & Equipment
    "SLB", "HAL", "BKR", "NOV", "FTI", "WHD", "WTTR", "OII", "LBRT", "NEX",
    "RES", "HLX", "CLB", "XPRO", "BOOM", "GEL", "TTI", "PUMP", "DWSN",
    "AROC", "SOI", "PTEN", "TDW", "GIFI", "MTRX", "DRQ", "MPLN", "OIS",
]

SECTOR_15_MATERIALS = [
    # Chemicals - Diversified & Specialty
    "DOW", "LYB", "CE", "EMN", "HUN", "WLK", "OLN", "TROX", "KRO", "MEOH",
    "ASIX", "IOSP", "KWR", "NGVT", "FUL", "RPM", "GRA", "BCPC", "HWKN",
    "APD", "ECL", "SHW", "PPG", "ALB", "IFF", "AVNT", "AXTA", "ASH", "GCP",
    "CBT", "CC", "FOE", "LTH", "MTX", "UFPI", "LTHM", "UNVR", "OLIN", "KALM",
    "NVZMY", "HXL", "NEU", "IOSP", "GPRE", "RYAM", "ZEUS", "GLATF", "AREC",
    # Agricultural Chemicals
    "NTR", "CF", "MOS", "FMC", "SMG", "CTVA", "ICL", "IPI", "GPRE", "ADM",
    "AGFY", "AVAV", "GRWG", "APPH", "AVO", "AGRO", "SEED", "LMNR", "SMID",
    # Construction Materials
    "VMC", "MLM", "EXP", "USLM", "SUM", "ROCK", "ITE", "MDU", "CNHI", "CRH",
    "CMCO", "ITE", "KNF", "TGLS", "APOG", "ASTE", "PGTI",
    # Metals & Mining
    "NEM", "FCX", "GOLD", "NUE", "STLD", "CLF", "X", "AA", "ATI", "CMC",
    "RS", "CRS", "WOR", "HAYN", "CENX", "KALU", "ARCH", "HCC", "BTU", 
    "CEIX", "ARLP", "AMR", "HL", "PAAS", "AG", "EXK", "CDE", "FSM", "RGLD",
    "WPM", "FNV", "SBSW", "OR", "SAND", "SSRM", "BTG", "IAG", "HMY", "DRD",
    "NGD", "GATO", "GPL", "SILV", "MAG", "SVM", "MUX", "EGO", "USAS",
    # Steel
    "TX", "TMST", "SCHN", "RYI", "SXC", "UFAB", "WS", "WIRE", "NMM", "PRLB",
    "MATV", "NSC", "CMC", "STLD", "MT", "PKX", "SID", "VALE", "RIO", "BHP",
    # Paper & Forest Products
    "IP", "WRK", "PKG", "SON", "SEE", "BLL", "CCK", "ATR", "GEF", "BERY",
    "UFPT", "PACK", "KRT", "CLW", "LSB", "SWM", "TG", "GLT", "RYN", "WY",
    "PCH", "PPC", "SLVM", "GPK", "TRS", "TREC", "CKH", "UFS",
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
    "OC", "IBP", "CSWI", "AAON", "NX", "UFPI", "SMG", "AMWD", "CABO", "CNR",
    # Construction & Engineering
    "ACM", "MTZ", "PWR", "DY", "EME", "FIX", "PRIM", "TPC", "MYRG", "STRL",
    "ORN", "CTO", "IESC", "GVA", "KBR", "FLR", "AGX", "NVEE", "TTEK", "WSC",
    "AAMC", "AGS", "BFAM", "BLD", "GLT", "ROAD", "PRIM", "CENX", "LPG",
    # Electrical Equipment
    "ETN", "ROK", "EMR", "AME", "RBC", "GNRC", "AZZ", "ATKR", "WCC", "HUBB",
    "POWL", "AYI", "EAF", "WIRE", "NVT", "VRT", "PLUG", "FLUX", "LTCH",
    "FCEL", "BLDP", "HYLN", "BLNK", "CHPT", "EVGO", "NKLA", "RIDE", "GOEV",
    # Industrial Conglomerates
    "MMM", "HON", "ITW", "ROP", "DHR", "IEP", "MGRC", "MDC", "GTES", "ESE",
    # Machinery
    "CAT", "DE", "PCAR", "CMI", "SWK", "TTC", "OSK", "AGCO", "CNHI", "ALG",
    "KMT", "MEC", "NPO", "CFX", "HAYW", "HLIO", "LNN", "MIDD", "MTW", "SXI",
    "TWI", "WTS", "BMI", "FLOW", "HI", "GTES", "AIT", "GTLS", "IDEX", "IEX",
    "ITT", "LECO", "MANT", "PNR", "RXO", "TKR", "WMS", "XYL", "CR", "PH",
    "IR", "FLS", "DOV", "GWW", "FAST", "WSO", "SITE", "FELE", "RBC", "GTLS",
    # Trading Companies & Distributors
    "GWW", "FAST", "WSO", "MSM", "SITE", "DXPE", "DNOW", "DXP", "HDSN", "PKOH",
    "SYX", "TITN", "WCC", "HDS", "CCMP", "POOL", "HWKN", "EVI", "MGRC", "RBC",
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
    "HA", "MESA", "RYAAY", "AZUL", "GOL", "CEA", "CPA", "ZNH", "LUV", "SNCY",
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
    "LCII", "REV", "CVII", "HYLN", "XL", "LEA", "BWA", "APTV", "VC", "DAN",
    # Auto Parts
    "APTV", "BWA", "LEA", "MGA", "ALV", "ADNT", "AXL", "GNTX", "VC", "DAN",
    "MOD", "PHIN", "SMP", "LCII", "THRM", "AEY", "DORM", "FOXF", "LKQ", "SRI",
    "STRT", "SUP", "TEN", "MTOR", "CDMO", "SHYF", "GTXMQ", "FRSX", "BSQR",
    # Auto Retail
    "AN", "ABG", "GPI", "PAG", "LAD", "SAH", "RUSHA", "KMX", "CVNA", "SFT",
    "CARS", "CARG", "VRM", "CZOO", "LOTZ", "DRVN", "HYRE", "SOS", "FRSH",
    # Home Improvement Retail
    "HD", "LOW", "FND", "LL", "SHC", "WSM", "RH", "ARHS", "ETH", "SNBR",
    "PRPL", "TPX", "LEG", "HVT", "FLXS", "PATK", "CSPR", "DBI", "LOVE",
    # Homebuilding
    "DHI", "LEN", "PHM", "NVR", "TOL", "KBH", "TMHC", "MDC", "MTH", "MHO",
    "TPH", "SKY", "CCS", "HOV", "BZH", "GRBK", "CVCO", "LGIH", "DFH", "LEGH",
    "UHG", "MERH", "NOAH", "STRW", "LOVE", "MSCI", "CBG", "JLL", "CWK", "RMR",
    # Household Appliances & Durables
    "WHR", "SEB", "HELE", "IRBT", "NPK", "HBB", "FLXS", "SNBR", "PRPL", "LCUT",
    "SKY", "LOVE", "LGIH", "IBP", "NOAH", "FIGS", "SN", "ALTO", "HEAR",
    # Leisure Products
    "HAS", "MAT", "POOL", "BC", "PTON", "NLS", "PRKS", "FNKO", "JAKK", "PLNT",
    "PLAY", "TRAK", "VSTO", "YETI", "FIZZ", "NILE", "CLVR", "RAVE", "PRPH",
    "GOLF", "ESGL", "FUN", "SIX", "SEAS", "PRKS", "SUM", "MTN", "SKI", "EPR",
    # Apparel & Luxury
    "NKE", "LULU", "TPR", "VFC", "PVH", "RL", "CPRI", "GIII", "GIL", "COLM",
    "UAA", "CROX", "DECK", "SKX", "SHOO", "WWW", "WEYS", "CATO", "HNST", "GES",
    "LEVI", "GOOS", "HBI", "SCVL", "CAL", "SMRT", "FIGS", "ONON", "HELE",
    "BOOT", "CURV", "DXLG", "CTRN", "EXPR", "AEO", "ANF", "BKE", "ZUMZ",
    # Home Furnishings
    "RH", "WSM", "ARHS", "ETH", "LOVE", "SNBR", "PRPL", "CSPR", "TPX", "LEG",
    "HVT", "FLXS", "PATK", "AMWD", "SNBR", "LCUT", "TILE", "FND", "LL", "SHC",
    # Casinos & Gaming
    "LVS", "WYNN", "MGM", "CZR", "DKNG", "PENN", "BYD", "MLCO", "RRR", "GDEN",
    "IGT", "SGMS", "GAN", "RSI", "BALY", "CHDN", "WBET", "GMBL", "SGHC", "EVRI",
    "AGS", "NUVB", "BETZ", "NGMS", "GIG", "PUCK", "LUCK", "MLCO", "WMS",
    # Hotels & Resorts
    "MAR", "HLT", "H", "IHG", "WH", "CHH", "VAC", "TNL", "PLYA", "MTN", "HGV",
    "BHR", "STAY", "CLDT", "HT", "RHP", "WYNDQ", "SVC", "APTS", "AHT", "DRH",
    "PK", "PEB", "RLJ", "SHO", "XHR", "INN", "SOHO", "HTGC", "ASHF", "HTLD",
    # Restaurants
    "MCD", "SBUX", "DPZ", "CMG", "YUM", "QSR", "WEN", "DNUT", "PZZA", "DRI",
    "TXRH", "BLMN", "EAT", "CAKE", "DIN", "JACK", "TACO", "WING", "SHAK", "BROS",
    "CAVA", "SG", "LOCO", "ARCO", "ARKR", "NDLS", "PBPB", "KRUS", "BJRI", "FAT",
    "RAVE", "RRGB", "RUTH", "BAGR", "KTRA", "RICK", "MSSR", "NATH", "CBRL",
    # Specialty Retail
    "AMZN", "TGT", "COST", "WMT", "DG", "DLTR", "FIVE", "OLLI", "BBY", "GME",
    "CHWY", "W", "ETSY", "EBAY", "WISH", "SHOP", "GRPN", "OPEN", "FIGS", "RENT",
    "BIRD", "TDUP", "REAL", "PRTS", "SSTK", "TCS", "ASO", "DKS", "HIBB", "SPWH",
    "PLCE", "BURL", "ROST", "TJX", "GPS", "EXPR", "ZUMZ", "BOOT", "BKE", "AAP",
    "AZO", "ORLY", "GPC", "MNRO", "PRTS", "DORM", "MPAA", "MOV", "FUL", "CTRN",
    "CURV", "DXLG", "SMRT", "SIG", "KAR", "CPRT", "SBH", "ULTA", "EYE", "WOOF",
    # Education Services
    "CHGG", "COUR", "DUOL", "LRN", "ATGE", "LOPE", "PRDO", "STRA", "TWOU",
    "UDMY", "BFAM", "LAUR", "LINC", "HLG", "AFYA", "GHC", "MEDP", "UTI", "APEI",
]

SECTOR_30_CONSUMER_STAPLES = [
    # Food & Beverage
    "PEP", "KO", "MDLZ", "KHC", "GIS", "K", "CAG", "CPB", "SJM", "HRL",
    "TSN", "PPC", "JJSF", "LANC", "INGR", "DAR", "CALM", "HAIN", "SMPL", "THS",
    "BRBR", "SENEA", "UNFI", "USFD", "PFGC", "DOLE", "CELH", "FIZZ", "MNST",
    "ZVIA", "FRPT", "FREE", "FARM", "LNDC", "SFD", "CVGW", "STKL", "BERY",
    "MGPI", "PSMT", "NGVC", "CSWI", "SEB", "BRCC", "VFF", "SFIX", "BWMN",
    # Beverages
    "BUD", "TAP", "SAM", "STZ", "DEO", "ABEV", "CCU", "PRMW", "WVVI", "COCO",
    "NAPA", "FIZZ", "NBEV", "ZVIA", "WEYS", "COKE", "CCEP", "MGPI", "REED",
    # Tobacco
    "PM", "MO", "BTI", "TPB", "VGR", "UVV", "CRLBF", "GRNH", "CURLF", "AYRWF",
    "TCNNF", "GTBIF", "CCHWF", "TRSSF", "CRLBF", "JUSHF", "MSOS", "MJ", "POTX",
    # Household Products
    "PG", "CL", "CHD", "CLX", "KMB", "SPB", "EPC", "ELF", "IPAR", "HELE",
    "CENT", "NUS", "USNA", "ENR", "REV", "COTY", "SKIN", "OLPX", "OLAPLEX",
    "GROV", "HLF", "NU", "HIMS", "HYFM", "NATR", "CMBM", "NWL", "SBH", "REVG",
    # Personal Products
    "EL", "COTY", "SKIN", "HIMS", "PRGO", "NWL", "HLF", "GROV", "OLPX", "HNST",
    "IPAR", "NATR", "MAMA", "OMI", "INGR", "TREE", "BNED", "SBH", "REV",
    # Retail - Grocery
    "KR", "ACI", "SFM", "IMKTA", "BGS", "GO", "NDLS", "CASY", "VLGEA", "WMK",
    "NGVC", "CHEF", "PFGC", "CENT", "UNFI", "SPTN", "FARM", "OLLI", "FWRG",
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
    "XNCR", "APLS", "RXDX", "TNGX", "ETNB", "SWTX", "RETA", "AVXL", "LXRX",
    "CGEM", "VRDN", "DAWN", "ACAD", "ANNX", "GERN", "REPL", "XERS", "ALLK",
    "BOLT", "MLYS", "TARS", "ARDX", "PRTX", "AKRO", "CRMD", "KRON", "BCAB",
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
    "DVA", "ADUS", "ENSG", "PNTG", "SEM", "NHC", "CCRN", "USPH", "SGRY",
    "OPCH", "ALHC", "HCSG", "BKD", "AFMD", "EVH", "GH", "ONEM", "PRVA",
    "EHAB", "DOCS", "PHR", "TALK", "AMWL", "TDOC", "HIMS", "HURN", "PGNY",
    "OSCR", "LFST", "CLVR", "SHCR", "ACCD", "SOPH", "HLAH", "PHAR", "CMAX",
    # Life Sciences Tools
    "TMO", "DHR", "A", "BIO", "ILMN", "MTD", "WAT", "PKI", "TECH", "CRL",
    "ICLR", "MEDP", "RVTY", "CDNA", "EXAS", "VCYT", "NVTA", "ME", "VEEV",
    "MYGN", "NTRA", "PACB", "TXG", "FLGT", "TWST", "RGEN", "NEO", "MXCT",
    "CSTL", "NGMS", "PSNL", "RDNT", "SDGR", "SEER", "CHRS", "HCAT", "MTSI",
]

SECTOR_40_FINANCIALS = [
    # Banks - Diversified & Regional
    "JPM", "BAC", "WFC", "C", "GS", "MS", "SCHW", "BK", "STT", "PNC",
    "TFC", "USB", "COF", "AXP", "DFS", "SYF", "ALLY", "HBAN", "KEY", "RF",
    "CFG", "FITB", "MTB", "ZION", "CMA", "SIVB", "PACW", "WAL", "FHN",
    "BOKF", "SNV", "VLY", "WBS", "EWBC", "GBCI", "IBKR", "ONB", "PNFP",
    "SBCF", "SEIC", "TOWN", "UBSI", "WAFD", "WSFS", "ASB", "BHF", "FBK",
    "FFIN", "FULT", "IBOC", "NBTB", "SBNY", "TBBK", "TCBI", "UCBI", "COLB",
    "CATY", "CVBF", "DCOM", "EFSC", "FMBI", "FRME", "GABC", "HWC", "INDB",
    "IBTX", "OFG", "PRK", "RNST", "SBSI", "SFBS", "SIVB", "STBA", "NYCB",
    "BPOP", "FBP", "BANC", "CPF", "LBAI", "MBFI", "ORRF", "PVBC", "SASR",
    "SMBC", "SYBT", "THFF", "UVSP", "BHLB", "BOCH", "CFFI", "CHCO", "CHMG",
    "CNOB", "EQBK", "FBIZ", "FCBC", "FMBH", "HNVR", "HOMB", "HTBK", "HTLF",
    "IBCP", "LCNB", "MBWM", "MNSB", "MOFG", "NBHC", "NRIM", "OPBK", "OSBC",
    "PKBK", "PLBC", "RBCAA", "SFNC", "SRCE", "SSB", "TRMK", "WABC", "WSBC",
    # Asset Management & Investment Banking
    "BLK", "BX", "KKR", "APO", "ARES", "OWL", "CG", "TPG", "TROW", "IVZ",
    "BEN", "FHI", "VCTR", "PZN", "GHL", "PJT", "MC", "MKTX", "LPLA", "CBOE",
    "CME", "ICE", "NDAQ", "COIN", "HOOD", "IBKR", "SCHW", "ETFC", "SEIC",
    "VIRT", "EVR", "HLI", "JEF", "LPL", "RJF", "SF", "PIPR", "SNEX", "COWN",
    "OPCH", "SCU", "STEP", "TWST", "VCTR", "WETF", "WDR", "DHF", "DSL", "EXG",
    # Insurance
    "BRK.A", "BRK.B", "PGR", "ALL", "TRV", "CB", "AIG", "MET", "PRU", "AFL",
    "AJG", "MMC", "AON", "WTW", "BRO", "ERIE", "CNA", "Y", "RNR", "THG",
    "WRB", "AIZ", "CNO", "FAF", "FNF", "GL", "HIG", "KMPR", "L", "LNC",
    "ORI", "PFG", "PLMR", "RDN", "RGA", "SLF", "SIGI", "CINF", "KNSL",
    "MCY", "MGRC", "NMIH", "RYAN", "ROOT", "ACGL", "AFG", "AGO", "ANAT",
    "AXS", "BCRH", "GNW", "HMN", "JRVR", "KREF", "LMND", "LTPZ", "MHLD",
    "NMIH", "NWLI", "OSCR", "PLMR", "PRIM", "RILY", "RNR", "STC", "STFC",
    # Financial Services
    "V", "MA", "PYPL", "SQ", "FIS", "FISV", "GPN", "AFRM", "UPST", "SOFI",
    "HOOD", "LMND", "OPEN", "BILL", "PAYO", "MQ", "TOST", "NAVI", "SLM",
    "ESNT", "MTG", "RDFN", "UWMC", "RKT", "GHLD", "CURO", "ENVA", "TREE",
    "OMF", "OZK", "PFSI", "PRAA", "QFIN", "RELY", "WRLD", "CACC", "ELVT",
    "FCFS", "GSKY", "LPRO", "MGNI", "MGRC", "MKTX", "MOGO", "MSCI", "NAVI",
    "RDFN", "RPAY", "STNE", "VNT", "XP", "LSCC", "FRHC", "IMXI", "CNNE",
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
    "EVOP", "FIVN", "FRSH", "GENI", "GWRE", "INFA", "KNBE", "LSPD", "MCFE",
    "MGNI", "MNDY", "NEWR", "OPAD", "ORCL", "QLYS", "REKR", "S", "SCWX",
    "SMCI", "SNCR", "SPNS", "SQSP", "SVMK", "TASK", "TBIO", "UPST", "WK",
    "WOLF", "XMTR", "YEXT", "YOU", "ZI", "ZS", "ZUORA", "ATVI", "EA", "TTWO",
    # Software - Infrastructure
    "IBM", "VMW", "FTNT", "SNPS", "KEYS", "AKAM", "FFIV", "GEN", "QLYS",
    "TENB", "VRNS", "VRNT", "RDWR", "SCWX", "SNCR", "NLOK", "MIME", "LDOS",
    "CTXS", "CDNS", "ANSS", "SYNC", "NTNX", "PSTG", "NATI", "SLAB", "CDK",
    # Semiconductors
    "NVDA", "AMD", "INTC", "TXN", "AVGO", "QCOM", "MU", "ADI", "NXPI",
    "MCHP", "LRCX", "AMAT", "KLAC", "MRVL", "ON", "SWKS", "QRVO", "MPWR",
    "SLAB", "DIOD", "RMBS", "CRUS", "FORM", "HIMX", "IMOS", "LSCC", "MTSI",
    "POWI", "SIMO", "SMTC", "ENTG", "KLIC", "MKSI", "ONTO", "UCTT", "WOLF",
    "ACMR", "AMKR", "AOSL", "ASML", "COHU", "LEDS", "NVMI", "PLAB", "SMCI",
    "TSM", "UMC", "AEHR", "ALGM", "AMBA", "AXTI", "CCMP", "CEVA", "CRDO",
    "GFS", "GSIT", "HIMX", "ICHR", "LSCC", "MXIM", "OLED", "PDFS", "POWI",
    "RMBS", "SGH", "SIMO", "SITM", "SMCI", "SYNA", "TER", "TSEM", "UTSI",
    # IT Services
    "ACN", "CTSH", "FIS", "FISV", "IT", "WIT", "EPAM", "GLOB", "GDYN",
    "EXLS", "PEGA", "PRFT", "SSNC", "TTEC", "VNET", "WEX", "BR", "CACI",
    "CNXC", "CSGP", "DXC", "FAF", "FOUR", "G", "GIB", "JKHY", "KD", "LDOS",
    "LPSN", "MANT", "MAXN", "ORCL", "SAIC", "SSTI", "TASK", "TLRY", "UPWK",
    # Hardware
    "AAPL", "HPQ", "HPE", "DELL", "NTAP", "WDC", "STX", "PSTG", "LOGI",
    "CRSR", "DGII", "DSGX", "HEAR", "IMMR", "NTGR", "SMCI", "SSYS", "ZBRA",
    "LQDT", "VIAV", "GLW", "APH", "TEL", "CDW", "NSIT", "SNX", "ATEN",
    "COMM", "CLFD", "DGII", "INSG", "NTGR", "SILC", "SSYS", "TRMB", "VICR",
    # Communications Equipment
    "CSCO", "MSI", "JNPR", "UI", "CIEN", "LITE", "CALX", "COMM", "HLIT",
    "INFN", "IRDM", "VIAV", "CASA", "DZSI", "IDCC", "INSG", "NTGR", "VCNX",
]

SECTOR_50_COMMUNICATION_SERVICES = [
    # Interactive Media & Services
    "GOOGL", "META", "SNAP", "PINS", "MTCH", "BMBL", "IAC", "ZG", "YELP",
    "GRPN", "ANGI", "TTD", "MGNI", "PUBM", "CARG", "CARS", "EVER", "TREE",
    "QNST", "DHC", "SPOT", "SONO", "SSTK", "EDIT", "VNET", "WB", "LZ",
    # Entertainment
    "DIS", "NFLX", "CMCSA", "CHTR", "WBD", "AMC", "CNK", "IMAX", "ROKU",
    "SIRI", "SPOT", "TME", "WMG", "MSGS", "MSGE", "LYV", "CMCSA", "FOX",
    "FOXA", "NWS", "NWSA", "VIAC", "DISCB", "DISCK", "DISCA", "GTN", "SSP",
    "IHRT", "CTO", "EVC", "GCI", "GME", "ISIG", "KNSL", "LBTYB", "LBTYK",
    "LSXMA", "LSXMB", "LSXMK", "NRDY", "PARA", "SCHL", "TGNA", "TRIP",
    # Gaming
    "EA", "TTWO", "RBLX", "DKNG", "GOGO", "GLBE", "HUYA", "BILI", "DDL",
    "DOYU", "GRVY", "PLTK", "SKLZ", "SOHU", "GLBE", "AGFY", "PERI", "ZNGA",
    "SRAD", "TSQ", "FUBO", "MYPS", "NCTY", "SLGG", "ESPO", "HERO", "NERD",
    # Telecom
    "T", "VZ", "TMUS", "LUMN", "USM", "TDS", "SHEN", "GOGO", "LBRDA",
    "LBRDK", "SBAC", "CCI", "AMT", "EQIX", "DLR", "UNIT", "CCOI", "GDS",
    "CORD", "OOMA", "BAND", "LNTH", "CMTL", "LUMN", "CCOI", "CNSL", "IRDM",
    # Advertising & Media
    "OMC", "IPG", "DLX", "MGNI", "ZETA", "MGID", "CARG", "ADT", "QNST",
    "SCOR", "TTD", "PUBM", "DSP", "IAS", "NCMI", "NEXS", "QUAD", "STCN",
    "TBLA", "VERX", "MGNI", "ADV", "BIGC", "BKNG", "EXPE", "SABR", "TRIP",
]

SECTOR_55_UTILITIES = [
    # Electric Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "ED", "PCG",
    "EIX", "WEC", "ES", "DTE", "AEE", "ETR", "FE", "PPL", "CMS", "EVRG",
    "PNW", "AES", "LNT", "OGE", "NWE", "NRG", "POR", "IDA", "AVA", "EE",
    "BKH", "NWN", "OGS", "PNM", "SWX", "UTL", "AWA", "AQN", "AGR", "AEE",
    "AEG", "AMPS", "ATO", "BIPC", "BIP", "CWEN", "CNP", "CPK", "CWENA",
    "DUKB", "EMRAF", "ENPH", "FSLR", "GPJA", "GPRK", "HE", "HIFR", "MGEE",
    "NFG", "NI", "NJR", "NRG", "OGS", "OTTR", "PEGI", "PEG", "PNM", "SBS",
    # Gas Utilities
    "NJR", "NFG", "NI", "SR", "SWX", "UGI", "ONE", "CPK", "SJI", "NWN",
    "OGS", "RGCO", "SMLP", "SPH", "SR", "SWX", "UGI", "APU", "BIP", "BIPC",
    # Multi-Utilities & Water
    "AWK", "WTRG", "CWT", "SJW", "YORW", "MSEX", "AWR", "ARTNA", "CWCO",
    "GWRS", "PNR", "WTR", "AWR", "XYL", "RXN", "AQUA", "TTC", "BMI", "FELE",
    # Renewable Energy
    "NEP", "AQN", "BEP", "CWEN", "HASI", "ORA", "RUN", "SPWR", "NOVA",
    "ENPH", "SEDG", "FSLR", "JKS", "ARRY", "CSIQ", "MAXN", "SHLS", "STEM",
    "OPAL", "PLUG", "BLDP", "FCEL", "BE", "CLNE", "EVGO", "CHPT", "BLNK",
    "DCFC", "PTRA", "PSNY", "RIVN", "LCID", "FSR", "GOEV", "NKLA", "WKHS",
]

SECTOR_60_REAL_ESTATE = [
    # REITs - Diversified
    "SPG", "O", "VICI", "WPC", "STOR", "NNN", "GTY", "GOOD", "AAT", "AHH",
    "AIV", "AKR", "ALX", "AVB", "BDN", "BRG", "BRX", "CDP", "CDR", "CERS",
    # REITs - Industrial
    "PLD", "DRE", "REXR", "STAG", "TRNO", "FR", "EGP", "COLD", "IIPR", "LAND",
    "MNR", "NSA", "PSTL", "PLYM", "GMRE", "ILPT", "INDT", "LXP", "MNR", "NLCP",
    # REITs - Office
    "BXP", "KRC", "SLG", "VNO", "HIW", "CUZ", "PGRE", "JBGS", "DEI", "PDM",
    "OFC", "ESRT", "BDN", "CLI", "CDR", "FSP", "ALEX", "CIO", "CXP", "DLR",
    "EQC", "ARE", "CADE", "CCIT", "COR", "DEA", "GOOD", "HPP", "NLY", "NSA",
    # REITs - Residential
    "EQR", "AVB", "ESS", "UDR", "CPT", "MAA", "AIV", "IRT", "NXRT", "ELME",
    "VRE", "CSR", "AHH", "IRET", "NEN", "SAFE", "STAR", "TRNO", "UMH", "VERIS",
    # REITs - Retail
    "REG", "FRT", "KIM", "BRX", "SITC", "ROIC", "UE", "AKR", "KRG", "MAC",
    "PEI", "CBL", "WRI", "WSR", "ALEX", "BFS", "FCPT", "IVT", "KITE", "NXRT",
    "OLP", "PECO", "RPT", "SAFE", "SKT", "STON", "UBA", "URG", "WHLR",
    # REITs - Healthcare
    "WELL", "VTR", "PEAK", "HR", "OHI", "LTC", "NHI", "SBRA", "CTRE", "CHCT",
    "MPW", "DOC", "GHC", "CMCT", "CTR", "GMRE", "HASI", "IIPR", "LTC", "MPW",
    # REITs - Self Storage
    "PSA", "EXR", "CUBE", "LSI", "NSA", "JCAP", "REXR", "COLD", "SELF", "STOR",
    # REITs - Data Center & Infrastructure
    "EQIX", "DLR", "AMT", "CCI", "SBAC", "UNIT", "CCOI", "CONE", "CORZ", "QTS",
    "CONE", "LADR", "LMRK", "SATS", "SBA", "UNIT", "VNET", "WIFI", "ZAYO",
    # REITs - Hotel
    "HST", "PK", "RHP", "PEB", "SHO", "DRH", "XHR", "INN", "CLDT", "AHT",
    "APLE", "BHR", "CHSP", "CPLG", "CRLBF", "FCH", "HT", "RLGY", "RLJ", "SOHO",
    # Real Estate Services
    "CBRE", "JLL", "CWK", "NMRK", "RMR", "FSV", "EXPI", "CIGI", "HF", "RMAX",
    "COMP", "OPEN", "RDFN", "RLGY", "CSGP", "REAL", "RDFN", "ZG", "IMXI",
]

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

