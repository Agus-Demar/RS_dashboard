"""
Industry Mapper for mapping tickers to StockCharts industries.

Uses Wikipedia S&P index data (500 + 400 + 600) as the primary source for 
industry classification. Maps Wikipedia sub-industry names to StockCharts
industry codes for consistency with the RS calculation system.

Provides approximately 1,500 stocks with industry classification data.
"""
import logging
from typing import Dict, List, Optional

import pandas as pd

from src.ingestion.sources.wikipedia_source import wikipedia_source
from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP, SECTOR_NAMES

logger = logging.getLogger(__name__)


# Known sub-industry to correct sector mappings
# Some Wikipedia data has incorrect sector assignments - this fixes them
GICS_SECTOR_CORRECTIONS = {
    "Agricultural & Farm Machinery": "Industrials",
}


# GICS/StockCharts Sector codes (2-digit)
GICS_SECTORS = {
    "Energy": "10",
    "Materials": "15",
    "Industrials": "20",
    "Consumer Discretionary": "25",
    "Consumer Staples": "30",
    "Health Care": "35",
    "Financials": "40",
    "Information Technology": "45",
    "Technology": "45",
    "Communication Services": "50",
    "Utilities": "55",
    "Real Estate": "60",
}


# Mapping from Wikipedia sub-industry names to StockCharts industry codes
# This provides a consistent translation between the two classification systems
SUBINDUSTRY_TO_STOCKCHARTS: Dict[str, str] = {
    # Energy
    "Oil & Gas Drilling": "100200",
    "Oil & Gas Equipment & Services": "100400",
    "Integrated Oil & Gas": "100500",
    "Oil & Gas Exploration & Production": "100300",
    "Oil & Gas Refining & Marketing": "100700",
    "Oil & Gas Storage & Transportation": "100600",
    "Coal & Consumable Fuels": "100100",
    
    # Materials
    "Commodity Chemicals": "150300",
    "Diversified Chemicals": "150300",
    "Specialty Chemicals": "151100",
    "Fertilizers & Agricultural Chemicals": "150600",
    "Industrial Gases": "150300",
    "Construction Materials": "150200",
    "Metal, Glass & Plastic Containers": "150400",
    "Paper & Plastic Packaging Products & Materials": "150400",
    "Aluminum": "150100",
    "Diversified Metals & Mining": "150800",
    "Copper": "150500",
    "Gold": "150700",
    "Precious Metals & Minerals": "150700",
    "Silver": "151000",
    "Steel": "151200",
    "Forest Products": "150900",
    "Paper Products": "150900",
    
    # Industrials
    "Aerospace & Defense": "200100",
    "Building Products": "200400",
    "Construction & Engineering": "200900",
    "Electrical Components & Equipment": "201100",
    "Heavy Electrical Equipment": "201100",
    "Industrial Conglomerates": "200800",
    "Construction Machinery & Heavy Transportation Equipment": "201500",
    "Agricultural & Farm Machinery": "201400",
    "Industrial Machinery & Supplies & Components": "201500",
    "Trading Companies & Distributors": "201600",
    "Commercial Printing": "200500",
    "Environmental & Facilities Services": "201300",
    "Office Services & Supplies": "200500",
    "Diversified Support Services": "200500",
    "Security & Alarm Services": "202000",
    "Human Resource & Employment Services": "202100",
    "Research & Consulting Services": "200500",
    "Data Processing & Outsourced Services": "200500",
    "Air Freight & Logistics": "200200",
    "Passenger Airlines": "200300",
    "Marine Transportation": "201700",
    "Rail Transportation": "201900",
    "Cargo Ground Transportation": "202200",
    "Passenger Ground Transportation": "202200",
    
    # Consumer Discretionary
    "Auto Parts & Equipment": "250100",
    "Tires & Rubber": "252000",
    "Automobile Manufacturers": "250200",
    "Motorcycle Manufacturers": "250200",
    "Consumer Electronics": "250400",
    "Home Furnishings": "250700",
    "Homebuilding": "251000",
    "Household Appliances": "251200",
    "Housewares & Specialties": "251200",
    "Leisure Products": "251300",
    "Apparel, Accessories & Luxury Goods": "251700",
    "Footwear": "250600",
    "Textiles": "251900",
    "Casinos & Gaming": "250300",
    "Hotels, Resorts & Cruise Lines": "251100",
    "Leisure Facilities": "251400",
    "Restaurants": "251600",
    "Education Services": "200500",
    "Specialized Consumer Services": "251800",
    "Advertising": "500100",
    "Broadcasting": "500200",
    "Cable & Satellite": "500300",
    "Publishing": "500600",
    "Movies & Entertainment": "500400",
    "Interactive Home Entertainment": "500400",
    "Interactive Media & Services": "500500",
    "Distributors": "251800",
    "Broadline Retail": "250800",
    "Apparel Retail": "251700",
    "Computer & Electronics Retail": "251800",
    "Home Improvement Retail": "250900",
    "Other Specialty Retail": "251800",
    "Automotive Retail": "251800",
    "Homefurnishing Retail": "250700",
    
    # Consumer Staples
    "Brewers": "300100",
    "Distillers & Vintners": "300100",
    "Soft Drinks & Non-alcoholic Beverages": "300200",
    "Agricultural Products & Services": "300400",
    "Packaged Foods & Meats": "300400",
    "Tobacco": "300800",
    "Household Products": "300600",
    "Personal Care Products": "300700",
    "Drug Retail": "300300",
    "Food Distributors": "300500",
    "Food Retail": "300500",
    "Consumer Staples Merchandise Retail": "300500",
    
    # Health Care
    "Biotechnology": "350100",
    "Pharmaceuticals": "350900",
    "Life Sciences Tools & Services": "350200",
    "Health Care Equipment": "350700",
    "Health Care Supplies": "350700",
    "Health Care Distributors": "350300",
    "Health Care Services": "350600",
    "Health Care Facilities": "350400",
    "Managed Health Care": "350500",
    "Health Care Technology": "350600",
    
    # Financials
    "Diversified Banks": "400200",
    "Regional Banks": "400300",
    "Diversified Financial Services": "400600",
    "Multi-Sector Holdings": "400600",
    "Specialized Finance": "400600",
    "Consumer Finance": "400500",
    "Asset Management & Custody Banks": "400100",
    "Investment Banking & Brokerage": "400400",
    "Diversified Capital Markets": "400400",
    "Financial Exchanges & Data": "400400",
    "Mortgage Real Estate Investment Trusts (REITs)": "600500",
    "Insurance Brokers": "400700",
    "Life & Health Insurance": "400800",
    "Multi-line Insurance": "400900",
    "Property & Casualty Insurance": "400900",
    "Reinsurance": "400900",
    "Transaction & Payment Processing Services": "400600",
    
    # Technology
    "IT Consulting & Other Services": "450900",
    "Internet Services & Infrastructure": "450200",
    "Application Software": "450100",
    "Systems Software": "451300",
    "Communications Equipment": "450300",
    "Technology Hardware, Storage & Peripherals": "450400",
    "Electronic Equipment & Instruments": "451000",
    "Electronic Components": "450800",
    "Electronic Manufacturing Services": "450800",
    "Technology Distributors": "450500",
    "Semiconductor Materials & Equipment": "451100",
    "Semiconductors": "451200",
    
    # Communication Services
    "Alternative Carriers": "500800",
    "Integrated Telecommunication Services": "500800",
    "Wireless Telecommunication Services": "500800",
    
    # Utilities
    "Electric Utilities": "550100",
    "Gas Utilities": "550200",
    "Multi-Utilities": "550400",
    "Water Utilities": "550600",
    "Independent Power Producers & Energy Traders": "550300",
    "Renewable Electricity": "550500",
    
    # Real Estate
    "Diversified REITs": "600100",
    "Industrial REITs": "600400",
    "Hotel & Resort REITs": "600300",
    "Office REITs": "600600",
    "Health Care REITs": "600200",
    "Multi-Family Residential REITs": "600700",
    "Single-Family Residential REITs": "600700",
    "Retail REITs": "600800",
    "Specialized REITs": "600900",
    "Data Center REITs": "600900",
    "Telecom Tower REITs": "600900",
    "Timber REITs": "600900",
    "Other Specialized REITs": "600900",
    "Diversified Real Estate Activities": "601100",
    "Real Estate Operating Companies": "601000",
    "Real Estate Development": "601000",
    "Real Estate Services": "601100",
}


