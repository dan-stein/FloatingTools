# python imports
import os

# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper

# maya imports
maya = None
pm = None


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

        # maya imports
        import maya
        import pymel.core as pm

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=None):
        # grab top menu
        mainWindow = pm.language.melGlobals['gMainWindow']

        # set parent
        parent = None
        path = ''
        base = os.path.basename(menuPath)

        # recursively build menu
        for menu in menuPath.split('/'):
            path += '/' + menu
            if menu == base:
                if command is not None:
                    pm.menuItem(label=base, command=command, parent=parent)
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
        pm.separator(MayaWrapper.MENUS['/' + menuPath])

    @staticmethod
    def loadFile(filePath):
        pass
