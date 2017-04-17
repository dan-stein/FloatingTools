# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper


# nuke imports
# import nuke


class NukeWrapper(AbstractApplication):
    FILE_TYPES = ['.nk', '.gizmo']
    NAME = 'Nuke'

    @classmethod
    def addMenuEntry(cls, menuPath, command):
        pass

    @classmethod
    def loadFile(cls, gitHubFileObject, fileType):
        pass


setWrapper(NukeWrapper)
