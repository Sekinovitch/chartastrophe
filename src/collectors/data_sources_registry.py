"""
Extensible registry of open data sources.
Allows easy addition of thousands of new real sources.
"""

from typing import Dict, List

class DataSourcesRegistry:
    """Centralized registry of all available open data sources."""
    
    @staticmethod
    def get_all_sources() -> Dict[str, Dict]:
        """Return all available data sources."""
        
        sources = {}
        
        # ===== SOURCES GOUVERNEMENTALES MONDIALES =====
        sources.update(DataSourcesRegistry._get_government_sources())
        
        # ===== SOURCES SCIENTIFIQUES =====
        sources.update(DataSourcesRegistry._get_scientific_sources())
        
        # ===== SOURCES ÉCONOMIQUES =====
        sources.update(DataSourcesRegistry._get_economic_sources())
        
        # ===== SOURCES SOCIALES ET CULTURELLES =====
        sources.update(DataSourcesRegistry._get_social_sources())
        
        # ===== SOURCES ENVIRONNEMENTALES =====
        sources.update(DataSourcesRegistry._get_environmental_sources())
        
        # ===== SOURCES TECHNOLOGIQUES =====
        sources.update(DataSourcesRegistry._get_tech_sources())
        
        return sources
    
    @staticmethod
    def _get_government_sources() -> Dict[str, Dict]:
        """Sources gouvernementales du monde entier."""
        return {
            # FRANCE
            'fr_insee_births': {
                'url': 'https://www.insee.fr/fr/statistiques/serie/000436394',
                'description': 'Monthly births in France (INSEE)',
                'type': 'json',
                'country': 'France'
            },
            'fr_insee_deaths': {
                'url': 'https://www.insee.fr/fr/statistiques/serie/000436398',
                'description': 'Monthly deaths in France (INSEE)',
                'type': 'json',
                'country': 'France'
            },
            'fr_meteo_temperature': {
                'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCS_mensuel.csv',
                'description': 'Average temperatures France (Météo-France)',
                'type': 'csv',
                'country': 'France'
            },
            'fr_sncf_delays': {
                'url': 'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-ter',
                'description': 'Retards trains TER (SNCF Open Data)',
                'type': 'json',
                'country': 'France'
            },
            
            # ROYAUME-UNI
            'uk_gov_gdp': {
                'url': 'https://api.ons.gov.uk/timeseries/abmi/dataset/qna/data',
                'description': 'UK quarterly GDP (ONS)',
                'type': 'json',
                'country': 'UK'
            },
            'uk_gov_unemployment': {
                'url': 'https://api.ons.gov.uk/timeseries/mgsx/dataset/lms/data',
                'description': 'UK unemployment rate (ONS)',
                'type': 'json',
                'country': 'UK'
            },
            
            # CANADA
            'ca_stats_population': {
                'url': 'https://www150.statcan.gc.ca/t1/wds/rest/getDataFromTableByVectorsAndLatestNPeriods',
                'description': 'Population du Canada (Statistique Canada)',
                'type': 'json',
                'country': 'Canada'
            },
            'ca_stats_inflation': {
                'url': 'https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/en/18100004',
                'description': 'Inflation Canada (Statistique Canada)',
                'type': 'csv',
                'country': 'Canada'
            },
            
            # AUSTRALIE
            'au_abs_gdp': {
                'url': 'https://api.data.abs.gov.au/data/ABS,GDP,1.0.0/all',
                'description': 'Australia GDP (Australian Bureau of Statistics)',
                'type': 'json',
                'country': 'Australia'
            },
            
            # NOUVELLE-ZÉLANDE
            'nz_stats_tourism': {
                'url': 'https://api.stats.govt.nz/Indicator/international-travel-and-migration',
                'description': 'Tourisme international Nouvelle-Zélande',
                'type': 'json',
                'country': 'New Zealand'
            }
        }
    
    @staticmethod
    def _get_scientific_sources() -> Dict[str, Dict]:
        """Scientific and research sources."""
        return {
            # NASA
            'nasa_exoplanets_confirmed': {
                'url': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_name,disc_year&format=json',
                'description': 'Exoplanètes confirmées par année (NASA)',
                'type': 'json',
                'organization': 'NASA'
            },
            'nasa_mars_rover_sols': {
                'url': 'https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?sol=1000&api_key=DEMO_KEY',
                'description': 'Photos du rover Mars Perseverance (NASA)',
                'type': 'json',
                'organization': 'NASA'
            },
            'nasa_earth_fireball': {
                'url': 'https://ssd-api.jpl.nasa.gov/fireball.api',
                'description': 'Météores/boules de feu détectés (NASA)',
                'type': 'json',
                'organization': 'NASA'
            },
            'nasa_solar_flares': {
                'url': 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR/2023-01-01/2023-12-31',
                'description': 'Solar flares (NASA DONKI)',
                'type': 'json',
                'organization': 'NASA'
            },
            
            # NOAA (Océanique et Atmosphérique)
            'noaa_global_temp': {
                'url': 'https://www.ncei.noaa.gov/data/global-summary-of-the-month/access/2023/',
                'description': 'Global monthly temperatures (NOAA)',
                'type': 'csv',
                'organization': 'NOAA'
            },
            'noaa_sea_ice': {
                'url': 'https://seaice.uni-bremen.de/data/amsr2/asi_daygrid_swath/n6250/2023/',
                'description': 'Étendue de la banquise arctique (NOAA)',
                'type': 'binary',
                'organization': 'NOAA'
            },
            
            # CERN
            'cern_lhc_luminosity': {
                'url': 'https://acc-stats.web.cern.ch/acc-stats/',
                'description': 'Luminosité du LHC (CERN)',
                'type': 'json',
                'organization': 'CERN'
            },
            
            # ArXiv (Publications scientifiques)
            'arxiv_ai_papers': {
                'url': 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1000&sortBy=submittedDate&sortOrder=descending',
                'description': 'Publications IA récentes (ArXiv)',
                'type': 'xml',
                'organization': 'ArXiv'
            },
            'arxiv_physics_papers': {
                'url': 'http://export.arxiv.org/api/query?search_query=cat:physics&max_results=1000&sortBy=submittedDate&sortOrder=descending',
                'description': 'Publications physique récentes (ArXiv)',
                'type': 'xml',
                'organization': 'ArXiv'
            }
        }
    
    @staticmethod
    def _get_economic_sources() -> Dict[str, Dict]:
        """Economic and financial sources."""
        return {
            # Banque Mondiale
            'wb_gdp_per_capita': {
                'url': 'https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&date=2000:2023',
                'description': 'Global GDP per capita (World Bank)',
                'type': 'json',
                'organization': 'World Bank'
            },
            'wb_urban_population': {
                'url': 'https://api.worldbank.org/v2/country/all/indicator/SP.URB.TOTL.IN.ZS?format=json&date=2000:2023',
                'description': 'Population urbaine par pays (Banque Mondiale)',
                'type': 'json',
                'organization': 'World Bank'
            },
            'wb_internet_penetration': {
                'url': 'https://api.worldbank.org/v2/country/all/indicator/IT.NET.USER.ZS?format=json&date=2000:2023',
                'description': 'Pénétration Internet par pays (Banque Mondiale)',
                'type': 'json',
                'organization': 'World Bank'
            },
            
            # FMI
            'imf_global_reserves': {
                'url': 'http://dataservices.imf.org/REST/SDMX_JSON.svc/GetData/IFS/A.USD.TFAA_XDC_USD_RATE..?startPeriod=2000&endPeriod=2023',
                'description': 'Réserves mondiales de change (FMI)',
                'type': 'json',
                'organization': 'IMF'
            },
            
            # Cryptomonnaies
            'crypto_bitcoin_price': {
                'url': 'https://api.coindesk.com/v1/bpi/historical/close.json?start=2023-01-01&end=2023-12-31',
                'description': 'Historical Bitcoin price (CoinDesk)',
                'type': 'json',
                'organization': 'CoinDesk'
            },
            'crypto_market_fear_greed': {
                'url': 'https://api.alternative.me/fng/?limit=365&format=json',
                'description': 'Indice Fear & Greed crypto (Alternative.me)',
                'type': 'json',
                'organization': 'Alternative.me'
            },
            
            # Bourse
            'yahoo_sp500': {
                'url': 'https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=1y&interval=1d',
                'description': 'S&P 500 evolution (Yahoo Finance)',
                'type': 'json',
                'organization': 'Yahoo Finance'
            }
        }
    
    @staticmethod
    def _get_social_sources() -> Dict[str, Dict]:
        """Sources sociales et culturelles."""
        return {
            # Wikipedia
            'wiki_fr_pageviews': {
                'url': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/fr.wikipedia/all-access/all-agents/daily/20230101/20231231',
                'description': 'French Wikipedia page views (Wikimedia)',
                'type': 'json',
                'organization': 'Wikimedia'
            },
            'wiki_global_edits': {
                'url': 'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/all-wikipedia/all-editor-types/daily/20230101/20231231',
                'description': 'Modifications Wikipedia globales (Wikimedia)',
                'type': 'json',
                'organization': 'Wikimedia'
            },
            
            # GitHub
            'github_python_repos': {
                'url': 'https://api.github.com/search/repositories?q=language:python+created:2023-01-01..2023-12-31&sort=stars&order=desc',
                'description': 'Nouveaux dépôts Python (GitHub)',
                'type': 'json',
                'organization': 'GitHub'
            },
            'github_trending_topics': {
                'url': 'https://api.github.com/search/repositories?q=created:2023-01-01..2023-12-31&sort=stars&order=desc',
                'description': 'Dépôts tendance (GitHub)',
                'type': 'json',
                'organization': 'GitHub'
            },
            
            # Reddit (via APIs publiques)
            'reddit_programming': {
                'url': 'https://www.reddit.com/r/programming/hot.json?limit=100',
                'description': 'Posts populaires r/programming (Reddit)',
                'type': 'json',
                'organization': 'Reddit'
            }
        }
    
    @staticmethod
    def _get_environmental_sources() -> Dict[str, Dict]:
        """Sources environnementales."""
        return {
            # USGS (Géologie)
            'usgs_earthquakes_real_time': {
                'url': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv',
                'description': 'Real-time earthquakes (USGS)',
                'type': 'csv',
                'organization': 'USGS'
            },
            'usgs_water_levels': {
                'url': 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00065&period=P30D',
                'description': 'Niveaux d\'eau rivières US (USGS)',
                'type': 'json',
                'organization': 'USGS'
            },
            
            # Qualité de l'air
            'openaq_air_quality': {
                'url': 'https://api.openaq.org/v2/measurements?limit=1000&order_by=datetime&sort=desc',
                'description': 'Global air quality (OpenAQ)',
                'type': 'json',
                'organization': 'OpenAQ'
            },
            
            # Volcans
            'volcano_activity': {
                'url': 'https://volcano.si.edu/api/v1/volcanoes',
                'description': 'Activité volcanique mondiale (Smithsonian)',
                'type': 'json',
                'organization': 'Smithsonian'
            }
        }
    
    @staticmethod
    def _get_tech_sources() -> Dict[str, Dict]:
        """Sources technologiques."""
        return {
            # Internet et domaines
            'internet_domains_new': {
                'url': 'https://www.verisign.com/en_US/channel-resources/domain-registry-products/zone-file/index.xhtml',
                'description': 'Nouveaux domaines .com/.net (Verisign)',
                'type': 'csv',
                'organization': 'Verisign'
            },
            
            # Satellites
            'satellite_launches': {
                'url': 'https://ll.thespacedevs.com/2.2.0/launch/?format=json&limit=100&ordering=-net',
                'description': 'Lancements de satellites récents (SpaceDev)',
                'type': 'json',
                'organization': 'SpaceDev'
            },
            
            # OpenStreetMap
            'osm_global_edits': {
                'url': 'https://osmstats.neis-one.org/api/statistics',
                'description': 'Modifications OpenStreetMap globales',
                'type': 'json',
                'organization': 'OpenStreetMap'
            }
        }
    
    @staticmethod
    def get_sources_by_category(category: str) -> Dict[str, Dict]:
        """Retourne les sources d'une catégorie spécifique."""
        category_methods = {
            'government': DataSourcesRegistry._get_government_sources,
            'scientific': DataSourcesRegistry._get_scientific_sources,
            'economic': DataSourcesRegistry._get_economic_sources,
            'social': DataSourcesRegistry._get_social_sources,
            'environmental': DataSourcesRegistry._get_environmental_sources,
            'tech': DataSourcesRegistry._get_tech_sources
        }
        
        if category in category_methods:
            return category_methods[category]()
        else:
            return {}
    
    @staticmethod
    def get_sources_count() -> int:
        """Retourne le nombre total de sources disponibles."""
        return len(DataSourcesRegistry.get_all_sources())
    
    @staticmethod
    def get_categories() -> List[str]:
        """Retourne la liste des catégories disponibles."""
        return ['government', 'scientific', 'economic', 'social', 'environmental', 'tech'] 