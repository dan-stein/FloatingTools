# python imports
import os
import imp

# FloatingTools imports
from AbstractApp import AbstractApplication


class MayaWrapper(AbstractApplication):
    FILE_TYPES = ['.ma', '.mb', '.py']
    NAME = 'Maya'
    APP_ICON = 'http://infocenter.com.qa/images/Autodesk-Maya-logo-256x256.png'
    ARGS = ['-script']

    MENUS = {}

    @classmethod
    def appTest(cls):
        # maya imports
        import maya
        import pymel.core as pm
        import maya.cmds as cmds

        cls.loadAPI(maya)
        cls.loadAPI(maya.cmds)
        cls.loadAPI(pymel.core)

    @classmethod
    def addMenuEntry(cls, menuPath, command=None, icon=None, enabled=None):
        mainWindow = cls.maya.mel.eval('$tmpVar=$gMainWindow')
        cls.cmds.setParent(mainWindow)

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

    @classmethod
    def addMenuSeparator(cls, menuPath):
        pass
        # pm.separator(MayaWrapper.MENUS['/' + menuPath])

    @classmethod
    def loadFile(cls, filePath):
        basename, ext = os.path.splitext(filePath)

        # py handler
        if ext in '.py':
            imp.load_source(filePath)