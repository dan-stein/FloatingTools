# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect, render_template_string

# package imports
from utilities import SERVER, ErrorPage

# python imports
import os
import imp
import traceback


@SERVER.route('/tool_shed', methods=['GET', 'POST'])
def renderToolShed():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """

    # grab latest source data.
    FloatingTools.Dashboard.setDashboardVariable('toolboxes', FloatingTools.toolboxes())
    FloatingTools.Dashboard.setDashboardVariable('sorted_toolboxes', sorted(FloatingTools.toolboxes().keys()))

    # create module key
    modules = {}
    for box in FloatingTools.Dashboard.dashboardEnv()['python_cloud'].values():
        for path in box:
            modules[path] = os.path.basename(path).replace('.py', '')
    FloatingTools.Dashboard.setDashboardVariable('python_module_key', modules)

    return render_template('ToolShed.html', **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/tool_shed/_save')
def saveToolShed():
    # grab toolbox
    for arg in request.args:
        try:
            toolbox, module = arg.split('|%|', 1)

            handler = FloatingTools.getToolbox(toolbox)

            # pull then set settings
            currentSettings = handler.settings()

            # add application if its not in the app list
            appName = FloatingTools.wrapperName()
            if appName not in currentSettings['apps']:
                currentSettings['apps'][appName] = dict()

            currentSettings['apps'][appName][module] = True if request.args.get(arg) == 'true' else False
            continue

        except:
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
        mod = imp.load_source(os.path.basename(request.args.get('module')).replace('.py', ''), request.args.get('module'))
        reload(mod)
        FloatingTools.FT_LOOGER.info('Module Imported/Reloaded: %s' % mod)
    except Exception, e:
        return render_template_string(
            ErrorPage(errorType=e, traceback=traceback.format_exc()),
            **FloatingTools.Dashboard.dashboardEnv()
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
    """
    FloatingTools.Dashboard.startServer(url='tool_shed')
