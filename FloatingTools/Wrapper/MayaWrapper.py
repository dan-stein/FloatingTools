# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper


class MayaWrapper(AbstractApplication):
    FILE_TYPES = ['.ma', '.mb']
    NAME = 'Maya'
    APP_ICON = 'http://area.autodesk.com/area_v2/assets/img/product/autodesk-maya.png'

    @staticmethod
    def appTest():
        import maya

    @staticmethod
    def addMenuEntry(menuPath, command):
        pass

    @staticmethod
    def loadFile(gitHubFileObject, fileType):
        pass


setWrapper(MayaWrapper)
