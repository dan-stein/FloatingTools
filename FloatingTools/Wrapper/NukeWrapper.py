# python imports
import os
import tempfile

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

    if os.name == 'posix':
        applicationDirectory = '/Applications'
        ext = '.app'

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
    def cloudImport(repository, filePath):
        nuke.executeInMainThreadWithResult(FloatingTools.cloudImport, (repository, filePath))

    @staticmethod
    def addMenuSeparator(menuPath):
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
    def loadFile(gitHubFileObject, fileType):
        """
        Nuke handler
        :param gitHubFileObject: 
        :param fileType: 
        :return: 
        """
        # nk handler
        if fileType in ['.nk', '.gizmo']:
            temp = tempfile.NamedTemporaryFile()
            path = temp.name
            temp.write(gitHubFileObject.decoded_content.replace('Gizmo', 'Group'))
            temp.seek(0)
            nuke.nodePaste(path)
            temp.close()


setWrapper(NukeWrapper)
