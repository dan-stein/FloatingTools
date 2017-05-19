# python imports
import os
import tempfile
from sys import platform

# FloatingTools imports
import FloatingTools
from AbstractApp import AbstractApplication, setWrapper

nuke = None
MENUS = ['Nuke', 'Node Graph', 'Nodes']

class NukeWrapper(AbstractApplication):
    # Wrapper settings
    FILE_TYPES = ['.nk', '.py', '.gizmo']
    NAME = 'Nuke'
    APP_ICON = 'http://www.vfxhive.com/images/products_img/FOUNDRYNUKE.jpg'
    ARGS = ['-t']
    MULTI_THREAD = True

    _launchers = {}

    applicationDirectory = None
    ext = None

    if platform == "linux" or platform == "linux2":
        pass

    elif platform == "darwin":
        applicationDirectory = '/Applications'
        ext = '.app'

    elif platform == "win32":
        applicationDirectory = 'C:/Program Files/'
        ext = '.exe'

    if applicationDirectory and os.path.exists(applicationDirectory):
        for app in os.listdir(applicationDirectory):
            if app.startswith('Nuke'):
                for launcher in os.listdir(os.path.join(applicationDirectory, app)):
                    if launcher.endswith(ext) \
                            and 'nuke' in launcher.lower() \
                            and 'commercial' not in launcher.lower() \
                            and 'ple' not in launcher.lower():
                        _launchers[os.path.splitext(launcher)[0]] = os.path.join(
                            os.path.join(applicationDirectory, app, launcher))

    EXECUTABLE = _launchers

    @staticmethod
    def addMenuSeparator(menuPath):
        # handle windows nonsense
        menuPath = menuPath.replace('\\', '/').replace('//', '/')
        for menu in MENUS:
            try:
                nuke.executeInMainThread(nuke.menu(menu).findItem(menuPath).addSeparator)
            except AttributeError:
                nuke.executeInMainThreadWithResult(nuke.menu(menu).addMenu, args=(menuPath,))
                nuke.executeInMainThread(nuke.menu(menu).findItem(menuPath).addSeparator)

    @staticmethod
    def appTest():
        global nuke
        import nuke

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=True):
        menuPath = menuPath.replace('\\', '/').replace('//', '/')
        if command is None:
            def command():
                pass
        for menu in MENUS:
            nuke.executeInMainThread(nuke.menu(menu).addCommand, args=(menuPath, command), kwargs={'icon': icon})
            try:
                nuke.executeInMainThread(nuke.menu(menu).findItem(menuPath).setEnabled, args=(enabled,))
            except AttributeError:
                pass

    @staticmethod
    def loadFile(filePath):
        """
        Nuke handler
        :type filePath: 
        :return: 
        """
        basename, ext = os.path.splitext(filePath)

        # nk handler
        if ext in ['.nk', '.gizmo']:

            # create temp file
            temp = open(filePath, mode='w')
            temp.write(temp.read().replace('Gizmo {', 'Group {\n name ' + basename))
            temp.close()

            # create node
            nuke.nodePaste(filePath)


setWrapper(NukeWrapper)
