import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    """Ajoute les traductions climatiques manquantes."""
    
    # Chemin vers le fichier de traductions
    translations_file = Path("data/pretranslated_datasets.json")
    
    if not translations_file.exists():
        print("❌ Fichier pretranslated_datasets.json non trouvé")
        return
    
    # Charger le fichier existant
    with open(translations_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 État actuel: {len(data['translations'])} traductions")
    
    # Nouvelles traductions climatiques NOAA
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
    
    # Données géologiques USGS
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
    
    # Combiner toutes les nouvelles traductions
    new_translations = {}
    new_translations.update(climate_noaa_translations)
    new_translations.update(geological_usgs_translations)
    
    print(f"🌡️ Ajout de {len(climate_noaa_translations)} traductions climatiques NOAA")
    print(f"🌍 Ajout de {len(geological_usgs_translations)} traductions géologiques USGS")
    
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
    data['metadata']['climate_datasets_added'] = translations_added
    data['metadata']['last_climate_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['metadata']['version'] = "3.1"
    
    # Sauvegarder le fichier
    with open(translations_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Résumé:")
    print(f"📊 Nouvelles traductions ajoutées: {translations_added}")
    print(f"📈 Total de traductions: {len(data['translations'])}")
    print(f"💾 Fichier mis à jour: {translations_file}")
    print(f"🆕 Version: 3.1")

if __name__ == "__main__":
    main() 