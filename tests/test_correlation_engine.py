"""
Unit tests for the correlation engine.
"""
import unittest
import pandas as pd
import numpy as np
from src.correlation.correlation_engine import CorrelationEngine

class TestCorrelationEngine(unittest.TestCase):
    def setUp(self):
        """Initialize test data."""
        self.engine = CorrelationEngine()
        
        # Create test data
        np.random.seed(42)
        self.data1 = pd.DataFrame({
            'A': np.random.normal(0, 1, 100),
            'B': np.random.normal(0, 1, 100)
        })
        self.data2 = pd.DataFrame({
            'C': self.data1['A'] * 2 + np.random.normal(0, 0.1, 100),  # Strong correlation with A
            'D': np.random.normal(0, 1, 100)  # No correlation
        })
        
    def test_calculate_correlation(self):
        """Test correlation calculation."""
        corr, p_value = self.engine.calculate_correlation(
            self.data1['A'],
            self.data2['C'],
            method='pearson'
        )
        self.assertGreater(abs(corr), 0.9)  # Strong correlation expected
        self.assertLess(p_value, 0.05)  # Significant correlation
        
    def test_find_correlations(self):
        """Test correlation search."""
        results = self.engine.find_correlations(
            [self.data1, self.data2],
            threshold=0.5
        )
        self.assertGreater(len(results), 0)
        
    def test_filter_significant_correlations(self):
        """Test filtering of significant correlations."""
        correlations = [
            {'correlation': 0.9, 'p_value': 0.01},
            {'correlation': 0.3, 'p_value': 0.2}
        ]
        filtered = self.engine.filter_significant_correlations(
            correlations,
            p_value_threshold=0.05
        )
        self.assertEqual(len(filtered), 1)
        
    def test_get_correlation_summary(self):
        """Test correlation summary."""
        correlations = [
            {'correlation': 0.9, 'p_value': 0.01},
            {'correlation': -0.8, 'p_value': 0.02}
        ]
        summary = self.engine.get_correlation_summary(correlations)
        self.assertEqual(summary['nombre_total'], 2)
        self.assertAlmostEqual(summary['correlation_moyenne'], 0.85)
        
    def test_invalid_method(self):
        """Test with invalid correlation method."""
        with self.assertRaises(ValueError):
            self.engine.calculate_correlation(
                self.data1['A'],
                self.data2['C'],
                method='invalid_method'
            )
            
    def test_missing_values(self):
        """Test with missing values."""
        series1 = pd.Series([1, 2, np.nan, 4, 5])
        series2 = pd.Series([2, 4, 6, 8, 10])
        corr, p_value = self.engine.calculate_correlation(series1, series2)
        self.assertIsNotNone(corr)
        
if __name__ == '__main__':
    unittest.main() 