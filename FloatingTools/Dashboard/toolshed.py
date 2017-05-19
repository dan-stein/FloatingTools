# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# package imports
from utilities import SERVER

# python imports
import os
import pydoc
import shutil
import urllib
import traceback


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


@SERVER.route('/tool_shed/_save')
def saveToolShed():
    sourceData = FloatingTools.sourceData()

    repositoryNames = [repo['name'] for repo in sourceData['repositories']]

    for repo in request.args:

        value = request.args.get(repo)

        if '.' in repo:
            toolbox, module = repo.split('.')

            toolboxSettings = None
            for box in sourceData['repositories']:
                if box['name'] == toolbox:
                    toolboxSettings = box
                    break

            app = 'Generic'
            if FloatingTools.APP_WRAPPER:
                app = FloatingTools.APP_WRAPPER.name()
            if app not in toolboxSettings:
                toolboxSettings[app] = {}

            if value == 'true':
                value = True
            else:
                value = False

            toolboxSettings[app][module] = value
            continue

        savedRepo = None
        for savedRepo in sourceData['repositories']:
            if savedRepo['name'] == repo:
                break
        if value == 'true':
            value = True
        else:
            value = False
        if repo not in repositoryNames:
            sourceData['repositories'].append({'name': repo, 'load': value})
        else:
            savedRepo['load'] = value

    FloatingTools.updateSources(sourceData)

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


@SERVER.route('/tool_shed/_doc')
def pyDoc():
    try:
        mod = __import__(request.args.get('module'))
    except Exception, e:
        return render_template('Error.html', error_type=e, error=traceback.format_exc())

    return render_template('PyDoc.html', module=request.args.get('module'), doc=pydoc.render_doc(mod, "Help on %s"))


@SERVER.route('/tool_shed/_addLocalToolbox')
def _addLocalToolbox():
    # get data
    username = request.args.get('username')
    repo = request.args.get('toolbox')

    # validate the username and repository are passed
    if not username and not repo:
        return redirect('/tool_shed')

    # repo path
    path = "%(username)s/%(repo)s" % locals()

    # load the source data
    sourceData = FloatingTools.sourceData()
    repositories = [repo['name'] for repo in sourceData['repositories']]

    if path not in repositories:
        sourceData['repositories'].append(dict(name=path, load=False))
        FloatingTools.updateSources(sourceData)

    return redirect('/tool_shed')


@SERVER.route('/tool_shed/_addToolbox')
def _addToolbox():
    # get data
    username = request.args.get('username')
    repo = request.args.get('toolbox')

    # validate the username and repository are passed
    if not username and not repo:
        return redirect('/tool_shed')

    # repo path
    path = "%(username)s/%(repo)s" % locals()

    # load the source data
    sourceData = FloatingTools.sourceData()
    repositories = [repo['name'] for repo in sourceData['repositories']]

    if path not in repositories:
        sourceData['repositories'].append(dict(name=path, load=False))
        FloatingTools.updateSources(sourceData)

    return redirect('/tool_shed')


@SERVER.route('/tool_shed/_removeToolbox')
def _removeToolbox():
    sources = FloatingTools.sourceData()

    # get data
    for toolbox in request.args:

        # clean local cached package
        localCache = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, *toolbox.split('/'))
        userDirectory = os.path.dirname(localCache)
        if os.path.exists(localCache):
            shutil.rmtree(localCache)

        # remove user directory if it is empty
        if not os.listdir(userDirectory):
            shutil.rmtree(userDirectory)

        # remove from the resources list
        for repo in sources['repositories']:
            if repo['name'] == toolbox:
                sources['repositories'].pop(sources['repositories'].index(repo))
                break

    FloatingTools.updateSources(sources)

    return redirect('/tool_shed')


def toolShed():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='tool_shed')
