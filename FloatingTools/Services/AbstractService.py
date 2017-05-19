"""
Forward preparation for supporting more services. 
"""


# currently supported services
SERVICES = dict()


class InvalidHandler(Exception):
    pass


def registerHandler(serviceName, handler):
    """
    Register a new handler for a service. For example, subclass the Toolbox class and create a handler for Dropbox.
    :param serviceName: 
    :param handler: 
    :return: 
    """
    global SERVICES

    # check that this is a valid handler.
    if not isinstance(handler, Handler):
        raise InvalidHandler('Toolbox handler registered is invalid! Must be a subclass of FloatingTools.Toolbox.\n'
                             'Type passed: ' + str(type(handler)))

    # register with global
    SERVICES[serviceName] = handler


def getHandler(handlerType):
    """
    Get the class associated with the handler type passed.
    :param handlerType: str key in the FloatingTools.Services.SERVICES
    :return: 
    """



class Handler(object):
    """
    Represents a FloatingTools compatible toolbox service
    """
    def __init__(self, source):
        """
        init toolbox
        :param source: 
        """
        # instance variables
        self._toolboxName = None
        self._source = source
        self._source_path = None
        self._files = []
        self._zips = []

        # run init functions
        self.loadSource(self._source)
        self.install()

    @classmethod
    def handlerName(cls):
        """
        This handlers name. This will be whatever you named the class.
        :return: 
        """
        return cls.__name__

    def setSourcePath(self, path):
        """
        Set the path that the original source is coming from.
        :param path: 
        :return: 
        """
        self._source_path = path

    def name(self):
        """
        Get the name of the toolbox that this handler represents.
        :return: 
        """
        return self._toolboxName

    def setName(self, name):
        """
        Set the name of the toolbox that this handler represents.
        :param name: 
        :return: 
        """
        self._toolboxName = name

    def loadSource(self, source):
        """
        --MUST SUBCLASS--
        
        This will be called when the tool box is initiated. Subclass this function to load your source information. 
        You should add your files here. To execute the installation of files, redefine Handler.install()
        
        Variables that should be set:
            self.setName(name of the toolbox)
            self.setSourcePath(where the source came from)
        
        :param source: 
        :return: 
        """
        raise NotImplementedError()

    def install(self):
        """
        --MUST SUBCLASS--

        This will be called when the tool box is initiated and after handler.loadSource. Subclass this function to 
        perform the actual install call.

        :return: 
        """
        raise NotImplementedError()

    def addFile(self, filePath, relativePath):
        """
        Add a file to this toolboxes file structure.
        :param relativePath: Path relative. Should be something like /path/to/file in the context of where it will be 
                installed in relation to the root of this toolbox.
        :param filePath: Path to the file. This can be anything, including a url if you choose to pass that, assuming 
                your handler is set up to handle that.
        :return: 
        """
        self._files.append(dict(filePath=filePath, relativePath=relativePath))

    def addZip(self, zipPath):
        """
        Add a zip archive that holds all the information you are looking to load from an archive.
        :param zipPath: must be an archive type that can be opened by pythons built in zip lib.
        :return: 
        """
        if zipPath not in self._zips:
            self._zips.append(zipPath)