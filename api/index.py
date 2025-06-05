import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wsgi import app

def handler(request):
    """Point d'entrée pour Vercel."""
    return app 