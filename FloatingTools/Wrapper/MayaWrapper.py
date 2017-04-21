# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper


class MayaWrapper(AbstractApplication):
    FILE_TYPES = ['.ma', '.mb']
    NAME = 'Maya'

    @staticmethod
    def appTest():
        import maya

    @classmethod
    def addMenuEntry(cls, menuPath, command):
        pass

    @classmethod
    def loadFile(cls, gitHubFileObject, fileType):
        pass


setWrapper(MayaWrapper)
