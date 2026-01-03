"""
Data module containing reference data and mappings.

This module provides:
- GICS sub-industry to ETF/Index mappings
- Reference data structures for financial classifications
"""

from src.data.gics_subindustry_etf_mapping import (
    GICS_SUBINDUSTRY_ETF_MAP,
    SECTOR_ETFS,
    SubIndustryETF,
    get_etf_for_gics_code,
    get_alt_etf_for_gics_code,
    get_subindustry_info,
    get_etf_for_subindustry_name,
    get_all_subindustries_by_sector,
    get_unique_etfs,
)

__all__ = [
    "GICS_SUBINDUSTRY_ETF_MAP",
    "SECTOR_ETFS",
    "SubIndustryETF",
    "get_etf_for_gics_code",
    "get_alt_etf_for_gics_code",
    "get_subindustry_info",
    "get_etf_for_subindustry_name",
    "get_all_subindustries_by_sector",
    "get_unique_etfs",
]

