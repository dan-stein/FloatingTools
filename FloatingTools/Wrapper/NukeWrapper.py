# python imports
import tempfile

# FloatingTools imports
from AbstractApp import AbstractApplication, setWrapper

nuke = None
MENUS = ['Nuke', 'Node Graph', 'Nodes']

class NukeWrapper(AbstractApplication):
    FILE_TYPES = ['.nk']
    NAME = 'Nuke'
    APP_ICON = 'http://www.vfxhive.com/images/products_img/FOUNDRYNUKE.jpg'

    @staticmethod
    def addMenuSeparator(menuPath):
        for menu in MENUS:
            nuke.menu(menu).findItem(menuPath).addSeparator()

    @staticmethod
    def appTest():
        global nuke
        import nuke

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=True):
        if command is None:
            def command():
                pass
        for menu in MENUS:
            nuke.menu(menu).addCommand(menuPath, command, icon=icon)
            nuke.menu(menu).findItem(menuPath).setEnabled(enabled)

    @staticmethod
    def loadFile(gitHubFileObject, fileType):
        """
        Nuke handler
        :param gitHubFileObject: 
        :param fileType: 
        :return: 
        """

        # nk handler
        if fileType == '.nk':
            temp = tempfile.NamedTemporaryFile()
            path = temp.name
            temp.write(gitHubFileObject.decoded_content)
            temp.seek(0)
            nuke.nodePaste(path)
            temp.close()

setWrapper(NukeWrapper)
