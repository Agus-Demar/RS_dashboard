"""
GICS Mapper for mapping tickers to sub-industries.

Uses Wikipedia S&P 500 data as the primary source for GICS classification.
Generates 8-digit GICS codes based on sub-industry names.
"""
import hashlib
import logging
from typing import Dict, List, Optional

import pandas as pd

from src.ingestion.sources.wikipedia_source import wikipedia_source

logger = logging.getLogger(__name__)


# GICS Sector codes (2-digit)
GICS_SECTORS = {
    "Energy": "10",
    "Materials": "15",
    "Industrials": "20",
    "Consumer Discretionary": "25",
    "Consumer Staples": "30",
    "Health Care": "35",
    "Financials": "40",
    "Information Technology": "45",
    "Communication Services": "50",
    "Utilities": "55",
    "Real Estate": "60",
}


class GICSMapper:
    """
    Maps tickers to GICS sub-industries.
    
    Uses Wikipedia S&P 500 data as the source of truth for GICS classification.
    Generates consistent 8-digit codes for sub-industries based on hashing.
    """
    
    def __init__(self):
        """Initialize GICS mapper."""
        self._sp500_data: Optional[pd.DataFrame] = None
        self._subindustry_codes: Dict[str, str] = {}
    
    def load_sp500_data(self) -> pd.DataFrame:
        """Load S&P 500 data from Wikipedia."""
        if self._sp500_data is None:
            self._sp500_data = wikipedia_source.fetch_sp500_constituents()
            self._build_subindustry_codes()
        return self._sp500_data
    
    def _build_subindustry_codes(self) -> None:
        """Build mapping of sub-industry names to 8-digit codes."""
        if self._sp500_data is None:
            return
        
        # Get unique sub-industries with their sectors
        subindustries = self._sp500_data.groupby(['sector', 'sub_industry']).size().reset_index()
        
        for _, row in subindustries.iterrows():
            sector = row['sector']
            sub_industry = row['sub_industry']
            
            code = self._generate_subindustry_code(sector, sub_industry)
            self._subindustry_codes[sub_industry] = code
    
    def _generate_subindustry_code(self, sector: str, sub_industry: str) -> str:
        """
        Generate an 8-digit GICS-style code for a sub-industry.
        
        Format: SSGGIIUU
        - SS: Sector code (2 digits)
        - GG: Industry group (derived from sub-industry hash)
        - II: Industry (derived from sub-industry hash)
        - UU: Sub-industry (derived from sub-industry hash)
        """
        # Get sector code
        sector_code = GICS_SECTORS.get(sector, "00")
        
        # Generate consistent 6-digit suffix from sub-industry name
        hash_input = f"{sector}:{sub_industry}".encode()
        hash_digest = hashlib.md5(hash_input).hexdigest()
        
        # Convert first 6 hex chars to 6 decimal digits
        suffix = ""
        for i in range(3):
            hex_pair = hash_digest[i*2:i*2+2]
            num = int(hex_pair, 16) % 100
            suffix += f"{num:02d}"
        
        return sector_code + suffix
    
    def get_subindustry_code(self, sub_industry_name: str) -> Optional[str]:
        """
        Get GICS code for a sub-industry name.
        
        Args:
            sub_industry_name: Full sub-industry name from Wikipedia
        
        Returns:
            8-digit GICS code or None if not found
        """
        # Ensure data is loaded
        self.load_sp500_data()
        return self._subindustry_codes.get(sub_industry_name)
    
    def map_ticker(self, ticker: str) -> Optional[Dict]:
        """
        Map a ticker to its GICS classification.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Dict with subindustry_code, subindustry_name, sector_code, sector_name
            or None if ticker not found
        """
        # Ensure data is loaded
        df = self.load_sp500_data()
        
        # Find ticker in data
        match = df[df['ticker'] == ticker.upper()]
        
        if match.empty:
            logger.debug(f"Ticker {ticker} not found in S&P 500 data")
            return None
        
        row = match.iloc[0]
        sector = row['sector']
        sub_industry = row['sub_industry']
        
        subindustry_code = self.get_subindustry_code(sub_industry)
        
        if not subindustry_code:
            logger.warning(f"Could not generate code for sub-industry: {sub_industry}")
            return None
        
        return {
            'ticker': ticker.upper(),
            'name': row.get('name', ticker),
            'subindustry_code': subindustry_code,
            'subindustry_name': sub_industry,
            'sector_code': subindustry_code[:2],
            'sector_name': sector,
            # These are derived from the full code
            'industry_group_code': subindustry_code[:4],
            'industry_group_name': sub_industry.split(' - ')[0] if ' - ' in sub_industry else sub_industry,
            'industry_code': subindustry_code[:6],
            'industry_name': sub_industry,
        }
    
    def map_batch(self, tickers: List[str]) -> pd.DataFrame:
        """
        Map multiple tickers to GICS classifications.
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            DataFrame with GICS mappings for found tickers
        """
        results = []
        for ticker in tickers:
            mapping = self.map_ticker(ticker)
            if mapping:
                results.append(mapping)
        
        return pd.DataFrame(results)
    
    def get_all_subindustries(self) -> pd.DataFrame:
        """
        Get all unique sub-industries from S&P 500 data.
        
        Returns:
            DataFrame with sub-industry details including generated codes
        """
        df = self.load_sp500_data()
        
        # Group by sub-industry
        subindustries = df.groupby(['sector', 'sub_industry']).agg({
            'ticker': 'count'
        }).reset_index()
        
        subindustries = subindustries.rename(columns={'ticker': 'stock_count'})
        
        # Add codes
        subindustries['code'] = subindustries['sub_industry'].apply(
            lambda x: self._subindustry_codes.get(x, '')
        )
        
        # Add derived codes
        subindustries['sector_code'] = subindustries['code'].str[:2]
        subindustries['industry_group_code'] = subindustries['code'].str[:4]
        subindustries['industry_code'] = subindustries['code'].str[:6]
        
        return subindustries.sort_values('code')
    
    def get_tickers_by_subindustry(self, subindustry_code: str) -> List[str]:
        """
        Get all tickers belonging to a sub-industry.
        
        Args:
            subindustry_code: 8-digit GICS code
        
        Returns:
            List of ticker symbols
        """
        df = self.load_sp500_data()
        
        # Find sub-industry name from code
        subindustry_name = None
        for name, code in self._subindustry_codes.items():
            if code == subindustry_code:
                subindustry_name = name
                break
        
        if not subindustry_name:
            return []
        
        matching = df[df['sub_industry'] == subindustry_name]
        return matching['ticker'].tolist()


# Singleton instance
gics_mapper = GICSMapper()

