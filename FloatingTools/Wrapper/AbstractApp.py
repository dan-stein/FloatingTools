# FloatingTools imports
import FloatingTools


def wrapper():
    """
    Wrapper object for the context of the application you are working in.
    :return: 
    """
    return FloatingTools.WRAPPER


def wrapperName():
    """
    Get the name of the current wrapper/application you are in. If there is no wrapper loaded, it assumes you are 
    running FloatingTools outside the context of any application and in straight python. If this is the case, it returns
    "Generic" signaling you are in the os version of FloatingTools. 
    
    OTHERWISE
    
    It will return the name of the wrapper application you are in.
    :return: 
    """
    return 'Generic' if not wrapper() else wrapper().name()


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

    def __init__(self):
        self.appTest()
        setWrapper(self.__class__)

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
    def loadFile(filePath):
        """
        MUST BE SUB-CLASSED
        :param filePath: 
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
