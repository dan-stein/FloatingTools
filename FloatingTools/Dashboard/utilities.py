"""
Utility functions for managing the server.
"""
# python imports
import webbrowser

# flask imports
from flask import request, Flask
from flask.blueprints import Blueprint

# python imports
import os
from threading import Thread

# globals

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__)
DASHBOARD_TEMPLATES = os.path.join(DASHBOARD_DIRECTORY_ROOT, 'templates')

# -- server set up
SERVER = Flask('Floating Tools Dashboard')
SERVER.register_blueprint(Blueprint('Modular Application', __name__, template_folder=DASHBOARD_TEMPLATES))

# -- variables
HOST = '127.0.0.1'
PORT = 5000
ADDRESS = 'http://%(HOST)s:%(PORT)s/' % locals()


def startServer(url=None):
    """
    Launch the server instance
    :type url: 
    :return: 
    """
    # open the url that is passed
    if url:
        webbrowser.open(ADDRESS + url)

    # start the server
    t = Thread(target=SERVER.run, args=(HOST, PORT))
    t.start()


@SERVER.route('/shutdown', methods=['GET', 'POST'])
def stopServer():
    """
    This is internally used for closing the server from the website.
    :return: 
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    return "Server shut down... Close this window."
