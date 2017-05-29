# python imports
import os
import imp

# FloatingTools imports
from AbstractApp import AbstractApplication

# maya imports
maya = None
pm = None
cmds = None


class MayaWrapper(AbstractApplication):
    FILE_TYPES = ['.ma', '.mb', '.py']
    NAME = 'Maya'
    APP_ICON = 'http://area.autodesk.com/area_v2/assets/img/product/autodesk-maya.png'
    ARGS = ['-script']

    MENUS = {}

    @staticmethod
    def appTest():
        global pm
        global maya
        global cmds

        # maya imports
        import maya
        import pymel.core as pm
        import maya.cmds as cmds

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=None):
        mainWindow = maya.mel.eval('$tmpVar=$gMainWindow')
        cmds.setParent(mainWindow)

        # set parent
        parent = None
        path = ''
        base = os.path.basename(menuPath)

        # recursively build menu
        for menu in menuPath.split('/'):
            path += '/' + menu
            if menu == base:
                if command is not None:
                    def wrapper(*args, **kwargs):
                        command()
                    pm.menuItem(label=base, command=wrapper, parent=parent)
                else:
                    pm.menuItem(label=base, parent=parent)
            elif path in MayaWrapper.MENUS:
                parent = MayaWrapper.MENUS[path]
            else:
                if parent is None:
                    parent = pm.menu(menu, parent=mainWindow)
                else:
                    parent = pm.subMenuItem(menu, parent=parent)

                MayaWrapper.MENUS[path] = parent

    @staticmethod
    def addMenuSeparator(menuPath):
        pass
        # pm.separator(MayaWrapper.MENUS['/' + menuPath])

    @staticmethod
    def loadFile(filePath):
        basename, ext = os.path.splitext(filePath)

        # py handler
        if ext in '.py':
            imp.load_source(filePath)