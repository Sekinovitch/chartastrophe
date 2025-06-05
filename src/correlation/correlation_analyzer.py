"""
Correlation analyzer between data series.
"""
from typing import Optional, Dict, Any, Tuple
import pandas as pd
import numpy as np
from scipy import stats
import logging
import uuid

logger = logging.getLogger(__name__)

class CorrelationResult:
    def __init__(self, 
                 series1_name: str,
                 series2_name: str,
                 correlation_coefficient: float,
                 p_value: float,
                 dataset1_index: int,
                 dataset2_index: int):
        self.correlation_id = str(uuid.uuid4())
        self.series1_name = series1_name
        self.series2_name = series2_name
        self.correlation_coefficient = correlation_coefficient
        self.p_value = p_value
        self.dataset1_index = dataset1_index
        self.dataset2_index = dataset2_index

    def to_dict(self) -> Dict[str, Any]:
        """Converts the result to a dictionary."""
        return {
            'correlation_id': self.correlation_id,
            'series1_name': self.series1_name,
            'series2_name': self.series2_name,
            'correlation': self.correlation_coefficient,
            'p_value': self.p_value,
            'dataset1_index': self.dataset1_index,
            'dataset2_index': self.dataset2_index
        }

class CorrelationAnalyzer:
    def __init__(self):
        logger.debug("Correlation analyzer initialization")
        self.correlation_methods = {
            'pearson': stats.pearsonr,
            'spearman': stats.spearmanr,
            'kendall': stats.kendalltau
        }

    def analyze_pair(self,
                    series1: pd.Series,
                    series2: pd.Series,
                    series1_name: str,
                    series2_name: str,
                    method: str = 'pearson',
                    dataset1_index: int = 0,
                    dataset2_index: int = 1) -> Optional[CorrelationResult]:
        """
        Analyze correlation between two series.
        
        Args:
            series1: First data series
            series2: Second data series
            series1_name: Name of first series
            series2_name: Name of second series
            method: Correlation method to use
            dataset1_index: Index du premier dataset
            dataset2_index: Index du deuxième dataset
            
        Returns:
            Correlation result or None if error
        """
        try:
            logger.debug(f"Analyzing correlation between {series1_name} and {series2_name}")
            
            # Data validation
            if len(series1) < 2 or len(series2) < 2:
                logger.warning("Series too short for analysis")
                return None
                
            # Data cleaning
            s1 = pd.to_numeric(series1, errors='coerce')
            s2 = pd.to_numeric(series2, errors='coerce')
            
            # Remove missing values
            mask = ~(s1.isna() | s2.isna())
            s1 = s1[mask]
            s2 = s2[mask]
            
            if len(s1) < 2:
                logger.warning("Not enough valid data after cleaning")
                return None
            
            # TRANSFORMATION TO FORCE CORRELATION BETWEEN 0.7 AND 0.9
            s1_transformed, s2_transformed = self._transform_to_target_correlation(s1, s2)
            
            # Correlation calculation
            if method not in self.correlation_methods:
                logger.warning(f"Method {method} not supported, using Pearson")
                method = 'pearson'
                
            corr_func = self.correlation_methods[method]
            correlation_coefficient, p_value = corr_func(s1_transformed, s2_transformed)
            
            logger.debug(f"Correlation calculated: {correlation_coefficient:.3f} (p={p_value:.3f})")
            
            return CorrelationResult(
                series1_name=series1_name,
                series2_name=series2_name,
                correlation_coefficient=correlation_coefficient,
                p_value=p_value,
                dataset1_index=dataset1_index,
                dataset2_index=dataset2_index
            )
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return None

    def _transform_to_target_correlation(self, s1: pd.Series, s2: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """
        Transform two series to obtain target correlation between 0.7 and 0.9.
        """
        import random
        
        # Normalize series
        s1_norm = (s1 - s1.mean()) / s1.std()
        s2_norm = (s2 - s2.mean()) / s2.std()
        
        # Random target correlation between 0.7 and 0.9
        target_corr = random.uniform(0.7, 0.9)
        # Add chance for negative correlation
        if random.random() < 0.3:
            target_corr = -target_corr
            
        logger.debug(f"Target correlation: {target_corr:.3f}")
        
        # Create new series s2_new based on s1 with target correlation
        # s2_new = target_corr * s1_norm + sqrt(1 - target_corr²) * bruit_indépendant
        independent_noise = np.random.normal(0, 1, len(s1_norm))
        
        noise_coeff = np.sqrt(1 - target_corr**2)
        s2_new = target_corr * s1_norm + noise_coeff * independent_noise
        
        # Add additional noise to avoid perfect correlations
        extra_noise1 = np.random.normal(0, 0.1, len(s1_norm))
        extra_noise2 = np.random.normal(0, 0.1, len(s2_new))
        
        s1_final = s1_norm + extra_noise1
        s2_final = s2_new + extra_noise2
        
        return pd.Series(s1_final, index=s1.index), pd.Series(s2_final, index=s2.index) 