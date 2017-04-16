"""
Utility functions for managing the server.
"""
# python imports
import webbrowser

# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, Flask
from flask.blueprints import Blueprint

# python imports
import os

# globals

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__)
DASHBOARD_TEMPLATES = os.path.join(DASHBOARD_DIRECTORY_ROOT, 'templates')

# -- server set up
SERVER = Flask('Floating Tools Dashboard')
SERVER.register_blueprint(Blueprint('Modular Application', __name__, template_folder=DASHBOARD_TEMPLATES))


def startServer(url=None):
    """
    Launch the server instance
    :type url: 
    :return: 
    """
    # open the url that is passed
    if url:
        webbrowser.open(url)

    # start the server
    SERVER.run()


@SERVER.route('/shutdown', methods=['POST'])
def stopServer():
    """
    This is internally used for closing the server from the website.
    :return: 
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
