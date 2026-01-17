#!/usr/bin/env python3
"""
StockCharts Sector Drill-Down Scraper

Extracts sector, industry, and stock ticker data from StockCharts.com
sector drill-down page via their API endpoints.

Usage:
    python -m scripts.scrape_stockcharts
    python -m scripts.scrape_stockcharts --output data/stockcharts_data.json
    python -m scripts.scrape_stockcharts --verbose

Output:
    JSON file containing:
    - sectors (11 S&P sectors)
    - industries within each sector
    - stock tickers within each industry
"""
import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

import httpx

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ingestion.utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# StockCharts base URL and known endpoints
STOCKCHARTS_BASE = "https://stockcharts.com"
SECTOR_SUMMARY_URL = f"{STOCKCHARTS_BASE}/freecharts/sectorsummary.html"

# Sector code mapping (aligned with GICS/S&P standards)
SECTOR_CODES = {
    "Communication Services": "50",
    "Consumer Discretionary": "25",
    "Consumer Staples": "30",
    "Energy": "10",
    "Financial": "40",
    "Financials": "40",
    "Health Care": "35",
    "Healthcare": "35",
    "Industrial": "20",
    "Industrials": "20",
    "Materials": "15",
    "Real Estate": "60",
    "Technology": "45",
    "Information Technology": "45",
    "Utilities": "55",
}

# Known API endpoints to try
API_ENDPOINTS = [
    "/j-sum/sum/sectordrilldown",
    "/j-sum/sum/sectors",
    "/j-sum/api/sectors",
    "/api/sectors",
    "/def/ind-grp-sec.js",
]

# Browser-like headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": SECTOR_SUMMARY_URL,
    "X-Requested-With": "XMLHttpRequest",
}


