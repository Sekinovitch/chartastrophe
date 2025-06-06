"""
Service de traduction intelligent utilisant des traductions pré-générées.
Charge les traductions depuis un fichier JSON généré une seule fois avec DeepL.
"""

import logging
import json
import os
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class TranslationService:
    """Service de traduction utilisant des traductions pré-générées."""
    
    def __init__(self):
        """Initialise le service de traduction."""
        self.pretranslated_datasets: Dict[str, str] = {}
        self.fallback_translations: Dict[str, str] = {}
        self.cache: Dict[str, str] = {}
        
        # Charger les traductions pré-générées
        self._load_pretranslated_datasets()
        
        # Appliquer les corrections communes automatiquement
        self.fix_common_issues()
        
        # Fallback : dictionnaire de traductions pour les termes de base
        self.fallback_translations = {
            'statistics': 'statistiques',
            'data': 'données',
            'trends': 'tendances',
            'analysis': 'analyse',
            'report': 'rapport',
            'market': 'marché',
            'global': 'mondial',
            'research': 'recherche',
            'development': 'développement',
            'technology': 'technologie',
            'environmental indicators': 'indicateurs environnementaux',
            'environmental indicators growth': 'croissance des indicateurs environnementaux',
            'air quality transport': 'qualité des transports',
            'transport quality': 'qualité des transports',
            'air quality': 'qualité de l\'air',
            'transport': 'transport',
            'quality': 'qualité',
            'growth': 'croissance',
            'patterns': 'modèles',
            'levels': 'niveaux',
            'measurements': 'mesures',
            'usage': 'utilisation',
            'activity': 'activité',
            'changes': 'changements',
            'artificial intelligence': 'intelligence artificielle',
            'machine learning': 'apprentissage automatique',
            'robotics': 'robotique',
            'quantum computing': 'informatique quantique',
            'climate change': 'changement climatique',
            'renewable energy': 'énergie renouvelable',
            'economic indicators': 'indicateurs économiques',
            'population growth': 'croissance démographique',
            'urban development': 'développement urbain',
            'public transportation': 'transport public',
            'social media': 'réseaux sociaux',
            'health statistics': 'statistiques de santé',
            'education data': 'données éducatives',
            'employment rates': 'taux d\'emploi',
            'housing prices': 'prix de l\'immobilier',
            'energy consumption': 'consommation d\'énergie',
            'air quality': 'qualité de l\'air',
            'water resources': 'ressources en eau',
            'food security': 'sécurité alimentaire',
            'digital transformation': 'transformation numérique',
            'innovation metrics': 'métriques d\'innovation',
            'productivity levels': 'niveaux de productivité'
        }
    
    def _load_pretranslated_datasets(self):
        """Charge les traductions pré-générées depuis le fichier JSON."""
        pretranslated_file = Path("data/pretranslated_datasets.json")
        
        if pretranslated_file.exists():
            try:
                with open(pretranslated_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.pretranslated_datasets = data.get('translations', {})
                metadata = data.get('metadata', {})
                
                logger.info(f"✅ Traductions pré-générées chargées: {len(self.pretranslated_datasets)} entrées")
                logger.info(f"📅 Générées le: {metadata.get('generated_at', 'inconnu')}")
                logger.info(f"🌐 Utilisation de DeepL: {metadata.get('deepl_api_used', False)}")
                
            except Exception as e:
                logger.warning(f"⚠️ Erreur lors du chargement des traductions pré-générées: {e}")
                self.pretranslated_datasets = {}
        else:
            logger.info("📝 Aucun fichier de traductions pré-générées trouvé")
            logger.info(f"💡 Générez-le avec: python scripts/pretranslate_datasets.py")
            self.pretranslated_datasets = {}
    
    def translate_text(self, text: str, target_lang: str = 'fr') -> str:
        """
        Traduit un texte en utilisant UNIQUEMENT les traductions pré-générées.
        AUCUNE traduction en temps réel avec DeepL n'est effectuée.
        
        Args:
            text: Texte à traduire (en anglais)
            target_lang: Langue cible ('fr' pour français, 'en' pour anglais)
            
        Returns:
            Texte traduit depuis le fichier pré-généré ou texte original
        """
        # Si langue anglaise ou texte vide, retourner tel quel
        if target_lang == 'en' or not text.strip():
            return text
        
        # Nettoyage du texte
        text = text.strip()
        
        # Vérification du cache
        cache_key = f"{text.lower()}_{target_lang}"
        if cache_key in self.cache:
            logger.debug(f"📁 Traduction trouvée dans le cache: {text[:50]}...")
            return self.cache[cache_key]
        
        # 1. Recherche dans les traductions pré-générées (exacte)
        translated = self._get_pretranslated(text)
        
        # 2. Si pas trouvé, recherche partielle dans les pré-générées
        if not translated:
            translated = self._get_pretranslated_partial(text)
        
        # 3. Si toujours pas trouvé, utiliser le dictionnaire de fallback
        if not translated:
            translated = self._translate_with_fallback(text, target_lang)
        
        # 4. Si aucune traduction disponible, retourner le texte original
        # AUCUN appel DeepL en temps réel - utilisation UNIQUEMENT des pré-traduites
        if not translated:
            translated = text
            logger.debug(f"⚠️ Pas de traduction pré-générée pour: {text[:50]}... - retour du texte original")
        
        # Mise en cache de la traduction
        self.cache[cache_key] = translated
        
        return translated
    
    def _get_pretranslated(self, text: str) -> Optional[str]:
        """Recherche une traduction exacte dans les traductions pré-générées."""
        if text in self.pretranslated_datasets:
            result = self.pretranslated_datasets[text]
            logger.debug(f"🎯 Pré-traduit (exact): '{text[:30]}...' → '{result[:30]}...'")
            return result
        return None
    
    def _get_pretranslated_partial(self, text: str) -> Optional[str]:
        """Recherche partielle dans les traductions pré-générées."""
        text_lower = text.lower()
        
        # Chercher des correspondances partielles
        for english_text, french_text in self.pretranslated_datasets.items():
            if english_text.lower() in text_lower or text_lower in english_text.lower():
                # Si on trouve une correspondance partielle, l'utiliser comme base
                logger.debug(f"🔍 Pré-traduit (partiel): '{text[:30]}...' → '{french_text[:30]}...'")
                return french_text
        
        return None
    
    def _translate_with_fallback(self, text: str, target_lang: str) -> Optional[str]:
        """Traduit en utilisant le dictionnaire de fallback."""
        if target_lang != 'fr':
            return None
        
        text_lower = text.lower()
        
        # Recherche exacte d'abord
        if text_lower in self.fallback_translations:
            result = self.fallback_translations[text_lower]
            if text[0].isupper():
                result = result.capitalize()
            logger.debug(f"📚 Fallback: '{text}' → '{result}'")
            return result
        
        # Recherche partielle pour des expressions complexes
        for english_term, french_term in self.fallback_translations.items():
            if english_term in text_lower:
                translated = text.replace(english_term, french_term)
                if translated != text:
                    logger.debug(f"📚 Fallback partiel: '{text}' → '{translated}'")
                    return translated
        
        return None
    
    def translate_dataset_name(self, name: str, target_lang: str = 'fr') -> str:
        """
        Traduit un nom de dataset en utilisant UNIQUEMENT les traductions pré-générées.
        
        Args:
            name: Nom du dataset (originalement en anglais)
            target_lang: Langue cible ('fr' pour français, 'en' pour anglais)
            
        Returns:
            Nom traduit vers la langue cible ou nom original en anglais
        """
        # Si la langue cible est l'anglais, retourner le nom original (déjà en anglais)
        if target_lang == 'en':
            logger.debug(f"🇺🇸 Langue anglaise demandée, retour du nom original: '{name}'")
            return name
        
        # Vérification du cache d'abord
        cache_key = f"{name.lower()}_{target_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 1. Recherche EXACTE dans les traductions pré-générées
        if name in self.pretranslated_datasets:
            translated = self.pretranslated_datasets[name]
            # Post-traitement léger pour améliorer la qualité
            translated = self._post_process_translation(translated)
            self.cache[cache_key] = translated
            logger.debug(f"✅ Pré-traduit: '{name[:40]}...' → '{translated[:40]}...'")
            return translated
        
        # 2. Recherche par mots-clés dans les traductions pré-générées
        translated = self._find_similar_pretranslated(name)
        if translated:
            translated = self._post_process_translation(translated)
            self.cache[cache_key] = translated
            logger.debug(f"🔍 Similarité trouvée: '{name[:40]}...' → '{translated[:40]}...'")
            return translated
        
        # 3. Si aucune traduction pré-générée, retourner le nom original
        logger.debug(f"⚠️ Pas de traduction pré-générée pour: '{name}'")
        self.cache[cache_key] = name
        return name
    
    def _find_similar_pretranslated(self, name: str) -> Optional[str]:
        """Trouve une traduction similaire en analysant les mots-clés."""
        name_lower = name.lower()
        
        # Mots-clés importants à rechercher
        keywords = name_lower.replace('-', ' ').replace('_', ' ').split()
        
        best_match = None
        best_score = 0
        
        for english_name, french_translation in self.pretranslated_datasets.items():
            english_lower = english_name.lower()
            
            # Compter les mots-clés communs
            english_words = english_lower.replace('-', ' ').replace('_', ' ').split()
            common_words = set(keywords) & set(english_words)
            
            if common_words:
                score = len(common_words) / max(len(keywords), len(english_words))
                if score > best_score and score > 0.3:  # Au moins 30% de similarité
                    best_score = score
                    best_match = french_translation
        
        return best_match
    
    def _clean_dataset_name_for_translation(self, name: str) -> str:
        """Nettoie le nom de dataset avant traduction."""
        import re
        
        # Supprimer les informations de pays/région qui peuvent confuser
        cleaned = re.sub(r'\s*\([^)]*\)\s*', '', name)
        
        # Supprimer les suffixes redondants
        cleaned = re.sub(r'\s+(data|statistics|trends|analysis|measurements|levels)$', '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _post_process_translation(self, translated: str) -> str:
        """Post-traite la traduction pour améliorer la qualité."""
        # Corrections spécifiques communes
        corrections = {
            'statistiques de naissance': 'statistiques de naissances',
            'données de naissances': 'données de naissance',
            'informatique quantique papiers': 'articles d\'informatique quantique',
            'marché du pétrole rapport': 'rapport du marché pétrolier',
            'transport de qualité': 'qualité des transports',
            'qualité air': 'qualité de l\'air',
            'air quality transport': 'qualité des transports',
            'environmental indicators': 'indicateurs environnementaux',
            'environmental indicators growth': 'croissance des indicateurs environnementaux',
            'transport quality': 'qualité des transports',
            'air transport': 'transport aérien',
            'growth': 'croissance',
            'trends': 'tendances',
            'patterns': 'modèles',
            'statistics': 'statistiques',
            'levels': 'niveaux',
            'measurements': 'mesures',
            'usage': 'utilisation',
            'activity': 'activité',
            'changes': 'changements'
        }
        
        result = translated.lower()
        
        # Appliquer les corrections
        for wrong, correct in corrections.items():
            if wrong in result:
                result = result.replace(wrong, correct)
        
        # Remettre la première lettre en majuscule
        if result:
            result = result[0].upper() + result[1:]
        
        # Corrections spécifiques pour des patterns problématiques
        import re
        
        # Corriger les mots anglais résiduels courants
        english_patterns = {
            r'\benvironmental\b': 'environnemental',
            r'\bindicators?\b': 'indicateurs',
            r'\bgrowth\b': 'croissance',
            r'\btrends?\b': 'tendances',
            r'\bpatterns?\b': 'modèles',
            r'\bstatistics?\b': 'statistiques',
            r'\blevels?\b': 'niveaux',
            r'\bmeasurements?\b': 'mesures',
            r'\busage\b': 'utilisation',
            r'\bactivity\b': 'activité',
            r'\bchanges?\b': 'changements',
            r'\banalysis\b': 'analyse',
            r'\breport\b': 'rapport',
            r'\bmarket\b': 'marché',
            r'\bdata\b': 'données',
            r'\bquality\b': 'qualité',
            r'\btransport\b': 'transport',
            r'\benergy\b': 'énergie',
            r'\bhealth\b': 'santé',
            r'\btechnology\b': 'technologie'
        }
        
        for pattern, replacement in english_patterns.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'utilisation du service."""
        return {
            'pretranslated_entries': len(self.pretranslated_datasets),
            'fallback_entries': len(self.fallback_translations),
            'cache_entries': len(self.cache),
            'pretranslated_file_exists': Path("data/pretranslated_datasets.json").exists(),
            'mode': 'pretranslated' if self.pretranslated_datasets else 'fallback_only'
        }
    
    def reload_pretranslated(self):
        """Recharge les traductions pré-générées depuis le fichier."""
        self._load_pretranslated_datasets()
        self.cache.clear()  # Vider le cache pour forcer le rechargement
        logger.info("🔄 Traductions pré-générées rechargées")
    
    def fix_common_issues(self):
        """Corrige les problèmes courants dans les traductions existantes."""
        if not self.pretranslated_datasets:
            return
        
        fixes_applied = 0
        common_fixes = {
            'Transport de qualité': 'Qualité des transports',
            'transport de qualité': 'qualité des transports',
            'AIr Quality Transport': 'Qualité des transports',
            'Air Quality Transport': 'Qualité des transports'
        }
        
        # Corriger les traductions dans le dictionnaire pré-généré
        for english, french in list(self.pretranslated_datasets.items()):
            corrected = french
            for wrong, correct in common_fixes.items():
                if wrong in corrected:
                    corrected = corrected.replace(wrong, correct)
            
            if corrected != french:
                self.pretranslated_datasets[english] = corrected
                fixes_applied += 1
                logger.info(f"🔧 Correction appliquée: '{french}' → '{corrected}'")
        
        # Vider le cache pour appliquer les corrections
        self.cache.clear()
        
        if fixes_applied > 0:
            logger.info(f"✅ {fixes_applied} corrections appliquées automatiquement")
        else:
            logger.info("✅ Aucune correction nécessaire")

# Instance globale du service de traduction
translation_service = TranslationService() 