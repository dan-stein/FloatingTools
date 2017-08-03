"""
Forward preparation for supporting more services. 
"""
# python imports
import os
import time
import shutil
import urllib
import zipfile
import traceback
from functools import partial

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


# main abstract class
class Service(object):
    """
Represents a FloatingTools compatible toolbox service
    """
    # reserved
    _TYPE_ = None
    SOURCE_FIELDS = dict()
    SOURCE_FIELDS_ORDER = dict()
    LOGIN_FIELDS = list()
    ICON = None
    WEBPAGE = None

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

    # globals
    SERVICES = {}
    TOOLBOXES = {}

    @staticmethod
    def get(service):
        """
Get a service by name.

:param service:
        """
        try:
            return Service.SERVICES[service]
        except KeyError:
            raise InvalidHandlerType('Handler Type passed does not exists.\n')

    @staticmethod
    def getToolbox(name):
        """
    Get a toolbox by its name.

    :param name:
        """
        try:
            return Service.TOOLBOXES[name]
        except KeyError:
            raise InvalidToolbox(name + ' is not a valid toolbox.')

    @staticmethod
    def toolboxes():
        return Service.TOOLBOXES.values()

    @staticmethod
    def downloadSource(url, path, timeout=5):
        """
Download source from a passed url and install it where you defined using the path parameter. This includes a
time out function.

:parameter url: str
:parameter path: str
:parameter timeout: How long to wait before timing out.
        """
        try:
            urllib.urlretrieve(url, path)
            return True
        except:
            FloatingTools.FT_LOOGER.warning('Connection time out from %s.\nPath may be invalid or the website has '
                                            'direct downloads blocked my flagging FloatingTools as spam.\nContact the '
                                            'site admin OR download and unpack to zip manually and point to it using '
                                            'the "Local" service instead of the URL service.' % url)
            return False

    @classmethod
    def registerService(cls, _type):
        """
        This needs to be done so FT knows how to handle different source types.
        
        :parameter _type:  
        """

        # register with global
        cls._TYPE_ = _type
        Service.SERVICES[_type] = cls
        try:
            cls.initialize()
        except:
            traceback.print_exc()

    @classmethod
    def serviceName(cls):
        """
        This is the services name. This will be whatever you named the class.
        """
        return cls.__name__

    @classmethod
    def initialize(cls):
        """
This will be called the first time a toolbox of this type is created. This is meant for installing libraries if they are
needed. For example, if you need boto3 for an Amazon Handler, you would call
FloatingTools.installPackage('boto3', 'boto') here. This is also meant for any other set up such as getting login data.

.. note::
    This is only called once during the first call to create a toolbox if this type.

.. code-block:: python
    :linenos:

    @classmethod
    def initialize(cls):
        # install the aws api lib through pip
        FloatingTools.installPackage('boto3', 'boto')

        import boto3
        from botocore.client import Config

        # set log in data for AWS
        os.environ['AWS_ACCESS_KEY_ID'] = cls.userData()['access key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = cls.userData()['secret key']

        cls.CONNECTION = boto3.resource('s3', config=Config(signature_version='s3v4'))
        """
        pass

    def __init__(self, **sourceFields):
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
        self._install_path = None
        self._id = id(self)
        self._is_pointer = False

        # run init functions
        self.loadSource(self._source)

        # validate the handlers been set up right.
        if not self._toolbox_name:
            raise NameError('There is no name assigned to this Toolbox Handler. You must check your handler to make '
                            'sure it sets the toolbox name in the Handler.loadSource function.')

        # register this instance as a toolbox
        Service.TOOLBOXES[self._toolbox_name] = self

    def _callInstall(self):
        if os.path.exists(self.installDirectory()):
            return

        if not os.path.exists(self.installDirectory()):
            os.makedirs(self.installDirectory())

        FloatingTools.FT_LOOGER.info('Initial install process for %s. This will add a one time load up lag. '
                                     'Please wait.' % self.name())

        self.install()

    def newToolbox(self, source):
        """
Add a new toolbox for this service.

:param source:
:param install:
        """
        return self.get(self.name())(**source)

    def installZip(self, zipPath):
        """
        Helper for installing zips.
        
        :parameter zipPath: str
        """
        # load zip file
        zipRef = zipfile.ZipFile(zipPath, 'r')

        # begin unpack
        os.chdir(self.installDirectory())
        root = zipRef.filelist[0].filename.split('/')[0]
        for i in zipRef.filelist:
            # create local paths
            cleanPath = i.filename.replace(root + '/', '')
            if cleanPath == '' or i.filename.startswith('__MACOSX') or os.path.basename(i.filename).startswith('.'):
                continue

            # extract file contents
            initialInstall = zipRef.extract(i)
            reinstallPath = os.path.join(self.installDirectory(), *i.filename.replace(root, '').split('/'))

            # move
            shutil.move(initialInstall, reinstallPath)

        # delete directory
        shutil.rmtree(os.path.join(self.installDirectory(), root))

        # close the zipfile
        zipRef.close()

        # remove old zip
        os.unlink(zipPath)

    def addMenuItem(self, menu, command, html=None):
        """
        A menu item will show up wrapper application and, if the html argument is passed as well, it will show up in 
        Dashboard in the ToolShed.

        :parameter menu: str for the menu to display. You can submenu with '/'
        :parameter command: callable function
        :parameter html: The raw html call as a string
        """
        self._toolbox_menu_order.append(menu)
        self._toolbox_menu_content[menu] = command

        # add html information
        if html and menu not in self._toolbox_html_content:
            self._toolbox_html_content[menu] = dict(tag=os.path.basename(menu), html=html)

    def sourcePath(self):
        """
        Path to the source data that builds the toolbox
        """
        return self._source_path

    def setSourcePath(self, path):
        """
        Set the path that the original source is coming from. Set during the Handler.loadSource()
        
.. code-block:: python
    :linenos:
    
    def loadSource(self, source):
        # simple example pulled from the URLHandler class
        
        website = source['URL'].split('.com')[0] + '.com'
        toolLink = os.path.dirname(source['URL']).rstrip('/')

        # set handler variables
        self.setSourcePath(source['URL']) # pass the website url that the zip will be downloaded from.
        
        etc...

:parameter path: any kind of python object
        """
        self._source_path = path

    def name(self):
        """
        Each Handler instance has a name that represents what toolbox it has loaded. This name is used for many 
        functions including the data model that the settings file saves.
        """
        return self._toolbox_name

    def setName(self, name):
        """
        This MUST be set during the Handler.loadSource() function.
        """
        self._toolbox_name = name

    def loadSource(self, source):
        """
        This will be called when the tool box is initiated. Subclass this function to load your source information add 
        your files (but not install). To execute the installation of files, redefine Handler.install()
        
.. code-block:: python
    :linenos:
    
    def loadSource(self, source):
        # simple example pulled from the GitHubHandler class
    
        username = source['username']
        repository = source['repository']
        
        githubLink = "www.github.com/%s/%s/" % (username, repository) 
        
        self.setName(username + '/' + repository)
        self.setSourcePath(githubLink)


:parameter source: dictionary with keys representing source field names and the associated values
        """
        raise NotImplementedError()

    def setIsPointer(self, value=False):
        """
        Handlers can either "pull" or "point". Pull boxes usually require files to be installed. Point boxes point to a 
        location on disk and do not modify the location at all. If you want to protect a location on disk from 
        accidental deletion through the Handler.uninstall() function, set this handler to be a pointer to block the 
        uninstall call.  
        """
        self._is_pointer = value

    def isPointer(self):
        """
        Handlers can either "pull" or "point". Pull boxes usually require files to be installed. Point boxes point to a 
        location on disk and do not modify the location at all. 
        """
        return self._is_pointer

    def setInstallLocation(self, location):
        """
        Set the location that the toolbox is to be installed in. This MUST be done if you intend on allowing for 
        Handler.uninstall() to work correctly.

        :parameter location: str
        """
        self._install_path = location

    def installDirectory(self):
        """
        Get the designated install directory for this toolbox. This is assigned to the cache directory inside 
        FloatingTools by default. You can set this in your handler.loadSource() function by using
        handler.setInstallLocation(Your path).
        
        This will respect '/' for declaring subdirectories. For example, 'aldmbmtl/toolbox' will create toolbox inside 
        aldmbmtl.
        """
        if not self._install_path:
            return os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, *self.name().split('/'))

        return self._install_path

    def install(self):
        """
        This will be called when the tool box is initiated and after the Handler.loadSource() call. Subclass this for 
        installing your content. This is required if the handler needs to download and unpack content from the internet.
        
        If this handler is defined in the loadSource as a "pointer" using Handler.setIsPointer(True), this function is 
        not required. Otherwise, you must sub-class this function or it will throw NotImplementedError.
        
.. code-block:: python
    :linenos:
    
    def install(self):
        # simple example pulled from the GitHubHandler class
        
        zipURL = self.sourcePath().get_archive_link('zipball')
        self.downloadSource(zipURL, zipPath)
        self.installZip(zipPath)
        """
        if not self._is_pointer:
            raise NotImplementedError()

    def uninstall(self):
        """
        Uninstalls this toolbox from the installation directory. This can not be undone and there is no safety question.
        """
        if not self._is_pointer:
            try:
                shutil.rmtree(self.installDirectory())
            except OSError:
                pass

        # delete self from global dict
        global TOOLBOXES
        del TOOLBOXES[self.name()]

    def loadTools(self):
        """
Load the tools on disk for this toolbox.
        """
        if not FloatingTools.activeWrapper():
            return

        # set the menus root
        menuRoot = 'FloatingTools/' + self.name().replace('/', '-')

        # create the toolbox fields predefined by the service.
        for menuField in self._toolbox_menu_order:
            FloatingTools.activeWrapper().addMenuEntry(
                menuRoot + '/' + menuField,
                command=self._toolbox_menu_content[menuField]
            )

        # add separator for tools section
        FloatingTools.activeWrapper().addMenuSeparator(menuRoot)

        # start timing tool loading
        start = time.time()

        # loop over install path and check for tools that match the wrappers file extensions
        for (path, dirs, files) in os.walk(self.installDirectory()):
            arcName = menuRoot + path.replace(self.installDirectory(), '')

            for file in files:
                base, ext = os.path.splitext(file)

                if ext not in FloatingTools.activeWrapper().fileTypes():
                    continue

                filePath = os.path.join(path, file)
                FloatingTools.activeWrapper().addMenuEntry(
                    menuPath=os.path.join(arcName, file),
                    command=partial(FloatingTools.activeWrapper().loadFile, filePath)
                )

        # end timing tool loading and report it to FT.NET and the console
        end = time.time()

        # report load times
        FloatingTools.FT_LOOGER.info('%s took: %s ms' % (self.name(), end - start))