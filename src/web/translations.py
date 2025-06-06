"""
Gestion des traductions pour l'interface utilisateur.
Supporte le français et l'anglais avec un système simple et efficace.
"""

TRANSLATIONS = {
    'fr': {
        # Page principale
        'title': 'Chartastrophe - Découvrez des corrélations avec de vraies données !',
        'description': 'Explorez des corrélations fascinantes et amusantes entre des données réelles provenant de sources officielles.',
        'discover_correlations': 'Découvrez des corrélations fascinantes',
        'generate_button': 'Générer une nouvelle corrélation',
        'regenerate_button': 'Générer une autre corrélation',
        'loading_message': 'Génération d\'une corrélation passionnante...',
        'about_link': 'À propos',
        
        # Interface principale
        'language_selector': 'Langue',
        'coefficient_label': 'Coefficient de corrélation',
        'share_title': 'Partager cette corrélation',
        'share_twitter': 'Partager sur Twitter',
        'share_facebook': 'Partager sur Facebook', 
        'share_instagram': 'Partager sur Instagram',
        'share_direct': 'Lien direct',
        
        # Section sources
        'data_sources': 'Sources des données',
        'source_type': 'Type de source',
        'source_url': 'URL de la source',
        
        # Feedback
        'feedback_title': 'Cette corrélation vous a-t-elle fait sourire ?',
        'feedback_funny': '😄 Amusante',
        'feedback_intriguing': '🤨 Intrigante',
        'feedback_not_funny': '😐 Pas drôle',
        'feedback_thanks': 'Merci pour votre avis !',
        
        # Messages d'erreur
        'error_generation': 'Impossible de générer une corrélation intéressante pour le moment. Veuillez réessayer dans quelques instants.',
        'error_rate_limit': 'Trop de requêtes. Veuillez patienter quelques minutes.',
        'error_not_found': 'Corrélation introuvable',
        'error_unexpected': 'Une erreur inattendue s\'est produite.',
        
        # Page À propos
        'about_title': 'À propos de Chartastrophe',
        'about_description': 'Chartastrophe est une application qui génère des corrélations amusantes et inattendues entre des données réelles.',
        'about_purpose': 'Notre objectif est de montrer que les données peuvent être à la fois éducatives et divertissantes.',
        'back_home': 'Retour à l\'accueil',
        
        # Page de partage
        'share_page_title': 'Corrélation partagée - Chartastrophe',
        'share_description': 'Découvrez cette corrélation fascinante générée par Chartastrophe',
        'explore_more': 'Explorez plus de corrélations',
    },
    'en': {
        # Page principale  
        'title': 'Chartastrophe - Discover correlations with real data!',
        'description': 'Explore fascinating and amusing correlations between real data from official sources.',
        'discover_correlations': 'Discover fascinating correlations',
        'generate_button': 'Generate a new correlation',
        'regenerate_button': 'Generate another correlation',
        'loading_message': 'Generating an exciting correlation...',
        'about_link': 'About',
        
        # Interface principale
        'language_selector': 'Language',
        'coefficient_label': 'Correlation coefficient',
        'share_title': 'Share this correlation',
        'share_twitter': 'Share on Twitter',
        'share_facebook': 'Share on Facebook',
        'share_instagram': 'Share on Instagram', 
        'share_direct': 'Direct link',
        
        # Section sources
        'data_sources': 'Data sources',
        'source_type': 'Source type',
        'source_url': 'Source URL',
        
        # Feedback
        'feedback_title': 'Did this correlation make you smile?',
        'feedback_funny': '😄 Funny',
        'feedback_intriguing': '🤨 Intriguing',
        'feedback_not_funny': '😐 Not funny',
        'feedback_thanks': 'Thank you for your feedback!',
        
        # Messages d'erreur
        'error_generation': 'Unable to generate an interesting correlation at the moment. Please try again in a few moments.',
        'error_rate_limit': 'Too many requests. Please wait a few minutes.',
        'error_not_found': 'Correlation not found',
        'error_unexpected': 'An unexpected error occurred.',
        
        # Page À propos
        'about_title': 'About Chartastrophe',
        'about_description': 'Chartastrophe is an application that generates amusing and unexpected correlations between real data.',
        'about_purpose': 'Our goal is to show that data can be both educational and entertaining.',
        'back_home': 'Back to home',
        
        # Page de partage
        'share_page_title': 'Shared Correlation - Chartastrophe',
        'share_description': 'Discover this fascinating correlation generated by Chartastrophe',
        'explore_more': 'Explore more correlations',
    }
}

def get_translation(lang, key, default=None):
    """
    Récupère une traduction pour une langue et une clé données.
    
    Args:
        lang (str): Code de langue ('fr' ou 'en')
        key (str): Clé de traduction
        default (str): Valeur par défaut si la traduction n'existe pas
    
    Returns:
        str: Traduction ou valeur par défaut
    """
    if lang not in TRANSLATIONS:
        lang = 'en'  # Langue par défaut
    
    return TRANSLATIONS[lang].get(key, default or key)

def get_supported_languages():
    """
    Retourne la liste des langues supportées.
    
    Returns:
        list: Liste des codes de langues supportées
    """
    return list(TRANSLATIONS.keys())

def get_language_names():
    """
    Retourne les noms des langues pour l'interface.
    
    Returns:
        dict: Dictionnaire des noms de langues
    """
    return {
        'fr': 'Français',
        'en': 'English'
    } 