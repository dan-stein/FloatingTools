# ft import
import FloatingTools

# python imports
import inspect
import traceback


def activeWrapper():
    return Wrapper.ACTIVE_WRAPPER


class Wrapper(object):
    """
Abstraction class for wrapping an application so FloatingTools can interact with the application it was loaded in.

Wrappers have specific class variables that must be set to help define how FloatingTools should handle the application 
at load up. 


.. code-block:: python
    :linenos:
    
    class Wrapper(object):
        def __init__(self):
            # Default settings
            FILE_TYPES      = []        # The file extensions associated with this application
            ARGS            = None      # sometimes you need to pass flags to the executable to execute a Python Script

You can modify all these settings...

.. code-block:: python
    :linenos:
    
    class NukeWrapper(Wrapper):
        def __init__(self):
            # Wrapper settings
            FILE_TYPES      = ['.nk', '.py', '.gizmo']
            ARGS            = ['-t']

    """
    # private
    ACTIVE_WRAPPER = None

    @classmethod
    def setActiveWrapper(cls, wrapper):
        """
Used to set the application wrapper used to act as middle man between FT and the external application. Application being
Nuke, Maya, ect. Only use this if you are sure of what you are doing.

:param wrapper:
        """
        if wrapper.__class__ is not Wrapper:
            Wrapper.ACTIVE_WRAPPER = wrapper

    def __init__(self):
        self.FILE_TYPES = []
        self.EXECUTABLE = None
        self.ARGS = None

        # load modules
        self.libraries = {}
        try:
            self.appTest()
            self.setActiveWrapper(self)

            # set up helper globals for all class functions
            for funcName in dir(self):
                try:
                    for name, lib in self.libraries.iteritems():
                        getattr(self, funcName).__func__.__globals__[name] = lib
                except AttributeError:
                    pass
        except:
            FloatingTools.FT_LOOGER.debug("Wrapper test for: %s" % self.__class__.__name__)
            FloatingTools.FT_LOOGER.debug(traceback.format_exc())

    def loadAPI(self, mod):
        """
Load the module(s) need for this application to function.

.. code-block:: python
    :linenos:

     def appTest(cls):
        import nuke
        cls.loadAPI(nuke)

:param mod:
        """
        modName = None
        for key, value in inspect.stack()[1][0].f_locals.iteritems():
            if value == mod:
                modName = key
                break

        if modName not in self.libraries:
            self.libraries[modName] = mod
            setattr(self, modName, mod)

    def loadedAPIs(self):
        """
An application should have libraries associated with it. To allow for cleaner code, the modules should be loaded on the
wrapper object. This will return a list of modules that are loaded on this wrapper.

.. code-block:: python
    :linenos:

    wrapper = FloatingTools.Wrapper()

    if 'nuke' in wrapper.loadedAPIs():
        wrapper.nuke
        do nuke stuff...

    if 'maya' in wrapper.loadedAPIs():
        wrapper.maya
        do maya stuff...

:return: list of strings for the modules loaded
        """
        return self.libraries

    def appTest(self):
        """
This should ideally return True if this is the wrapper for the app you're in. If you don't do this, FloatingTools wraps 
the function and if it fails, assumes this is not the wrapper for the application it is in.
        
.. code-block:: python
    :linenos:

    class NukeWrapper(Wrapper):
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
        if Wrapper.ACTIVE_WRAPPER:
            raise NotImplementedError

    def addMenuSeparator(self, menuPath):
        """
If your application allows for UI separators, define the behavior here.

:param menuPath: Path to add the separator to
        """
        pass

    def addMenuEntry(self, menuPath, command=None, icon=None, enabled=None):
        """
MUST BE SUB-CLASSED

Each application requires the certain calls to modify the UI. FloatingTools only targets the top bar of the 
application you are trying to modify.
        
.. code-block:: python
    :linenos:

    class NukeWrapper(Wrapper):

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
        if Wrapper.ACTIVE_WRAPPER:
            raise NotImplementedError

    def loadFile(self, filePath):
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
        if Wrapper.ACTIVE_WRAPPER:
            raise NotImplementedError

    def fileTypes(self):
        """
Return the file types associated with this application.
        """
        return self.FILE_TYPES

    def setFileTypes(self, *args):
        """
Pass the file extensions that are associated with this application.

:param args:
        """
        self.FILE_TYPES = args