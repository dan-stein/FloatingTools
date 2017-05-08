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
import time

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

    localRepos = {}
    for repo in FloatingTools.gitHubConnect().get_user().get_repos():
        localRepos[repo.name] = repo

    # get the user repositories and add to the dashboard env
    FloatingTools.Dashboard.setDashboardVariable('user_repos', sorted(localRepos.keys()))

    # handle local toolbox
    localToolbox = request.args.get("toolbox")
    if not localToolbox:
        localToolbox = localRepos.keys()[0]
    FloatingTools.Dashboard.setDashboardVariable('toolbox', localToolbox)
    FloatingTools.Dashboard.setDashboardVariable('toolbox_data', None)

    # validate the local toolbox
    data = None
    try:
        data = json.loads(localRepos[localToolbox].get_file_contents('/toolbox.json').decoded_content)
    except UnknownObjectException:
        pass
    finally:
        FloatingTools.Dashboard.setDashboardVariable('toolbox_data', data)

    FloatingTools.Dashboard.setDashboardVariable('benchmark_data', _BENCHMARK_DATA)
    FloatingTools.Dashboard.setDashboardVariable('benchmark_file_count', len(_BENCHMARK_DATA['files']))
    FloatingTools.Dashboard.setDashboardVariable('benchmark_directory_count', len(_BENCHMARK_DATA['directories']))

    return render_template('Toolbox.html', **FloatingTools.Dashboard.dashboardEnv())


def recursiveRepoWalk(repo, path):
    """
    --private--
    :return: 
    """
    global _BENCHMARK_DATA

    try:
        repoContents = repo.get_dir_contents(path.strip('/'))

        for fo in repoContents:
            # loop over directories
            if fo.type == 'dir':
                _BENCHMARK_DATA['directories'].append(fo.name)
                recursiveRepoWalk(repo, fo.path)
            else:
                _BENCHMARK_DATA['files'].append(fo.name)

    except GithubException:
        pass


@SERVER.route('/toolbox/_setup')
def setUpToolbox():
    """
    --private--
    :return: 
    """
    toolbox = FloatingTools.Dashboard.dashboardEnv()['toolbox']
    toolboxRepo = FloatingTools.gitHubConnect().get_user().get_repo(toolbox)

    toolboxRepo.create_file(
        '/toolbox.json',
        'Setting up as FloatingTools Toolbox!',
        json.dumps(dict(paths=[]), indent=4, sort_keys=True)
    )

    return redirect('/toolbox?toolbox=' + toolbox)


@SERVER.route('/toolbox/_benchmark')
def benchmark():
    """
    --private--
    :return: 
    """
    global _BENCHMARK_DATA
    _BENCHMARK_DATA = dict(directories=[], files=[], applications={}, paths={})

    toolbox = FloatingTools.Dashboard.dashboardEnv()['toolbox']
    toolboxRepo = FloatingTools.gitHubConnect().get_user().get_repo(toolbox)
    contentFile = toolboxRepo.get_file_contents('toolbox.json')
    toolboxMap = json.loads(contentFile.decoded_content)

    paths = toolboxMap['paths']
    if not paths:
        paths = ['/']

    for path in paths:
        if '{Applications}' in path:
            for app in FloatingTools.APP_WRAPPERS:
                try:
                    appPath = path.replace('{Applications}', app.NAME)
                    toolboxRepo.get_dir_contents(appPath.strip('/'))

                    if app.NAME not in _BENCHMARK_DATA['applications']:
                        _BENCHMARK_DATA['applications'][app.NAME] = {}

                    startTime = time.time()
                    recursiveRepoWalk(toolboxRepo, appPath)
                    endTime = time.time()

                    _BENCHMARK_DATA['applications'][app.NAME][appPath] = endTime - startTime
                except GithubException:
                    pass

        else:
            try:
                startTime = time.time()
                recursiveRepoWalk(toolboxRepo, path)
                endTime = time.time()

                _BENCHMARK_DATA['paths'][path] = endTime - startTime

            except GithubException:
                pass

    return redirect('/toolbox?toolbox=' + toolbox)


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


@SERVER.route('/toolbox/_save')
def saveToolbox():
    """
    --private--
    :return: 
    """
    return redirect('/toolbox')


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
