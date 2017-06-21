# FloatingTools imports
import FloatingTools

# python imports
import inspect
import traceback


def wrapper():
    """
Wrapper object for the context of the application you are working in. 
    """
    return FloatingTools.WRAPPER


def wrapperName():
    """
Get the name of the current wrapper/application you are in. If there is no wrapper loaded, it assumes you are 
running FloatingTools outside the context of any application and in straight python. If this is the case, it returns
"Generic" signaling you are in the os version of FloatingTools. 

OTHERWISE

It will return the name of the wrapper application you are in.
    """
    return 'Generic' if not wrapper() else wrapper().name()


def setWrapper(klass):
    """
Register the Wrapper class for the application you are in.
    
    :param klass:
    """
    FloatingTools.WRAPPER = klass


class AbstractApplication(object):
    """
Abstraction class for wrapping an application so FloatingTools can interact with the application it was loaded in.

Wrappers have specific class variables that must be set to help define how FloatingTools should handle the application 
at load up. 


.. code-block:: python
    :linenos:
    
    class AbstractApplication(object):
        # Default settings
        FILE_TYPES      = []        # The file extensions associated with this application
        NAME            = None      # Name of the application (REQUIRED)
        APP_ICON        = None      # The HTML icon for the application (Just for looks)
        EXECUTABLE      = None      # This is the executable path that the application would use to run its Python Interpreter.
        ARGS            = None      # sometimes you need to pass flags to the executable to execute a Python Script
        MULTI_THREAD    = False     # Set whether the application supports Python multi threading

You can modify all these settings...

.. code-block:: python
    :linenos:
    
    class NukeWrapper(AbstractApplication):
        # Wrapper settings
        FILE_TYPES      = ['.nk', '.py', '.gizmo']
        NAME            = 'Nuke'
        APP_ICON        = 'http://www.vfxhive.com/images/products_img/FOUNDRYNUKE.jpg'
        ARGS            = ['-t']
        MULTI_THREAD    = True

    """
    FILE_TYPES = []
    NAME = None
    APP_ICON = None
    EXECUTABLE = None
    ARGS = None
    MULTI_THREAD = False

    # load modules
    libraries = {}

    def __init__(self):
        self.appTest()
        setWrapper(self.__class__)

        # set up helper globals for all class functions
        for funcName in dir(self):
            try:
                for name, lib in self.libraries.iteritems():
                    getattr(self, funcName).__func__.__globals__[name] = lib
            except AttributeError:
                pass

    @classmethod
    def loadAPI(cls, mod):
        """
Load the module(s) need for this application to function.

.. code-block:: python
    :linenos:

     def appTest(cls):
        import nuke
        cls.loadModule(nuke)

:param mod:
        """
        modName = None
        for key, value in inspect.stack()[1][0].f_locals.iteritems():
            if value == mod:
                modName = key
                break

        if modName not in cls.libraries:
            cls.libraries[modName] = mod
            setattr(cls, modName, mod)

    @classmethod
    def loadedAPIs(cls):
        """
An application should have libraries associated with it. To allow for cleaner code, the modules should be loaded on the
wrapper object. This will return a list of modules that are loaded on this wrapper.

.. code-block:: python
    :linenos:

    wrapper = FloatingTools.wrapper()

    if 'nuke' in wrapper.loadedAPIs():
        wrapper.nuke
        do nuke stuff...

    if 'maya' in wrapper.loadedAPIs():
        wrapper.maya
        do maya stuff...

:return: list of strings for the modules loaded
        """
        return cls.libraries

    @classmethod
    def appTest(cls):
        """
This should ideally return True if this is the wrapper for the app you're in. If you don't do this, FloatingTools wraps 
the function and if it fails, assumes this is not the wrapper for the application it is in.
        
.. code-block:: python
    :linenos:

    class NukeWrapper(AbstractApplication):
        def appTest():
            try:
                import nuke
                return True
            except ImportError:
                return False
        
        # --- OR --- #
        
        def appTest():
            import nuke

        """
        raise NotImplementedError

    @staticmethod
    def addMenuSeparator(menuPath):
        """
If your application allows for UI separators, define the behavior here.

:param menuPath: Path to add the separator to
        """
        pass

    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=None):
        """
MUST BE SUB-CLASSED

Each application requires the certain calls to modify the UI. FloatingTools only targets the top bar of the 
application you are trying to modify.
        
.. code-block:: python
    :linenos:

    class NukeWrapper(AbstractApplication):

        def addMenuEntry(menuPath, command=None, icon=None, enabled=True):
            # from NukeWrapper
            nuke.executeInMainThread(nuke.menu(menu).addCommand, args=(menuPath, command), kwargs={'icon': icon})

.. warning::
    
    If your wrapper supports multi threading, you may need to make sure you execute the application specific command in 
    the main thread. In the example above, you can see I had to use nuke.executeInMainThread. The reason being this is 
    all called from the spawned threads at the load up process.

:param enabled: bool
:param menuPath: a string laying out how the menu to the command should be laid out. Example: 'top/sub/command'
:param command: a callable to be executed
:param icon: optional
        """
        raise NotImplementedError

    @staticmethod
    def loadFile(filePath):
        """
Each application has a special way of importing data. For example, in nuke you can take the file path and paste
it into the the node graph. You would define that behavior here.

The file path is passed to you from the loader in FloatingTools. All you need to do is handle it how you'd like.
        
.. code-block:: python
    :linenos:
    
    def loadFile(self, filePath):
        # from NukeWrapper
        basename, ext = os.path.splitext(filePath)
    
        # nk handler
        if ext in ['.nk', '.gizmo']:
        
            # create node
            nuke.nodePaste(filePath)
        
:param filePath: str
        """
        raise NotImplementedError

    @classmethod
    def fileTypes(cls):
        """
Return the file types associated with this application.
        """
        return cls.FILE_TYPES

    @classmethod
    def name(cls):
        """
Get the name of the current application.
        """
        return cls.NAME
