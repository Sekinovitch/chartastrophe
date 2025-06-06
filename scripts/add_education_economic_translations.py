import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Ajoute les traductions manquantes pour éducation et économie."""
    
    # Chemin vers le fichier de traductions
    translations_file = Path("data/pretranslated_datasets.json")
    
    if not translations_file.exists():
        print("❌ Fichier pretranslated_datasets.json non trouvé")
        return
    
    # Charger le fichier existant
    with open(translations_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 État actuel: {len(data['translations'])} traductions")
    
    # Nouvelles traductions éducatives
    education_translations = {
        "Bilingual Education Outcomes": "Résultats de l'Éducation Bilingue",
        "University Enrollment Data": "Données d'Inscription Universitaire",
        "Higher Education Completion": "Achèvement de l'Enseignement Supérieur",
        "School Performance Data": "Données de Performance Scolaire",
        "Education Performance Data": "Données de Performance Éducative",
        "Education Funding": "Financement de l'Éducation",
        "Education Statistics": "Statistiques d'Éducation",
        "Student Debt Statistics": "Statistiques de la Dette Étudiante",
        "Digital Literacy Rates": "Taux d'Alphabétisation Numérique",
        "Education Excellence Indicators": "Indicateurs d'Excellence Éducative"
    }
    
    # Nouvelles traductions économiques - Réserve Fédérale
    federal_reserve_translations = {
        "Federal Funds Rate": "Taux des Fonds Fédéraux",
        "Treasury 10year Yield": "Rendement du Trésor à 10 ans",
        "Housing Starts": "Mises en Chantier de Logements",
        "Industrial Production": "Production Industrielle",
        "Retail Sales": "Ventes au Détail",
        "Consumer Sentiment": "Confiance des Consommateurs",
        "VIX Volatility Index": "Indice de Volatilité VIX",
        "Dollar Index DXY": "Indice Dollar DXY",
        "Payroll Employment": "Emploi sur les Salaires",
        "Initial Jobless Claims": "Demandes Initiales d'Allocations Chômage",
        "Money Supply M2": "Masse Monétaire M2"
    }
    
    # Nouvelles traductions données alternatives économiques
    alternative_economic_translations = {
        "Satellite Economic Activity": "Activité Économique Satellite",
        "Social Media Sentiment Stocks": "Sentiment Médias Sociaux Actions",
        "Google Search Economic Indicators": "Indicateurs Économiques Recherches Google",
        "Credit Card Spending Trends": "Tendances de Dépenses Cartes de Crédit",
        "Supply Chain Disruption Index": "Indice de Perturbation Chaîne d'Approvisionnement",
        "Labor Market Mobility": "Mobilité du Marché du Travail",
        "Housing Market Sentiment": "Sentiment du Marché Immobilier",
        "Consumer Confidence Alternative": "Confiance des Consommateurs Alternative"
    }
    
    # Nouvelles traductions données gouvernementales avancées
    government_advanced_translations = {
        "Regional Unemployment Statistics": "Statistiques de Chômage Régional",
        "European Election Results": "Résultats des Élections Européennes",
        "Road Traffic Safety Statistics": "Statistiques de Sécurité Routière",
        "Legislative Election Results": "Résultats des Élections Législatives",
        "NHS Healthcare Waiting Times": "Temps d'Attente des Soins de Santé NHS",
        "Brexit Trade Impact Analysis": "Analyse de l'Impact Commercial du Brexit",
        "Digital Exclusion Index": "Indice d'Exclusion Numérique",
        "Food Security Metrics": "Indicateurs de Sécurité Alimentaire",
        "Universal Credit Claims": "Demandes de Crédit Universel",
        "Knife Crime Statistics": "Statistiques de Criminalité au Couteau"
    }
    
    # Nouvelles traductions données scientifiques avancées
    space_advanced_translations = {
        "Astronomy Picture of the Day": "Image Astronomique du Jour",
        "Near Earth Objects Detection Data": "Données de Détection d'Objets Géocroiseurs",
        "Mars Weather Monitoring": "Surveillance Météorologique de Mars",
        "Earth Satellite Imagery": "Imagerie Satellite Terrestre",
        "Kepler Exoplanet Discoveries": "Découvertes d'Exoplanètes Kepler",
        "Mars Curiosity Rover Photography": "Photographie du Rover Curiosity",
        "Solar Flare Activity Monitoring": "Surveillance de l'Activité des Éruptions Solaires",
        "Asteroid Belt Tracking Data": "Données de Suivi de la Ceinture d'Astéroïdes",
        "International Space Station Position": "Position de la Station Spatiale Internationale",
        "Artemis Lunar Mission Data": "Données de Mission Lunaire Artemis",
        "James Webb Space Telescope Observations": "Observations du Télescope Spatial James Webb"
    }
    
    # Combiner toutes les nouvelles traductions
    new_translations = {}
    new_translations.update(education_translations)
    new_translations.update(federal_reserve_translations)
    new_translations.update(alternative_economic_translations)
    new_translations.update(government_advanced_translations)
    new_translations.update(space_advanced_translations)
    
    print(f"🎓 Ajout de {len(education_translations)} traductions éducatives")
    print(f"🏦 Ajout de {len(federal_reserve_translations)} traductions Réserve Fédérale")
    print(f"📈 Ajout de {len(alternative_economic_translations)} traductions économiques alternatives")
    print(f"🏛️ Ajout de {len(government_advanced_translations)} traductions gouvernementales avancées")
    print(f"🚀 Ajout de {len(space_advanced_translations)} traductions spatiales avancées")
    
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
    data['metadata']['education_economic_datasets_added'] = translations_added
    data['metadata']['last_education_economic_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['metadata']['version'] = "3.3"
    
    # Sauvegarder le fichier
    with open(translations_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Résumé:")
    print(f"📊 Nouvelles traductions ajoutées: {translations_added}")
    print(f"📈 Total de traductions: {len(data['translations'])}")
    print(f"💾 Fichier mis à jour: {translations_file}")
    print(f"🆕 Version: 3.3")

if __name__ == "__main__":
    main() 