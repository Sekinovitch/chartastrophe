"""
Chartastrophe application configuration
Absurd and hilarious correlation generator
"""
import logging
import sys
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# ========================================
# MAIN CONFIGURATION
# ========================================

# Statistical correlation parameters
CORRELATION_CONFIG: Dict[str, Any] = {
    'min_samples': 10,              # Minimum number of data points
    'min_correlation': 0.3,         # Minimum coefficient (lowered for more variety)
    'max_p_value': 0.05,           # Statistical significance threshold
    'methods': ['pearson', 'spearman', 'kendall']  # Available methods
}

# Data generation parameters
DATA_CONFIG: Dict[str, Any] = {
    'n_points': 60,                 # Number of points per time series
    'trend_range': (-0.2, 0.2),    # Range for trends
    'seasonality_range': (0.3, 0.7), # Range for seasonality
    'noise_range': (0.1, 0.3),     # Range for random noise
    'max_datasets': 1000,          # Maximum number of datasets in cache
    'refresh_interval': 3600       # Refresh interval (seconds)
}

# ========================================
# SECURITY CONFIGURATION
# ========================================

SECURITY_CONFIG: Dict[str, Any] = {
    'rate_limit': {
        'window_size': 60,          # Time window (seconds)
        'max_requests': 30          # Max requests per window
    },
    'allowed_hosts': ['127.0.0.1', 'localhost', '0.0.0.0'],
    'session_timeout': 3600,       # Session timeout (seconds)
    'max_file_size': 10 * 1024 * 1024,  # Max file size (10 MB)
    'cors_origins': ['http://localhost:3000', 'http://127.0.0.1:5000']
}

# ========================================
# PERFORMANCE CONFIGURATION
# ========================================

PERFORMANCE_CONFIG: Dict[str, Any] = {
    'cache_timeout': 300,           # Cache timeout (seconds)
    'max_workers': os.cpu_count() or 4,  # Workers for parallel processing
    'batch_size': 1000,            # Processing batch size
    'timeout': 30,                 # General timeout (seconds)
    'memory_limit': 512 * 1024 * 1024,  # Memory limit (512 MB)
    'enable_compression': True      # Response compression
}

# ========================================
# LOGGING CONFIGURATION
# ========================================

LOGGING_CONFIG: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'chartastrophe.log',
            'mode': 'w',
            'encoding': 'utf-8'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'json',
            'filename': 'chartastrophe_errors.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'chartastrophe': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'werkzeug': {  # Flask development server
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# ========================================
# FLASK CONFIGURATION
# ========================================

FLASK_CONFIG: Dict[str, Any] = {
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
    'DEBUG': os.environ.get('FLASK_DEBUG', 'True').lower() == 'true',
    'TESTING': False,
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'MAX_CONTENT_LENGTH': SECURITY_CONFIG['max_file_size']
}

# ========================================
# EXTERNAL API CONFIGURATION
# ========================================

API_CONFIG: Dict[str, Any] = {
    'timeout': 10,                  # Timeout for external APIs
    'retries': 3,                   # Number of attempts
    'backoff_factor': 0.3,          # Exponential backoff factor
    'user_agent': 'Chartastrophe/1.0 (Educational Purpose)',
    'rate_limit_delay': 1           # Delay between requests (seconds)
}

# ========================================
# DEEPL TRANSLATION CONFIGURATION
# ========================================

DEEPL_CONFIG: Dict[str, Any] = {
    # Pour utiliser DeepL, définissez votre clé API dans une variable d'environnement
    # ou utilisez la version gratuite (limitée à 500 000 caractères/mois)
    'api_key': os.environ.get('DEEPL_API_KEY', None),  # Clé API DeepL (optionnelle)
    'use_free_api': True,           # Utiliser l'API gratuite si pas de clé
    'source_lang': 'EN',            # Langue source (anglais)
    'target_lang': 'FR',            # Langue cible (français)
    'formality': 'default',         # Niveau de formalité (default, more, less)
    'timeout': 5,                   # Timeout pour les requêtes DeepL
    'max_retries': 2,               # Nombre de tentatives en cas d'échec
    'fallback_to_dict': True,       # Utiliser le dictionnaire si DeepL échoue
    'cache_translations': True      # Mettre en cache les traductions
}

# ========================================
# ENVIRONMENT VARIABLES
# ========================================

def get_env_config() -> Dict[str, Any]:
    """Get configuration from environment variables."""
    return {
        'HOST': os.environ.get('HOST', '127.0.0.1'),
        'PORT': int(os.environ.get('PORT', 5000)),
        'ENV': os.environ.get('FLASK_ENV', 'development'),
        'DEBUG': os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    } 