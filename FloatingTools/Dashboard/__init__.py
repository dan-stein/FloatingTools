"""
Dashboard handles the web interface
"""
# flask imports
from flask import Flask
from flask.blueprints import Blueprint

# dashboard imports
from utilities import startServer

# python imports
import os

# globals

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__)
DASHBOARD_TEMPLATES = os.path.join(DASHBOARD_DIRECTORY_ROOT, 'templates')

# -- server set up
SERVER = Flask('Floating Tools Dashboard')
SERVER.register_blueprint(Blueprint('Modular Application', __name__, template_folder=DASHBOARD_TEMPLATES))
