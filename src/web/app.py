"""
Flask web interface application.
"""
from flask import Flask, Blueprint
from . import routes
import logging
import os
from pathlib import Path
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

# Create main blueprint
bp = Blueprint('web', __name__)

def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Application configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production'),
        CACHE_DIR=Path(os.getenv('CACHE_DIR', 'data/cache')),
        CACHE_EXPIRATION=int(os.getenv('CACHE_EXPIRATION', 3600)),
        # Session configuration for language support
        SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=86400  # 24 hours
    )
    
    # Configure template and static folders
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    # Create cache directory if needed
    Path(app.config['CACHE_DIR']).mkdir(parents=True, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(routes.bp)
    
    logger.info("Flask application created successfully")
    return app

# Create the app instance for direct import
app = create_app()