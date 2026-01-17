"""
Data module containing reference data and mappings.

This module provides:
- StockCharts industry to ETF/Index mappings
- Reference data structures for financial classifications
- Additional ticker lists organized by industry
"""

from src.data.stockcharts_industry_mapping import (
    INDUSTRY_ETF_MAP,
    SECTOR_ETFS,
    SECTOR_NAMES,
    IndustryETF,
    get_etf_for_industry_code,
    get_alt_etf_for_industry_code,
    get_industry_info,
    get_etf_for_industry_name,
    get_all_industries_by_sector,
    get_unique_etfs,
    get_etf_usage_stats,
    get_sector_fallback_count,
    get_industry_by_name,
    # Backward compatibility aliases
    GICS_SUBINDUSTRY_ETF_MAP,
    get_etf_for_gics_code,
    get_alt_etf_for_gics_code,
    get_subindustry_info,
    get_etf_for_subindustry_name,
    get_all_subindustries_by_sector,
)

from src.data.additional_tickers import (
    INDUSTRY_TICKERS,
    get_all_additional_tickers,
    get_tickers_for_industry,
    get_industry_code_for_ticker,
    # Backward compatibility sector exports
    SECTOR_10_ENERGY,
    SECTOR_15_MATERIALS,
    SECTOR_20_INDUSTRIALS,
    SECTOR_25_CONSUMER_DISCRETIONARY,
    SECTOR_30_CONSUMER_STAPLES,
    SECTOR_35_HEALTHCARE,
    SECTOR_40_FINANCIALS,
    SECTOR_45_TECHNOLOGY,
    SECTOR_50_COMMUNICATION_SERVICES,
    SECTOR_55_UTILITIES,
    SECTOR_60_REAL_ESTATE,
)

# For backward compatibility, also create alias
SubIndustryETF = IndustryETF

__all__ = [
    # New naming
    "INDUSTRY_ETF_MAP",
    "SECTOR_ETFS",
    "SECTOR_NAMES",
    "IndustryETF",
    "get_etf_for_industry_code",
    "get_alt_etf_for_industry_code",
    "get_industry_info",
    "get_etf_for_industry_name",
    "get_all_industries_by_sector",
    "get_unique_etfs",
    "get_etf_usage_stats",
    "get_sector_fallback_count",
    "get_industry_by_name",
    # Backward compatibility
    "GICS_SUBINDUSTRY_ETF_MAP",
    "SubIndustryETF",
    "get_etf_for_gics_code",
    "get_alt_etf_for_gics_code",
    "get_subindustry_info",
    "get_etf_for_subindustry_name",
    "get_all_subindustries_by_sector",
    # Additional tickers
    "INDUSTRY_TICKERS",
    "get_all_additional_tickers",
    "get_tickers_for_industry",
    "get_industry_code_for_ticker",
    # Sector exports
    "SECTOR_10_ENERGY",
    "SECTOR_15_MATERIALS",
    "SECTOR_20_INDUSTRIALS",
    "SECTOR_25_CONSUMER_DISCRETIONARY",
    "SECTOR_30_CONSUMER_STAPLES",
    "SECTOR_35_HEALTHCARE",
    "SECTOR_40_FINANCIALS",
    "SECTOR_45_TECHNOLOGY",
    "SECTOR_50_COMMUNICATION_SERVICES",
    "SECTOR_55_UTILITIES",
    "SECTOR_60_REAL_ESTATE",
]
