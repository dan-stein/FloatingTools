"""
Handles all loading operations
"""
__all__ = [
    'loadTools'
]

# python imports
import os
import sys
import imp
import time
import threading
import traceback
import webbrowser
from functools import partial

# FloatingTools imports
import FloatingTools


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
_LOCK = threading.Lock()

# add to dashboard
FloatingTools.Dashboard.setDashboardVariable('wildcards', WILDCARDS)


def loadToolbox(handler, path):
    """
    --private--
    :return: 
    """
    global PYTHON_MODULES

    # add this repo to the registered python modules
    if handler.name() not in PYTHON_MODULES:
        PYTHON_MODULES[handler.name()] = []

    # compile search path
    searchPath = handler.installDirectory() + path

    # start timer for heavy processing functions
    startTime = time.time()
    for root, dirs, files in os.walk(searchPath):

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
                if pyPath not in PYTHON_MODULES[handler.name()]:
                    PYTHON_MODULES[handler.name()].append(pyPath)

            sys.path.append(pyPath)

        # loop over contents
        for fo in files:
            if fo.endswith('.py') and fo != '__init__.py':
                PYTHON_MODULES[handler.name()].append(os.path.join(root, fo))
                continue

            if FloatingTools.wrapper():
                # filter out files that do not pertain to this application
                basename, ext = os.path.splitext(fo)
                if ext not in FloatingTools.wrapper().fileTypes():
                    continue

                # register tool with the application
                toolboxPath = FloatingTools.__name__ + '/' + handler.name().replace('/', '.')
                menuPath = (toolboxPath + '/' + root.replace(searchPath, '') + '/' + fo)
                FloatingTools.wrapper().addMenuEntry(
                    menuPath.replace('\\', '/').replace('//', '/'),
                    partial(FloatingTools.wrapper().loadFile, os.path.join(root, fo))
                )

    # end time and log execution time
    endTime = time.time()

    # log the data and update
    _LOCK.acquire()
    sourceData = FloatingTools.sourceData()
    for source in sourceData:
        if source['name'] != handler.name():
            continue

        # log load time for the current app
        source['loadTimes'][FloatingTools.wrapperName()] = '{:.6f}'.format(endTime - startTime)
        break

    FloatingTools.updateSources(sourceData)
    _LOCK.release()


def loadTools():
    """
    Main tool loading function.
    :return: 
    """
    # set up dashboard in the application wrapper if there is one loaded.
    if FloatingTools.wrapper():
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Toolbox',
                                             FloatingTools.Dashboard.toolbox)
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Tool Shed',
                                             FloatingTools.Dashboard.toolShed)
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Applications',
                                             FloatingTools.Dashboard.applications)
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Settings',
                                             FloatingTools.Dashboard.settings)
        FloatingTools.wrapper().addMenuSeparator(FloatingTools.__name__ + '/Dashboard')
        FloatingTools.wrapper().addMenuSeparator(FloatingTools.__name__)
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Support/HatfieldFX',
                                             lambda: webbrowser.open("http://www.hatfieldfx.com/floating-tools"))
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Dashboard/Support/Repository',
                                             lambda: webbrowser.open("https://github.com/aldmbmtl/FloatingTools"))

        FloatingTools.wrapper().addMenuSeparator(FloatingTools.__name__)
        FloatingTools.wrapper().addMenuEntry(FloatingTools.__name__ + '/Toolboxes', FloatingTools.Dashboard.toolShed)

    # pull source data
    sourceData = FloatingTools.sourceData()

    # log threads
    threads = []

    # begin repo loop.
    for source in sourceData:

        # skip installing and loading if the toolbox isn't requested, but load the toolbox reference for potential
        # later use.
        _LOCK.acquire()
        if not source['load']:
            FloatingTools.createToolbox(source['type'], source['source'], install=False)
            continue

        # get handler data
        toolbox = FloatingTools.createToolbox(source['type'], source['source'])
        _LOCK.release()

        # connect to the repository
        FloatingTools.FT_LOOGER.info('Loading %s with the %s handler...' % (source['name'], source['type']))

        # make tool box information menus
        if FloatingTools.wrapper():
            toolboxPath = FloatingTools.__name__ + '/' + toolbox.name().replace('/', '.')
            for menuItem in toolbox._toolbox_menu_order:
                FloatingTools.wrapper().addMenuEntry(toolboxPath + menuItem, toolbox._toolbox_menu_content[menuItem])
            FloatingTools.wrapper().addMenuSeparator(toolboxPath)

        # loop over the toolbox path
        for path in toolbox.toolboxPaths():

            # handle wildcard logic
            for card in WILDCARDS:
                path = path.replace('{%s}' % card, WILDCARDS[card]['value'])

            # spawn thread if it is a thread supporting application
            if FloatingTools.wrapper() and not FloatingTools.wrapper().MULTI_THREAD:
                loadToolbox(toolbox, path)
            else:
                t = threading.Thread(name=toolbox.name(), target=loadToolbox, args=(toolbox, path))
                t.setDaemon(True)
                threads.append(t)
                t.start()

    # hold the main thread till load up is complete.
    for thread in threads:
        thread.join()

    # load auto load modules
    FloatingTools.FT_LOOGER.info('Starting Auto-Imports...')
    for source in sourceData:
        if source['load'] and FloatingTools.wrapperName() in source['apps']:
            for mod, load in source['apps'][FloatingTools.wrapperName()].iteritems():
                if load:
                    try:
                        FloatingTools.FT_LOOGER.info('\tAuto-Importing: ' + mod)
                        imp.load_source(os.path.basename(mod).replace('.py', ''), mod)
                        FloatingTools.FT_LOOGER.info('\t\tComplete')
                    except ImportError:
                        FloatingTools.FT_LOOGER.info('\t\tFailed')
                        FloatingTools.FT_LOOGER.info('\n')
                        traceback.print_exc()
                        FloatingTools.FT_LOOGER.info('\n')


# set virtual system variables
FloatingTools.Dashboard.setDashboardVariable('python_cloud', PYTHON_MODULES)