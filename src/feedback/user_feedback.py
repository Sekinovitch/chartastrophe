"""
User feedback system to improve funny correlations.
"""
import json
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class UserFeedback:
    def __init__(self):
        self.feedback_file = 'user_feedback.json'
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> Dict:
        """Load feedback data from file."""
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Feedback loaded: {len(data.get('correlations', {}))} rated correlations")
                    return data
        except Exception as e:
            logger.error(f"Error loading feedback: {e}")
        
        return {
            'correlations': {},  # correlation_id -> {'rating': 'funny'/'boring', 'timestamp': '...', 'series': ['...', '...']}
            'dataset_scores': defaultdict(float),  # dataset_name -> score (positive = funny, negative = boring)
            'combination_scores': defaultdict(float)  # 'dataset1|dataset2' -> score
        }
    
    def _save_feedback(self):
        """Save feedback data to file."""
        try:
            # Convert defaultdict to regular dict for JSON serialization
            data_to_save = {
                'correlations': self.feedback_data['correlations'],
                'dataset_scores': dict(self.feedback_data['dataset_scores']),
                'combination_scores': dict(self.feedback_data['combination_scores'])
            }
            
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
    
    def add_feedback(self, correlation_id: str, rating: str, series1_name: str, series2_name: str):
        """
        Add user feedback for a correlation.
        
        Args:
            correlation_id: Unique correlation identifier
            rating: User rating ('funny', 'intriguing', 'boring')
            series1_name: Name of first series
            series2_name: Name of second series
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Record correlation feedback
            self.feedback_data['correlations'][correlation_id] = {
                'rating': rating,
                'timestamp': timestamp,
                'series': [series1_name, series2_name]
            }
            
            # Update dataset scores
            if rating == 'funny':
                score_change = 1.0
            elif rating == 'intriguing':
                score_change = 0.3  # Positive but lower score than funny
            else:  # boring
                score_change = -0.5
                
            self.feedback_data['dataset_scores'][series1_name] += score_change
            self.feedback_data['dataset_scores'][series2_name] += score_change
            
            # Update combination score
            combo_key = f"{series1_name}|{series2_name}"
            combo_key_reverse = f"{series2_name}|{series1_name}"
            self.feedback_data['combination_scores'][combo_key] += score_change
            self.feedback_data['combination_scores'][combo_key_reverse] += score_change
            
            self._save_feedback()
            logger.info(f"Feedback added: {rating} for {series1_name} vs {series2_name}")
            
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
    
    def get_dataset_priorities(self) -> List[str]:
        """
        Get list of datasets prioritized by positive feedback.
        
        Returns:
            List of dataset names sorted by score (highest first)
        """
        try:
            sorted_datasets = sorted(
                self.feedback_data['dataset_scores'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Return only datasets with positive scores
            positive_datasets = [name for name, score in sorted_datasets if score > 0]
            logger.debug(f"Priority datasets: {positive_datasets[:5]}")  # Log top 5
            return positive_datasets
            
        except Exception as e:
            logger.error(f"Error getting dataset priorities: {e}")
            return []
    
    def get_funny_keywords(self) -> List[str]:
        """
        Extract keywords from funny correlations to improve future generations.
        
        Returns:
            List of keywords associated with funny correlations
        """
        keywords = []
        try:
            for corr_data in self.feedback_data['correlations'].values():
                if corr_data['rating'] == 'funny':
                    for series_name in corr_data['series']:
                        # Extract keywords from series names
                        words = series_name.lower().split()
                        keywords.extend(words)
            
            # Count keyword frequency
            from collections import Counter
            keyword_counts = Counter(keywords)
            
            # Return most frequent keywords
            return [word for word, count in keyword_counts.most_common(20)]
            
        except Exception as e:
            logger.error(f"Error extracting funny keywords: {e}")
            return []
    
    def should_prioritize_dataset(self, dataset_name: str) -> bool:
        """
        Determine if a dataset should be prioritized based on feedback.
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            True if the dataset should be prioritized
        """
        score = self.feedback_data['dataset_scores'].get(dataset_name, 0)
        return score > 0.5  # Threshold to consider a dataset as "funny"
    
    def get_stats(self) -> Dict:
        """
        Return feedback statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_feedback = len(self.feedback_data['correlations'])
        funny_count = sum(1 for corr in self.feedback_data['correlations'].values() if corr['rating'] == 'funny')
        intriguing_count = sum(1 for corr in self.feedback_data['correlations'].values() if corr['rating'] == 'intriguing')
        boring_count = sum(1 for corr in self.feedback_data['correlations'].values() if corr['rating'] == 'boring')
        
        top_datasets = sorted(
            self.feedback_data['dataset_scores'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'total_feedback': total_feedback,
            'funny_count': funny_count,
            'intriguing_count': intriguing_count,
            'boring_count': boring_count,
            'funny_ratio': funny_count / total_feedback if total_feedback > 0 else 0,
            'intriguing_ratio': intriguing_count / total_feedback if total_feedback > 0 else 0,
            'top_funny_datasets': top_datasets
        }

# Global instance
user_feedback = UserFeedback() 