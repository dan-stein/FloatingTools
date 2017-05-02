# FloatingTools imports
import FloatingTools


def wrapper():
    """
    Wrapper object for the context of the application you are working in.
    :return: 
    """
    return FloatingTools.WRAPPER


def setWrapper(klass):
    """
    Register the Wrapper class for the application you are in.
    :param klass: 
    :return: 
    """
    FloatingTools.WRAPPER = klass


class AbstractApplication(object):
    """
    Abstraction class for wrapping an application so FloatingTools can interact with the application it was loaded in.
    """
    FILE_TYPES = []
    NAME = None
    WRAPPER_PATH = None
    APP_ICON = None
    EXECUTABLE = None
    ARGS = None
    MULTI_THREAD = False

    @staticmethod
    def cloudImport(repository, filePath):
        """
        Some applications have a specific call to execute code in the main thread. This is only needed if you are 
        wrapping an application for multi-threaded load up.
          
          For example, when adding menu items to Nuke; if the call is made from an outside thread, the menu item will 
          do nothing when clicked. To fix this, you must use Nukes nuke.executeInMainThread(). In some applications, 
          this is not an issue. By default, this is a direct wrap to FloatingTools.cloudImport.
        
        :param repository: 
        :param filePath: 
        :return: 
        """
        FloatingTools.cloudImport(repository, filePath)

    @staticmethod
    def appTest():
        """
        MUST BE SUB-CLASSED
        
        This should ideally return True if this is the wrapper for the app you're in. If you don't do this, 
        FloatingTools wraps the function and if it fails, assums this is not the wrapper for the application it is in.
        
        An example would be:
            def appTest():
                try:
                    import nuke
                    return True
                except ImportError:
                    return False
                    
            - OR -
            
            def appTest():
                import nuke
                
        :return: 
        """
        raise NotImplementedError

    @staticmethod
    def addMenuSeparator(menuPath):
        """
        OPTIONAL SUB-CLASS
        :param menuPath: Path to add the separator to.
        :return: 
        """
        pass

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=None):
        """
        MUST BE SUB-CLASSED
        :param enabled: 
        :param menuPath: a string laying out how the menu to the command should be laid out. Example: 'top/sub/command'
        :param command: a callable to be executed
        :param icon: optional
        :return: 
        """
        raise NotImplementedError

    @staticmethod
    def loadFile(gitHubFileObject, fileType):
        """
        MUST BE SUB-CLASSED
        :param gitHubFileObject: 
        :param fileType: 
        :return: 
        """
        raise NotImplementedError

    @classmethod
    def fileTypes(cls):
        """
        Return the file types associated with this application.
        :return: 
        """
        return cls.FILE_TYPES

    @classmethod
    def name(cls):
        """
        Get the name of the current application.
        :return: 
        """
        return cls.NAME
