"""
Utility functions for managing the server.
"""
# FloatingTools imports
import FloatingTools

# python imports
import webbrowser

# flask imports
from flask import request, Flask

# python imports
import os
from threading import Thread

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__)
DASHBOARD_STATIC = os.path.join(DASHBOARD_DIRECTORY_ROOT, 'static')
DASHBOARD_TEMPLATES = os.path.join(DASHBOARD_DIRECTORY_ROOT, 'templates')

# -- server set up
SERVER = Flask('Floating Tools Dashboard',
               template_folder=DASHBOARD_TEMPLATES,
               static_path=DASHBOARD_STATIC)

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


def setDashboardVariable(key, value):
    """
    Pass a variable to the dashboard web front end.
    :param key: 
    :param value: 
    :return: 
    """
    FloatingTools.Dashboard.SITE_ENV[key] = value
