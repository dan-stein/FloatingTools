"""
Forward preparation for supporting more services. 
"""
# python imports
import os
import shutil

# ft imports
import FloatingTools


# currently supported services
SERVICES = dict()
TOOLBOXES = dict()


# Errors
class InvalidHandler(Exception):
    pass


class InvalidHandlerType(Exception):
    pass


class InvalidToolbox(Exception):
    pass


# functions
def getHandler(handlerType):
    """
    Get the class associated with the handler type passed.
    :param handlerType: str key in the FloatingTools.Services.SERVICES
    :return: 
    """
    try:
        return SERVICES[handlerType]
    except KeyError:
        raise InvalidHandlerType('Handler Type passed does not exists.\n')


def getToolbox(name):
    """
    Get a toolbox by its name.
    :param name: 
    :return: 
    """
    try:
        return TOOLBOXES[name]
    except KeyError:
        raise InvalidToolbox(name + ' is not a valid toolbox.')


def toolboxes():
    """
    Get all the currently loaded toolboxes
    :return: 
    """
    return TOOLBOXES


def createToolbox(_type, source, install=True):
    """
    Create a toolbox. You must pass a valid type of handler with the proper 
    :param _type: 
    :param source: 
    :return: 
    """
    return getHandler(_type)(install=install, **source)


