# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template

# package imports
from utilities import SERVER


@SERVER.route('/settings')
def renderSettings():
    """
    Render settings page to configure Floating Tools
    :return: 
    """

    repositories = ['etgteg', 'hrthrth', 'qwrerterg', 'aregregrae']

    return render_template('Settings.html', repositories=repositories)


def settings():
    """
    Launch settings page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='http://127.0.0.1:5000/settings')
