"""
Correlation engine for analyzing and finding relationships between different datasets.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Tuple
from datetime import datetime
import uuid
import logging
from collections import defaultdict, deque
import time

from ..collectors.real_data_collector import RealDataCollector
from ..correlation.correlation_analyzer import CorrelationAnalyzer
from ..generator.explanation_generator import ExplanationGenerator
from ..data_sources import SOURCES
from ..config import CORRELATION_CONFIG
from ..feedback.user_feedback import user_feedback

logger = logging.getLogger(__name__)

class CorrelationEngine:
    def __init__(self):
        logger.debug("Initializing correlation engine")
        self.data_collector = RealDataCollector()
        self.analyzer = CorrelationAnalyzer()
        self.generator = ExplanationGenerator()
        self.correlation_methods = ['pearson', 'spearman', 'kendall']
        
        # Cache to avoid regenerating the same data
        self.datasets_cache = {}
        self.cache_timestamp = 0
        self.cache_duration = 60  # Reduced to 1 minute instead of 5 for more diversity
        
        # Anti-redundancy system
        self.recent_combinations = deque(maxlen=100)  # Keep last 100 combinations (instead of 50)
        self.dataset_usage_count = defaultdict(int)  # Usage counter per dataset
        self.max_dataset_reuse = 2  # Maximum reuses of a dataset before avoiding it (reduced from 3 to 2)
        
    def _get_cached_datasets(self, n_datasets: int = 5) -> Dict[str, pd.Series]:
        """Retrieve datasets from cache or generate them."""
        current_time = time.time()
        
        # Check if cache is valid
        if (current_time - self.cache_timestamp < self.cache_duration and 
            len(self.datasets_cache) >= n_datasets * 3):  # Require 3x more datasets in cache
            logger.info("Using datasets cache")
            # Return random sample from cache
            import random
            cached_keys = list(self.datasets_cache.keys())
            selected_keys = random.sample(cached_keys, min(n_datasets, len(cached_keys)))
            return {key: self.datasets_cache[key] for key in selected_keys}
        
        # Regenerate cache with much more data
        logger.info("Regenerating datasets cache")
        self.datasets_cache = self.data_collector.get_datasets(n_datasets * 8)  # 8x more data for cache
        self.cache_timestamp = current_time
        
        # Return random sample
        import random
        cached_keys = list(self.datasets_cache.keys())
        selected_keys = random.sample(cached_keys, min(n_datasets, len(cached_keys)))
        return {key: self.datasets_cache[key] for key in selected_keys}
        
    def _prioritize_datasets_by_feedback(self, datasets: Dict[str, pd.Series]) -> Dict[str, pd.Series]:
        """Prioritize datasets based on user feedback."""
        try:
            # Retrieve popular datasets
            funny_priorities = user_feedback.get_dataset_priorities()
            
            if not funny_priorities:
                logger.info("No feedback available, using default order")
                return datasets
            
            # Separate datasets based on feedback
            prioritized = {}
            non_prioritized = {}
            
            for name, series in datasets.items():
                if user_feedback.should_prioritize_dataset(name):
                    prioritized[name] = series
                else:
                    non_prioritized[name] = series
            
            # Combine by prioritizing popular datasets
            result = {**prioritized, **non_prioritized}
            
            logger.info(f"Datasets prioritized by feedback: {len(prioritized)} priority, {len(non_prioritized)} others")
            return result
            
        except Exception as e:
            logger.warning(f"Error during feedback prioritization: {e}")
            return datasets
    
    def _filter_datasets_for_diversity(self, datasets: Dict[str, pd.Series]) -> Dict[str, pd.Series]:
        """Filters datasets to avoid redundancies and promote diversity."""
        try:
            # Separate datasets based on recent usage
            fresh_datasets = {}
            overused_datasets = {}
            
            for name, series in datasets.items():
                usage_count = self.dataset_usage_count.get(name, 0)
                if usage_count < self.max_dataset_reuse:
                    fresh_datasets[name] = series
                else:
                    overused_datasets[name] = series
            
            # Prioritize less used datasets
            if len(fresh_datasets) >= 5:  # Enough fresh datasets
                logger.info(f"Using fresh datasets: {len(fresh_datasets)} available")
                return fresh_datasets
            else:
                # Mix fresh and overused if not enough fresh datasets
                logger.info(f"Mixing fresh datasets ({len(fresh_datasets)}) and reused ({len(overused_datasets)})")
                
                # Reset overused dataset counters if necessary
                if len(fresh_datasets) < 2:
                    logger.info("Resetting overuse counters")
                    for name in overused_datasets:
                        self.dataset_usage_count[name] = 0
                    return {**fresh_datasets, **overused_datasets}
                
                return {**fresh_datasets, **overused_datasets}
                
        except Exception as e:
            logger.warning(f"Error during diversity filtering: {e}")
            return datasets

    def get_source_info(self, series_name: str) -> Dict:
        """
        Retrieve source information for a given series.
        
        Args:
            series_name: Name of the series
            
        Returns:
            Dictionary containing source information
        """
        # Search in available sources
        for source_id, source_info in SOURCES.items():
            if source_info['name'] == series_name:
                return {
                    'name': source_info['name'],
                    'url': source_info['url'],
                    'category': source_info['category']
                }
        return None

    def generate_random_correlations(self, n_datasets: int = 5) -> List[Dict]:
        """
        Generate random correlations from real data.
        
        Args:
            n_datasets: Number of datasets to use
            
        Returns:
            List of correlations with their explanations
        """
        try:
            logger.info(f"Starting generation of {n_datasets} real correlations")
            
            # Retrieve real data
            datasets = self._get_cached_datasets(n_datasets)
            logger.info(f"Real data retrieved: {len(datasets)} datasets")
            
            # Prioritize based on user feedback
            datasets = self._prioritize_datasets_by_feedback(datasets)
            
            # Filter to avoid redundancies
            datasets = self._filter_datasets_for_diversity(datasets)
            
            if len(datasets) < 2:
                logger.warning("Not enough datasets retrieved to generate correlations")
                return []
            
            # Correlation analysis (optimized)
            correlations = []
            total_comparisons = 0
            successful_comparisons = 0
            max_comparisons = 15  # Limit to speed up
            
            dataset_items = list(datasets.items())
            
            for i, (name1, series1) in enumerate(dataset_items):
                if total_comparisons >= max_comparisons:
                    break
                    
                for j, (name2, series2) in enumerate(dataset_items[i+1:], i+1):
                    if total_comparisons >= max_comparisons:
                        break
                    
                    # Check if this combination was used recently
                    if self._is_combination_recent(name1, name2):
                        logger.debug(f"Combination '{name1}' + '{name2}' recently used, skipping")
                        continue
                        
                    total_comparisons += 1
                    logger.debug(f"Analyzing correlation between '{name1}' and '{name2}'")
                    
                    try:
                        # Date alignment
                        if isinstance(series1.index, pd.DatetimeIndex) and \
                           isinstance(series2.index, pd.DatetimeIndex):
                            common_index = series1.index.intersection(series2.index)
                            if len(common_index) < CORRELATION_CONFIG['min_samples']:
                                logger.debug(f"Not enough common dates between '{name1}' and '{name2}' ({len(common_index)} < {CORRELATION_CONFIG['min_samples']})")
                                continue
                            s1 = series1[common_index]
                            s2 = series2[common_index]
                        else:
                            s1 = series1
                            s2 = series2
                        
                        # Data validation
                        if len(s1) != len(s2):
                            logger.debug(f"Series of different lengths: {len(s1)} vs {len(s2)}")
                            continue
                            
                        if len(s1) < CORRELATION_CONFIG['min_samples']:
                            logger.debug(f"Not enough data points: {len(s1)} < {CORRELATION_CONFIG['min_samples']}")
                            continue
                        
                        # Correlation calculation
                        result = self.analyzer.analyze_pair(
                            s1, s2,
                            name1, name2,
                            dataset1_index=i,
                            dataset2_index=j
                        )
                        
                        if result is not None:
                            coef = result.correlation_coefficient
                            p_val = result.p_value
                            logger.info(f"Correlation found between '{name1}' and '{name2}': {coef:.3f} (p={p_val:.3f})")
                            
                            # Threshold validation
                            if abs(coef) >= CORRELATION_CONFIG['min_correlation'] and \
                               p_val <= CORRELATION_CONFIG['max_p_value']:
                                successful_comparisons += 1
                                
                                # Retrieve transformed data for graph
                                s1_transformed, s2_transformed = self.analyzer._transform_to_target_correlation(s1, s2)
                                
                                # Add data for graph (transformed data)
                                correlation_data = result.to_dict()
                                correlation_data['data_x'] = s1_transformed.tolist()
                                correlation_data['data_y'] = s2_transformed.tolist()
                                correlation_data['series1_name'] = name1
                                correlation_data['series2_name'] = name2
                                
                                # Add real source information
                                sources = []
                                if hasattr(series1, 'source_name') and hasattr(series1, 'source_url'):
                                    sources.append({
                                        'name': series1.source_name,
                                        'url': series1.source_url,
                                        'category': 'Public data'
                                    })
                                if hasattr(series2, 'source_name') and hasattr(series2, 'source_url'):
                                    sources.append({
                                        'name': series2.source_name,
                                        'url': series2.source_url,
                                        'category': 'Public data'
                                    })
                                correlation_data['sources'] = sources
                                
                                # Record this combination as used
                                self._record_combination(name1, name2)
                                
                                correlations.append(correlation_data)
                            else:
                                logger.debug(f"Correlation rejected: |{coef:.3f}| < {CORRELATION_CONFIG['min_correlation']} or p={p_val:.3f} > {CORRELATION_CONFIG['max_p_value']}")
                            
                    except Exception as e:
                        logger.error(f"Error during analysis of '{name1}' vs '{name2}': {str(e)}")
                        continue
            
            logger.info(f"Analyses performed: {successful_comparisons}/{total_comparisons} successful comparisons")
            
            if not correlations:
                logger.warning("No significant correlation found")
                return []
            
            # Sort correlations by strength
            correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            logger.info(f"Total number of significant correlations: {len(correlations)}")
            
            # Generate explanations
            results = []
            for corr in correlations[:1]:  # Keep only the best correlation
                logger.info(f"Generating explanation for correlation between '{corr['series1_name']}' and '{corr['series2_name']}'")
                explanation = self.generator.generate_explanation(corr)
                results.append({
                    **corr,
                    'title': explanation['title'],
                    'explanation': explanation['explanation']
                })
            
            logger.info(f"Results generated: {len(results)} correlations")
            return results
            
        except Exception as e:
            logger.error(f"Error during correlation generation: {str(e)}")
            return []

    def generate_random_correlation(self) -> Dict:
        """Generate a single random correlation."""
        correlations = self.generate_random_correlations(n_datasets=5)
        if correlations:
            correlation = correlations[0]
            correlation['correlation_id'] = str(uuid.uuid4())
            return correlation
        else:
            raise Exception("No correlation found")

    def find_correlations(self, 
                         datasets: List[pd.DataFrame], 
                         method: str = 'pearson',
                         threshold: float = 0.7) -> List[Dict]:
        """
        Find all significant correlations between datasets.
        
        Args:
            datasets: List of DataFrames to analyze
            method: Correlation method ('pearson', 'spearman', or 'kendall')
            threshold: Minimum correlation threshold
            
        Returns:
            List of significant correlations
        """
        if method not in self.correlation_methods:
            raise ValueError(f"Method {method} not supported. Use: {list(self.correlation_methods)}")
            
        logger.info(f"Starting correlation analysis with {method} method")
        results = []
        
        for i, df1 in enumerate(datasets):
            for j, df2 in enumerate(datasets[i+1:], i+1):
                for col1 in df1.columns:
                    for col2 in df2.columns:
                        try:
                            result = self.analyzer.analyze_pair(
                                df1[col1],
                                df2[col2],
                                col1,
                                col2,
                                method=method,
                                dataset1_index=i,
                                dataset2_index=j
                            )
                            
                            if result is not None and abs(result.correlation_coefficient) >= threshold:
                                results.append(result.to_dict())
                                
                        except Exception as e:
                            logger.warning(f"Error calculating correlation between {col1} and {col2}: {str(e)}")
                            
        logger.info(f"Analysis completed. {len(results)} correlations found.")
        return results

    def filter_significant_correlations(self, 
                                      correlations: List[Dict],
                                      p_value_threshold: float = 0.05) -> List[Dict]:
        """
        Filter statistically significant correlations.
        
        Args:
            correlations: List of correlations to filter
            p_value_threshold: Significance threshold
            
        Returns:
            List of significant correlations
        """
        significant_correlations = [
            corr for corr in correlations 
            if corr['p_value'] < p_value_threshold
        ]
        
        logger.info(f"Filtering performed: {len(significant_correlations)}/{len(correlations)} significant correlations")
        return significant_correlations

    def get_correlation_summary(self, correlations: List[Dict]) -> Dict:
        """
        Generate summary of found correlations.
        
        Args:
            correlations: List of correlations
            
        Returns:
            Dictionary containing correlation statistics
        """
        if not correlations:
            return {"message": "No correlation found"}
            
        corr_values = [abs(c['correlation']) for c in correlations]
        return {
            "total_count": len(correlations),
            "average_correlation": np.mean(corr_values),
            "max_correlation": np.max(corr_values),
            "min_correlation": np.min(corr_values),
            "standard_deviation": np.std(corr_values),
            "timestamp": datetime.now().isoformat()
        }

    def _is_combination_recent(self, name1: str, name2: str) -> bool:
        """Check if a dataset combination was used recently."""
        combination1 = (name1, name2)
        combination2 = (name2, name1)  # Reverse order
        return combination1 in self.recent_combinations or combination2 in self.recent_combinations
    
    def _record_combination(self, name1: str, name2: str):
        """Record a combination as recently used."""
        combination = (name1, name2)
        self.recent_combinations.append(combination)
        
        # Increment usage counters
        self.dataset_usage_count[name1] += 1
        self.dataset_usage_count[name2] += 1
        
        logger.debug(f"Combination recorded: {name1} + {name2} (usages: {self.dataset_usage_count[name1]}, {self.dataset_usage_count[name2]})") 