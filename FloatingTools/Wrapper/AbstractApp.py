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

    @classmethod
    def addMenuEntry(cls, menuPath, command):
        """
        MUST BE SUB-CLASSED
        :param menuPath: a string laying out how the menu to the command should be layed out. Example: 'top/sub/command'
        :param command: a callable to be executed
        :return: 
        """
        raise NotImplementedError

    @classmethod
    def loadFile(cls, gitHubFileObject, fileType):
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
