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
from getpass import getuser
from threading import Thread

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__).replace('\\', '/')
DASHBOARD_TEMPLATES = DASHBOARD_DIRECTORY_ROOT + '/templates'

# -- server set up
SERVER = Flask('Floating Tools Dashboard', template_folder=DASHBOARD_TEMPLATES)

# -- variables
HOST = '0.0.0.0'
PORT = 5000
ADDRESS = 'http://%(HOST)s:%(PORT)s/' % locals()


def startServer(url=None):
    """
    Launch the server instance.
    
    :parameter url: 
    """
    # start the server
    t = Thread(name='FloatingTools Web-Service', target=SERVER.run, args=(HOST, PORT))
    t.start()

    # open the url that is passed
    if url:
        if url == '/':
            webbrowser.open(ADDRESS)
        else:
            webbrowser.open(ADDRESS + url)


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


def dashboardEnv():
    """
    Get the dashboard env variables.
    :return: 
    """
    return FloatingTools.Dashboard.SITE_ENV
