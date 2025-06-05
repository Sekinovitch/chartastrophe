"""
Package containing the web interface of the application.
"""

from flask import Flask

app = Flask(__name__, 
           template_folder='templates',  # Specify the templates folder
           static_folder='static'        # Specify static files folder
) 