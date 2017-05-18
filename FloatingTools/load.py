"""
Handles all loading operations
"""
__all__ = [
    'loadTools'
]

# python imports
import os
import sys
import json
import time
import threading
import webbrowser
from functools import partial

# FloatingTools imports
import FloatingTools

# GitHub imports
from github import GithubException

# Globals
WILDCARDS = dict(
    Applications=dict(
        value=FloatingTools.APP_WRAPPER.name() if FloatingTools.APP_WRAPPER is not None else 'Generic',
        doc='Represents the current application.'),
    OS=dict(
        value=os.name,
        doc='The operating systems python name.')
)
PYTHON_MODULES = {}

# add to dashboard
FloatingTools.Dashboard.setDashboardVariable('wildcards', WILDCARDS)


def repoWalk(repo):
    """
    --private--
    :param repo: 
    :return: 
    """
    global PYTHON_MODULES

    # add this repo to the registered python modules
    if repo.full_name not in PYTHON_MODULES:
        PYTHON_MODULES[repo.full_name] = []

    # get local repository path
    repoPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, *repo.full_name.split('/'))

    for root, dirs, files in os.walk(repoPath):

        # py detection
        isPackage = False
        hasPython = False
        for fo in files:
            if isPackage and hasPython:
                break
            if fo.endswith('.py'):
                hasPython = True
            if fo == '__init__.py':
                isPackage = True

        # handle python files
        if hasPython:
            pyPath = root
            if isPackage:
                pyPath = os.path.dirname(pyPath)
                pyName = os.path.basename(pyPath)
                if pyName not in PYTHON_MODULES[repo.full_name]:
                    PYTHON_MODULES[repo.full_name].append(pyName)

            sys.path.append(pyPath)

        # loop over contents
        for fo in files:
            if fo.endswith('.py') and fo != '__init__.py':
                PYTHON_MODULES[repo.full_name].append(fo.replace('.py', ''))
                continue

            if FloatingTools.APP_WRAPPER:

                # filter out files that do not pertain to this application
                basename, ext = os.path.splitext(fo)
                if ext not in FloatingTools.APP_WRAPPER.fileTypes():
                    continue

                # register tool with the application
                FloatingTools.APP_WRAPPER.addMenuEntry(
                    os.path.join(FloatingTools.__name__, repo.full_name.replace('/', '.'), root.replace(repoPath, ''), fo).replace('\\', '/').replace('//', '/'),
                    partial(FloatingTools.APP_WRAPPER.loadFile, fo, ext))


def timeWalk(repository, repoObj, path):
    # execute repo walk with timer
    startTime = time.time()
    repoWalk(repoObj)
    endTime = time.time()

    # load the source data to be stored
    sourceData = FloatingTools.sourceData()
    if 'loadTimes' not in sourceData:
        sourceData['loadTimes'] = {}

    # add the repo to the load times catalog
    if repository not in sourceData['loadTimes']:
        sourceData['loadTimes'][repository] = {}

    # log the data and update
    sourceData['loadTimes'][repository][
        FloatingTools.APP_WRAPPER.name() if FloatingTools.APP_WRAPPER else 'Generic'
    ] = endTime - startTime
    FloatingTools.updateSources(sourceData)


def loadTools():
    """
    Main tool loading function.
    :return: 
    """
    # set up dashboard in the application wrapper if there is one loaded.
    if FloatingTools.APP_WRAPPER:
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Dashboard/Settings',
                                               FloatingTools.Dashboard.settings)
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Network Toolboxes',
                                               FloatingTools.Dashboard.toolShed)

    # pull repository data
    repoData = FloatingTools.sourceData()['repositories']

    # log threads
    threads = []

    # begin repo loop.
    for repo in repoData:

        # skip loading if the isn't requested
        if not repo['load']:
            continue

        # connect to the repository
        FloatingTools.FT_LOOGER.info('Loading Repository: ' + repo['name'])
        repoName = repo['name']
        repo = FloatingTools.gitHubConnect().get_repo(repoName)

        localRepoPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, *repo.full_name.split('/'))
        if not os.path.exists(localRepoPath):
            FloatingTools.downloadToolbox(repo)

        # load toolbox data
        toolboxData = dict(paths=['/'])
        if 'toolbox.json' in os.listdir(localRepoPath):
            toolboxData = json.loads(repo.get_file_contents('/toolbox.json').decoded_content)
        else:
            try:
                toolboxData = json.loads(repo.get_file_contents('/toolbox.json').decoded_content)
            except GithubException:
                pass

        if FloatingTools.APP_WRAPPER:
            # make tool box information menus
            toolboxPath = FloatingTools.__name__ + '/' + repo.full_name.replace('/', '.')
            repoURL = "https://github.com/" + repo.full_name
            FloatingTools.APP_WRAPPER.addMenuEntry(toolboxPath + '/Open on Github',
                                                   partial(webbrowser.open, repoURL)
                                                   )
            FloatingTools.APP_WRAPPER.addMenuEntry(toolboxPath + '/License',
                                                   partial(webbrowser.open, repoURL + '/blob/master/LICENSE')
                                                   )
            FloatingTools.APP_WRAPPER.addMenuEntry(toolboxPath + '/About',
                                                   partial(webbrowser.open, repoURL + '/blob/master/README.md')
                                                   )
            FloatingTools.APP_WRAPPER.addMenuSeparator(toolboxPath)

        # loop over the toolbox path
        for path in toolboxData['paths']:

            # handle wildcard logic
            for card in WILDCARDS:
                path = path.replace('{%s}' % card, WILDCARDS[card]['value'])

            # spawn thread if it is a thread supporting application
            if FloatingTools.APP_WRAPPER and not FloatingTools.APP_WRAPPER.MULTI_THREAD:
                timeWalk(repoName, repo, path)
            else:
                t = threading.Thread(name=repoName, target=timeWalk, args=(repoName, repo, path))
                t.setDaemon(True)
                threads.append(t)
                t.start()

    # hold the main thread till load up is complete.
    for thread in threads:
        thread.join()

    if FloatingTools.APP_WRAPPER:
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/HatfieldFX',
                                               lambda: webbrowser.open("http://www.hatfieldfx.com/floating-tools"))
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/Repository',
                                               lambda: webbrowser.open("https://github.com/aldmbmtl/FloatingTools"))


# set virtual system variables
FloatingTools.Dashboard.setDashboardVariable('python_cloud', PYTHON_MODULES)