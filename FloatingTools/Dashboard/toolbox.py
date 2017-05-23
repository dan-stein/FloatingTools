# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# github imports
from github import UnknownObjectException, GithubException

# package imports
from utilities import SERVER

# python imports
import json


# private globals
_BENCHMARK_DATA = dict(directories=[], files=[], applications={}, paths={})


def toolbox():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='toolbox')


@SERVER.route('/toolbox', methods=['GET', 'POST'])
def renderToolbox():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """
    # handle local toolbox
    localToolbox = request.args.get("toolbox")

    localRepos = {}
    for repo in FloatingTools.gitHubConnect().get_user().get_repos():
        localRepos[repo.name] = repo

    # check if the user has any repositories set up.
    FloatingTools.Dashboard.setDashboardVariable('has_repo', False)
    if localRepos:
        FloatingTools.Dashboard.setDashboardVariable('has_repo', True)
        if not localToolbox:
            localToolbox = sorted(localRepos.keys())[0]

    # register toolbox
    FloatingTools.Dashboard.setDashboardVariable('toolbox', localToolbox)

    # get the user repositories and add to the dashboard env
    FloatingTools.Dashboard.setDashboardVariable('username', FloatingTools.gitHubConnect().get_user().login)
    FloatingTools.Dashboard.setDashboardVariable('user_repos', sorted(localRepos.keys()))

    # pull the data for the repo
    FloatingTools.Dashboard.setDashboardVariable('toolbox_data', None)
    FloatingTools.Dashboard.setDashboardVariable('has_lic', False)
    FloatingTools.Dashboard.setDashboardVariable('has_readme', False)

    try:
        repo = FloatingTools.gitHubConnect().get_user().get_repo(localToolbox)
        repo.get_file_contents('/LICENSE')
        FloatingTools.Dashboard.setDashboardVariable('has_lic', True)
    except (GithubException, UnknownObjectException):
        pass

    try:
        repo = FloatingTools.gitHubConnect().get_user().get_repo(localToolbox)
        repo.get_file_contents('/README.md')
        FloatingTools.Dashboard.setDashboardVariable('has_readme', True)
    except (GithubException, UnknownObjectException):
        pass

    try:
        repo = FloatingTools.gitHubConnect().get_user().get_repo(localToolbox)
        FloatingTools.Dashboard.setDashboardVariable('toolbox_data', json.loads(
            repo.get_file_contents('/toolbox.json').decoded_content
        ))
    except (GithubException, UnknownObjectException):
        pass

    return render_template('Toolbox.html', **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/toolbox/_createToolbox')
def createToolbox():
    """
    --private--
    :return: 
    """
    # pull request data
    name = request.args.get('name')

    # do nothing if name is blank
    if not name:
        return redirect('/toolbox')

    # set env var for the toolbox in question
    FloatingTools.Dashboard.setDashboardVariable('toolbox', name)

    # pull users env
    user = FloatingTools.gitHubConnect().get_user()

    # create the repository if it doesnt exist
    for repo in user.get_repos():
        if repo.name == name:
            return redirect('/toolbox?toolbox=' + name)

    # create toolbox repository
    user.create_repo(name)
    _setUpToolbox()

    # redirect
    return redirect('/toolbox?toolbox=' + FloatingTools.Dashboard.dashboardEnv()['toolbox'])


@SERVER.route('/toolbox/_setup')
def setUpToolbox():
    """
    --private--
    :return: 
    """
    _setUpToolbox()
    return redirect('/toolbox?toolbox=' + FloatingTools.Dashboard.dashboardEnv()['toolbox'])


@SERVER.route('/toolbox/_addPath')
def addToolboxPath():
    """
    --private--
    :return: 
    """
    toolbox = FloatingTools.Dashboard.dashboardEnv()['toolbox']
    path = request.args.get('path')

    toolboxRepo = FloatingTools.gitHubConnect().get_user().get_repo(toolbox)
    contentFile = toolboxRepo.get_file_contents('toolbox.json')
    toolboxMap = json.loads(contentFile.decoded_content)

    if path not in toolboxMap['paths']:
        toolboxMap['paths'].append(path)

    toolboxRepo.update_file(
        path='/toolbox.json',
        message='Adding %s to toolbox.' % path,
        content=json.dumps(toolboxMap, indent=4, sort_keys=True),
        sha=contentFile.sha
    )

    return redirect('/toolbox?toolbox=' + toolbox)


@SERVER.route('/toolbox/_removePath')
def removeToolboxPath():
    """
    --private--
    :return: 
    """
    toolbox = FloatingTools.Dashboard.dashboardEnv()['toolbox']

    toolboxRepo = FloatingTools.gitHubConnect().get_user().get_repo(toolbox)
    contentFile = toolboxRepo.get_file_contents('toolbox.json')
    toolboxMap = json.loads(contentFile.decoded_content)

    for path in request.args:
        if path in toolboxMap['paths']:
            toolboxMap['paths'].remove(path)

    toolboxRepo.update_file(
        path='/toolbox.json',
        message='Removing %s from toolbox.' % str([path for path in request.args]),
        content=json.dumps(toolboxMap, indent=4, sort_keys=True),
        sha=contentFile.sha
    )

    return redirect('/toolbox?toolbox=' + toolbox)


@SERVER.route('/toolbox_paths')
def toolboxPaths():
    return render_template('ToolboxPaths.html')


def _setUpToolbox():
    toolbox = FloatingTools.Dashboard.dashboardEnv()['toolbox']
    toolboxRepo = FloatingTools.gitHubConnect().get_user().get_repo(toolbox)

    toolboxRepo.create_file(
        '/toolbox.json',
        'Setting up as FloatingTools Toolbox!',
        json.dumps(dict(paths=[]), indent=4, sort_keys=True)
    )