# main abstract class
class Handler(object):
    """
    Represents a FloatingTools compatible toolbox service
    """
    # reserved
    _TYPE_ = None
    SOURCE_FIELDS = dict()
    SOURCE_FIELDS_ORDER = dict()

    # data model for Toolboxes
    DATA_MODEL = dict(
        # information used to describe the toolbox for recreation
        type=None,      # assigned at toolbox creation    (str)
        name=None,      # assigned at toolbox creation    (str)
        source=None,    # assigned at toolbox creation    (dict)

        # settings
        load=False,     # to load or not
        apps={},        # script loading settings help here organized by application

        # diagnostics
        loadTimes={},   # toolbox load times organized by application
    )

    @classmethod
    def addSourceField(cls, label, _type=str):
        """
        Adding a source field is required for setting up the source data. This can be a url field or fields. Usually 
        string types are fine.

        :param label: The label that will be presented on the field 
        :param _type: This will determine the kind of field that will be presented when the field is rendered on the 
        website front end

        :return: 
        """
        if cls.__name__ not in cls.SOURCE_FIELDS:
            cls.SOURCE_FIELDS[cls.__name__] = {}
        cls.SOURCE_FIELDS[cls.__name__][label] = _type

        if cls.__name__ not in cls.SOURCE_FIELDS_ORDER:
            cls.SOURCE_FIELDS_ORDER[cls.__name__] = []
        cls.SOURCE_FIELDS_ORDER[cls.__name__].append(label)

    @classmethod
    def registerHandler(cls, _type):
        """
        This needs to be done so FT knows how to handle different source types.
        :param _type: 
        :return: 
        """
        global SERVICES

        # register with global
        cls._TYPE_ = _type
        SERVICES[_type] = cls

        FloatingTools.Dashboard.setDashboardVariable('services', SERVICES)

    @classmethod
    def handlerName(cls):
        """
        This handlers name. This will be whatever you named the class.
        :return: 
        """
        return cls.__name__

    def __str__(self):
        return "Toolbox Handler(Service: %s, Name: %s, Loaded: %s)" % (
            self._TYPE_,
            self.name(),
            self.settings()['load']
        )

    def __init__(self, install=True, **sourceFields):
        """
        init toolbox
        :param source: 
        """
        global TOOLBOXES

        # instance variables
        self._toolbox_name = None
        self._source = sourceFields
        self._source_path = None
        self._source_settings = None
        self._toolbox_paths = None
        self._toolbox_menu_order = []
        self._toolbox_menu_content = {}
        self._toolbox_html_content = {}
        self._id = id(self)

        # run init functions
        self.loadSource(self._source)

        # validate the handlers been set up right.
        if not self._toolbox_name:
            raise NameError('There is no name assigned to this Toolbox Handler. You must check your handler to make '
                            'sure it sets the toolbox name in the Handler.loadSource function.')

        # only run install process if it doesnt appear to be installed already.
        if install:
            if not os.path.exists(self.installDirectory()):
                os.makedirs(self.installDirectory())

                # execute install command
                self.install()

        # register this instance as a toolbox
        TOOLBOXES[self._toolbox_name] = self

        # settings file
        self.settings()

    def updateSettings(self, update):
        """
        pass the new dictionary with the settings for this toolbox
        :param update: 
        :return: 
        """
        sourceData = FloatingTools.sourceData()
        for source in sourceData:
            if source['name'] == self._toolbox_name:
                sourceData.pop(sourceData.index(source))
                sourceData.append(update)
                self._source_settings = update
                break

        FloatingTools.updateSources(sourceData)


    def settings(self):
        """
        Get the saved settings for this toolbox.
        :return: 
        """
        if not self._source_settings:
            # pull source data
            sourceData = FloatingTools.sourceData()
            for source in sourceData:
                if source['name'] == self._toolbox_name:
                    self._source_settings = source
                    break

            # create a default entry if it doesnt exist
            if not self._source_settings:
                # clone the model so the global is untouched.
                settings = self.DATA_MODEL.copy()

                # set default values
                settings['name'] = self.name()
                settings['type'] = self._TYPE_
                settings['source'] = self._source

                # update source data and set instance variable
                sourceData.append(settings)
                FloatingTools.updateSources(sourceData)
                self._source_settings = settings

        return self._source_settings

    def addMenuItem(self, menu, command, html=None):
        """
        Add a command that will show up in the application with your handler.
        :param menu: 
        :param command:
        :param html: 
        :return: 
        """
        self._toolbox_menu_order.append(menu)
        self._toolbox_menu_content[menu] = command

        # add html information
        if html and menu not in self._toolbox_html_content:
            self._toolbox_html_content[menu] = dict(tag=os.path.basename(menu), html=html)

    def toolboxPaths(self):
        """
        Get the path for this toolbox.
        :return: 
        """
        # default is the whole toolbox
        paths = ['/']

        # pull from the set source paths for the toolbox
        if self._toolbox_paths:
            paths = self._toolbox_paths

        return paths

    def setToolboxPaths(self, listOfPaths):
        """
        Must be a list of load up paths. Wild card values are evaluated at tool loading. No substitution required here.
        :param listOfPaths: 
        :return: 
        """
        if not isinstance(listOfPaths, list):
            raise TypeError('Must be a <list> of paths')

        self._toolbox_paths = listOfPaths

    def sourcePath(self):
        """
        Path to the source data that builds the toolbox
        :return: 
        """
        return self._source_path

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
        return self._toolbox_name

    def setName(self, name):
        """
        Set the name of the toolbox that this handler represents.
        :param name: 
        :return: 
        """
        self._toolbox_name = name

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

    def installDirectory(self):
        """
        Get the designated install directory for this toolbox. This is assigned to the cache directory inside FT.
        
        This will respect '/' for declaring subdirectories. For example, 'aldmbmtl/toolbox' will create toolbox inside 
        aldmbmtl.
        
        :return: 
        """
        return os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, *self.name().split('/'))

    def install(self):
        """
        --MUST SUBCLASS--

        This will be called when the tool box is initiated and after handler.loadSource. Subclass this function to 
        perform the actual install call.

        :return: 
        """
        raise NotImplementedError()

    def uninstall(self):
        """
        Uninstalls this toolbox from the installation directory
        :return: 
        """
        shutil.rmtree(self.installDirectory())

        # purge all settings from the source data
        data = FloatingTools.sourceData()
        for toolbox in data:
            if toolbox['name'] == self.name():
                data.remove(toolbox)
                break
        FloatingTools.updateSources(data)

        # delete self from global dict
        global TOOLBOXES
        del TOOLBOXES[self.name()]