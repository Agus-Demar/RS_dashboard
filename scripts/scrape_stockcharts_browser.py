#!/usr/bin/env python3
"""
StockCharts Browser-Based Scraper

Uses Playwright to scrape sector, industry, and stock ticker data from StockCharts.com
sector drill-down page. This handles the dynamically loaded JavaScript content.

Usage:
    python -m scripts.scrape_stockcharts_browser
    python -m scripts.scrape_stockcharts_browser --headless
    python -m scripts.scrape_stockcharts_browser --output data/stockcharts_tickers.json

Output:
    JSON file containing sectors, industries, and stock tickers
"""
import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple

from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

# StockCharts URLs
BASE_URL = "https://stockcharts.com/freecharts"
SECTOR_SUMMARY_URL = f"{BASE_URL}/sectorsummary.html?O=3"

# Sector ETF to code mapping
SECTOR_ETF_TO_CODE = {
    "XLE": ("10", "Energy"),
    "XLB": ("15", "Materials"),
    "XLI": ("20", "Industrials"),
    "XLY": ("25", "Consumer Discretionary"),
    "XLP": ("30", "Consumer Staples"),
    "XLV": ("35", "Health Care"),
    "XLF": ("40", "Financials"),
    "XLK": ("45", "Technology"),
    "XLC": ("50", "Communication Services"),
    "XLU": ("55", "Utilities"),
    "XLRE": ("60", "Real Estate"),
}

