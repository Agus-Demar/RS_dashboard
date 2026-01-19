"""
StockCharts Data Loader.

Provides the ground truth for industry/stock structure from the scraped
StockCharts data. This is the canonical source for:
- Industry classification (104 industries across 11 sectors)
- Stock-to-industry assignments
- ETF mappings for RS/SCTR calculations

All RS and SCTR calculations should use this module to ensure consistency
with the actual StockCharts classification.
"""
import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from functools import lru_cache

logger = logging.getLogger(__name__)

# Default path to scraped data
DEFAULT_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "stockcharts_tickers.json"


@dataclass
class Industry:
    """Industry from StockCharts classification."""
    code: str                    # 6-digit industry code (e.g., "350100")
    name: str                    # Industry name (e.g., "Biotechnology")
    sector_code: str             # 2-digit sector code (e.g., "35")
    sector_name: str             # Sector name (e.g., "Health Care")
    tickers: List[str] = field(default_factory=list)  # Stock tickers in this industry
    primary_etf: Optional[str] = None  # Primary ETF for RS/SCTR calculation
    alt_etf: Optional[str] = None       # Alternative ETF
    is_sector_fallback: bool = False    # True if using broad sector ETF


@dataclass  
class Sector:
    """Sector from StockCharts classification."""
    code: str                    # 2-digit sector code
    name: str                    # Sector name
    etf: str                     # Sector ETF (XLE, XLB, etc.)
    industries: Dict[str, Industry] = field(default_factory=dict)


