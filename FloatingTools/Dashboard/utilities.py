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
import socket
from ui import *
from threading import Thread
from traceback import format_exc

# -- directories
DASHBOARD_DIRECTORY_ROOT = os.path.dirname(__file__).replace('\\', '/')
DASHBOARD_TEMPLATES = DASHBOARD_DIRECTORY_ROOT + '/templates'

# -- server set up
SERVER = Flask('Floating Tools Dashboard', template_folder=DASHBOARD_TEMPLATES, static_folder=DASHBOARD_TEMPLATES)

# -- variables
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDRESS = 'http://%(HOST)s:%(PORT)s/' % locals()
SERVER_THREAD = None


class ErrorPage(Page):
    def __init__(self):
        info = format_exc()
        errorType = info.strip().rsplit('\n', 1)[1]

        super(ErrorPage, self).__init__(errorType)

        panel = Panel()
        panel.addToHeader(Header(size=4, value=Element('strong', Font(errorType, color='red'))))
        textArea = Element('textarea', '\n' + info, wrap='soft', rows=15, cols=150)
        textArea.addFlag('disabled')
        panel.addTobody(textArea)
        self.add(panel)


def startServer(url=None):
    """
    Launch the server instance.
    
    :parameter url: 
    """
    global SERVER_THREAD

    # start the server
    SERVER_THREAD = Thread(name='FloatingTools Web-Service', target=SERVER.run, args=(HOST, PORT), kwargs={'threaded': True})
    if FloatingTools.wrapperName() != 'Generic':
        SERVER_THREAD.setDaemon(True)
    SERVER_THREAD.start()

    # ping peers
    from network import refreshPeers
    refreshPeers()

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

    p = Div()
    p.addValue(Center(Header('Server successfully shut down', 3)))
    p.addDivider()
    p.addValue(Center(Header('Close this tab if you\'d like.', 5)))

    return p.html()


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
    FloatingTools.Dashboard.setDashboardVariable('is_user', True)
    try:
        if request.remote_addr != HOST:
            FloatingTools.Dashboard.setDashboardVariable('is_user', False)
    except RuntimeError:
        pass

    return FloatingTools.Dashboard.SITE_ENV
