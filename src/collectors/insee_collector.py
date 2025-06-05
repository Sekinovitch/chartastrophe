"""
Data collector for INSEE API.
"""
import os
import requests
import pandas as pd
from typing import List, Dict
from dotenv import load_dotenv
import base64

load_dotenv()

class InseeCollector:
    def __init__(self):
        self.base_url = "https://api.insee.fr/series/BDM/V1"
        self.token_url = "https://api.insee.fr/token"
        self.client_id = os.getenv("INSEE_CLIENT_ID")
        self.client_secret = os.getenv("INSEE_CLIENT_SECRET")
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "INSEE credentials are required. "
                "Create a .env file with INSEE_CLIENT_ID and INSEE_CLIENT_SECRET"
            )
        
        self.access_token = self._get_access_token()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
    
    def _get_access_token(self) -> str:
        """Obtient un jeton d'accès auprès de l'API INSEE."""
        # Création des credentials en Base64
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials_bytes = credentials.encode('ascii')
        base64_credentials = base64.b64encode(credentials_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {base64_credentials}"
        }
        
        data = {
            "grant_type": "client_credentials"
        }
        
        response = requests.post(
            self.token_url,
            headers=headers,
            data=data,
            verify=True  # Enable SSL verification
        )
        
        if response.status_code != 200:
            raise ValueError(f"INSEE authentication error: {response.text}")
        
        return response.json()["access_token"]
    
    def get_series_data(self, series_id: str) -> pd.DataFrame:
        """
        Retrieve time series data.
        
        Args:
            series_id: INSEE series identifier
        """
        url = f"{self.base_url}/data/SERIES_BDM/{series_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract series data
        series_data = []
        for point in data["series"][0]["values"]:
            series_data.append({
                "date": point["timeperiod"],
                "value": point["value"]
            })
        
        df = pd.DataFrame(series_data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        
        return df
    
    def search_series(self, query: str) -> List[Dict]:
        """
        Search series by keyword.
        """
        url = f"{self.base_url}/series"
        params = {"q": query}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()["series"] 