class StockChartsDataLoader:
    """
    Loads and provides access to scraped StockCharts data.
    
    This is the ground truth for industry/stock structure. Use this
    instead of hardcoded mappings for RS/SCTR calculations.
    """
    
    # Sector ETF mapping
    SECTOR_ETFS = {
        "10": ("Energy", "XLE"),
        "15": ("Materials", "XLB"),
        "20": ("Industrials", "XLI"),
        "25": ("Consumer Discretionary", "XLY"),
        "30": ("Consumer Staples", "XLP"),
        "35": ("Health Care", "XLV"),
        "40": ("Financials", "XLF"),
        "45": ("Technology", "XLK"),
        "50": ("Communication Services", "XLC"),
        "55": ("Utilities", "XLU"),
        "60": ("Real Estate", "XLRE"),
    }
    
    # Industry name to ETF mapping (primary ETFs for industries)
    # Only includes industry-specific ETFs, not sector-wide ETFs
    INDUSTRY_ETFS = {
        # Energy
        "Coal": ("XLE", None, True),  # Sector fallback
        "Oil Equipment & Services": ("XES", "IEZ", False),
        "Integrated Oil & Gas": ("XLE", "VDE", True),  # Sector fallback
        "Exploration & Production": ("XOP", "IEO", False),
        "Pipelines": ("AMLP", "MLPA", False),
        
        # Materials
        "Aluminum": ("XME", "PICK", False),
        "Commodity Chemicals": ("XLB", None, True),
        "Specialty Chemicals": ("XLB", None, True),
        "Containers & Packaging": ("XLB", None, True),
        "Gold Mining": ("GDX", "GDXJ", False),
        "Mining": ("XME", "PICK", False),
        "Nonferrous Metals": ("XME", None, False),
        "Paper": ("WOOD", "CUT", False),
        "Steel": ("SLX", "XME", False),
        
        # Industrials
        "Aerospace": ("ITA", "XAR", False),
        "Airlines": ("JETS", "IYT", False),
        "Building Materials & Fixtures": ("XHB", "ITB", False),
        "Business Support Services": ("XLI", None, True),
        "Commercial Vehicles & Trucks": ("XLI", "PAVE", True),
        "Defense": ("ITA", "XAR", False),
        "Delivery Services": ("IYT", "XTN", False),
        "Diversified Industrials": ("XLI", None, True),
        "Heavy Construction": ("PAVE", "PKB", False),
        "Industrial Machinery": ("PAVE", "XLI", False),
        "Industrial Suppliers": ("XLI", None, True),
        "Marine Transportation": ("SEA", "IYT", False),
        "Railroad": ("IYT", "XTN", False),
        "Trucking": ("IYT", "XTN", False),
        "Waste & Disposal Services": ("EVX", "XLI", False),
        
        # Consumer Discretionary
        "Apparel Retailers": ("XRT", "RTH", False),
        "Auto Parts": ("CARZ", "XLY", False),
        "Automobiles": ("CARZ", "XLY", False),
        "Broadline Retailers": ("XRT", "RTH", False),
        "Clothing & Accessories": ("XRT", "XLY", False),
        "Durable Household Products": ("XHB", None, False),
        "Footwear": ("XRT", "XLY", False),
        "Furnishings": ("XHB", "XLY", False),
        "Gambling": ("BJK", "BETZ", False),
        "Home Construction": ("XHB", "ITB", False),
        "Home Improvement Retailers": ("XHB", "ITB", False),
        "Hotels": ("BEDZ", "PEJ", False),
        "Recreational Products": ("PEJ", "XLY", False),
        "Recreational Services": ("PEJ", "XLY", False),
        "Restaurants & Bars": ("EATZ", "PBJ", False),
        "Specialized Consumer Services": ("XLY", None, True),
        "Specialty Retailers": ("XRT", "RTH", False),
        "Tires": ("XLY", None, True),
        "Toys": ("XLY", None, True),
        "Travel & Tourism": ("PEJ", "XLY", False),
        "Business Training & Employment Agencies": ("XLI", None, True),
        
        # Consumer Staples
        "Brewers": ("PBJ", "XLP", False),
        "Distillers & Vintners": ("PBJ", "XLP", False),
        "Drug Retailers": ("XRT", "XLP", False),
        "Food Products": ("PBJ", "VDC", False),
        "Food Retailers & Wholesalers": ("XLP", "VDC", True),
        "General Retailers": ("XRT", "XLP", False),
        "Nondurable Household Products": ("XLP", "VDC", True),
        "Personal Products": ("XLP", "VDC", True),
        "Soft Drinks": ("PBJ", "XLP", False),
        "Tobacco": ("XLP", "VDC", True),
        
        # Health Care
        "Biotechnology": ("XBI", "IBB", False),
        "Health Care Providers": ("XHS", "IHF", False),
        "Medical Equipment": ("IHI", "XHE", False),
        "Medical Supplies": ("IHI", "XHE", False),
        "Pharmaceuticals": ("XPH", "IHE", False),
        
        # Financials
        "Asset Managers": ("XLF", "VFH", True),
        "Banks": ("KRE", "KBE", False),
        "Consumer Finance": ("XLF", "VFH", True),
        "Financial Administration": ("XLF", "VFH", True),
        "Full Line Insurance": ("KIE", "IAK", False),
        "Insurance Brokers": ("KIE", "IAK", False),
        "Investment Services": ("IAI", "XLF", False),
        "Life Insurance": ("KIE", "IAK", False),
        "Mortgage Finance": ("REM", "XLF", False),
        "Property & Casualty Insurance": ("KIE", "IAK", False),
        "Reinsurance": ("KIE", "IAK", False),
        "Specialty Finance": ("XLF", "VFH", True),
        
        # Technology
        "Computer Hardware": ("XLK", "VGT", True),
        "Computer Services": ("XLK", "VGT", True),
        "Electrical Components & Equipment": ("XLK", "VGT", True),
        "Electronic Equipment": ("XLK", "VGT", True),
        "Renewable Energy Equipment": ("ICLN", "TAN", False),
        "Semiconductors": ("SMH", "SOXX", False),
        "Software": ("IGV", "XSW", False),
        "Telecommunications Equipment": ("XLC", "VOX", True),
        
        # Communication Services
        "Broadcasting & Entertainment": ("PEJ", "XLC", False),
        "Fixed Line Telecommunications": ("XLC", "VOX", True),
        "Internet": ("FDN", "PNQI", False),
        "Media Agencies": ("XLC", "VOX", True),
        "Mobile Telecommunications": ("XLC", "VOX", True),
        "Publishing": ("XLC", "VOX", True),
        
        # Utilities
        "Conventional Electricity": ("XLU", "VPU", True),
        "Gas Distribution": ("XLU", "VPU", True),
        "Multiutilities": ("XLU", "VPU", True),
        "Water": ("PHO", "FIW", False),
        
        # Real Estate
        "Diversified REITs": ("VNQ", "IYR", False),
        "Hotel & Lodging REITs": ("XLRE", "VNQ", True),
        "Industrial & Office REITs": ("XLRE", "VNQ", True),
        "Mortgage REITs": ("REM", "MORT", False),
        "Real Estate Holding & Development": ("XLRE", "VNQ", True),
        "Real Estate Services": ("XLRE", "VNQ", True),
        "Residential REITs": ("REZ", "VNQ", False),
        "Retail REITs": ("XLRE", "VNQ", True),
        "Specialty REITs": ("XLRE", "VNQ", True),
    }
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize data loader.
        
        Args:
            data_path: Path to stockcharts_tickers.json (uses default if None)
        """
        self.data_path = data_path or DEFAULT_DATA_PATH
        self._data: Optional[dict] = None
        self._sectors: Dict[str, Sector] = {}
        self._industries: Dict[str, Industry] = {}
        self._ticker_to_industry: Dict[str, str] = {}
        self._etf_usage: Dict[str, List[str]] = defaultdict(list)
        self._shared_etfs: Set[str] = set()
        self._loaded = False
    
    def load(self, force_reload: bool = False) -> bool:
        """
        Load data from JSON file.
        
        Args:
            force_reload: If True, reload even if already loaded
            
        Returns:
            True if loaded successfully
        """
        if self._loaded and not force_reload:
            return True
        
        if not self.data_path.exists():
            logger.error(f"Data file not found: {self.data_path}")
            return False
        
        try:
            with open(self.data_path) as f:
                self._data = json.load(f)
            
            self._parse_data()
            self._identify_shared_etfs()
            self._loaded = True
            
            logger.info(
                f"Loaded StockCharts data: {len(self._sectors)} sectors, "
                f"{len(self._industries)} industries, {len(self._ticker_to_industry)} stocks"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to load StockCharts data: {e}")
            return False
    
    def _parse_data(self):
        """Parse the loaded JSON data into structured objects."""
        from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP
        
        self._sectors.clear()
        self._industries.clear()
        self._ticker_to_industry.clear()
        self._etf_usage.clear()
        
        # Build name-to-code lookup from existing mapping (for database compatibility)
        name_to_code_map = {}
        for code, info in INDUSTRY_ETF_MAP.items():
            # Normalize names for matching
            name_lower = info.name.lower().strip()
            name_to_code_map[name_lower] = (code, info)
        
        industry_counter = defaultdict(int)  # Track industry indices per sector
        used_codes = set()  # Track used codes to ensure uniqueness
        
        for sector_data in self._data.get("sectors", []):
            sector_code = sector_data.get("code", "")
            sector_name = sector_data.get("name", "")
            
            # Get sector ETF
            sector_info = self.SECTOR_ETFS.get(sector_code)
            sector_etf = sector_info[1] if sector_info else "SPY"
            
            sector = Sector(
                code=sector_code,
                name=sector_name,
                etf=sector_etf,
            )
            
            for industry_data in sector_data.get("industries", []):
                industry_name = industry_data.get("name", "")
                industry_name_lower = industry_name.lower().strip()
                industry_counter[sector_code] += 1
                
                # Try to find existing code from mapping (for database compatibility)
                # First check direct name match
                existing_mapping = name_to_code_map.get(industry_name_lower)
                
                # If not found, check aliases
                if not existing_mapping:
                    alias_name = self.NAME_ALIASES.get(industry_name_lower)
                    if alias_name:
                        existing_mapping = name_to_code_map.get(alias_name.lower())
                
                if existing_mapping:
                    # Use existing code from stockcharts_industry_mapping
                    industry_code = existing_mapping[0]
                    info = existing_mapping[1]
                    primary_etf = info.primary_etf
                    alt_etf = info.alt_etf
                    is_fallback = info.is_sector_fallback
                else:
                    # Try fuzzy matching for slight name differences
                    found = False
                    for name_key, (code, info) in name_to_code_map.items():
                        # Check for partial match
                        if (name_key in industry_name_lower or 
                            industry_name_lower in name_key or
                            self._names_match(industry_name_lower, name_key)):
                            industry_code = code
                            primary_etf = info.primary_etf
                            alt_etf = info.alt_etf
                            is_fallback = info.is_sector_fallback
                            found = True
                            break
                    
                    if not found:
                        # Generate new code for industries not in existing mapping
                        industry_code = f"{sector_code}{industry_counter[sector_code]:02d}00"
                        while industry_code in used_codes:
                            industry_counter[sector_code] += 1
                            industry_code = f"{sector_code}{industry_counter[sector_code]:02d}00"
                        
                        # Get ETF from INDUSTRY_ETFS dict or use sector fallback
                        etf_info = self.INDUSTRY_ETFS.get(industry_name)
                        if etf_info:
                            primary_etf, alt_etf, is_fallback = etf_info
                        else:
                            primary_etf, alt_etf, is_fallback = sector_etf, None, True
                            logger.debug(f"Industry '{industry_name}' not found in mapping, using sector fallback")
                
                # Avoid duplicate codes
                if industry_code in used_codes:
                    # Code already used, generate a new one
                    industry_counter[sector_code] += 1
                    industry_code = f"{sector_code}{industry_counter[sector_code]:02d}00"
                    while industry_code in used_codes:
                        industry_counter[sector_code] += 1
                        industry_code = f"{sector_code}{industry_counter[sector_code]:02d}00"
                
                used_codes.add(industry_code)
                
                tickers = industry_data.get("tickers", [])
                
                industry = Industry(
                    code=industry_code,
                    name=industry_name,
                    sector_code=sector_code,
                    sector_name=sector_name,
                    tickers=tickers,
                    primary_etf=primary_etf,
                    alt_etf=alt_etf,
                    is_sector_fallback=is_fallback,
                )
                
                sector.industries[industry_code] = industry
                self._industries[industry_code] = industry
                
                # Track ticker to industry mapping
                for ticker in tickers:
                    self._ticker_to_industry[ticker.upper()] = industry_code
                
                # Track ETF usage (for identifying shared ETFs)
                if not is_fallback:
                    self._etf_usage[primary_etf].append(industry_code)
            
            self._sectors[sector_code] = sector
    
    # Name aliases to map scraped names to database/mapping names
    NAME_ALIASES = {
        # Scraped name -> Database/mapping name
        "oil equipment & services": "oil & gas - equipment & services",
        "medical equipment": "medical devices",
        "medical supplies": "medical instruments",
        "business support services": "business services",
        "heavy construction": "engineering & construction",
        "industrial suppliers": "industrial distribution",
        "marine transportation": "marine shipping",
        "business training & employment agencies": "staffing",
        "waste & disposal services": "waste management",
        "broadline retailers": "general merchandise",
        "recreational products": "leisure products",
        "clothing & accessories": "textiles & apparel",
        "distillers & vintners": "beverages: alcoholic",
        "brewers": "beverages: alcoholic",  # Combined
        "asset managers": "asset management",
        "electrical components & equipment": "electronic components",
        "electronic equipment": "electronic components",
        "media agencies": "advertising",
        "gas distribution": "gas utilities",
        "mortgage reits": "reits - mortgage",
        "real estate holding & development": "real estate development",
        "mortgage finance": "mortgage reits",  # Alternative mapping
        # REITs variations
        "diversified reits": "reits - diversified",
        "specialty reits": "reits - specialty",
        "residential reits": "reits - residential",
        "retail reits": "reits - retail",
        "industrial & office reits": "reits - industrial",
        "hotel & lodging reits": "reits - hotel & motel",
        # Additional mappings for remaining mismatches
        "delivery services": "air freight",
        "building materials & fixtures": "building products",
        "industrial machinery": "heavy machinery",
        "investment services": "brokers & exchanges",
    }
    
    def _names_match(self, name1: str, name2: str) -> bool:
        """Check if two industry names are essentially the same."""
        n1 = name1.lower().strip()
        n2 = name2.lower().strip()
        
        # Direct match
        if n1 == n2:
            return True
        
        # Check aliases
        if self.NAME_ALIASES.get(n1) == n2:
            return True
        if self.NAME_ALIASES.get(n2) == n1:
            return True
        
        # Common name variations
        variations = [
            ("oil & gas", "oil and gas"),
            ("e&p", "exploration & production"),
            ("exploration & production", "e&p"),
            ("software", "application software"),
            ("reits", "reit"),
            ("reits -", ""),
            ("- specialty", "specialty"),
            ("- diversified", "diversified"),
            ("&", "and"),
        ]
        
        # Apply variations
        n1_mod = n1
        n2_mod = n2
        for old, new in variations:
            n1_mod = n1_mod.replace(old, new)
            n2_mod = n2_mod.replace(old, new)
        
        # Remove common suffixes
        for suffix in [" reits", " reit", "s "]:
            n1_mod = n1_mod.replace(suffix, " ")
            n2_mod = n2_mod.replace(suffix, " ")
        
        n1_mod = " ".join(n1_mod.split())
        n2_mod = " ".join(n2_mod.split())
        
        return n1_mod == n2_mod
    
    def _identify_shared_etfs(self):
        """Identify ETFs that are used by multiple industries."""
        self._shared_etfs = {
            etf for etf, industries in self._etf_usage.items()
            if len(industries) > 1
        }
        
        if self._shared_etfs:
            logger.debug(f"Identified {len(self._shared_etfs)} shared ETFs: {self._shared_etfs}")
    
    def ensure_loaded(self):
        """Ensure data is loaded, loading if necessary."""
        if not self._loaded:
            self.load()
    
    @property
    def sectors(self) -> Dict[str, Sector]:
        """Get all sectors."""
        self.ensure_loaded()
        return self._sectors
    
    @property
    def industries(self) -> Dict[str, Industry]:
        """Get all industries."""
        self.ensure_loaded()
        return self._industries
    
    @property
    def shared_etfs(self) -> Set[str]:
        """Get ETFs that are shared by multiple industries."""
        self.ensure_loaded()
        return self._shared_etfs
    
    def get_industry(self, code: str) -> Optional[Industry]:
        """Get industry by code."""
        self.ensure_loaded()
        return self._industries.get(code)
    
    def get_industry_by_name(self, name: str) -> Optional[Industry]:
        """Get industry by name (case-insensitive)."""
        self.ensure_loaded()
        name_lower = name.lower()
        for industry in self._industries.values():
            if industry.name.lower() == name_lower:
                return industry
        return None
    
    def get_sector(self, code: str) -> Optional[Sector]:
        """Get sector by code."""
        self.ensure_loaded()
        return self._sectors.get(code)
    
    def get_industry_for_ticker(self, ticker: str) -> Optional[str]:
        """Get industry code for a stock ticker."""
        self.ensure_loaded()
        return self._ticker_to_industry.get(ticker.upper())
    
    def get_tickers_for_industry(self, industry_code: str) -> List[str]:
        """Get all tickers in an industry."""
        industry = self.get_industry(industry_code)
        return industry.tickers if industry else []
    
    def get_etf_for_industry(self, industry_code: str) -> Optional[str]:
        """
        Get the ETF to use for RS/SCTR calculation for an industry.
        
        Returns the primary ETF only if:
        - It's not a sector fallback
        - It's not shared by multiple industries
        
        Industries with shared ETFs should use market-cap-weighted
        aggregation of individual stock prices instead.
        
        Args:
            industry_code: 6-digit industry code
            
        Returns:
            ETF ticker if unique, None if should use aggregation
        """
        industry = self.get_industry(industry_code)
        if not industry:
            return None
        
        # Don't use sector fallback ETFs
        if industry.is_sector_fallback:
            return None
        
        # Don't use shared ETFs
        if industry.primary_etf in self._shared_etfs:
            return None
        
        return industry.primary_etf
    
    def should_use_aggregation(self, industry_code: str) -> bool:
        """
        Check if an industry should use market-cap-weighted aggregation.
        
        Returns True if:
        - Industry uses a sector fallback ETF
        - Industry's ETF is shared with other industries
        
        Args:
            industry_code: 6-digit industry code
            
        Returns:
            True if should use aggregation, False if can use ETF directly
        """
        return self.get_etf_for_industry(industry_code) is None
    
    def get_industries_using_etf(self, etf_ticker: str) -> List[str]:
        """Get all industry codes that use a specific ETF."""
        self.ensure_loaded()
        return self._etf_usage.get(etf_ticker, [])
    
    def get_all_tickers(self) -> Set[str]:
        """Get all stock tickers from the scraped data."""
        self.ensure_loaded()
        return set(self._ticker_to_industry.keys())
    
    def get_industry_count(self) -> int:
        """Get total number of industries."""
        self.ensure_loaded()
        return len(self._industries)
    
    def get_sector_count(self) -> int:
        """Get total number of sectors."""
        self.ensure_loaded()
        return len(self._sectors)
    
    def get_stats(self) -> Dict:
        """Get statistics about the loaded data."""
        self.ensure_loaded()
        
        industries_with_unique_etf = sum(
            1 for code in self._industries
            if self.get_etf_for_industry(code) is not None
        )
        
        industries_using_aggregation = len(self._industries) - industries_with_unique_etf
        
        return {
            "sectors": len(self._sectors),
            "industries": len(self._industries),
            "stocks": len(self._ticker_to_industry),
            "shared_etfs": len(self._shared_etfs),
            "industries_with_unique_etf": industries_with_unique_etf,
            "industries_using_aggregation": industries_using_aggregation,
            "source_file": str(self.data_path),
            "scraped_at": self._data.get("scraped_at") if self._data else None,
        }


# Singleton instance for easy access
_loader_instance: Optional[StockChartsDataLoader] = None


def get_loader() -> StockChartsDataLoader:
    """Get the singleton StockChartsDataLoader instance."""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = StockChartsDataLoader()
        _loader_instance.load()
    return _loader_instance


def get_industry(code: str) -> Optional[Industry]:
    """Convenience function to get industry by code."""
    return get_loader().get_industry(code)


def get_etf_for_industry(industry_code: str) -> Optional[str]:
    """Convenience function to get ETF for industry."""
    return get_loader().get_etf_for_industry(industry_code)


def should_use_aggregation(industry_code: str) -> bool:
    """Convenience function to check if aggregation should be used."""
    return get_loader().should_use_aggregation(industry_code)


def get_shared_etfs() -> Set[str]:
    """Convenience function to get shared ETFs."""
    return get_loader().shared_etfs
