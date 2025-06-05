"""
Main package for Correlactions.
"""
from flask import Flask
from pathlib import Path
import logging
from dotenv import load_dotenv
import os

# Loading environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.getenv('LOG_FILE', 'correlactions.log')
)

logger = logging.getLogger(__name__)

__version__ = '1.0.0'

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    
    # Application configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev'),
        CACHE_DIR=Path(os.getenv('CACHE_DIR', 'data/cache')),
        CACHE_EXPIRATION=int(os.getenv('CACHE_EXPIRATION', 3600))
    )
    
    # Configuration of template and static folders
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/templates')
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/static')
    
    # Create cache directory if needed
    Path(app.config['CACHE_DIR']).mkdir(parents=True, exist_ok=True)
    
    # Register blueprints
    from .web.app import bp as web_bp
    app.register_blueprint(web_bp)
    
    return app 