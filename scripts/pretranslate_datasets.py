#!/usr/bin/env python3
"""
Script de pré-traduction des noms de datasets avec DeepL.
À exécuter une seule fois pour générer le fichier de traductions.

Usage: python scripts/pretranslate_datasets.py
"""

import sys
import os
import json
import time
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    print("❌ DeepL non installé. Installez avec: pip install deepl")
    sys.exit(1)

from src.config import DEEPL_CONFIG
from src.collectors.real_data_collector import RealSourceGenerator

def collect_all_dataset_names():
    """Collecte tous les noms de datasets possibles."""
    print("📊 Collecte de tous les noms de datasets possibles...")
    
    generator = RealSourceGenerator()
    dataset_names = set()
    
    # Générer beaucoup de datasets pour capturer toutes les variations
    print("   🔄 Génération de 500 datasets pour capturer toutes les variations...")
    for i in range(500):
        if i % 50 == 0:
            print(f"   📈 Progression: {i}/500")
        
        try:
            dataset = generator.generate_real_dataset('en')
            dataset_names.add(dataset.name)
        except Exception as e:
            print(f"   ⚠️ Erreur lors de la génération du dataset {i}: {e}")
            continue
    
    # Ajouter des noms de base manuellement pour s'assurer qu'ils sont inclus
    base_names = [
        "Monthly Birth Statistics",
        "Real Estate Transaction Data",
        "Regional Unemployment Statistics", 
        "University Enrollment Data",
        "Global Temperature Anomalies",
        "Renewable Energy Capacity",
        "Mars Curiosity Rover Photography",
        "Google Search Trends",
        "Wikipedia Page Views",
        "Reddit Activity",
        "Programming Language Trends",
        "Global GDP Statistics",
        "CO2 Emissions Data",
        "Internet Usage Statistics",
        "French Railway Station Usage",
        "Paris Metro Station Traffic",
        "NASA Space Data",
        "Climate Change Indicators",
        "Economic Growth Patterns",
        "Technology Innovation Metrics"
    ]
    
    dataset_names.update(base_names)
    
    print(f"✅ Collecté {len(dataset_names)} noms de datasets uniques")
    return sorted(list(dataset_names))

def translate_with_deepl(names_list, api_key):
    """Traduit tous les noms avec DeepL."""
    print("🌐 Traduction avec DeepL...")
    
    if not api_key:
        print("❌ Clé API DeepL manquante. Vérifiez votre fichier .env")
        return {}
    
    translator = deepl.Translator(api_key)
    translations = {}
    total = len(names_list)
    
    # Traiter par petits lots pour éviter de surcharger l'API
    batch_size = 10
    request_delay = 0.5  # Délai entre les requêtes
    
    for i in range(0, total, batch_size):
        batch = names_list[i:i + batch_size]
        print(f"   📦 Lot {i//batch_size + 1}/{(total + batch_size - 1)//batch_size} ({len(batch)} éléments)")
        
        for j, name in enumerate(batch):
            try:
                if name.strip():  # Éviter les chaînes vides
                    result = translator.translate_text(
                        name,
                        source_lang='EN',
                        target_lang='FR',
                        formality='default'
                    )
                    translations[name] = result.text.strip()
                    print(f"     ✅ '{name[:40]}...' → '{result.text[:40]}...'")
                else:
                    translations[name] = name
                
                # Délai entre les requêtes
                if j < len(batch) - 1:  # Pas de délai après le dernier élément du lot
                    time.sleep(request_delay)
                    
            except deepl.exceptions.QuotaExceededException:
                print(f"❌ Quota DeepL dépassé après {len(translations)} traductions")
                break
            except deepl.exceptions.DeepLException as e:
                print(f"   ⚠️ Erreur DeepL pour '{name}': {e}")
                translations[name] = name  # Garder l'original si échec
            except Exception as e:
                print(f"   ⚠️ Erreur générale pour '{name}': {e}")
                translations[name] = name
        
        # Délai entre les lots
        if i + batch_size < total:
            print(f"   ⏰ Pause de {request_delay * 2}s entre les lots...")
            time.sleep(request_delay * 2)
    
    print(f"✅ Traduction terminée: {len(translations)} entrées")
    return translations

def save_translations(translations, output_file):
    """Sauvegarde les traductions dans un fichier JSON."""
    print(f"💾 Sauvegarde dans {output_file}...")
    
    # Créer le répertoire si nécessaire
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Ajouter des métadonnées
    data = {
        "metadata": {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_translations": len(translations),
            "deepl_api_used": True,
            "version": "1.0"
        },
        "translations": translations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Sauvegardé {len(translations)} traductions")

def main():
    """Fonction principale."""
    print("🚀 Pré-traduction des datasets avec DeepL")
    print("=" * 50)
    
    # Vérifier la clé API
    api_key = DEEPL_CONFIG.get('api_key')
    if not api_key:
        print("❌ Clé API DeepL non trouvée.")
        print("   Assurez-vous d'avoir DEEPL_API_KEY dans votre fichier .env")
        return
    
    # Fichier de sortie
    output_file = "data/pretranslated_datasets.json"
    
    try:
        # Étape 1: Collecter tous les noms
        dataset_names = collect_all_dataset_names()
        
        # Étape 2: Traduire avec DeepL
        translations = translate_with_deepl(dataset_names, api_key)
        
        if not translations:
            print("❌ Aucune traduction générée")
            return
        
        # Étape 3: Sauvegarder
        save_translations(translations, output_file)
        
        print("\n🎉 Pré-traduction terminée avec succès!")
        print(f"📁 Fichier généré: {output_file}")
        print(f"📊 Nombre de traductions: {len(translations)}")
        print("\n💡 L'application utilisera maintenant ces traductions pré-générées")
        print("   plus besoin d'appeler DeepL à chaque génération!")
        
    except KeyboardInterrupt:
        print("\n⏸️ Arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 