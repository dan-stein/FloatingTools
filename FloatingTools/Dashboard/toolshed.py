# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template

# package imports
from utilities import SERVER


@SERVER.route('/tool_shed', methods=['GET', 'POST'])
def renderToolShed():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """
    return render_template('ToolShed.html', **FloatingTools.Dashboard.dashboardEnv())


def toolShed():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='tool_shed')
