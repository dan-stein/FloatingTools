# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template

# package imports
from utilities import SERVER


@SERVER.route('/settings', methods=['GET', 'POST'])
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
    FloatingTools.Dashboard.startServer(url='settings')
