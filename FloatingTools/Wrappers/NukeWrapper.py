# python imports
import os
from sys import executable

# FloatingTools imports
from AbstractApp import AbstractApplication

MENUS = ['Nuke', 'Node Graph', 'Nodes']

class NukeWrapper(AbstractApplication):
    # Wrapper settings
    FILE_TYPES = ['.nk', '.py', '.gizmo']
    NAME = 'Nuke'
    APP_ICON = 'https://s3.amazonaws.com/fxhome-static/images/product/ignite-pro-2017/foundry-nuke.png'
    ARGS = ['-t']
    MULTI_THREAD = True
    EXECUTABLE = executable

    @staticmethod
    def addMenuSeparator(menuPath):
        # handle windows nonsense
        menuPath = menuPath.replace('\\', '/').replace('//', '/')
        for menu in MENUS:
            try:
                nuke.executeInMainThread(nuke.menu(menu).findItem(menuPath).addSeparator)
            except AttributeError:
                pass

    @classmethod
    def appTest(cls):
        import nuke
        import nukescripts
        import PySide

        NukeWrapper.loadAPI(nuke)
        NukeWrapper.loadAPI(nukescripts)
        NukeWrapper.loadAPI(PySide)

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
            fo = open(filePath, mode='r')
            code = fo.read()
            fo.close()

            temp = open(filePath, mode='w')
            temp.write(code.replace('Gizmo {', 'Group {\n name ' + os.path.basename(basename)))
            temp.close()

            # create node
            nuke.nodePaste(filePath)
