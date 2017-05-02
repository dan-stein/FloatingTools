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
    return render_template('Settings.html')

def settings():
    """
    Launch settings page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='settings')
