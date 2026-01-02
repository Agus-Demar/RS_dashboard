"""
Wikipedia data source for S&P 500 constituents.

Scrapes the S&P 500 companies list from Wikipedia to get
ticker symbols with their GICS sub-industry classifications.
"""
import logging
from typing import Optional

import httpx
import pandas as pd

from src.ingestion.utils.retry import with_retry

logger = logging.getLogger(__name__)


class WikipediaSource:
    """
    Scrape S&P 500 constituents from Wikipedia.
    
    Features:
    - Completely FREE
    - Includes actual GICS sub-industry names
    - Regularly updated by Wikipedia editors
    
    Source: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
    """
    
    SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
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
        """
        logger.info("Fetching S&P 500 constituents from Wikipedia...")
        
        try:
            # Headers to avoid 403 Forbidden from Wikipedia
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
            
            # Fetch HTML
            with httpx.Client(timeout=30, headers=headers) as client:
                response = client.get(self.SP500_URL)
                response.raise_for_status()
                html = response.text
            
            # Parse tables from HTML
            tables = pd.read_html(html)
            
            if not tables:
                raise ValueError("No tables found on Wikipedia page")
            
            # First table is current constituents
            df = tables[0]
            
            logger.info(f"Found {len(df)} S&P 500 constituents")
            
            # Standardize column names
            column_mapping = {
                'Symbol': 'ticker',
                'Security': 'name',
                'GICS Sector': 'sector',
                'GICS Sub-Industry': 'sub_industry',
                'Headquarters Location': 'headquarters',
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
                df['ticker'] = df['ticker'].str.replace('.', '-', regex=False)
            
            # Select relevant columns
            required_columns = ['ticker', 'name', 'sector', 'sub_industry']
            available_columns = [c for c in required_columns if c in df.columns]
            
            if len(available_columns) < 4:
                logger.warning(
                    f"Missing columns. Available: {df.columns.tolist()}, "
                    f"Required: {required_columns}"
                )
            
            result = df[available_columns].copy()
            
            # Remove any rows with missing ticker
            result = result.dropna(subset=['ticker'])
            
            logger.info(f"Returning {len(result)} valid constituents")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching S&P 500 constituents: {e}")
            raise
    
    def fetch_sp500_changes(self) -> Optional[pd.DataFrame]:
        """
        Fetch historical S&P 500 additions/deletions.
        
        Returns:
            DataFrame with recent index changes, or None if not available
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            with httpx.Client(timeout=30, headers=headers) as client:
                response = client.get(self.SP500_URL)
                response.raise_for_status()
                html = response.text
            
            tables = pd.read_html(html)
            
            # Second table is typically the changes history
            if len(tables) > 1:
                changes_df = tables[1]
                logger.info(f"Found {len(changes_df)} historical changes")
                return changes_df
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not fetch S&P 500 changes: {e}")
            return None
    
    def get_unique_subindustries(self) -> pd.DataFrame:
        """
        Get unique GICS sub-industries from S&P 500.
        
        Returns:
            DataFrame with unique sub-industries and their sectors
        """
        constituents = self.fetch_sp500_constituents()
        
        if 'sub_industry' not in constituents.columns:
            raise ValueError("sub_industry column not found in data")
        
        # Get unique sub-industries with their sectors
        unique = constituents.groupby('sub_industry').agg({
            'sector': 'first',
            'ticker': 'count'
        }).reset_index()
        
        unique = unique.rename(columns={'ticker': 'stock_count'})
        unique = unique.sort_values('sub_industry')
        
        logger.info(f"Found {len(unique)} unique sub-industries in S&P 500")
        return unique


# Singleton instance
wikipedia_source = WikipediaSource()

