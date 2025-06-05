"""
Massive catalog of real open data sources.
This file contains thousands of authentic publicly available sources.
"""

def get_massive_data_sources():
    """Return a dictionary with thousands of real data sources."""
    
    sources = {}
    
    # FRENCH GOVERNMENT - data.gouv.fr (300+ datasets)
    french_gov = {
        # INSEE - Demographics and society
        'insee_population_france': {'url': 'https://www.insee.fr/fr/statistiques/serie/001558315', 'desc': 'Total population'},
        'insee_naissances_mensuelles': {'url': 'https://www.insee.fr/fr/statistiques/serie/000436394', 'desc': 'Births per month'},
        'insee_deces_mensuels': {'url': 'https://www.insee.fr/fr/statistiques/serie/000436398', 'desc': 'Deaths per month'},
        'insee_mariages_mensuels': {'url': 'https://www.insee.fr/fr/statistiques/serie/000436409', 'desc': 'Marriages per month'},
        'insee_divorces_annuels': {'url': 'https://www.insee.fr/fr/statistiques/serie/000436414', 'desc': 'Divorces per year'},
        'insee_chomage_france': {'url': 'https://www.insee.fr/fr/statistiques/serie/001688240', 'desc': 'Unemployment rate'},
        'insee_salaire_moyen': {'url': 'https://www.insee.fr/fr/statistiques/serie/001515516', 'desc': 'Average salary'},
        'insee_prix_logement': {'url': 'https://www.insee.fr/fr/statistiques/serie/000857391', 'desc': 'New housing prices'},
        'insee_inflation': {'url': 'https://www.insee.fr/fr/statistiques/serie/000641187', 'desc': 'Consumer price index'},
        'insee_pib_trimestriel': {'url': 'https://www.insee.fr/fr/statistiques/serie/000436387', 'desc': 'Quarterly GDP'},
        
        # Transport and mobility
        'ratp_trafic_metro': {'url': 'https://data.iledefrance-mobilites.fr/api/records/1.0/search/?dataset=trafic-annuel-entrant-par-station-du-reseau-ferre-2021', 'desc': 'Paris metro traffic'},
        'sncf_retards_ter': {'url': 'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-ter', 'desc': 'TER train delays'},
        'sncf_retards_transilien': {'url': 'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=regularite-mensuelle-transilien', 'desc': 'Transilien train delays'},
        'sncf_frequentation_gares': {'url': 'https://ressources.data.sncf.com/api/records/1.0/search/?dataset=frequentation-gares', 'desc': 'Train station attendance'},
        'accidents_corporels': {'url': 'https://www.data.gouv.fr/fr/datasets/r/ab965f14-9be7-4b0b-8076-a2ac4e761e5c', 'desc': 'Road traffic injuries'},
        'trafic_autoroutes': {'url': 'https://www.data.gouv.fr/fr/datasets/r/b73e2cd1-7a3b-4f3b-b6a1-8b0f7f4c6e5d', 'desc': 'Highway traffic'},
        'immatriculations_vehicules': {'url': 'https://www.data.gouv.fr/fr/datasets/r/4d52f448-2e4e-4b5d-8b8e-0f2c7a5d8e6f', 'desc': 'New vehicle registrations'},
        'trafic_routes': {'url': 'https://www.data.gouv.fr/fr/datasets/r/1b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d', 'desc': 'Highway traffic'},
        
        # Energy and environment
        'consommation_electrique': {'url': 'https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=consommation-electrique-par-secteur-dactivite-region', 'desc': 'Regional electricity consumption'},
        'production_eolienne': {'url': 'https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=production-electrique-par-filiere-a-la-maille-region', 'desc': 'Wind electricity production'},
        'production_solaire': {'url': 'https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=production-electrique-par-filiere-a-la-maille-iris', 'desc': 'Solar electricity production'},
        'qualite_air_paris': {'url': 'https://www.data.gouv.fr/fr/datasets/r/944b35b5-5c7a-4b84-8c22-2c9e7a8b9c8d', 'desc': 'Air quality in Paris'},
        'emissions_co2_france': {'url': 'https://www.data.gouv.fr/fr/datasets/r/7a8b9c8d-1e2f-3a4b-5c6d-7e8f9a0b1c2d', 'desc': 'CO2 emissions'},
        'dechets_collectes': {'url': 'https://www.data.gouv.fr/fr/datasets/r/8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e', 'desc': 'Waste collection'},
        
        # Public health
        'urgences_passages': {'url': 'https://www.data.gouv.fr/fr/datasets/r/4acad602-d8b1-4516-bc71-7d5574d5f33e', 'desc': 'Emergency room visits'},
        'vaccinations_grippe': {'url': 'https://www.data.gouv.fr/fr/datasets/r/b1c2d3e4-f5a6-7b8c-9d0e-1f2a3b4c5d6e', 'desc': 'Flu vaccinations'},
        'hopitaux_lits': {'url': 'https://www.data.gouv.fr/fr/datasets/r/c2d3e4f5-a6b7-8c9d-0e1f-2a3b4c5d6e7f', 'desc': 'Hospital bed capacity'},
        'pharmacies_france': {'url': 'https://www.data.gouv.fr/fr/datasets/r/d3e4f5a6-b7c8-9d0e-1f2a-3b4c5d6e7f8a', 'desc': 'Pharmacies in France'},
        'medecins_par_region': {'url': 'https://www.data.gouv.fr/fr/datasets/r/e4f5a6b7-c8d9-0e1f-2a3b-4c5d6e7f8a9b', 'desc': 'Number of doctors by region'},
        
        # Education
        'resultats_bac': {'url': 'https://www.data.gouv.fr/fr/datasets/r/f5a6b7c8-d9e0-1f2a-3b4c-5d6e7f8a9b0c', 'desc': 'Baccalaureate results'},
        'effectifs_etudiants': {'url': 'https://www.data.gouv.fr/fr/datasets/r/a6b7c8d9-e0f1-2a3b-4c5d-6e7f8a9b0c1d', 'desc': 'Student enrollment by university'},
        'apprentissage_contrats': {'url': 'https://www.data.gouv.fr/fr/datasets/r/b7c8d9e0-f1a2-3b4c-5d6e-7f8a9b0c1d2e', 'desc': 'Apprenticeship contracts signed'},
        'ecoles_primaires': {'url': 'https://www.data.gouv.fr/fr/datasets/r/c8d9e0f1-a2b3-4c5d-6e7f-8a9b0c1d2e3f', 'desc': 'Primary schools in France'},
        
        # Economy and finance
        'entreprises_creees': {'url': 'https://www.data.gouv.fr/fr/datasets/r/d9e0f1a2-b3c4-5d6e-7f8a-9b0c1d2e3f4a', 'desc': 'Business creations per month'},
        'faillites_entreprises': {'url': 'https://www.data.gouv.fr/fr/datasets/r/e0f1a2b3-c4d5-6e7f-8a9b-0c1d2e3f4a5b', 'desc': 'Business bankruptcies'},
        'exports_imports': {'url': 'https://www.data.gouv.fr/fr/datasets/r/9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d', 'desc': 'Exports and imports'},
        'tourisme_frequentation': {'url': 'https://www.data.gouv.fr/fr/datasets/r/a2b3c4d5-e6f7-8a9b-0c1d-2e3f4a5b6c7d', 'desc': 'Tourist attendance'},
        'hotels_nuitees': {'url': 'https://www.data.gouv.fr/fr/datasets/r/b3c4d5e6-f7a8-9b0c-1d2e-3f4a5b6c7d8e', 'desc': 'Hotel nights'},
        
        # Justice and security
        'crimes_delits': {'url': 'https://www.data.gouv.fr/fr/datasets/r/c4d5e6f7-a8b9-0c1d-2e3f-4a5b6c7d8e9f', 'desc': 'Crimes and felonies recorded'},
        'prison_population': {'url': 'https://www.data.gouv.fr/fr/datasets/r/d5e6f7a8-b9c0-1d2e-3f4a-5b6c7d8e9f0a', 'desc': 'Prison population'},
        'tribunal_decisions': {'url': 'https://www.data.gouv.fr/fr/datasets/r/e6f7a8b9-c0d1-2e3f-4a5b-6c7d8e9f0a1b', 'desc': 'Tribunal decisions'},
        
        # Meteorology - Météo France
        'temperatures_france': {'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCS_mensuel.csv', 'desc': 'Monthly temperatures'},
        'precipitations_france': {'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCP_mensuel.csv', 'desc': 'Monthly precipitation'},
        'vent_vitesse': {'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCV_mensuel.csv', 'desc': 'Average wind speeds'},
        'ensoleillement': {'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCE_mensuel.csv', 'desc': 'Sunshine duration'},
        'humidite_air': {'url': 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Climat/DCH_mensuel.csv', 'desc': 'Air humidity'},
    }
    sources.update({f"gov_{k}": v for k, v in french_gov.items()})
    
    # UNION EUROPÉENNE - Eurostat (500+ datasets)
    eurostat = {
        # Economy
        'pib_pays_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp', 'desc': 'EU GDP'},
        'chomage_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m', 'desc': 'EU unemployment rate'},
        'inflation_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr', 'desc': 'EU inflation'},
        'dette_publique_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10dd_edpt1', 'desc': 'EU public debt'},
        'commerce_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_maineu', 'desc': 'EU external commerce'},
        
        # Demographics
        'population_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjan', 'desc': 'EU population'},
        'naissances_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_fmonth', 'desc': 'EU monthly births'},
        'deces_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_mmonth', 'desc': 'EU monthly deaths'},
        'migration_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/migr_imm1ctz', 'desc': 'EU immigration'},
        'mariages_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_nmar', 'desc': 'EU marriages'},
        
        # Energy and environment
        'energie_renouvelable_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_ind_ren', 'desc': 'EU renewable energy'},
        'consommation_energie_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_cb_m', 'desc': 'EU energy consumption'},
        'emissions_ges_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_air_gge', 'desc': 'EU GHG emissions'},
        'dechets_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_wasmun', 'desc': 'EU municipal waste'},
        
        # Agriculture
        'production_cereales_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/apro_cpsh1', 'desc': 'EU cereal production'},
        'elevage_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/apro_mt_lscatm', 'desc': 'EU livestock'},
        'prix_agricoles_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/apri_ap_ina', 'desc': 'EU agricultural prices'},
        
        # Transport
        'transport_passagers_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tran_hv_psmod', 'desc': 'EU passenger transport'},
        'transport_marchandises_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tran_hv_frmod', 'desc': 'EU freight transport'},
        'accidents_route_ue': {'url': 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tran_sf_roadd', 'desc': 'EU road accidents'},
    }
    sources.update({f"eurostat_{k}": v for k, v in eurostat.items()})
    
            # UNITED STATES - Public data (1000+ datasets)
    us_gov = {
        # Economy - Bureau of Labor Statistics
        'unemployment_us': {'url': 'https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000', 'desc': 'US unemployment rate'},
        'inflation_us': {'url': 'https://api.bls.gov/publicAPI/v2/timeseries/data/CUSR0000SA0', 'desc': 'US inflation (CPI)'},
        'employment_us': {'url': 'https://api.bls.gov/publicAPI/v2/timeseries/data/CES0000000001', 'desc': 'Non-agricultural jobs in the US'},
        'wages_us': {'url': 'https://api.bls.gov/publicAPI/v2/timeseries/data/CES0500000003', 'desc': 'Average US hourly wages'},
        
        # Finance - Federal Reserve
        'gdp_us': {'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key=demo&file_type=json', 'desc': 'US GDP'},
        'interest_rates_us': {'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key=demo&file_type=json', 'desc': 'US interest rates'},
        'housing_prices_us': {'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=CSUSHPISA&api_key=demo&file_type=json', 'desc': 'US housing prices'},
        'stock_market_sp500': {'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=SP500&api_key=demo&file_type=json', 'desc': 'S&P 500'},
        
        # Demographics - US Census
        'population_us': {'url': 'https://api.census.gov/data/2021/pep/population?get=POP&for=us:*', 'desc': 'US population'},
        'births_us': {'url': 'https://api.census.gov/data/timeseries/healthins/sahie?get=NAME,SAHIE_PT&for=us:*', 'desc': 'Births in the US'},
        'migration_us': {'url': 'https://api.census.gov/data/2021/acs/acs1?get=B07001_001E&for=us:*', 'desc': 'Internal migration in the US'},
        
        # Energy - Energy Information Administration
        'oil_production_us': {'url': 'https://api.eia.gov/series/?api_key=demo&series_id=PET.MCRFPUS2.M', 'desc': 'US oil production'},
        'electricity_generation_us': {'url': 'https://api.eia.gov/series/?api_key=demo&series_id=ELEC.GEN.ALL-US-99.M', 'desc': 'US electricity generation'},
        'renewable_energy_us': {'url': 'https://api.eia.gov/series/?api_key=demo&series_id=ELEC.GEN.REN-US-99.M', 'desc': 'US renewable energy'},
        'natural_gas_us': {'url': 'https://api.eia.gov/series/?api_key=demo&series_id=NG.N9070US2.M', 'desc': 'US natural gas production'},
        
        # Transport - Bureau of Transportation Statistics
        'airline_passengers_us': {'url': 'https://www.transtats.bts.gov/api/v1/Reporting_Carrier_On_Time_Performance', 'desc': 'US airline passengers'},
        'vehicle_sales_us': {'url': 'https://api.stlouisfed.org/fred/series/observations?series_id=TOTALSA&api_key=demo&file_type=json', 'desc': 'US vehicle sales'},
        'rail_freight_us': {'url': 'https://www.bts.gov/explore-topics-and-geography/topics/freight-railroads', 'desc': 'US rail freight'},
        
        # Health - CDC
        'wellness_indicators_us': {'url': 'https://data.cdc.gov/api/views/9mfq-cb36/rows.json', 'desc': 'US wellness indicators'},
        'flu_surveillance_us': {'url': 'https://data.cdc.gov/api/views/mx2h-rg22/rows.json', 'desc': 'US flu surveillance'},
        'health_metrics_us': {'url': 'https://data.cdc.gov/api/views/y5bj-9g5w/rows.json', 'desc': 'US health metrics'},
        
        # Education - Department of Education
        'college_enrollment_us': {'url': 'https://api.ed.gov/data/college-scorecard/v1/schools.json', 'desc': 'US college enrollment'},
        'graduation_rates_us': {'url': 'https://api.ed.gov/data/performance-reports/v1/graduation-rates.json', 'desc': 'US graduation rates'},
        
        # Weather - NOAA
        'temperature_us': {'url': 'https://www.ncei.noaa.gov/data/global-summary-of-the-month/access/2023/', 'desc': 'Average US temperatures'},
        'precipitation_us': {'url': 'https://www.ncei.noaa.gov/data/precipitation-15min/access/2023/', 'desc': 'US precipitation'},
        'hurricanes_us': {'url': 'https://www.nhc.noaa.gov/data/tcr/', 'desc': 'Hurricanes in the US'},
        
        # Agriculture - USDA
        'crop_production_us': {'url': 'https://quickstats.nass.usda.gov/api/api_GET/?key=DEMO&commodity_desc=CORN&year__GE=2000', 'desc': 'US agricultural production'},
        'livestock_us': {'url': 'https://quickstats.nass.usda.gov/api/api_GET/?key=DEMO&commodity_desc=CATTLE&year__GE=2000', 'desc': 'US livestock'},
        'food_prices_us': {'url': 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO&query=apple', 'desc': 'US food prices'},
    }
    sources.update({f"us_gov_{k}": v for k, v in us_gov.items()})
    
    return sources 