class GICSMapper:
    """
    Maps tickers to StockCharts industries.
    
    Uses Wikipedia S&P index data (S&P 500, S&P 400 MidCap, S&P 600 SmallCap)
    as the source of truth for classification, then maps to StockCharts
    industry codes for RS calculation consistency.
    
    This provides approximately 1,500 stocks with industry data.
    """
    
    def __init__(self, use_all_indices: bool = True):
        """
        Initialize industry mapper.
        
        Args:
            use_all_indices: If True, use all S&P indices (500+400+600).
                           If False, use only S&P 500 for backward compatibility.
        """
        self._all_data: Optional[pd.DataFrame] = None
        self._subindustry_codes: Dict[str, str] = {}
        self._use_all_indices = use_all_indices
    
    def load_sp500_data(self) -> pd.DataFrame:
        """
        Load stock data from Wikipedia.
        
        Note: Despite the name (kept for backward compatibility), this method
        will load all S&P indices if use_all_indices=True was set in __init__.
        
        Returns:
            DataFrame with stock data including GICS classifications
        """
        if self._all_data is None:
            if self._use_all_indices:
                logger.info("Loading all S&P index data (500 + 400 + 600)...")
                self._all_data = wikipedia_source.fetch_all_sp_constituents()
            else:
                logger.info("Loading S&P 500 data only...")
                self._all_data = wikipedia_source.fetch_sp500_constituents()
            
            # Apply sector corrections for known misclassifications
            self._all_data = self._apply_sector_corrections(self._all_data)
            self._build_subindustry_codes()
        return self._all_data
    
    def _apply_sector_corrections(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply sector corrections for known misclassifications in Wikipedia data.
        
        Args:
            df: DataFrame with stock data
        
        Returns:
            Cleaned DataFrame with correct sector assignments
        """
        if 'sub_industry' not in df.columns or 'sector' not in df.columns:
            return df
        
        initial_count = len(df)
        
        for sub_industry, correct_sector in GICS_SECTOR_CORRECTIONS.items():
            wrong_sector_mask = (
                (df['sub_industry'] == sub_industry) & 
                (df['sector'] != correct_sector)
            )
            wrong_count = wrong_sector_mask.sum()
            if wrong_count > 0:
                logger.info(
                    f"Removing {wrong_count} stocks with incorrect sector for "
                    f"'{sub_industry}' (keeping only '{correct_sector}')"
                )
                df = df[~wrong_sector_mask]
        
        removed = initial_count - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} stocks with incorrect sector assignments")
        
        return df
    
    def load_all_data(self) -> pd.DataFrame:
        """
        Load all S&P index data regardless of use_all_indices setting.
        
        Returns:
            DataFrame with all S&P index constituents
        """
        return wikipedia_source.fetch_all_sp_constituents()
    
    def _build_subindustry_codes(self) -> None:
        """Build mapping of sub-industry names to StockCharts codes."""
        if self._all_data is None:
            return
        
        subindustries = self._all_data.groupby(['sector', 'sub_industry']).size().reset_index()
        
        for _, row in subindustries.iterrows():
            sector = row['sector']
            sub_industry = row['sub_industry']
            
            # Try to find a mapping to StockCharts code
            code = self._map_to_stockcharts_code(sector, sub_industry)
            self._subindustry_codes[sub_industry] = code
    
    def _map_to_stockcharts_code(self, sector: str, sub_industry: str) -> str:
        """
        Map a Wikipedia sub-industry to a StockCharts industry code.
        
        Args:
            sector: GICS sector name
            sub_industry: GICS sub-industry name
        
        Returns:
            6-digit StockCharts industry code
        """
        # Try exact match first
        if sub_industry in SUBINDUSTRY_TO_STOCKCHARTS:
            return SUBINDUSTRY_TO_STOCKCHARTS[sub_industry]
        
        # Try partial matching
        sub_lower = sub_industry.lower()
        for wiki_name, code in SUBINDUSTRY_TO_STOCKCHARTS.items():
            if wiki_name.lower() in sub_lower or sub_lower in wiki_name.lower():
                return code
        
        # Fall back to sector-based default
        sector_code = GICS_SECTORS.get(sector, "45")
        
        # Try to find any industry in that sector
        for code, info in INDUSTRY_ETF_MAP.items():
            if info.sector_code == sector_code:
                return code
        
        # Ultimate fallback - return a generic code for the sector
        return f"{sector_code}0100"
    
    def get_subindustry_code(self, sub_industry_name: str) -> Optional[str]:
        """
        Get StockCharts industry code for a sub-industry name.
        
        Args:
            sub_industry_name: Full sub-industry name from Wikipedia
        
        Returns:
            6-digit StockCharts code or None if not found
        """
        self.load_sp500_data()
        return self._subindustry_codes.get(sub_industry_name)
    
    def map_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Map a ticker to its industry classification.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dict with subindustry_code, subindustry_name, sector_code, sector_name
            or None if ticker not found
        """
        df = self.load_sp500_data()
        
        match = df[df['ticker'] == ticker.upper()]
        
        if match.empty:
            logger.debug(f"Ticker {ticker} not found in S&P index data")
            return None
        
        row = match.iloc[0]
        sector = row['sector']
        sub_industry = row['sub_industry']
        
        subindustry_code = self.get_subindustry_code(sub_industry)
        
        if not subindustry_code:
            logger.warning(f"Could not map sub-industry: {sub_industry}")
            return None
        
        # Get sector code from the industry code
        sector_code = subindustry_code[:2]
        sector_name = SECTOR_NAMES.get(sector_code, sector)
        
        # Get industry info from mapping
        industry_info = INDUSTRY_ETF_MAP.get(subindustry_code)
        industry_name = industry_info.name if industry_info else sub_industry
        
        return {
            'ticker': ticker.upper(),
            'name': row.get('name', ticker),
            'subindustry_code': subindustry_code,
            'subindustry_name': industry_name,
            'sector_code': sector_code,
            'sector_name': sector_name,
            'industry_group_code': subindustry_code[:4],
            'industry_group_name': industry_name,
            'industry_code': subindustry_code,
            'industry_name': industry_name,
        }
    
    def map_batch(self, tickers: List[str]) -> pd.DataFrame:
        """
        Map multiple tickers to industry classifications.
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            DataFrame with industry mappings for found tickers
        """
        results = []
        for ticker in tickers:
            mapping = self.map_ticker(ticker)
            if mapping:
                results.append(mapping)
        
        return pd.DataFrame(results)
    
    def get_all_subindustries(self) -> pd.DataFrame:
        """
        Get all unique sub-industries from S&P index data.
        
        Returns:
            DataFrame with sub-industry details including codes
        """
        df = self.load_sp500_data()
        
        subindustries = df.groupby(['sector', 'sub_industry']).agg({
            'ticker': 'count'
        }).reset_index()
        
        subindustries = subindustries.rename(columns={'ticker': 'stock_count'})
        
        subindustries['code'] = subindustries['sub_industry'].apply(
            lambda x: self._subindustry_codes.get(x, '')
        )
        
        subindustries['sector_code'] = subindustries['code'].str[:2]
        subindustries['industry_group_code'] = subindustries['code'].str[:4]
        subindustries['industry_code'] = subindustries['code'].str[:6]
        
        return subindustries.sort_values('code')
    
    def get_tickers_by_subindustry(self, subindustry_code: str) -> List[str]:
        """
        Get all tickers belonging to an industry.
        
        Args:
            subindustry_code: 6-digit industry code
        
        Returns:
            List of ticker symbols
        """
        df = self.load_sp500_data()
        
        subindustry_name = None
        for name, code in self._subindustry_codes.items():
            if code == subindustry_code:
                subindustry_name = name
                break
        
        if not subindustry_name:
            return []
        
        matching = df[df['sub_industry'] == subindustry_name]
        return matching['ticker'].tolist()
    
    def get_all_tickers(self) -> List[str]:
        """
        Get all tickers from the loaded data.
        
        Returns:
            List of all ticker symbols
        """
        df = self.load_sp500_data()
        return df['ticker'].tolist()
    
    def get_stock_count_by_index(self) -> Dict[str, int]:
        """
        Get count of stocks by S&P index source.
        
        Returns:
            Dict mapping index name to stock count
        """
        df = self.load_sp500_data()
        if 'index_source' in df.columns:
            return df['index_source'].value_counts().to_dict()
        return {'SP500': len(df)}
    
    def get_coverage_stats(self) -> Dict:
        """
        Get comprehensive coverage statistics.
        
        Returns:
            Dict with various statistics about the data
        """
        df = self.load_sp500_data()
        
        stats = {
            'total_stocks': len(df),
            'unique_sectors': df['sector'].nunique() if 'sector' in df.columns else 0,
            'unique_subindustries': df['sub_industry'].nunique() if 'sub_industry' in df.columns else 0,
            'stocks_per_subindustry_avg': 0,
            'stocks_per_subindustry_min': 0,
            'stocks_per_subindustry_max': 0,
        }
        
        if 'sub_industry' in df.columns:
            subindustry_counts = df['sub_industry'].value_counts()
            stats['stocks_per_subindustry_avg'] = round(subindustry_counts.mean(), 1)
            stats['stocks_per_subindustry_min'] = subindustry_counts.min()
            stats['stocks_per_subindustry_max'] = subindustry_counts.max()
        
        if 'index_source' in df.columns:
            stats['by_index'] = df['index_source'].value_counts().to_dict()
        
        return stats


# Singleton instance - uses all indices by default for comprehensive coverage
gics_mapper = GICSMapper(use_all_indices=True)