# Industry index to code mappings (from stockcharts_industry_mapping.py)
INDUSTRY_NAME_TO_CODE = {
    # Energy (10)
    "Coal": "100100",
    "Oil & Gas - Drilling": "100200",
    "Oil & Gas Drilling": "100200",
    "Oil & Gas - E&P": "100300",
    "Oil & Gas Exploration & Production": "100300",
    "Oil & Gas - Equipment & Services": "100400",
    "Oil & Gas Equipment & Services": "100400",
    "Oil & Gas - Integrated": "100500",
    "Integrated Oil & Gas": "100500",
    "Oil & Gas - Pipelines": "100600",
    "Oil & Gas Pipelines": "100600",
    "Oil & Gas - Refining": "100700",
    "Oil & Gas Refining & Marketing": "100700",
    # Materials (15)
    "Aluminum": "150100",
    "Building Materials": "150200",
    "Chemicals": "150300",
    "Containers & Packaging": "150400",
    "Copper": "150500",
    "Fertilizers": "150600",
    "Fertilizers & Agricultural Chemicals": "150600",
    "Gold": "150700",
    "Metals & Mining": "150800",
    "Paper & Forest Products": "150900",
    "Silver": "151000",
    "Specialty Chemicals": "151100",
    "Steel": "151200",
    # Industrials (20)
    "Aerospace": "200100",
    "Aerospace & Defense": "200100",
    "Air Freight": "200200",
    "Air Freight & Logistics": "200200",
    "Airlines": "200300",
    "Building Products": "200400",
    "Business Services": "200500",
    "Commercial Services & Supplies": "200500",
    "Capital Goods": "200600",
    "Commercial Vehicles": "200700",
    "Commercial Vehicles & Trucks": "200700",
    "Conglomerates": "200800",
    "Industrial Conglomerates": "200800",
    "Construction Materials": "200900",
    "Construction & Engineering": "200900",
    "Defense": "201000",
    "Electrical Equipment": "201100",
    "Engineering & Construction": "201200",
    "Environmental Services": "201300",
    "Environmental & Facilities Services": "201300",
    "Farm Machinery": "201400",
    "Agricultural & Farm Machinery": "201400",
    "Heavy Machinery": "201500",
    "Machinery": "201500",
    "Industrial Machinery": "201500",
    "Industrial Distribution": "201600",
    "Trading Companies & Distributors": "201600",
    "Marine Shipping": "201700",
    "Marine": "201700",
    "Packaging": "201800",
    "Railroads": "201900",
    "Security Services": "202000",
    "Security & Alarm Services": "202000",
    "Staffing": "202100",
    "Human Resource & Employment Services": "202100",
    "Trucking": "202200",
    "Waste Management": "202300",
    # Consumer Discretionary (25)
    "Auto Parts": "250100",
    "Auto Parts & Equipment": "250100",
    "Automobiles": "250200",
    "Automobile Manufacturers": "250200",
    "Casinos & Gaming": "250300",
    "Consumer Electronics": "250400",
    "Consumer Electronics Retail": "250400",
    "Department Stores": "250500",
    "Footwear": "250600",
    "Furnishings": "250700",
    "Home Furnishings": "250700",
    "General Merchandise": "250800",
    "General Merchandise Stores": "250800",
    "Home Improvement": "250900",
    "Home Improvement Retail": "250900",
    "Homebuilders": "251000",
    "Homebuilding": "251000",
    "Hotels & Motels": "251100",
    "Hotels, Resorts & Cruise Lines": "251100",
    "Housewares": "251200",
    "Housewares & Specialties": "251200",
    "Leisure Products": "251300",
    "Recreational Services": "251400",
    "Leisure Facilities": "251400",
    "Recreational Vehicles": "251500",
    "Motorcycle Manufacturers": "251500",
    "Restaurants": "251600",
    "Retail Apparel": "251700",
    "Apparel Retail": "251700",
    "Specialty Retail": "251800",
    "Specialty Stores": "251800",
    "Textiles & Apparel": "251900",
    "Apparel, Accessories & Luxury Goods": "251900",
    "Tires": "252000",
    "Tires & Rubber": "252000",
    "Toys": "252100",
    "Leisure Products & Toys": "252100",
    # Consumer Staples (30)
    "Beverages: Alcoholic": "300100",
    "Brewers": "300100",
    "Distillers & Vintners": "300100",
    "Beverages: Non-Alcoholic": "300200",
    "Soft Drinks": "300200",
    "Drug Retailers": "300300",
    "Drug Retail": "300300",
    "Food Products": "300400",
    "Packaged Foods & Meats": "300400",
    "Food Retailers": "300500",
    "Food Retail": "300500",
    "Food Distributors": "300500",
    "Household Products": "300600",
    "Personal Products": "300700",
    "Tobacco": "300800",
    # Health Care (35)
    "Biotechnology": "350100",
    "Diagnostics & Research": "350200",
    "Life Sciences Tools & Services": "350200",
    "Healthcare Distributors": "350300",
    "Health Care Distributors": "350300",
    "Healthcare Facilities": "350400",
    "Health Care Facilities": "350400",
    "Healthcare Plans": "350500",
    "Managed Health Care": "350500",
    "Healthcare Services": "350600",
    "Health Care Services": "350600",
    "Medical Devices": "350700",
    "Health Care Equipment": "350700",
    "Medical Instruments": "350800",
    "Health Care Supplies": "350800",
    "Pharmaceuticals": "350900",
    # Financials (40)
    "Asset Management": "400100",
    "Asset Management & Custody Banks": "400100",
    "Banks: Diversified": "400200",
    "Diversified Banks": "400200",
    "Banks: Regional": "400300",
    "Regional Banks": "400300",
    "Brokers & Exchanges": "400400",
    "Investment Banking & Brokerage": "400400",
    "Financial Exchanges & Data": "400400",
    "Consumer Finance": "400500",
    "Financial Services": "400600",
    "Diversified Financial Services": "400600",
    "Multi-Sector Holdings": "400600",
    "Insurance: Brokers": "400700",
    "Insurance Brokers": "400700",
    "Insurance: Life": "400800",
    "Life & Health Insurance": "400800",
    "Insurance: P&C": "400900",
    "Property & Casualty Insurance": "400900",
    "Insurance: Specialty": "401000",
    "Reinsurance": "401000",
    "Multi-line Insurance": "401000",
    "Mortgage Finance": "401100",
    "Thrifts & Mortgage Finance": "401100",
    "Savings & Loans": "401200",
    # Technology (45)
    "Application Software": "450100",
    "Cloud Computing": "450200",
    "Internet Services & Infrastructure": "450200",
    "Communication Equipment": "450300",
    "Communications Equipment": "450300",
    "Computer Hardware": "450400",
    "Technology Hardware, Storage & Peripherals": "450400",
    "Computer Services": "450500",
    "IT Consulting & Other Services": "450500",
    "Cybersecurity": "450600",
    "Systems Software": "450600",
    "Data Processing": "450700",
    "Data Processing & Outsourced Services": "450700",
    "Electronic Components": "450800",
    "Electronic Equipment & Instruments": "450800",
    "IT Consulting": "450900",
    "Scientific Instruments": "451000",
    "Electronic Manufacturing Services": "451000",
    "Semiconductor Equipment": "451100",
    "Semiconductors": "451200",
    "Software Infrastructure": "451300",
    # Communication Services (50)
    "Advertising": "500100",
    "Broadcasting": "500200",
    "Cable & Satellite": "500300",
    "Entertainment": "500400",
    "Movies & Entertainment": "500400",
    "Internet": "500500",
    "Interactive Media & Services": "500500",
    "Interactive Home Entertainment": "500500",
    "Publishing": "500600",
    "Telecom Equipment": "500700",
    "Telecom Services": "500800",
    "Integrated Telecommunication Services": "500800",
    "Wireless Telecommunication Services": "500800",
    "Alternative Carriers": "500800",
    # Utilities (55)
    "Electric Utilities": "550100",
    "Gas Utilities": "550200",
    "Independent Power": "550300",
    "Independent Power Producers & Energy Traders": "550300",
    "Multi-Utilities": "550400",
    "Renewable Energy": "550500",
    "Renewable Electricity": "550500",
    "Water Utilities": "550600",
    # Real Estate (60)
    "REITs - Diversified": "600100",
    "Diversified REITs": "600100",
    "REITs - Healthcare": "600200",
    "Health Care REITs": "600200",
    "REITs - Hotel & Motel": "600300",
    "Hotel & Resort REITs": "600300",
    "REITs - Industrial": "600400",
    "Industrial REITs": "600400",
    "REITs - Mortgage": "600500",
    "Mortgage REITs": "600500",
    "REITs - Office": "600600",
    "Office REITs": "600600",
    "REITs - Residential": "600700",
    "Residential REITs": "600700",
    "REITs - Retail": "600800",
    "Retail REITs": "600800",
    "REITs - Specialty": "600900",
    "Specialized REITs": "600900",
    "Data Center REITs": "600900",
    "Timber REITs": "600900",
    "Real Estate Development": "601000",
    "Real Estate Services": "601100",
    "Real Estate Management & Development": "601100",
}


