"""
Wikipedia data source for S&P index constituents.

Scrapes the S&P 500, S&P 400 MidCap, and S&P 600 SmallCap companies lists
from Wikipedia to get ticker symbols with their GICS sub-industry classifications.
This provides approximately 1,500 stocks with GICS classifications.
"""
import logging
from io import StringIO
from typing import Optional, Dict, List

import httpx
import pandas as pd

from src.ingestion.utils.retry import with_retry

logger = logging.getLogger(__name__)


class WikipediaSource:
    """
    Scrape S&P index constituents from Wikipedia.
    
    Features:
    - Completely FREE
    - Includes actual GICS sub-industry names
    - Regularly updated by Wikipedia editors
    - Supports S&P 500, S&P 400 MidCap, and S&P 600 SmallCap
    
    Sources:
    - S&P 500: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
    - S&P 400: https://en.wikipedia.org/wiki/List_of_S%26P_400_companies
    - S&P 600: https://en.wikipedia.org/wiki/List_of_S%26P_600_companies
    """
    
    SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    SP400_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
    SP600_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
    
    INDEX_URLS = {
        'SP500': SP500_URL,
        'SP400': SP400_URL,
        'SP600': SP600_URL,
    }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for Wikipedia requests."""
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    def _standardize_columns(self, df: pd.DataFrame, index_name: str) -> pd.DataFrame:
        """
        Standardize column names and clean ticker symbols.
        
        Args:
            df: Raw DataFrame from Wikipedia
            index_name: Name of the index for logging
        
        Returns:
            Cleaned DataFrame with standardized columns
        """
        # Common column mappings across S&P index pages
        column_mapping = {
            'Symbol': 'ticker',
            'Ticker': 'ticker',
            'Ticker symbol': 'ticker',
            'Company': 'name',
            'Security': 'name',
            'Name': 'name',
            'GICS Sector': 'sector',
            'Sector': 'sector',
            'GICS Sub-Industry': 'sub_industry',
            'GICS Sub Industry': 'sub_industry',
            'Sub-Industry': 'sub_industry',
            'Headquarters Location': 'headquarters',
            'Headquarters': 'headquarters',
            'Date added': 'date_added',
            'CIK': 'cik',
            'Founded': 'founded',
        }
        
        # Rename columns that exist
        rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_dict)
        
        # Clean ticker symbols
        # Some have issues like BRK.B which yfinance expects as BRK-B
        if 'ticker' in df.columns:
            df['ticker'] = df['ticker'].astype(str).str.replace('.', '-', regex=False)
            df['ticker'] = df['ticker'].str.strip()
        
        # Select relevant columns
        required_columns = ['ticker', 'name', 'sector', 'sub_industry']
        available_columns = [c for c in required_columns if c in df.columns]
        
        if len(available_columns) < 4:
            logger.warning(
                f"{index_name}: Missing columns. Available: {df.columns.tolist()}, "
                f"Required: {required_columns}"
            )
        
        result = df[available_columns].copy()
        
        # Remove any rows with missing ticker or sub_industry
        if 'ticker' in result.columns:
            result = result.dropna(subset=['ticker'])
        if 'sub_industry' in result.columns:
            result = result.dropna(subset=['sub_industry'])
        
        return result
    
    @with_retry(max_retries=3, base_delay=2.0)
    def _fetch_index_constituents(self, url: str, index_name: str) -> pd.DataFrame:
        """
        Fetch index constituents from a Wikipedia page.
        
        Args:
            url: Wikipedia page URL
            index_name: Name of the index for logging
        
        Returns:
            DataFrame with standardized columns
        """
        logger.info(f"Fetching {index_name} constituents from Wikipedia...")
        
        try:
            with httpx.Client(timeout=30, headers=self._get_headers()) as client:
                response = client.get(url)
                response.raise_for_status()
                html = response.text
            
            # Parse tables from HTML
            tables = pd.read_html(StringIO(html))
            
            if not tables:
                raise ValueError(f"No tables found on {index_name} Wikipedia page")
            
            # First table is current constituents
            df = tables[0]
            
            logger.info(f"Found {len(df)} {index_name} constituents")
            
            result = self._standardize_columns(df, index_name)
            
            # Add index source column
            result['index_source'] = index_name
            
            logger.info(f"Returning {len(result)} valid {index_name} constituents")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching {index_name} constituents: {e}")
            raise
    
    @with_retry(max_retries=3, base_delay=2.0)
    def fetch_sp500_constituents(self) -> pd.DataFrame:
        """
        Fetch S&P 500 constituents with GICS classification.
        
        Returns:
            DataFrame with columns:
            - ticker: Stock symbol
            - name: Company name
            - sector: GICS sector
            - sub_industry: GICS sub-industry
            - index_source: 'SP500'
        """
        return self._fetch_index_constituents(self.SP500_URL, 'SP500')
    
    @with_retry(max_retries=3, base_delay=2.0)
    def fetch_sp400_constituents(self) -> pd.DataFrame:
        """
        Fetch S&P 400 MidCap constituents with GICS classification.
        
        Returns:
            DataFrame with columns:
            - ticker: Stock symbol
            - name: Company name
            - sector: GICS sector
            - sub_industry: GICS sub-industry
            - index_source: 'SP400'
        """
        return self._fetch_index_constituents(self.SP400_URL, 'SP400')
    
    @with_retry(max_retries=3, base_delay=2.0)
    def fetch_sp600_constituents(self) -> pd.DataFrame:
        """
        Fetch S&P 600 SmallCap constituents with GICS classification.
        
        Returns:
            DataFrame with columns:
            - ticker: Stock symbol
            - name: Company name
            - sector: GICS sector
            - sub_industry: GICS sub-industry
            - index_source: 'SP600'
        """
        return self._fetch_index_constituents(self.SP600_URL, 'SP600')
    
    def fetch_all_sp_constituents(self) -> pd.DataFrame:
        """
        Fetch all S&P index constituents (500 + 400 + 600 = ~1500 stocks).
        
        This combines S&P 500 Large Cap, S&P 400 MidCap, and S&P 600 SmallCap
        to provide comprehensive coverage of US equities with GICS classifications.
        
        Returns:
            DataFrame with columns:
            - ticker: Stock symbol
            - name: Company name
            - sector: GICS sector
            - sub_industry: GICS sub-industry
            - index_source: 'SP500', 'SP400', or 'SP600'
        """
        logger.info("Fetching all S&P index constituents (SP500 + SP400 + SP600)...")
        
        all_dfs = []
        
        # Fetch each index
        for index_name, url in self.INDEX_URLS.items():
            try:
                df = self._fetch_index_constituents(url, index_name)
                all_dfs.append(df)
                logger.info(f"Successfully fetched {len(df)} {index_name} stocks")
            except Exception as e:
                logger.error(f"Failed to fetch {index_name}: {e}")
                # Continue with other indices even if one fails
        
        if not all_dfs:
            raise ValueError("Failed to fetch any S&P index constituents")
        
        # Combine all DataFrames
        combined = pd.concat(all_dfs, ignore_index=True)
        
        # Remove duplicates (some stocks may appear in multiple indices during transitions)
        # Keep the first occurrence (prioritize larger indices)
        combined = combined.drop_duplicates(subset=['ticker'], keep='first')
        
        # Only keep stocks with valid sub_industry
        if 'sub_industry' in combined.columns:
            combined = combined[combined['sub_industry'].notna()]
            combined = combined[combined['sub_industry'].str.strip() != '']
        
        logger.info(f"Total unique stocks with GICS classification: {len(combined)}")
        
        # Log breakdown by sector
        if 'sector' in combined.columns:
            sector_counts = combined['sector'].value_counts()
            for sector, count in sector_counts.items():
                logger.debug(f"  {sector}: {count} stocks")
        
        return combined
    
    def fetch_sp500_changes(self) -> Optional[pd.DataFrame]:
        """
        Fetch historical S&P 500 additions/deletions.
        
        Returns:
            DataFrame with recent index changes, or None if not available
        """
        try:
            with httpx.Client(timeout=30, headers=self._get_headers()) as client:
                response = client.get(self.SP500_URL)
                response.raise_for_status()
                html = response.text
            
            tables = pd.read_html(StringIO(html))
            
            # Second table is typically the changes history
            if len(tables) > 1:
                changes_df = tables[1]
                logger.info(f"Found {len(changes_df)} historical changes")
                return changes_df
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not fetch S&P 500 changes: {e}")
            return None
    
    def get_unique_subindustries(self, use_all_indices: bool = True) -> pd.DataFrame:
        """
        Get unique GICS sub-industries from S&P indices.
        
        Args:
            use_all_indices: If True, use all S&P indices (500+400+600).
                           If False, use only S&P 500.
        
        Returns:
            DataFrame with unique sub-industries and their sectors
        """
        if use_all_indices:
            constituents = self.fetch_all_sp_constituents()
            index_desc = "all S&P indices"
        else:
            constituents = self.fetch_sp500_constituents()
            index_desc = "S&P 500"
        
        if 'sub_industry' not in constituents.columns:
            raise ValueError("sub_industry column not found in data")
        
        # Get unique sub-industries with their sectors
        unique = constituents.groupby('sub_industry').agg({
            'sector': 'first',
            'ticker': 'count'
        }).reset_index()
        
        unique = unique.rename(columns={'ticker': 'stock_count'})
        unique = unique.sort_values('sub_industry')
        
        logger.info(f"Found {len(unique)} unique sub-industries in {index_desc}")
        return unique
    
    def get_subindustry_coverage_stats(self) -> pd.DataFrame:
        """
        Get statistics on stock coverage by sub-industry across all indices.
        
        Returns:
            DataFrame with sub-industry, sector, and counts by index
        """
        all_data = self.fetch_all_sp_constituents()
        
        # Create pivot table showing counts by sub-industry and index
        pivot = all_data.pivot_table(
            index=['sector', 'sub_industry'],
            columns='index_source',
            values='ticker',
            aggfunc='count',
            fill_value=0
        ).reset_index()
        
        # Add total column
        index_cols = [c for c in pivot.columns if c.startswith('SP')]
        pivot['total'] = pivot[index_cols].sum(axis=1)
        
        # Sort by total count descending
        pivot = pivot.sort_values('total', ascending=False)
        
        return pivot


# Singleton instance
wikipedia_source = WikipediaSource()

