"""
Handles all loading operations
"""
__all__ = [
    'cloudImport',
    'loadTools'
]

# python imports
import os
import sys
import imp
import json
import time
import threading
import traceback
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

# add to dashboard
FloatingTools.Dashboard.setDashboardVariable('wildcards', WILDCARDS)


def cloudImport(repo, path):
    """
    Import a module from Github.
    :param repo: 
    :param path: 
    :return: 
    """
    try:
        moduleName = os.path.splitext(os.path.basename(path))[0]
        mod = imp.new_module(moduleName)

        code = compile(
            str(FloatingTools.gitHubConnect().get_repo(repo).get_file_contents(path).decoded_content),
            '<string>',
            'exec'
        )

        # execute the code object
        exec code in mod.__dict__

        sys.modules[moduleName] = mod

        return mod
    except:
        print "Failed to import %s %s" % (repo, path)
        traceback.print_exc()


def repoWalk(repo, path, root):
    """
    --private--
    :param repo: 
    :param path:
    :param root: 
    :return: 
    """
    try:
        repoContents = repo.get_dir_contents(path)

        for fo in repoContents:

            # loop over directories
            if fo.type == 'dir':
                repoWalk(repo, fo.path, root)

            elif fo.name == 'ft_init.py':
                # built in init file for floating tools
                if FloatingTools.WRAPPER:
                    FloatingTools.WRAPPER.cloudImport(repo.full_name, fo.path)
                else:
                    cloudImport(repo.full_name, fo.path)

            elif FloatingTools.APP_WRAPPER:
                # filter out files that do not pertain to this application
                basename, ext = os.path.splitext(fo.name)
                if ext not in FloatingTools.APP_WRAPPER.fileTypes():
                    continue

                # register tool with the application
                FloatingTools.APP_WRAPPER.addMenuEntry(
                    os.path.join(
                        FloatingTools.__name__,
                        repo.full_name.replace('/', '.'),
                        fo.path
                    ).replace(root, '').replace('//', '/'),
                    partial(FloatingTools.APP_WRAPPER.loadFile, fo, ext))

            else:
                pass

    except GithubException:
        FloatingTools.FT_LOOGER.error(path + ' is not a valid path in this toolbox.')


def timeWalk(repository, repoObj, path):
    startTime = time.time()
    repoWalk(repoObj, path, path.strip('/'))
    endTime = time.time()

    sourceData = FloatingTools.sourceData()

    if 'loadTimes' not in sourceData:
        sourceData['loadTimes'] = {}

    if repository not in sourceData['loadTimes']:
        sourceData['loadTimes'][repository] = {}
    sourceData['loadTimes'][repository][
        FloatingTools.APP_WRAPPER.name() if FloatingTools.APP_WRAPPER else 'Generic'] = endTime - startTime
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

    # begin repo loop.
    for repo in repoData:

        if not repo['load']:
            continue

        # connect to the repository
        FloatingTools.FT_LOOGER.info('Loading Repository: ' + repo['name'])
        repoName = repo['name']
        repo = FloatingTools.gitHubConnect().get_repo(repoName)

        # load toolbox data
        try:
            toolboxData = json.loads(repo.get_file_contents('/toolbox.json').decoded_content)
        except GithubException:
            toolboxData = dict(paths=['/'])

        if FloatingTools.APP_WRAPPER:
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

            for card in WILDCARDS:
                path = path.replace('{%s}' % card, WILDCARDS[card]['value'])

            # spawn thread
            if FloatingTools.APP_WRAPPER and not FloatingTools.APP_WRAPPER.MULTI_THREAD:
                timeWalk(repoName, repo, path)
            else:
                t = threading.Thread(name=repoName, target=timeWalk, args=(repoName, repo, path))
                t.start()

    if FloatingTools.APP_WRAPPER:
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/HatfieldFX',
                                               lambda: webbrowser.open("http://www.hatfieldfx.com/floating-tools"))
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/Repository',
                                               lambda: webbrowser.open("https://github.com/aldmbmtl/FloatingTools"))