class StockChartsScraper:
    """Scrapes sector/industry/stock data from StockCharts."""
    
    def __init__(self, rate_limit: float = 0.5):
        """
        Initialize scraper.
        
        Args:
            rate_limit: Requests per second (default 0.5 = 1 request per 2 seconds)
        """
        self.client = httpx.Client(headers=HEADERS, timeout=30.0, follow_redirects=True)
        self.rate_limiter = RateLimiter(calls_per_second=rate_limit)
        self.data: Dict[str, Any] = {
            "source": "stockcharts.com",
            "scraped_at": None,
            "sectors": []
        }
    
    def close(self):
        """Close HTTP client."""
        self.client.close()
    
    def _request(self, url: str) -> Optional[httpx.Response]:
        """Make rate-limited request."""
        self.rate_limiter.acquire_sync()
        try:
            logger.debug(f"Requesting: {url}")
            response = self.client.get(url)
            return response
        except httpx.RequestError as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def discover_api_endpoints(self) -> Optional[str]:
        """
        Try to discover the API endpoint used for sector data.
        
        Returns:
            Working API endpoint URL or None
        """
        logger.info("Discovering StockCharts API endpoints...")
        
        # First, get the main page to analyze scripts
        response = self._request(SECTOR_SUMMARY_URL + "?O=3")
        if response and response.status_code == 200:
            html = response.text
            
            # Look for API URLs in the HTML/JavaScript
            api_patterns = [
                r'url\s*:\s*["\']([^"\']+/j-sum/[^"\']+)["\']',
                r'fetch\s*\(["\']([^"\']+/api/[^"\']+)["\']',
                r'\.get\s*\(["\']([^"\']+sectors[^"\']*)["\']',
                r'src=["\']([^"\']+\.js)["\']',
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, html)
                for match in matches:
                    logger.debug(f"Found potential endpoint: {match}")
        
        # Try known endpoints
        for endpoint in API_ENDPOINTS:
            url = f"{STOCKCHARTS_BASE}{endpoint}"
            response = self._request(url)
            
            if response and response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "json" in content_type or "javascript" in content_type:
                    logger.info(f"Found working endpoint: {endpoint}")
                    return url
        
        return None
    
    def scrape_via_html_parsing(self) -> Dict[str, Any]:
        """
        Fallback: Scrape data by parsing HTML pages directly.
        
        StockCharts uses JavaScript to load data, but we can navigate
        through the drill-down pages.
        """
        logger.info("Scraping via HTML page navigation...")
        
        sectors_data = []
        
        # The O parameter controls the view:
        # O=3 is "All S&P Sectors" view
        # We need to click into each sector to get industries
        
        # Get the main sector list page
        response = self._request(f"{SECTOR_SUMMARY_URL}?O=3")
        if not response or response.status_code != 200:
            logger.error("Failed to fetch sector summary page")
            return {"sectors": []}
        
        html = response.text
        
        # Extract sector links - they follow pattern ?O=x where x is sector ID
        sector_pattern = r'<a[^>]+href="sectorsummary\.html\?O=(\d+)"[^>]*>([^<]+)</a>'
        sector_matches = re.findall(sector_pattern, html, re.IGNORECASE)
        
        # Also try looking for sector names in the page
        sector_link_pattern = r'href="[^"]*sectorsummary[^"]*\?O=(\d+)[^"]*"[^>]*>([A-Za-z\s&]+)<'
        sector_matches.extend(re.findall(sector_link_pattern, html))
        
        # Remove duplicates and clean up
        seen = set()
        unique_sectors = []
        for sector_id, sector_name in sector_matches:
            sector_name = sector_name.strip()
            if sector_name and sector_id not in seen and len(sector_name) > 2:
                seen.add(sector_id)
                unique_sectors.append((sector_id, sector_name))
        
        logger.info(f"Found {len(unique_sectors)} potential sectors")
        
        # Process each sector
        for sector_id, sector_name in unique_sectors:
            logger.info(f"Processing sector: {sector_name} (ID: {sector_id})")
            
            sector_data = self._scrape_sector(sector_id, sector_name)
            if sector_data and sector_data.get("industries"):
                sectors_data.append(sector_data)
        
        return {"sectors": sectors_data}
    
    def _scrape_sector(self, sector_id: str, sector_name: str) -> Optional[Dict]:
        """Scrape industries and stocks for a specific sector."""
        
        # Get sector page
        response = self._request(f"{SECTOR_SUMMARY_URL}?O={sector_id}")
        if not response or response.status_code != 200:
            return None
        
        html = response.text
        
        # Get sector code
        sector_code = SECTOR_CODES.get(sector_name, "00")
        
        industries = []
        
        # Look for industry links within the sector page
        # Industries typically link to O=xxx where xxx is > 100
        industry_pattern = r'href="[^"]*sectorsummary[^"]*\?O=(\d{3,})[^"]*"[^>]*>([^<]+)<'
        industry_matches = re.findall(industry_pattern, html)
        
        # Process each industry
        industry_counter = 1
        for industry_id, industry_name in industry_matches:
            industry_name = industry_name.strip()
            if not industry_name or len(industry_name) < 2:
                continue
                
            logger.debug(f"  Processing industry: {industry_name}")
            
            tickers = self._scrape_industry_tickers(industry_id)
            
            industries.append({
                "name": industry_name,
                "stockcharts_id": industry_id,
                "code": f"{sector_code}{industry_counter:02d}00",
                "tickers": tickers
            })
            industry_counter += 1
        
        return {
            "name": sector_name,
            "code": sector_code,
            "stockcharts_id": sector_id,
            "industries": industries
        }
    
    def _scrape_industry_tickers(self, industry_id: str) -> List[str]:
        """Scrape stock tickers for a specific industry."""
        
        response = self._request(f"{SECTOR_SUMMARY_URL}?O={industry_id}")
        if not response or response.status_code != 200:
            return []
        
        html = response.text
        tickers = []
        
        # Look for stock symbols - typically 1-5 uppercase letters
        # They appear in links to symbol pages
        ticker_patterns = [
            r'/h-sc/ui\?s=([A-Z]{1,5})(?:&|")',
            r'symbol=([A-Z]{1,5})(?:&|")',
            r'>([A-Z]{1,5})</a>',
            r'data-symbol="([A-Z]{1,5})"',
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, html)
            tickers.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tickers = []
        for ticker in tickers:
            if ticker not in seen and len(ticker) >= 1:
                seen.add(ticker)
                unique_tickers.append(ticker)
        
        return unique_tickers
    
    def scrape_via_js_data(self) -> Dict[str, Any]:
        """
        Try to extract data from JavaScript files/inline data.
        
        StockCharts often embeds data directly in JavaScript.
        """
        logger.info("Attempting to extract data from JavaScript sources...")
        
        # Try to get industry/sector definition file
        js_urls = [
            f"{STOCKCHARTS_BASE}/def/ind-grp-sec.js",
            f"{STOCKCHARTS_BASE}/def/industries.js",
            f"{STOCKCHARTS_BASE}/j-sum/def/sectors.js",
        ]
        
        for url in js_urls:
            response = self._request(url)
            if response and response.status_code == 200:
                logger.info(f"Found JS data at: {url}")
                return self._parse_js_data(response.text)
        
        return {"sectors": []}
    
    def _parse_js_data(self, js_content: str) -> Dict[str, Any]:
        """Parse JavaScript content for sector/industry data."""
        
        sectors_data = []
        
        # Look for data structures in JavaScript
        # Common patterns: var sectors = [...], const data = {...}
        json_pattern = r'(?:var|let|const)\s+\w+\s*=\s*(\[[\s\S]*?\]);'
        matches = re.findall(json_pattern, js_content)
        
        for match in matches:
            try:
                data = json.loads(match)
                if isinstance(data, list) and len(data) > 0:
                    logger.debug(f"Found data structure with {len(data)} items")
                    # Analyze structure
                    if isinstance(data[0], dict):
                        if any(key in str(data[0].keys()).lower() for key in ['sector', 'industry', 'symbol']):
                            return self._transform_js_data(data)
            except json.JSONDecodeError:
                continue
        
        return {"sectors": sectors_data}
    
    def _transform_js_data(self, raw_data: List[Dict]) -> Dict[str, Any]:
        """Transform raw JS data into our format."""
        # This will be customized based on the actual data structure found
        return {"sectors": [], "raw": raw_data}
    
    def run(self) -> Dict[str, Any]:
        """
        Run the complete scraping process.
        
        Tries multiple methods to extract data.
        """
        import datetime
        
        self.data["scraped_at"] = datetime.datetime.now().isoformat()
        
        # Method 1: Try API endpoints
        api_url = self.discover_api_endpoints()
        if api_url:
            logger.info(f"Using API endpoint: {api_url}")
            response = self._request(api_url)
            if response and response.status_code == 200:
                try:
                    api_data = response.json()
                    if api_data:
                        self.data.update(self._transform_api_data(api_data))
                        if self.data.get("sectors"):
                            return self.data
                except json.JSONDecodeError:
                    pass
        
        # Method 2: Try JavaScript data files
        js_data = self.scrape_via_js_data()
        if js_data.get("sectors"):
            self.data.update(js_data)
            return self.data
        
        # Method 3: HTML parsing fallback
        html_data = self.scrape_via_html_parsing()
        self.data.update(html_data)
        
        return self.data
    
    def _transform_api_data(self, api_data: Any) -> Dict[str, Any]:
        """Transform API response into our format."""
        # Will be customized based on actual API response
        if isinstance(api_data, list):
            return {"sectors": api_data}
        elif isinstance(api_data, dict):
            return api_data
        return {"sectors": []}


