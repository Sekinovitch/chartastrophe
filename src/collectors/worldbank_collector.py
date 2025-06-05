"""
Data collector for World Bank API.
"""
import requests
import pandas as pd
from typing import List, Dict, Optional

class WorldBankCollector:
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
        self.format = "json"
    
    def get_indicator_data(
        self,
        indicator_code: str,
        country: str = "FR",
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Retrieve data for a specific indicator.
        
        Args:
            indicator_code: World Bank indicator code
            country: ISO country code (default: FR for France)
            start_year: Start year (optional)
            end_year: End year (optional)
        """
        url = f"{self.base_url}/country/{country}/indicator/{indicator_code}"
        params = {
            "format": self.format,
            "per_page": 1000
        }
        
        if start_year:
            params["date"] = f"{start_year}:{end_year or 2024}"
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()[1]  # First element contains metadata
        
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"], format="%Y")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        
        return df[["date", "value", "indicator.value", "country.value"]]
    
    def search_indicators(self, query: str) -> List[Dict]:
        """
        Search indicators by keyword.
        """
        url = f"{self.base_url}/indicators"
        params = {
            "format": self.format,
            "per_page": 100,
            "search": query
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()[1]  # First element contains metadata 