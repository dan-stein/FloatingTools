# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# package imports
from utilities import SERVER

# python imports
import traceback


@SERVER.route('/tool_shed', methods=['GET', 'POST'])
def renderToolShed():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """
    # grab latest source data.
    FloatingTools.Dashboard.setDashboardVariable('toolboxes', FloatingTools.toolboxes())

    return render_template('ToolShed.html', **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/tool_shed/_save')
def saveToolShed():

    # grab toolbox
    for arg in request.args:
        if '.' in arg:
            print arg
        else:
            handler = FloatingTools.getToolbox(arg)

            # pull then set settings
            currentSettings = handler.settings()
            currentSettings['load'] = True
            if request.args.get(arg) == 'false':
                currentSettings['load'] = False

            # save
            handler.updateSettings(currentSettings)

    return redirect('/tool_shed')


@SERVER.route('/tool_shed/_import')
def pyImport():
    try:
        __import__(request.args.get('module'))
    except Exception, e:
        return render_template('Error.html',
                               error_type=e,
                               error=traceback.format_exc()
                               )
    return redirect('/tool_shed')


@SERVER.route('/tool_shed/_addToolbox')
def _addToolbox():
    # vars
    source = {}
    service = None

    # pull vars from the form data passed from the website
    for key in request.args:
        if key == 'service':
            service = request.args.get(key)
        else:
            source[key] = request.args.get(key)

    # create new toolbox
    FloatingTools.createToolbox(service, source)

    return redirect('/tool_shed')


@SERVER.route('/tool_shed/_removeToolbox')
def _removeToolbox():

    # get data
    for toolbox in request.args:
        box = FloatingTools.getToolbox(toolbox)
        if box:
            box.uninstall()

    return redirect('/tool_shed')


def toolShed():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='tool_shed')
