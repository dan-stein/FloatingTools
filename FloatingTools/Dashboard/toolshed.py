# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

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


@SERVER.route('/tool_shed/_save')
def saveToolShed():
    sourceData = FloatingTools.sourceData()

    repositoryNames = [repo['name'] for repo in sourceData['repositories']]

    for repo in request.args:
        value = request.args.get(repo)
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
