# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template

# package imports
from utilities import SERVER

# python imports
import urllib


@SERVER.route('/tool_shed', methods=['GET', 'POST'])
def renderToolShed():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """
    # tool shed link
    link = "https://github.com/aldmbmtl/FloatingTools/wiki/Tool-Shed"
    shed = urllib.urlopen(link).read().split('<div class="markdown-body">')[1].split('</div>')[0]

    toolshed = []

    for i in shed.split('<li>'):
        if '</li>' not in i:
            continue
        toolshed.append(i.split('</li>')[0])

    # grab latest source data.
    FloatingTools.Dashboard.setDashboardVariable('sources', FloatingTools.sourceData())
    FloatingTools.Dashboard.setDashboardVariable('tool_shed', toolshed)

    return render_template('ToolShed.html', **FloatingTools.Dashboard.dashboardEnv())


def toolShed():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='tool_shed')
