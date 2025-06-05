"""
Chartastrophe - Flask application entry point
Absurd and hilarious correlation generator
"""
import logging.config
import os
import sys
from src.web.app import create_app
from src.config import SECURITY_CONFIG, PERFORMANCE_CONFIG, FLASK_CONFIG, get_env_config

# Configuration du logging
try:
    logging.config.fileConfig('logging.conf')
except FileNotFoundError:
    # Basic configuration if file doesn't exist
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger('chartastrophe')

def create_application():
    """Create and configure Flask application."""
    try:
        app = create_app()
        
        # Configuration de sécurité
        app.config.update(
            SESSION_COOKIE_SECURE=False,  # True in production with HTTPS
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax',
            PERMANENT_SESSION_LIFETIME=SECURITY_CONFIG['session_timeout'],
            MAX_CONTENT_LENGTH=SECURITY_CONFIG['max_file_size']
        )
        
        # Configuration Flask depuis config.py
        app.config.update(FLASK_CONFIG)
        
        logger.info("Chartastrophe application created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Error creating application: {e}")
        sys.exit(1)

# Création de l'application
app = create_application()

if __name__ == '__main__':
    # Configuration depuis les variables d'environnement
    env_config = get_env_config()
    
    logger.info("🚀 Starting Chartastrophe server...")
    logger.info(f"📊 Application accessible at: http://{env_config['HOST']}:{env_config['PORT']}")
    logger.info(f"🎯 Environment: {env_config['ENV']}")
    logger.info(f"🔧 Debug: {'Enabled' if env_config['DEBUG'] else 'Disabled'}")
    
    try:
        # Start server with optimized parameters
        app.run(
            debug=env_config['DEBUG'],
            host=env_config['HOST'],
            port=env_config['PORT'],
            threaded=True,
            use_reloader=env_config['DEBUG'],
            use_debugger=env_config['DEBUG']
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Error starting server: {e}")
        sys.exit(1) 