class StockChartsBrowserScraper:
    """Browser-based scraper for StockCharts sector drill-down."""
    
    def __init__(self, headless: bool = True, slow_mo: int = 50):
        """
        Initialize the browser scraper.
        
        Args:
            headless: Run browser in headless mode
            slow_mo: Slow down browser operations (ms)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.data: Dict[str, Any] = {
            "source": "stockcharts.com",
            "scraped_at": None,
            "sectors": []
        }
        self.all_tickers: Set[str] = set()
    
    def start(self):
        """Start the browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self.page = self.browser.new_page()
        self.page.set_default_timeout(60000)  # 60 second timeout
        logger.info(f"Browser started (headless={self.headless})")
    
    def stop(self):
        """Stop the browser."""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser stopped")
    
    def wait_for_table(self, timeout: int = 10000):
        """Wait for the data table to load."""
        try:
            self.page.wait_for_selector("#sectorTable tbody tr", timeout=timeout)
            time.sleep(1)  # Extra wait for data to populate
        except PlaywrightTimeout:
            logger.warning("Table did not load in time")
    
    def extract_tickers_from_table(self) -> List[Tuple[str, str]]:
        """
        Extract stock tickers from the current page's data table.
        
        Returns:
            List of (ticker, name) tuples
        """
        tickers = []
        
        # Find all rows in the table body
        rows = self.page.query_selector_all("#sectorTable tbody tr")
        
        for row in rows:
            try:
                # Get ticker from symlink span
                ticker_elem = row.query_selector("span.symlink")
                name_elem = row.query_selector("td:nth-child(3) a, td:nth-child(3)")
                
                if ticker_elem:
                    ticker = ticker_elem.inner_text().strip()
                    name = name_elem.inner_text().strip() if name_elem else ""
                    
                    # Skip ETFs and index funds
                    if ticker and not ticker.startswith("$"):
                        tickers.append((ticker, name))
            except Exception as e:
                logger.debug(f"Error extracting ticker from row: {e}")
        
        return tickers
    
    def extract_drilldown_links(self) -> List[Tuple[str, str]]:
        """
        Extract drill-down links from the current page.
        
        Returns:
            List of (url, name) tuples for drill-down links
        """
        links = []
        
        # Find links that go to deeper drill-down levels
        link_elements = self.page.query_selector_all("#sectorTable tbody tr td a[href*='sectorsummary.html?']")
        
        for elem in link_elements:
            try:
                href = elem.get_attribute("href")
                name = elem.inner_text().strip()
                
                if href and name and "SECTOR_" in href or "G=" in href:
                    # Construct full URL
                    if href.startswith("sectorsummary.html"):
                        href = f"{BASE_URL}/{href}"
                    elif not href.startswith("http"):
                        href = f"{BASE_URL}/{href}"
                    
                    links.append((href, name))
            except Exception as e:
                logger.debug(f"Error extracting link: {e}")
        
        return links
    
    def get_industry_code(self, industry_name: str, sector_code: str, industry_index: int) -> str:
        """Get industry code from name or generate one."""
        # Try to find a matching code
        for name, code in INDUSTRY_NAME_TO_CODE.items():
            if name.lower() == industry_name.lower():
                return code
            if name.lower() in industry_name.lower() or industry_name.lower() in name.lower():
                return code
        
        # Generate a code based on sector and index
        return f"{sector_code}{industry_index:02d}00"
    
    def scrape_industry_stocks(self, industry_url: str) -> List[str]:
        """
        Scrape individual stock tickers from an industry page.
        
        Args:
            industry_url: URL of the industry drill-down page
            
        Returns:
            List of stock tickers
        """
        logger.debug(f"Scraping industry: {industry_url}")
        
        try:
            self.page.goto(industry_url, wait_until="networkidle")
            self.wait_for_table()
            
            tickers = []
            ticker_tuples = self.extract_tickers_from_table()
            
            for ticker, name in ticker_tuples:
                # Filter out ETFs (usually ends with specific patterns)
                if not any(x in name.lower() for x in ['sector fund', 'index fund', 'etf']):
                    tickers.append(ticker)
                    self.all_tickers.add(ticker)
            
            return tickers
            
        except Exception as e:
            logger.error(f"Error scraping industry {industry_url}: {e}")
            return []
    
    def scrape_sector(self, sector_url: str, sector_code: str, sector_name: str) -> Dict[str, Any]:
        """
        Scrape industries and stocks from a sector page.
        
        Args:
            sector_url: URL of the sector drill-down page
            sector_code: 2-digit sector code
            sector_name: Sector name
            
        Returns:
            Sector data with industries and tickers
        """
        logger.info(f"Scraping sector: {sector_name} ({sector_code})")
        
        sector_data = {
            "name": sector_name,
            "code": sector_code,
            "industries": []
        }
        
        try:
            self.page.goto(sector_url, wait_until="networkidle")
            self.wait_for_table()
            
            # Get drill-down links (these are industries)
            industry_links = self.extract_drilldown_links()
            logger.info(f"  Found {len(industry_links)} industries in {sector_name}")
            
            for i, (industry_url, industry_name) in enumerate(industry_links):
                # Skip the sector fund itself
                if "sector fund" in industry_name.lower():
                    continue
                
                industry_code = self.get_industry_code(industry_name, sector_code, i + 1)
                
                # Navigate to industry and get stocks
                tickers = self.scrape_industry_stocks(industry_url)
                
                industry_data = {
                    "name": industry_name,
                    "code": industry_code,
                    "tickers": tickers
                }
                sector_data["industries"].append(industry_data)
                
                logger.info(f"    {industry_name}: {len(tickers)} tickers")
                
                # Go back to sector page for next industry
                self.page.goto(sector_url, wait_until="networkidle")
                self.wait_for_table()
            
        except Exception as e:
            logger.error(f"Error scraping sector {sector_name}: {e}")
        
        return sector_data
    
    def scrape_all(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Scrape all sectors, industries, and stocks.
        
        Args:
            output_path: Path to save incremental data
        
        Returns:
            Complete data structure
        """
        logger.info("Starting full scrape...")
        
        # Navigate to main sector summary page
        logger.info(f"Navigating to {SECTOR_SUMMARY_URL}")
        self.page.goto(SECTOR_SUMMARY_URL, wait_until="networkidle")
        self.wait_for_table()
        
        # Get sector links
        sector_links = self.extract_drilldown_links()
        logger.info(f"Found {len(sector_links)} sector links")
        
        sectors = []
        
        for url, name in sector_links:
            # Determine sector code from URL or name
            sector_code = None
            sector_name = name
            
            # Check if URL contains sector ETF
            for etf, (code, sname) in SECTOR_ETF_TO_CODE.items():
                if f"SECTOR_{etf}" in url or etf in name.upper():
                    sector_code = code
                    sector_name = sname
                    break
            
            if not sector_code:
                # Try to match by name
                for etf, (code, sname) in SECTOR_ETF_TO_CODE.items():
                    if sname.lower() in name.lower():
                        sector_code = code
                        sector_name = sname
                        break
            
            if sector_code:
                sector_data = self.scrape_sector(url, sector_code, sector_name)
                sectors.append(sector_data)
                
                # Save incrementally after each sector
                if output_path:
                    self.data["scraped_at"] = datetime.now().isoformat()
                    self.data["sectors"] = sectors
                    self.data["total_tickers"] = len(self.all_tickers)
                    save_data(self.data, output_path)
                    logger.info(f"Saved incremental data ({len(self.all_tickers)} total tickers)")
        
        self.data["scraped_at"] = datetime.now().isoformat()
        self.data["sectors"] = sectors
        self.data["total_tickers"] = len(self.all_tickers)
        
        return self.data
    
    def run(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Run the scraper."""
        try:
            self.start()
            return self.scrape_all(output_path)
        finally:
            self.stop()


def save_data(data: Dict[str, Any], output_path: Path):
    """Save scraped data to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {output_path}")


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main():
    parser = argparse.ArgumentParser(description="Scrape StockCharts sector drill-down")
    parser.add_argument(
        "--output", "-o",
        default="data/stockcharts_tickers.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser with visible window"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    output_path = Path(args.output)
    headless = not args.no_headless
    
    logger.info("Starting StockCharts browser scraper...")
    scraper = StockChartsBrowserScraper(headless=headless)
    
    try:
        data = scraper.run(output_path)
        
        # Count tickers
        total_tickers = 0
        for sector in data.get("sectors", []):
            for industry in sector.get("industries", []):
                total_tickers += len(industry.get("tickers", []))
        
        logger.info(f"Scraped {len(data.get('sectors', []))} sectors")
        logger.info(f"Total tickers found: {total_tickers}")
        
        save_data(data, output_path)
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
