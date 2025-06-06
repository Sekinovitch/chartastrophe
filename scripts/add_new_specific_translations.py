#!/usr/bin/env python3
"""
Ajoute les nouvelles traductions spécifiques pour les datasets améliorés.
"""


import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ajouter le dossier racine au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

def main():
    """Ajoute toutes les nouvelles traductions spécifiques."""
    
    # Chemin vers le fichier de traductions
    translations_file = Path("data/pretranslated_datasets.json")
    
    if not translations_file.exists():
        print("❌ Fichier pretranslated_datasets.json non trouvé")
        return
    
    # Charger le fichier existant
    with open(translations_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Nouvelles traductions spécifiques à ajouter
    new_translations = {
        # Tesla et véhicules électriques
        "Tesla Supercharger Network Expansion (USA)": "Expansion du réseau de superchargeurs Tesla (États-Unis)",
        "Tesla Supercharger Station Utilization Rates": "Taux d'utilisation des stations de superchargeurs Tesla",
        "Tesla Model S Adoption Rates (California)": "Taux d'adoption de la Tesla Model S (Californie)",
        "Tesla Supercharger Session Duration (Minutes)": "Durée des sessions de superchargeur Tesla (minutes)",
        "Tesla Solar-Powered Charging Stations": "Stations de recharge Tesla alimentées par l'énergie solaire",
        "Tesla Supercharger Electricity Costs (kWh)": "Coûts d'électricité des superchargeurs Tesla (kWh)",
        
        # Énergie - IEA
        "Global Fossil Fuel Consumption (Gigawatts)": "Consommation mondiale de combustibles fossiles (gigawatts)",
        "European Solar Panel Capacity (Megawatts)": "Capacité européenne de panneaux solaires (mégawatts)",
        "US Household Energy Efficiency Ratings": "Classements d'efficacité énergétique des ménages américains",
        "Coal vs Wind Carbon Emissions (Tons)": "Émissions de carbone charbon vs éolien (tonnes)",
        "Nuclear vs Solar Power Generation (France)": "Production d'énergie nucléaire vs solaire (France)",
        "Rural Energy Access (Sub-Saharan Africa)": "Accès à l'énergie rurale (Afrique subsaharienne)",
        "OPEC Crude Oil Prices (per Barrel)": "Prix du pétrole brut de l'OPEP (par baril)",
        "Household Natural Gas Heating Consumption": "Consommation de gaz naturel pour le chauffage domestique",
        "German Coal Power Plant Closures": "Fermetures de centrales électriques au charbon en Allemagne",
        "Lithium Battery Mineral Demand": "Demande de minéraux pour batteries au lithium",
        
        # Énergie renouvelable - IRENA
        "Danish Wind Farm Capacity (Gigawatts)": "Capacité des parcs éoliens danois (gigawatts)",
        "California Solar Panel Installer Jobs": "Emplois d'installateurs de panneaux solaires en Californie",
        "Offshore Wind Construction Costs (Billions)": "Coûts de construction éolienne offshore (milliards)",
        "Kenyan Village Solar Microgrid Projects": "Projets de micro-réseaux solaires villageois kenyans",
        "Government Renewable Energy Subsidies (Millions)": "Subventions gouvernementales pour les énergies renouvelables (millions)",
        "Japanese Green Hydrogen Fuel Cell Potential": "Potentiel japonais de piles à combustible à hydrogène vert",
        
        # Transport US
        "Delta Airlines Flight Delays (Minutes, Atlanta)": "Retards de vols Delta Airlines (minutes, Atlanta)",
        "Amazon Delivery Truck Miles (California)": "Kilomètres de camions de livraison Amazon (Californie)",
        "Interstate Highway Traffic (Cars/Hour, Texas)": "Trafic autoroutier inter-états (voitures/heure, Texas)",
        "NYC Subway Ridership (Million Passengers)": "Fréquentation du métro de New York (millions de passagers)",
        "Central Park Daily Bicycle Riders": "Cyclistes quotidiens de Central Park",
        "Los Angeles Port Container Ship Traffic": "Trafic de porte-conteneurs du port de Los Angeles",
        "Chicago Freight Train Cargo (Tons)": "Fret ferroviaire de Chicago (tonnes)",
        "Highway Speed Limit vs Accident Rates": "Limites de vitesse autoroutières vs taux d'accidents",
        "Tesla Model 3 Registrations (Florida)": "Immatriculations Tesla Model 3 (Floride)",
        "Uber Ride Requests (San Francisco)": "Demandes de courses Uber (San Francisco)",
        "Waymo Self-Driving Test Miles (Arizona)": "Kilomètres de tests de conduite autonome Waymo (Arizona)",
        "Scooter Sharing Trips (Washington DC)": "Trajets de trottinettes partagées (Washington DC)",
        
        # Santé - CDC et WHO
        "Tobacco Use Prevention (USA)": "Prévention de l'usage du tabac (États-Unis)",
        "Chronic Disease Indicators (USA)": "Indicateurs de maladies chroniques (États-Unis)",
        "Environmental Health Tracking (USA)": "Suivi de la santé environnementale (États-Unis)",
        "Foodborne Illness Outbreaks (USA)": "Épidémies de maladies d'origine alimentaire (États-Unis)",
        "Injury Violence Prevention (USA)": "Prévention des blessures et de la violence (États-Unis)",
        "Maternal Infant Health (USA)": "Santé maternelle et infantile (États-Unis)",
        "Occupational Health Safety (USA)": "Sécurité et santé au travail (États-Unis)",
        "Reproductive Health Data (USA)": "Données de santé reproductive (États-Unis)",
        
        # Santé mentale
        "Mental Illness Prevalence": "Prévalence des maladies mentales",
        "Suicide Statistics": "Statistiques de suicide",
        "Treatment Utilization": "Utilisation des traitements",
        "Mental Health Workforce": "Personnel de santé mentale",
        "Research Funding Trends": "Tendances de financement de la recherche",
        "Digital Mental Health": "Santé mentale numérique",
        
        # Technologie et innovation
        "Programming Language Trends": "Tendances des langages de programmation",
        "Open Source Contributions": "Contributions open source",
        "Developer Activity Patterns": "Modèles d'activité des développeurs",
        "Repository Growth Rates": "Taux de croissance des dépôts",
        "Code Collaboration Networks": "Réseaux de collaboration de code",
        "Security Vulnerability Reports": "Rapports de vulnérabilités de sécurité",
        
        # Brevets et innovation
        "Patent Applications By Field": "Demandes de brevets par domaine",
        "Innovation Indicators": "Indicateurs d'innovation",
        "Technology Transfer Data": "Données de transfert de technologie",
        "Startup Patent Filings": "Dépôts de brevets de startups",
        "AI Related Patents": "Brevets liés à l'IA",
        "Green Technology Patents": "Brevets de technologies vertes",
        
        # Recherches Google spécifiques
        "Pizza Delivery Near Me Searches": "Recherches de livraison de pizza à proximité",
        "Bitcoin Price Panic Searches": "Recherches de panique sur le prix du Bitcoin",
        "Weather App Downloads Rainy Days": "Téléchargements d'applications météo les jours de pluie",
        "Netflix Password Sharing Searches": "Recherches de partage de mot de passe Netflix",
        "Spotify Wrapped December Searches": "Recherches Spotify Wrapped en décembre",
        "Amazon Prime Day Deal Searches": "Recherches d'offres Amazon Prime Day",
        "Voting Booth Locations Election Day": "Recherches de bureaux de vote le jour des élections",
        "Olympic Medal Count Searches": "Recherches de décompte de médailles olympiques",
        "Christmas Gift Ideas Last Minute": "Recherches d'idées cadeaux de Noël de dernière minute",
        "Coffee Shop Hours Monday Morning": "Recherches d'horaires de cafés le lundi matin",
        "Cat Videos YouTube Searches": "Recherches de vidéos de chats sur YouTube",
        "Dog Adoption Weekend Searches": "Recherches d'adoption de chiens le week-end",
        "TikTok Dance Tutorial Searches": "Recherches de tutoriels de danse TikTok",
        "Minecraft Server Setup Searches": "Recherches de configuration de serveur Minecraft",
        "ChatGPT Homework Help Searches": "Recherches d'aide aux devoirs ChatGPT",
        "Artificial Intelligence Job Replacement Fears": "Craintes de remplacement d'emplois par l'intelligence artificielle",
        "Climate Change Anxiety Searches": "Recherches d'anxiété liée au changement climatique",
        "Electric Car Charging Stations Map Searches": "Recherches de cartes de stations de recharge de voitures électriques",
        "NFT Art Investment Regret Searches": "Recherches de regrets d'investissement dans l'art NFT",
        "Crypto Wallet Password Recovery Searches": "Recherches de récupération de mot de passe de portefeuille crypto",
        "Metaverse Headset Motion Sickness Searches": "Recherches de mal des transports avec casques métavers",
        "Sustainable Clothing Brands Searches": "Recherches de marques de vêtements durables",
        "Plant Based Burger Taste Test Searches": "Recherches de tests de goût de hamburgers végétaux",
        "Carbon Footprint Calculator Personal Searches": "Recherches de calculateurs d'empreinte carbone personnelle",
        "Mars Mission Application NASA Searches": "Recherches de candidatures pour missions Mars NASA",
        "Self Driving Car Accident News Searches": "Recherches d'actualités d'accidents de voitures autonomes",
        "Quantum Computer vs Laptop Speed Searches": "Recherches de vitesse ordinateur quantique vs portable",
        "CRISPR Gene Editing Ethics Debate Searches": "Recherches de débats éthiques sur l'édition génique CRISPR",
        "Solar Panel Installation Cost Calculator Searches": "Recherches de calculateurs de coûts d'installation de panneaux solaires",
        "Therapy Appointment Booking Searches": "Recherches de réservation de rendez-vous thérapeutiques",
        "Work From Home Productivity Tips Searches": "Recherches de conseils de productivité en télétravail",
        "Digital Detox App Recommendations Searches": "Recherches de recommandations d'applications de détox numérique",
        "Freelance Tax Deduction Guide Searches": "Recherches de guides de déductions fiscales pour freelances",
        "Universal Basic Income Pilot Program Searches": "Recherches de programmes pilotes de revenu universel de base",
        "Lab Grown Meat Grocery Store Availability Searches": "Recherches de disponibilité de viande cultivée en épicerie",
        "Vertical Garden Apartment Balcony Searches": "Recherches de jardins verticaux pour balcons d'appartement",
        "Ocean Plastic Cleanup Donation Searches": "Recherches de dons pour le nettoyage du plastique océanique",
        "Space Tourism Ticket Prices Searches": "Recherches de prix de billets de tourisme spatial",
        "Brain Implant Elon Musk Neuralink Searches": "Recherches d'implants cérébraux Elon Musk Neuralink",
        "Anti Aging Supplements Effectiveness Searches": "Recherches d'efficacité des compléments anti-âge",
        "Genetic Testing Privacy Concerns Searches": "Recherches de préoccupations de confidentialité des tests génétiques",
        "Synthetic Biology Safety Regulations Searches": "Recherches de réglementations de sécurité en biologie synthétique",
        "Nuclear Fusion Breakthrough News Searches": "Recherches d'actualités de percées en fusion nucléaire",
        "Cryptocurrency Tax Reporting Searches": "Recherches de déclaration fiscale de cryptomonnaies",
        "Social Media Break Benefits Searches": "Recherches de bénéfices de pauses des réseaux sociaux",
        "VPN Privacy Protection Searches": "Recherches de protection de la vie privée VPN",
        "Inflation Grocery Budget Calculator Searches": "Recherches de calculateurs de budget alimentaire avec inflation",
        "Affordable Housing Lottery Application Searches": "Recherches de candidatures de loterie de logements abordables"
    }
    
    # Nouvelles traductions manquantes (datasets World Bank)
    missing_worldbank_translations = {
        "Total Population by Country": "Population Totale par Pays",
        "Gross Domestic Product by Country (World Bank)": "Produit Intérieur Brut par Pays (Banque Mondiale)", 
        "International Unemployment Rates": "Taux de Chômage Internationaux",
        "CO2 Emissions per Person": "Émissions de CO2 par Personne",
        "Internet Users by Country": "Utilisateurs d'Internet par Pays",
        "Global Infant Mortality Rates": "Taux de Mortalité Infantile Mondial",
        "Adult Literacy Rates": "Taux d'Alphabétisation des Adultes",
        "Electric Power Consumption per Person": "Consommation d'Électricité par Personne",
        "Global Urban Population": "Population Urbaine Mondiale",
        "International Trade (% of GDP)": "Commerce International (% du PIB)",
        "Global Inflation Rates": "Taux d'Inflation Mondiaux",
        "Global GDP per Person": "PIB Mondial par Personne", 
        "Global Life Expectancy": "Espérance de Vie Mondiale",
        "Forest Area by Country": "Superficie Forestière par Pays",
        "Renewable Electricity Production": "Production d'Électricité Renouvelable"
    }
    
    print(f"📋 Ajout de {len(missing_worldbank_translations)} traductions World Bank manquantes...")
    new_translations.update(missing_worldbank_translations)
    
    # Nouvelles traductions manquantes (datasets climatiques NOAA)
    climate_noaa_translations = {
        "Sea Level Rise Measurements": "Mesures de la Montée du Niveau de la Mer",
        "Arctic Ice Extent Decline": "Déclin de l'Étendue de la Glace Arctique",
        "Coral Bleaching Events": "Événements de Blanchissement Corallien",
        "Extreme Weather Frequency": "Fréquence des Phénomènes Météorologiques Extrêmes",
        "Drought Severity Index": "Indice de Sévérité de la Sécheresse",
        "Wildfire Risk Assessment": "Évaluation du Risque d'Incendies de Forêt",
        "Atmospheric CO2 Levels": "Niveaux de CO2 Atmosphérique",
        "Ocean Acidification Data": "Données d'Acidification Océanique",
        "Climate Change Indicators": "Indicateurs du Changement Climatique",
        "Hurricane Intensity Analysis": "Analyse d'Intensité des Ouragans",
        "Global Temperature Anomalies": "Anomalies de Température Mondiale",
        "Global Precipitation Data": "Données de Précipitations Mondiales",
        "Ocean Storm Tracking": "Suivi des Tempêtes Océaniques",
        "Global Ocean Temperature": "Température Océanique Mondiale"
    }
    
    print(f"🌡️ Ajout de {len(climate_noaa_translations)} traductions climatiques NOAA...")
    new_translations.update(climate_noaa_translations)
    
    # Données géologiques USGS manquantes
    geological_usgs_translations = {
        "Global Seismic Activity": "Activité Sismique Mondiale",
        "Major Earthquakes (Magnitude 4.5+)": "Tremblements de Terre Majeurs (Magnitude 4.5+)",
        "Significant Earthquakes": "Tremblements de Terre Significatifs",
        "Global Landslide Events": "Événements de Glissements de Terrain Mondiaux",
        "Volcanic Activity Alerts": "Alertes d'Activité Volcanique",
        "Groundwater Level Monitoring": "Surveillance du Niveau des Eaux Souterraines",
        "Mineral Production Statistics": "Statistiques de Production Minérale",
        "River Streamflow Measurements": "Mesures du Débit des Rivières",
        "Tsunami Warning System Data": "Données du Système d'Alerte Tsunami",
        "Geological Hazards Assessment": "Évaluation des Risques Géologiques"
    }
    
    print(f"🌍 Ajout de {len(geological_usgs_translations)} traductions géologiques USGS...")
    new_translations.update(geological_usgs_translations)
    
    # Ajouter les nouvelles traductions
    translations_added = 0
    for english, french in new_translations.items():
        if english not in data['translations']:
            data['translations'][english] = french
            translations_added += 1
            print(f"✅ Ajouté: {english} → {french}")
        else:
            print(f"⚠️  Déjà présent: {english}")
    
    # Mettre à jour les métadonnées
    data['metadata']['total_translations'] = len(data['translations'])
    data['metadata']['specific_datasets_added'] = translations_added
    data['metadata']['last_specific_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['metadata']['version'] = "3.0"
    
    # Sauvegarder le fichier
    with open(translations_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Résumé:")
    print(f"📊 Nouvelles traductions ajoutées: {translations_added}")
    print(f"📈 Total de traductions: {len(data['translations'])}")
    print(f"💾 Fichier mis à jour: {translations_file}")
    print(f"🆕 Version: 3.0")

if __name__ == "__main__":
    main() 