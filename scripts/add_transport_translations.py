import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Ajoute les traductions manquantes pour transport et mobilité urbaine."""
    
    # Chemin vers le fichier de traductions
    translations_file = Path("data/pretranslated_datasets.json")
    
    if not translations_file.exists():
        print("❌ Fichier pretranslated_datasets.json non trouvé")
        return
    
    # Charger le fichier existant
    with open(translations_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 État actuel: {len(data['translations'])} traductions")
    
    # Nouvelles traductions transport intelligent et mobilité urbaine
    smart_mobility_translations = {
        "Multimodal Journey Planning": "Planification de Trajets Multimodaux",
        "Connected Vehicle Data": "Données de Véhicules Connectés",
        "Traffic Light Optimization": "Optimisation des Feux de Circulation",
        "Parking Availability Sensors": "Capteurs de Disponibilité de Stationnement",
        "Air Quality Transport": "Qualité de l'Air Transport",
        "Carbon Footprint Commuting": "Empreinte Carbone des Déplacements",
        "Travel Times By City": "Temps de Trajet par Ville",
        "Speed Patterns Traffic": "Modèles de Vitesse du Trafic",
        "Origin Destination Flows": "Flux Origine-Destination",
        "Traffic Congestion Index": "Indice de Congestion du Trafic",
        "Ride Demand Patterns": "Modèles de Demande de Courses",
        "Surge Pricing Analysis": "Analyse des Prix Dynamiques",
        "Driver Earnings Trends": "Tendances des Revenus des Conducteurs",
        "Passenger Safety Metrics": "Indicateurs de Sécurité des Passagers"
    }
    
    # Traductions pour les données de vélos partagés
    bike_sharing_translations = {
        "Station Information": "Informations des Stations",
        "Station Status Realtime": "État des Stations en Temps Réel", 
        "Trip Data Monthly": "Données de Trajets Mensuelles",
        "Bike Availability Patterns": "Modèles de Disponibilité des Vélos",
        "Usage Demographics": "Démographie d'Utilisation",
        "Seasonal Ridership Trends": "Tendances Saisonnières de Fréquentation",
        "Docking Station Optimization": "Optimisation des Stations d'Accueil",
        "Bike Maintenance Schedules": "Calendriers de Maintenance des Vélos"
    }
    
    # Données d'aviation avancées
    aviation_advanced_translations = {
        "Live Flights Tracking": "Suivi des Vols en Direct",
        "Airport Delays Analysis": "Analyse des Retards d'Aéroports",
        "Route Statistics Global": "Statistiques de Routes Mondiales",
        "Aircraft Movements": "Mouvements d'Aéronefs",
        "Airline Performance Metrics": "Indicateurs de Performance des Compagnies",
        "Flight Cancellation Rates": "Taux d'Annulation des Vols"
    }
    
    # Transport ferroviaire français avancé
    french_rail_advanced_translations = {
        "French Regional Train Punctuality": "Ponctualité des Trains Régionaux Français",
        "French Railway Station Usage": "Utilisation des Gares Ferroviaires Françaises",
        "French Train Station Attendance": "Fréquentation des Gares Françaises",
        "Paris Metro Station Traffic": "Trafic des Stations de Métro Parisien",
        "Paris Metro Station Accessibility": "Accessibilité des Stations de Métro Parisien"
    }
    
    # Combiner toutes les nouvelles traductions
    new_translations = {}
    new_translations.update(smart_mobility_translations)
    new_translations.update(bike_sharing_translations)
    new_translations.update(aviation_advanced_translations)
    new_translations.update(french_rail_advanced_translations)
    
    print(f"🚗 Ajout de {len(smart_mobility_translations)} traductions mobilité intelligente")
    print(f"🚲 Ajout de {len(bike_sharing_translations)} traductions vélos partagés")
    print(f"✈️ Ajout de {len(aviation_advanced_translations)} traductions aviation avancées")
    print(f"🚆 Ajout de {len(french_rail_advanced_translations)} traductions ferroviaires françaises")
    
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
    data['metadata']['transport_datasets_added'] = translations_added
    data['metadata']['last_transport_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['metadata']['version'] = "3.2"
    
    # Sauvegarder le fichier
    with open(translations_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Résumé:")
    print(f"📊 Nouvelles traductions ajoutées: {translations_added}")
    print(f"📈 Total de traductions: {len(data['translations'])}")
    print(f"💾 Fichier mis à jour: {translations_file}")
    print(f"🆕 Version: 3.2")

if __name__ == "__main__":
    main() 