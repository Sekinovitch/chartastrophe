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
        self.title_templates = [
            "🔬 Surprising link discovered between {var1} and {var2}",
            "📊 Unexpected correlation: {var1} influences {var2}",
            "🎯 Study reveals: {var1} predicts {var2}",
            "📈 Hidden relationship between {var1} and {var2}",
            "🧮 {var1} and {var2} evolve in concert",
            "📋 Discovery: {var1} correlated with {var2}",
            "🔍 Analysis confirms the link {var1} → {var2}",
            "⚡ Mysterious connection: {var1} affects {var2}",
            "🎲 Pattern detected between {var1} and {var2}",
            "🔬 {var1} synchronized with {var2}"
        ]
        
        self.explanation_templates = [
            "Our algorithms analyzed {nb_points} data points and discovered this astonishing correlation. Statistics don't lie: when one evolves, the other follows! Our experts think it's either a fascinating phenomenon or a cosmic coincidence.",
            
            "A team of data scientists scrutinized {nb_points} measurements to reveal this surprising association. The correlation coefficient suggests a stronger link than expected. It's the kind of discovery that makes statisticians raise an eyebrow.",
            
            "After analyzing {nb_points} observations, this relationship clearly emerges from the data. Predictive models confirm: there's definitely something happening here. Pure coincidence or real phenomenon? The debate remains open.",
            
            "The numbers speak: across {nb_points} analyzed points, the correlation is undeniable. Our machine learning algorithms detected this recurring pattern. It's the type of result that makes researchers say 'well, that's odd'.",
            
            "A meta-analysis of {nb_points} data reveals this unexpected association. Statistical tests confirm it's not due to chance. Whether it's science or magic remains to be seen... probably a bit of both.",
            
            "Artificial intelligence identified this correlation by scrutinizing {nb_points} measurements. Neural networks don't understand why, but they're categorical: it works! Modern science in all its splendor."
        ]
        
        self.bonus_comments = [
            "The results were validated three times - we couldn't believe it ourselves!",
            "This discovery will make waves in laboratories... and coffee shops.",
            "Our statisticians are still scratching their heads over this one.",
            "It's the kind of correlation you find while looking for something else.",
            "Data never lies, even when it surprises!",
            "A beautiful illustration that the world is more connected than we think.",
            "Proof that reality sometimes surpasses statistical fiction.",
            "This correlation deserves its place in the pantheon of unexpected discoveries."
        ]
        
        self.correlation_qualifiers = {
            'strong': ['remarkable', 'impressive', 'robust', 'solid', 'striking'],
            'medium': ['notable', 'interesting', 'visible', 'measurable', 'surprising'],
            'weak': ['subtle', 'discrete', 'delicate', 'emerging', 'shy']
        }

    def generate_explanation(self, correlation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a pseudo-scientific explanation for a correlation.
        
        Args:
            correlation_data: Correlation data
            
        Returns:
            Dictionary containing title and explanation
        """
        try:
            # Extract series names
            series1 = correlation_data.get('series1_name', 'Indicator 1')
            series2 = correlation_data.get('series2_name', 'Indicator 2')
            correlation = correlation_data.get('correlation', 0)
            data_x = correlation_data.get('data_x', [])
            nb_points = len(data_x) if data_x else 14  # Number of data points
            
            # Select templates
            title_template = random.choice(self.title_templates)
            explanation_template = random.choice(self.explanation_templates)
            bonus_comment = random.choice(self.bonus_comments)
            
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
                qualifier = random.choice(self.correlation_qualifiers['strong'])
            elif coef > 0.4:
                qualifier = random.choice(self.correlation_qualifiers['medium'])
            else:
                qualifier = random.choice(self.correlation_qualifiers['weak'])
                
            # Build final explanation with bonus comment
            complete_explanation = f"A {qualifier} correlation (r = {correlation:.3f}) has been identified. " + explanation + f" {bonus_comment}"
            
            logger.info(f"Pseudo-scientific explanation generated for correlation between {series1} and {series2}")
            
            return {
                'title': title,
                'explanation': complete_explanation,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
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
    
    def generate(self, correlation: CorrelationResult) -> AbsurdExplanation:
        """Generates an absurd explanation for a correlation."""
        
        # Generate title and explanation
        explanation_data = self.generate_explanation({
            'series1_name': correlation.series1_name,
            'series2_name': correlation.series2_name,
            'correlation': correlation.correlation_coefficient
        })
        
        return AbsurdExplanation(
            title=explanation_data['title'],
            explanation=explanation_data['explanation'],
            correlation_result=correlation
        )