def create_hardcoded_data() -> Dict[str, Any]:
    """
    Create hardcoded StockCharts sector/industry structure.
    
    This is based on the known StockCharts US Industries classification.
    Used as fallback when scraping fails or for offline development.
    """
    import datetime
    
    return {
        "source": "stockcharts.com",
        "scraped_at": datetime.datetime.now().isoformat(),
        "method": "hardcoded",
        "sectors": [
            {
                "name": "Communication Services",
                "code": "50",
                "industries": [
                    {"name": "Advertising", "code": "500100", "tickers": []},
                    {"name": "Broadcasting", "code": "500200", "tickers": []},
                    {"name": "Cable & Satellite", "code": "500300", "tickers": []},
                    {"name": "Entertainment", "code": "500400", "tickers": []},
                    {"name": "Internet", "code": "500500", "tickers": []},
                    {"name": "Publishing", "code": "500600", "tickers": []},
                    {"name": "Telecom Equipment", "code": "500700", "tickers": []},
                    {"name": "Telecom Services", "code": "500800", "tickers": []},
                ]
            },
            {
                "name": "Consumer Discretionary",
                "code": "25",
                "industries": [
                    {"name": "Auto Parts", "code": "250100", "tickers": []},
                    {"name": "Automobiles", "code": "250200", "tickers": []},
                    {"name": "Casinos & Gaming", "code": "250300", "tickers": []},
                    {"name": "Consumer Electronics", "code": "250400", "tickers": []},
                    {"name": "Department Stores", "code": "250500", "tickers": []},
                    {"name": "Footwear", "code": "250600", "tickers": []},
                    {"name": "Furnishings", "code": "250700", "tickers": []},
                    {"name": "General Merchandise", "code": "250800", "tickers": []},
                    {"name": "Home Improvement", "code": "250900", "tickers": []},
                    {"name": "Homebuilders", "code": "251000", "tickers": []},
                    {"name": "Hotels & Motels", "code": "251100", "tickers": []},
                    {"name": "Housewares", "code": "251200", "tickers": []},
                    {"name": "Leisure Products", "code": "251300", "tickers": []},
                    {"name": "Recreational Services", "code": "251400", "tickers": []},
                    {"name": "Recreational Vehicles", "code": "251500", "tickers": []},
                    {"name": "Restaurants", "code": "251600", "tickers": []},
                    {"name": "Retail Apparel", "code": "251700", "tickers": []},
                    {"name": "Specialty Retail", "code": "251800", "tickers": []},
                    {"name": "Textiles & Apparel", "code": "251900", "tickers": []},
                    {"name": "Tires", "code": "252000", "tickers": []},
                    {"name": "Toys", "code": "252100", "tickers": []},
                ]
            },
            {
                "name": "Consumer Staples",
                "code": "30",
                "industries": [
                    {"name": "Beverages: Alcoholic", "code": "300100", "tickers": []},
                    {"name": "Beverages: Non-Alcoholic", "code": "300200", "tickers": []},
                    {"name": "Drug Retailers", "code": "300300", "tickers": []},
                    {"name": "Food Products", "code": "300400", "tickers": []},
                    {"name": "Food Retailers", "code": "300500", "tickers": []},
                    {"name": "Household Products", "code": "300600", "tickers": []},
                    {"name": "Personal Products", "code": "300700", "tickers": []},
                    {"name": "Tobacco", "code": "300800", "tickers": []},
                ]
            },
            {
                "name": "Energy",
                "code": "10",
                "industries": [
                    {"name": "Coal", "code": "100100", "tickers": []},
                    {"name": "Oil & Gas - Drilling", "code": "100200", "tickers": []},
                    {"name": "Oil & Gas - E&P", "code": "100300", "tickers": []},
                    {"name": "Oil & Gas - Equipment & Services", "code": "100400", "tickers": []},
                    {"name": "Oil & Gas - Integrated", "code": "100500", "tickers": []},
                    {"name": "Oil & Gas - Pipelines", "code": "100600", "tickers": []},
                    {"name": "Oil & Gas - Refining", "code": "100700", "tickers": []},
                ]
            },
            {
                "name": "Financials",
                "code": "40",
                "industries": [
                    {"name": "Asset Management", "code": "400100", "tickers": []},
                    {"name": "Banks: Diversified", "code": "400200", "tickers": []},
                    {"name": "Banks: Regional", "code": "400300", "tickers": []},
                    {"name": "Brokers & Exchanges", "code": "400400", "tickers": []},
                    {"name": "Consumer Finance", "code": "400500", "tickers": []},
                    {"name": "Financial Services", "code": "400600", "tickers": []},
                    {"name": "Insurance: Brokers", "code": "400700", "tickers": []},
                    {"name": "Insurance: Life", "code": "400800", "tickers": []},
                    {"name": "Insurance: P&C", "code": "400900", "tickers": []},
                    {"name": "Insurance: Specialty", "code": "401000", "tickers": []},
                    {"name": "Mortgage Finance", "code": "401100", "tickers": []},
                    {"name": "Savings & Loans", "code": "401200", "tickers": []},
                ]
            },
            {
                "name": "Health Care",
                "code": "35",
                "industries": [
                    {"name": "Biotechnology", "code": "350100", "tickers": []},
                    {"name": "Diagnostics & Research", "code": "350200", "tickers": []},
                    {"name": "Healthcare Distributors", "code": "350300", "tickers": []},
                    {"name": "Healthcare Facilities", "code": "350400", "tickers": []},
                    {"name": "Healthcare Plans", "code": "350500", "tickers": []},
                    {"name": "Healthcare Services", "code": "350600", "tickers": []},
                    {"name": "Medical Devices", "code": "350700", "tickers": []},
                    {"name": "Medical Instruments", "code": "350800", "tickers": []},
                    {"name": "Pharmaceuticals", "code": "350900", "tickers": []},
                ]
            },
            {
                "name": "Industrials",
                "code": "20",
                "industries": [
                    {"name": "Aerospace", "code": "200100", "tickers": []},
                    {"name": "Air Freight", "code": "200200", "tickers": []},
                    {"name": "Airlines", "code": "200300", "tickers": []},
                    {"name": "Building Products", "code": "200400", "tickers": []},
                    {"name": "Business Services", "code": "200500", "tickers": []},
                    {"name": "Capital Goods", "code": "200600", "tickers": []},
                    {"name": "Commercial Vehicles", "code": "200700", "tickers": []},
                    {"name": "Conglomerates", "code": "200800", "tickers": []},
                    {"name": "Construction Materials", "code": "200900", "tickers": []},
                    {"name": "Defense", "code": "201000", "tickers": []},
                    {"name": "Electrical Equipment", "code": "201100", "tickers": []},
                    {"name": "Engineering & Construction", "code": "201200", "tickers": []},
                    {"name": "Environmental Services", "code": "201300", "tickers": []},
                    {"name": "Farm Machinery", "code": "201400", "tickers": []},
                    {"name": "Heavy Machinery", "code": "201500", "tickers": []},
                    {"name": "Industrial Distribution", "code": "201600", "tickers": []},
                    {"name": "Marine Shipping", "code": "201700", "tickers": []},
                    {"name": "Packaging", "code": "201800", "tickers": []},
                    {"name": "Railroads", "code": "201900", "tickers": []},
                    {"name": "Security Services", "code": "202000", "tickers": []},
                    {"name": "Staffing", "code": "202100", "tickers": []},
                    {"name": "Trucking", "code": "202200", "tickers": []},
                    {"name": "Waste Management", "code": "202300", "tickers": []},
                ]
            },
            {
                "name": "Materials",
                "code": "15",
                "industries": [
                    {"name": "Aluminum", "code": "150100", "tickers": []},
                    {"name": "Building Materials", "code": "150200", "tickers": []},
                    {"name": "Chemicals", "code": "150300", "tickers": []},
                    {"name": "Containers & Packaging", "code": "150400", "tickers": []},
                    {"name": "Copper", "code": "150500", "tickers": []},
                    {"name": "Fertilizers", "code": "150600", "tickers": []},
                    {"name": "Gold", "code": "150700", "tickers": []},
                    {"name": "Metals & Mining", "code": "150800", "tickers": []},
                    {"name": "Paper & Forest Products", "code": "150900", "tickers": []},
                    {"name": "Silver", "code": "151000", "tickers": []},
                    {"name": "Specialty Chemicals", "code": "151100", "tickers": []},
                    {"name": "Steel", "code": "151200", "tickers": []},
                ]
            },
            {
                "name": "Real Estate",
                "code": "60",
                "industries": [
                    {"name": "REITs - Diversified", "code": "600100", "tickers": []},
                    {"name": "REITs - Healthcare", "code": "600200", "tickers": []},
                    {"name": "REITs - Hotel & Motel", "code": "600300", "tickers": []},
                    {"name": "REITs - Industrial", "code": "600400", "tickers": []},
                    {"name": "REITs - Mortgage", "code": "600500", "tickers": []},
                    {"name": "REITs - Office", "code": "600600", "tickers": []},
                    {"name": "REITs - Residential", "code": "600700", "tickers": []},
                    {"name": "REITs - Retail", "code": "600800", "tickers": []},
                    {"name": "REITs - Specialty", "code": "600900", "tickers": []},
                    {"name": "Real Estate Development", "code": "601000", "tickers": []},
                    {"name": "Real Estate Services", "code": "601100", "tickers": []},
                ]
            },
            {
                "name": "Technology",
                "code": "45",
                "industries": [
                    {"name": "Application Software", "code": "450100", "tickers": []},
                    {"name": "Cloud Computing", "code": "450200", "tickers": []},
                    {"name": "Communication Equipment", "code": "450300", "tickers": []},
                    {"name": "Computer Hardware", "code": "450400", "tickers": []},
                    {"name": "Computer Services", "code": "450500", "tickers": []},
                    {"name": "Cybersecurity", "code": "450600", "tickers": []},
                    {"name": "Data Processing", "code": "450700", "tickers": []},
                    {"name": "Electronic Components", "code": "450800", "tickers": []},
                    {"name": "IT Consulting", "code": "450900", "tickers": []},
                    {"name": "Scientific Instruments", "code": "451000", "tickers": []},
                    {"name": "Semiconductor Equipment", "code": "451100", "tickers": []},
                    {"name": "Semiconductors", "code": "451200", "tickers": []},
                    {"name": "Software Infrastructure", "code": "451300", "tickers": []},
                ]
            },
            {
                "name": "Utilities",
                "code": "55",
                "industries": [
                    {"name": "Electric Utilities", "code": "550100", "tickers": []},
                    {"name": "Gas Utilities", "code": "550200", "tickers": []},
                    {"name": "Independent Power", "code": "550300", "tickers": []},
                    {"name": "Multi-Utilities", "code": "550400", "tickers": []},
                    {"name": "Renewable Energy", "code": "550500", "tickers": []},
                    {"name": "Water Utilities", "code": "550600", "tickers": []},
                ]
            },
        ]
    }


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape StockCharts sector/industry data"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="data/stockcharts_data.json",
        help="Output JSON file path (default: data/stockcharts_data.json)"
    )
    parser.add_argument(
        "--hardcoded",
        action="store_true",
        help="Use hardcoded data instead of scraping (for offline development)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    logger.info("=" * 60)
    logger.info("StockCharts Sector Data Scraper")
    logger.info("=" * 60)
    
    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.hardcoded:
        logger.info("Using hardcoded StockCharts industry structure...")
        data = create_hardcoded_data()
    else:
        # Run scraper
        scraper = StockChartsScraper()
        try:
            data = scraper.run()
            
            # If scraping yielded no data, fall back to hardcoded
            if not data.get("sectors"):
                logger.warning("Scraping returned no data, using hardcoded structure")
                data = create_hardcoded_data()
        finally:
            scraper.close()
    
    # Summary
    total_industries = sum(len(s.get("industries", [])) for s in data.get("sectors", []))
    total_tickers = sum(
        len(ind.get("tickers", []))
        for s in data.get("sectors", [])
        for ind in s.get("industries", [])
    )
    
    logger.info("")
    logger.info("Results:")
    logger.info(f"  Sectors: {len(data.get('sectors', []))}")
    logger.info(f"  Industries: {total_industries}")
    logger.info(f"  Tickers: {total_tickers}")
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"  Output: {output_path}")
    logger.info("=" * 60)
    
    return data


if __name__ == "__main__":
    main()
