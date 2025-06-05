"""
Simulated data collector for generating absurd correlations.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional
from ..config import DATA_CONFIG

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        logger.debug("Initializing data collector")
        # Simulated data sources
        self.data_sources = {
            'culture': {
                'baguettes': "Baguette sales in France",
                'fromages': "Cheese consumption per capita",
                'vins': "Wine sales in liters",
                'croissants': "Croissant production",
                'cafes': "Coffee consumption in kg"
            },
            'economy': {
                'pib': "GDP per capita in euros",
                'population': "Population of France",
                'internet': "Percentage of French people on Internet",
                'forets': "Forest area in France (%)",
                'co2': "CO2 emissions per capita"
            },
            'leisure': {
                'festivals': "Number of festivals in France",
                'musees': "Museum attendance",
                'cinemas': "Cinema entries",
                'restaurants': "Michelin starred restaurants",
                'vacances': "Holiday departures"
            }
        }

    def generate_timeseries(self, trend: float = 0.1, seasonality: float = 0.5, noise: float = 0.2) -> pd.Series:
        """Generates a time series with trend, seasonality and noise."""
        logger.debug(f"Generating time series (trend={trend:.3f}, seasonality={seasonality:.3f}, noise={noise:.3f})")
        
        # Generate dates
        n_points = DATA_CONFIG['n_points']
        end_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        dates = pd.date_range(end=end_date, periods=n_points, freq='ME')  # End of month
        
        # Series components
        t = np.linspace(0, 1, n_points)
        trend_component = trend * t
        seasonality_component = seasonality * np.sin(2 * np.pi * 4 * t)  # 4 cycles over the period
        noise_component = noise * np.random.randn(n_points)
        
        # Combine components
        values = trend_component + seasonality_component + noise_component
        
        # Normalize to have values between -1 and 1
        values = (values - values.min()) / (values.max() - values.min()) * 2 - 1
        
        logger.debug(f"Time series generated with {n_points} points")
        return pd.Series(values, index=dates)

    def get_random_datasets(self, n: int = 5) -> Dict[str, pd.Series]:
        """Retrieves several random simulated datasets."""
        logger.info(f"Generating {n} random datasets")
        datasets = {}
        
        # Create list of all sources
        all_sources = []
        for category, source_data in self.data_sources.items():
            for id, name in source_data.items():
                all_sources.append((category, id, name))
        
        logger.info(f"Available sources: {len(all_sources)} sources in {len(self.data_sources)} categories")
        
        # Random selection of n sources
        selected_sources = random.sample(all_sources, min(n, len(all_sources)))
        logger.info(f"Selected sources: {[name for _, _, name in selected_sources]}")
        
        # Generate data for each source
        for category, id, name in selected_sources:
            try:
                logger.debug(f"Generating data for '{name}' (category: {category})")
                
                # Random parameters for generation
                trend = random.uniform(*DATA_CONFIG['trend_range'])
                seasonality = random.uniform(*DATA_CONFIG['seasonality_range'])
                noise = random.uniform(*DATA_CONFIG['noise_range'])
                
                series = self.generate_timeseries(trend, seasonality, noise)
                series.name = name
                
                # Add some random missing values (max 10%)
                mask = np.random.random(len(series)) > 0.1
                series = series[mask]
                
                datasets[name] = series
                logger.info(f"Data generated for '{name}': {len(series)} valid points")
                
            except Exception as e:
                logger.error(f"Error generating data for '{name}': {str(e)}")
                continue
        
        logger.info(f"Total datasets generated: {len(datasets)}/{len(selected_sources)}")
        return datasets 