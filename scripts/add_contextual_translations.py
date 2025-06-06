#!/usr/bin/env python3
"""
Script pour ajouter des traductions contextuelles au fichier de traductions.
Ajoute des traductions avec plus de contexte pour améliorer la compréhension.

Usage: python scripts/add_contextual_translations.py
"""

import json
import sys
from pathlib import Path

def load_translations():
    """Charge le fichier de traductions."""
    file_path = Path("data/pretranslated_datasets.json")
    if not file_path.exists():
        print("❌ Fichier de traductions non trouvé!")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_translations(data):
    """Sauvegarde le fichier de traductions."""
    file_path = Path("data/pretranslated_datasets.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_contextual_translations():
    """Ajoute des traductions contextuelles manquantes."""
    
    # Traductions contextuelles à ajouter
    contextual_translations = {
        # Bike sharing context
        "Usage Demographics": "Démographie d'utilisation des vélos partagés",
        "Usage Demographics Patterns": "Modèles démographiques d'utilisation des vélos",
        "Demographics Usage": "Utilisation démographique des vélos partagés",
        "Bike Usage Demographics": "Démographie d'utilisation des vélos",
        "Bike Share Demographics": "Démographie des vélos partagés",
        "Bike Share Usage Demographics": "Démographie d'utilisation des vélos partagés",
        
        # AI/ML context - traductions complètes en français
        "AI Machine Learning Papers": "Articles d'intelligence artificielle et apprentissage automatique",
        "AI Machine Learning Papers Usage": "Utilisation des articles IA et apprentissage automatique",
        "AI Machine Learning Papers Utilisation": "Articles d'IA et d'apprentissage automatique",
        "Machine Learning Papers": "Articles d'apprentissage automatique",
        "Artificial Intelligence Papers": "Articles d'intelligence artificielle",
        "AI Research Papers": "Articles de recherche en IA",
        "ML Research Trends": "Tendances de recherche en apprentissage automatique",
        
        # Digital mental health context
        "Digital Mental Health Activity": "Activité de santé mentale numérique",
        "Digital Mental Health Growth": "Croissance de la santé mentale numérique",
        "Mental Health Digital": "Santé mentale numérique",
        "Digital Wellness": "Bien-être numérique",
        "Mental Wellness Digital": "Bien-être mental numérique",
        
        # Transportation context
        "Transport Quality": "Qualité des transports",
        "Air Quality Transport": "Qualité de l'air et transports",
        "Transportation Quality": "Qualité des transports",
        "Quality Transport": "Qualité des transports",
        
        # Climate and environment - termes complets
        "Environmental Indicators": "Indicateurs environnementaux",
        "Environmental Indicators Growth": "Croissance des indicateurs environnementaux",
        "Climate Indicators": "Indicateurs climatiques",
        "Environmental Data": "Données environnementales",
        "Environmental Monitoring": "Surveillance environnementale",
        "Environmental Statistics": "Statistiques environnementales",
        
        # Social media context with proper French
        "Social Media Activity": "Activité sur les réseaux sociaux",
        "Social Media Engagement": "Engagement sur les réseaux sociaux",
        "Social Media Trends": "Tendances des réseaux sociaux",
        "Social Media Usage": "Utilisation des réseaux sociaux",
        
        # Technology trends - complet en français
        "Tech Trends": "Tendances technologiques",
        "Technology Trends": "Tendances technologiques",
        "Tech Innovation": "Innovation technologique",
        "Tech Disruption": "Disruption technologique",
        "Technology Innovation": "Innovation technologique",
        
        # Economic data with context
        "Economic Growth": "Croissance économique",
        "GDP Growth": "Croissance du PIB",
        "Economic Indicators": "Indicateurs économiques",
        "Financial Indicators": "Indicateurs financiers",
        "Market Trends": "Tendances du marché",
        
        # Health data with proper context
        "Health Statistics": "Statistiques de santé",
        "Health Data": "Données de santé",
        "Healthcare Data": "Données de soins de santé",
        "Medical Statistics": "Statistiques médicales",
        "Public Health": "Santé publique",
        
        # Energy and environment
        "Renewable Energy": "Énergie renouvelable",
        "Clean Energy": "Énergie propre",
        "Energy Production": "Production d'énergie",
        "Energy Consumption": "Consommation d'énergie",
        "Carbon Emissions": "Émissions de carbone",
        
        # Common suffixes with better French
        "Growth Patterns": "Modèles de croissance",
        "Usage Patterns": "Modèles d'utilisation", 
        "Activity Patterns": "Modèles d'activité",
        "Trend Analysis": "Analyse des tendances",
        "Statistical Analysis": "Analyse statistique",
        "Data Analysis": "Analyse de données",
        
        # Space and scientific
        "Space Data": "Données spatiales",
        "Space Research": "Recherche spatiale",
        "Space Exploration": "Exploration spatiale",
        "NASA Data": "Données de la NASA",
        "Scientific Data": "Données scientifiques",
        
        # Transportation details
        "Air Traffic": "Trafic aérien",
        "Traffic Data": "Données de trafic",
        "Transportation Data": "Données de transport",
        "Public Transport": "Transport public",
        "Railway Data": "Données ferroviaires",
        
        # Common problematic terms - fully in French
        "Performance Metrics": "Indicateurs de performance",
        "Utilization Rates": "Taux d'utilisation",
        "Adoption Rates": "Taux d'adoption",
        "Success Metrics": "Indicateurs de succès",
        "Quality Metrics": "Indicateurs de qualité"
    }
    
    print("📊 Chargement du fichier de traductions...")
    data = load_translations()
    if not data:
        return False
    
    print(f"🔍 {len(data['translations'])} traductions existantes")
    
    # Ajouter les nouvelles traductions contextuelles
    added_count = 0
    updated_count = 0
    
    print("\n➕ Ajout des traductions contextuelles...")
    
    for english, french in contextual_translations.items():
        if english in data['translations']:
            # Mettre à jour si la traduction actuelle est de moins bonne qualité
            current = data['translations'][english]
            if len(french) > len(current) or english.lower() in current.lower():
                data['translations'][english] = french
                updated_count += 1
                print(f"🔄 Mis à jour: '{english}' → '{french}'")
        else:
            # Ajouter nouvelle traduction
            data['translations'][english] = french
            added_count += 1
            print(f"➕ Ajouté: '{english}' → '{french}'")
    
    # Mettre à jour les métadonnées
    data['metadata']['contextual_translations_added'] = added_count
    data['metadata']['contextual_translations_updated'] = updated_count
    data['metadata']['last_contextual_update'] = "2025-06-06 15:10:00"
    
    print(f"\n💾 Sauvegarde...")
    save_translations(data)
    
    print(f"\n🎉 Terminé !")
    print(f"➕ {added_count} nouvelles traductions ajoutées")
    print(f"🔄 {updated_count} traductions mises à jour")
    print(f"📊 Total: {len(data['translations'])} traductions")
    
    return True

def main():
    """Fonction principale."""
    print("🔧 Ajout de traductions contextuelles")
    print("=" * 50)
    
    success = add_contextual_translations()
    
    if success:
        print("\n✅ Traductions contextuelles ajoutées avec succès!")
        print("🚀 Le service de traduction aura maintenant plus de contexte.")
    else:
        print("\n❌ Erreur lors de l'ajout des traductions.")
        sys.exit(1)

if __name__ == "__main__":
    main() 