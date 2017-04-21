# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper


class NukeWrapper(AbstractApplication):
    FILE_TYPES = ['.nk', '.gizmo']
    NAME = 'Nuke'

    @staticmethod
    def appTest():
        import nuke

    @classmethod
    def addMenuEntry(cls, menuPath, command):
        pass

    @classmethod
    def loadFile(cls, gitHubFileObject, fileType):
        pass


setWrapper(NukeWrapper)
