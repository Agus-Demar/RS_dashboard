"""
Tests for the Mansfield RS Calculator.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.rs_calculator import MansfieldRSCalculator, calculate_percentile_ranks


class TestMansfieldRSCalculator:
    """Tests for MansfieldRSCalculator class."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return MansfieldRSCalculator(sma_period_weeks=52)
    
    @pytest.fixture
    def sample_prices(self):
        """Create sample price data."""
        # Generate 2 years of daily data
        dates = pd.date_range(
            end=date.today(),
            periods=504,  # ~2 years of trading days
            freq='B'  # Business days
        )
        
        # Asset prices: trending up with some noise
        np.random.seed(42)
        asset_returns = np.random.normal(0.0005, 0.015, len(dates))
        asset_prices = 100 * np.exp(np.cumsum(asset_returns))
        
        # Benchmark prices: similar but slightly different
        benchmark_returns = np.random.normal(0.0003, 0.012, len(dates))
        benchmark_prices = 100 * np.exp(np.cumsum(benchmark_returns))
        
        asset = pd.Series(asset_prices, index=dates)
        benchmark = pd.Series(benchmark_prices, index=dates)
        
        return asset, benchmark
    
    def test_calculate_rs_line(self, calculator, sample_prices):
        """Test RS Line calculation."""
        asset, benchmark = sample_prices
        
        rs_line = calculator.calculate_rs_line(asset, benchmark)
        
        # RS Line should have same length as input (after alignment)
        assert len(rs_line) == len(asset)
        
        # RS Line values should be positive
        assert (rs_line > 0).all()
        
        # RS Line = (Asset / Benchmark) * 100
        expected_first = (asset.iloc[0] / benchmark.iloc[0]) * 100
        assert abs(rs_line.iloc[0] - expected_first) < 0.0001
    
    def test_calculate_rs_sma(self, calculator, sample_prices):
        """Test RS SMA calculation."""
        asset, benchmark = sample_prices
        rs_line = calculator.calculate_rs_line(asset, benchmark)
        
        rs_sma = calculator.calculate_rs_sma(rs_line)
        
        # First 52 weeks (~260 trading days) should be NaN
        # Actually depends on implementation - check that we have some NaN at start
        assert rs_sma.isna().sum() > 0
        
        # Later values should not be NaN
        assert rs_sma.dropna().shape[0] > 0
    
    def test_calculate_mansfield_rs(self, calculator, sample_prices):
        """Test Mansfield RS calculation."""
        asset, benchmark = sample_prices
        rs_line = calculator.calculate_rs_line(asset, benchmark)
        rs_sma = calculator.calculate_rs_sma(rs_line)
        
        mansfield_rs = calculator.calculate_mansfield_rs(rs_line, rs_sma)
        
        # Mansfield RS should be centered around 0
        valid_rs = mansfield_rs.dropna()
        assert valid_rs.mean() < 50  # Should not be wildly positive
        assert valid_rs.mean() > -50  # Should not be wildly negative
    
    def test_calculate_full(self, calculator, sample_prices):
        """Test full calculation pipeline."""
        asset, benchmark = sample_prices
        
        result = calculator.calculate_full(asset, benchmark)
        
        # Should have all three columns
        assert 'rs_line' in result.columns
        assert 'rs_line_sma_52w' in result.columns
        assert 'mansfield_rs' in result.columns
        
        # Should have same length as input
        assert len(result) == len(asset)
    
    def test_outperforming_asset(self, calculator):
        """Test that strongly outperforming asset has positive RS."""
        dates = pd.date_range(end=date.today(), periods=300, freq='B')
        
        # Asset doubles while benchmark stays flat
        asset = pd.Series(np.linspace(100, 200, len(dates)), index=dates)
        benchmark = pd.Series([100] * len(dates), index=dates)
        
        result = calculator.calculate_full(asset, benchmark)
        
        # Latest Mansfield RS should be strongly positive
        latest_rs = result['mansfield_rs'].dropna().iloc[-1]
        assert latest_rs > 0
    
    def test_underperforming_asset(self, calculator):
        """Test that underperforming asset has negative RS."""
        dates = pd.date_range(end=date.today(), periods=300, freq='B')
        
        # Asset halves while benchmark stays flat
        asset = pd.Series(np.linspace(100, 50, len(dates)), index=dates)
        benchmark = pd.Series([100] * len(dates), index=dates)
        
        result = calculator.calculate_full(asset, benchmark)
        
        # Latest Mansfield RS should be negative
        latest_rs = result['mansfield_rs'].dropna().iloc[-1]
        assert latest_rs < 0


class TestPercentileRanks:
    """Tests for percentile ranking function."""
    
    def test_basic_ranking(self):
        """Test basic percentile calculation."""
        rs_values = pd.Series({
            'A': -20,
            'B': -10,
            'C': 0,
            'D': 10,
            'E': 20,
        })
        
        percentiles = calculate_percentile_ranks(rs_values)
        
        # E should have highest percentile
        assert percentiles['E'] > percentiles['D'] > percentiles['C']
        
        # A should have lowest percentile
        assert percentiles['A'] < percentiles['B'] < percentiles['C']
    
    def test_percentile_range(self):
        """Test that percentiles are in 0-100 range."""
        rs_values = pd.Series(np.random.randn(100))
        
        percentiles = calculate_percentile_ranks(rs_values)
        
        assert percentiles.min() >= 0
        assert percentiles.max() <= 100
    
    def test_handles_nan(self):
        """Test that NaN values are handled."""
        rs_values = pd.Series({
            'A': -10,
            'B': np.nan,
            'C': 10,
        })
        
        percentiles = calculate_percentile_ranks(rs_values)
        
        # Should only have percentiles for valid values
        assert 'A' in percentiles.index
        assert 'C' in percentiles.index
        assert len(percentiles) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

