"""
Absurd explanation generator for correlations.
"""
import random
from typing import Dict, List, Any
import logging
from datetime import datetime
from dataclasses import dataclass
from src.correlation.correlation_analyzer import CorrelationResult
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class AbsurdExplanation:
    title: str
    explanation: str
    correlation_result: CorrelationResult

class ExplanationGenerator:
    def __init__(self):
        # Templates in French
        self.title_templates_fr = [
            "📊 Relation statistique surprenante : {var1} et {var2}",
            "🔍 L'analyse des données révèle : {var1} influence {var2}",
            "🧪 Étude de recherche : {var1} prédit {var2}",
            "🕵️ Motif statistique caché entre {var1} et {var2}",
            "⚡ Découverte mathématique : {var1} et {var2} évoluent de concert",
            "🔬 Investigation scientifique : {var1} corrélé avec {var2}",
            "📈 L'analyse statistique confirme le lien {var1} → {var2}",
            "💡 Découverte de recherche inattendue : {var1} affecte {var2}",
            "🎯 Découverte de data mining : motif détecté entre {var1} et {var2}",
            "📊 Analyse quantitative : {var1} synchronisé avec {var2}",
            "🔗 Preuve empirique : {var1} connecté à {var2}",
            "🌐 L'investigation Big Data révèle {var1} lié à {var2}",
            "📐 La modélisation statistique montre {var1} en relation avec {var2}",
            "🔎 Étude de corrélation : {var1} correspond avec {var2}",
            "🚀 Percée en science des données : {var1} parallèle à {var2}",
            "🧮 Analyse mathématique : {var1} reflète {var2}",
            "📋 Résultats de recherche : {var1} suit {var2}",
            "⭐ Découverte statistique : {var1} s'aligne avec {var2}",
            "🎲 Recherche quantitative : {var1} coïncide avec {var2}",
            "📊 Rapport d'analytique de données : {var1} varie avec {var2}"
        ]
        
        # Templates in English
        self.title_templates_en = [
            "📊 Surprising Statistical Relationship: {var1} and {var2}",
            "🔍 Data Analysis Reveals: {var1} influences {var2}",
            "🧪 Research Study: {var1} predicts {var2}",
            "🕵️ Hidden Statistical Pattern between {var1} and {var2}",
            "⚡ Mathematical Discovery: {var1} and {var2} evolve in concert",
            "🔬 Scientific Investigation: {var1} correlated with {var2}",
            "📈 Statistical Analysis confirms the link {var1} → {var2}",
            "💡 Unexpected Research Finding: {var1} affects {var2}",
            "🎯 Data Mining Discovery: Pattern detected between {var1} and {var2}",
            "📊 Quantitative Analysis: {var1} synchronized with {var2}",
            "🔗 Empirical Evidence: {var1} connected to {var2}",
            "🌐 Big Data Investigation reveals {var1} linked to {var2}",
            "📐 Statistical Modeling shows {var1} relates to {var2}",
            "🔎 Correlation Study: {var1} corresponds with {var2}",
            "🚀 Data Science Breakthrough: {var1} parallels {var2}",
            "🧮 Mathematical Analysis: {var1} mirrors {var2}",
            "📋 Research Findings: {var1} tracks with {var2}",
            "⭐ Statistical Discovery: {var1} aligns with {var2}",
            "🎲 Quantitative Research: {var1} coincides with {var2}",
            "📊 Data Analytics Report: {var1} varies with {var2}"
        ]
        
        # Explanations in French
        self.explanation_templates_fr = [
            "Nos algorithmes ont analysé {nb_points} points de données et découvert cette corrélation étonnante. Les statistiques ne mentent pas : quand l'un évolue, l'autre suit ! Nos experts pensent que c'est soit un phénomène fascinant, soit une coïncidence cosmique.",
            
            "Une équipe de data scientists a scruté {nb_points} mesures pour révéler cette association surprenante. Le coefficient de corrélation suggère un lien plus fort qu'attendu. C'est le genre de découverte qui fait lever un sourcil aux statisticiens.",
            
            "Après avoir analysé {nb_points} observations, cette relation émerge clairement des données. Les modèles prédictifs confirment : il se passe définitivement quelque chose ici. Pure coïncidence ou vrai phénomène ? Le débat reste ouvert.",
            
            "Les chiffres parlent : sur {nb_points} points analysés, la corrélation est indéniable. Nos algorithmes d'apprentissage automatique ont détecté ce motif récurrent. C'est le type de résultat qui fait dire aux chercheurs 'tiens, c'est bizarre'.",
            
            "Une méta-analyse de {nb_points} données révèle cette association inattendue. Les tests statistiques confirment que ce n'est pas dû au hasard. Que ce soit de la science ou de la magie reste à voir... probablement un peu des deux.",
            
            "L'intelligence artificielle a identifié cette corrélation en scrutant {nb_points} mesures. Les réseaux de neurones ne comprennent pas pourquoi, mais ils sont catégoriques : ça marche ! La science moderne dans toute sa splendeur."
        ]
        
        # Explanations in English
        self.explanation_templates_en = [
            "Our algorithms analyzed {nb_points} data points and discovered this astonishing correlation. Statistics don't lie: when one evolves, the other follows! Our experts think it's either a fascinating phenomenon or a cosmic coincidence.",
            
            "A team of data scientists scrutinized {nb_points} measurements to reveal this surprising association. The correlation coefficient suggests a stronger link than expected. It's the kind of discovery that makes statisticians raise an eyebrow.",
            
            "After analyzing {nb_points} observations, this relationship clearly emerges from the data. Predictive models confirm: there's definitely something happening here. Pure coincidence or real phenomenon? The debate remains open.",
            
            "The numbers speak: across {nb_points} analyzed points, the correlation is undeniable. Our machine learning algorithms detected this recurring pattern. It's the type of result that makes researchers say 'well, that's odd'.",
            
            "A meta-analysis of {nb_points} data reveals this unexpected association. Statistical tests confirm it's not due to chance. Whether it's science or magic remains to be seen... probably a bit of both.",
            
            "Artificial intelligence identified this correlation by scrutinizing {nb_points} measurements. Neural networks don't understand why, but they're categorical: it works! Modern science in all its splendor."
        ]
        
        # Bonus comments in French
        self.bonus_comments_fr = [
            "Les résultats ont été validés trois fois - nous n'arrivions pas à y croire nous-mêmes !",
            "Cette découverte va faire des vagues dans les laboratoires... et les cafés.",
            "Nos statisticiens se grattent encore la tête sur celle-ci.",
            "C'est le genre de corrélation qu'on trouve en cherchant autre chose.",
            "Les données ne mentent jamais, même quand elles surprennent !",
            "Une belle illustration que le monde est plus connecté qu'on ne le pense.",
            "La preuve que la réalité dépasse parfois la fiction statistique.",
            "Cette corrélation mérite sa place au panthéon des découvertes inattendues."
        ]
        
        # Bonus comments in English
        self.bonus_comments_en = [
            "The results were validated three times - we couldn't believe it ourselves!",
            "This discovery will make waves in laboratories... and coffee shops.",
            "Our statisticians are still scratching their heads over this one.",
            "It's the kind of correlation you find while looking for something else.",
            "Data never lies, even when it surprises!",
            "A beautiful illustration that the world is more connected than we think.",
            "Proof that reality sometimes surpasses statistical fiction.",
            "This correlation deserves its place in the pantheon of unexpected discoveries."
        ]
        
        # Correlation qualifiers in French
        self.correlation_qualifiers_fr = {
            'strong': ['remarquable', 'impressionnante', 'robuste', 'solide', 'frappante'],
            'medium': ['notable', 'intéressante', 'visible', 'mesurable', 'surprenante'],
            'weak': ['subtile', 'discrète', 'délicate', 'émergente', 'timide']
        }
        
        # Correlation qualifiers in English
        self.correlation_qualifiers_en = {
            'strong': ['remarkable', 'impressive', 'robust', 'solid', 'striking'],
            'medium': ['notable', 'interesting', 'visible', 'measurable', 'surprising'],
            'weak': ['subtle', 'discrete', 'delicate', 'emerging', 'shy']
        }

    def generate_explanation(self, correlation_data: Dict[str, Any], language: str = 'en') -> Dict[str, Any]:
        """
        Generates a pseudo-scientific explanation for a correlation.
        
        Args:
            correlation_data: Correlation data
            language: Language code ('fr' or 'en')
            
        Returns:
            Dictionary containing title and explanation
        """
        try:
            logger.info(f"🔤 ExplanationGenerator called with language: {language}")
            
            # Extract series names
            series1 = correlation_data.get('series1_name', 'Indicator 1')
            series2 = correlation_data.get('series2_name', 'Indicator 2')
            correlation = correlation_data.get('correlation', 0)
            data_x = correlation_data.get('data_x', [])
            nb_points = len(data_x) if data_x else 14  # Number of data points
            
            logger.info(f"📊 Generating explanation for: {series1} vs {series2}")
            
            # Translate dataset names if French language is requested
            if language == 'fr':
                try:
                    from ..services.translation_service import translation_service
                    translated_series1 = translation_service.translate_dataset_name(series1)
                    translated_series2 = translation_service.translate_dataset_name(series2)
                    logger.info(f"🔄 Translated for title: {series1} → {translated_series1}")
                    logger.info(f"🔄 Translated for title: {series2} → {translated_series2}")
                    series1 = translated_series1
                    series2 = translated_series2
                except Exception as e:
                    logger.warning(f"Could not translate dataset names: {e}")
                    # Continue with original names if translation fails
            
            # Select templates based on language
            if language == 'fr':
                title_template = random.choice(self.title_templates_fr)
                explanation_template = random.choice(self.explanation_templates_fr)
                bonus_comment = random.choice(self.bonus_comments_fr)
                correlation_qualifiers = self.correlation_qualifiers_fr
            else:
                title_template = random.choice(self.title_templates_en)
                explanation_template = random.choice(self.explanation_templates_en)
                bonus_comment = random.choice(self.bonus_comments_en)
                correlation_qualifiers = self.correlation_qualifiers_en
            
            # Generate title and explanation
            title = title_template.format(var1=series1.lower(), var2=series2.lower())
            
            # Replace number of points in explanation
            explanation = explanation_template.format(
                var1=series1.lower(), 
                var2=series2.lower(),
                nb_points=nb_points
            )
            
            # Add qualifier based on correlation strength
            coef = abs(correlation)
            if coef > 0.7:
                qualifier = random.choice(correlation_qualifiers['strong'])
            elif coef > 0.4:
                qualifier = random.choice(correlation_qualifiers['medium'])
            else:
                qualifier = random.choice(correlation_qualifiers['weak'])
                
            # Build final explanation with bonus comment
            if language == 'fr':
                complete_explanation = f"Une corrélation {qualifier} (r = {correlation:.3f}) a été identifiée. " + explanation + f" {bonus_comment}"
            else:
                complete_explanation = f"A {qualifier} correlation (r = {correlation:.3f}) has been identified. " + explanation + f" {bonus_comment}"
            
            logger.info(f"Pseudo-scientific explanation generated for correlation between {series1} and {series2}")
            
            return {
                'title': title,
                'explanation': complete_explanation,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            if language == 'fr':
                return {
                    'title': "📊 Analyse statistique en cours",
                    'explanation': "Une corrélation intéressante a été détectée par nos algorithmes d'analyse. L'équipe de recherche étudie actuellement les implications de cette découverte dans un cadre méthodologique rigoureux.",
                    'generated_at': datetime.now().isoformat()
                }
            else:
                return {
                    'title': "📊 Statistical analysis in progress",
                    'explanation': "An interesting correlation has been detected by our analysis algorithms. The research team is currently studying the implications of this discovery within a rigorous methodological framework.",
                    'generated_at': datetime.now().isoformat()
                }
    
    def generate_batch(self, correlations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates explanations for a list of correlations.
        
        Args:
            correlations: List of correlations
            
        Returns:
            List of generated explanations
        """
        return [self.generate_explanation(corr) for corr in correlations]
    
    def generate(self, correlation: CorrelationResult, language: str = 'en') -> AbsurdExplanation:
        """Generates an absurd explanation for a correlation."""
        
        # Generate title and explanation
        explanation_data = self.generate_explanation({
            'series1_name': correlation.series1_name,
            'series2_name': correlation.series2_name,
            'correlation': correlation.correlation_coefficient
        }, language=language)
        
        return AbsurdExplanation(
            title=explanation_data['title'],
            explanation=explanation_data['explanation'],
            correlation_result=correlation
        )