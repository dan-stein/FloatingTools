"""
Navigation functions for walking around the pipeline structure.
"""
# FT import
import FloatingTools
from FloatingTools.packages.wordpress_xmlrpc.methods.taxonomies import GetTerms
from FloatingTools.packages.wordpress_xmlrpc.methods.posts import GetPosts
from C_File import GetCloudFile


class CloudFileSystem(object):
    """
    Object that represents the file system on the cloud
    """

    _systemMap = {}
    _systemObjects = {}
    _systemMapNames = {}
    _systemFiles = []
    _cachedFilePaths = {}

    def __init__(self):

        # instance variables
        self.con = FloatingTools.connection()
        self.cwd = '0'
        self._currentPath = []
        self._currentDirectory = {}

        # cache all system information if it hasn't been done yet.
        if not self._systemFiles:
            for directory in self.con.call(GetTerms('category', {'number': 999999})):

                if directory.parent not in self._systemMap:

                    self._systemMap[directory.parent] = []

                self._systemMap[directory.parent].append(directory.id)
                self._systemObjects[directory.id] = directory
                self._systemMapNames[directory.id] = directory.name

            for wp_obj in FloatingTools.connection().call(GetPosts()):
                self._systemFiles.append(GetCloudFile(wp_obj))

        # start at root level
        self.cd('0')

    def _recurse(self, obj):
        self._currentPath.insert(0, obj.name)
        if obj.parent == '0':
            return
        self._recurse(self._systemObjects[obj.parent])

    def currentDirectory(self):
        """
        The directory you are currently in.
        :return:
        """
        self._currentPath = []
        self._recurse(self._systemObjects[self.cwd])
        return '/'.join(self._currentPath)

    def root(self):
        """
        Get the root directory path
        :return:
        """
        self.cd('0')

    def up(self):
        """
        Go up a directory.
        :return:
        """
        self.cwd = self._systemObjects[self.cwd].parent

        for directory in self._systemMap[self.cwd]:
            self._currentDirectory[self._systemMapNames[directory]] = directory

    def cd(self, directory):
        """
        Change to a directory
        :param directory:
        :return:
        """
        if directory == '0':
            self.cwd = directory
        else:
            self.cwd = self._currentDirectory[directory]

        for directory in self._systemMap[self.cwd]:
            self._currentDirectory[self._systemMapNames[directory]] = directory

    def ls(self):
        """
        List the contents of the current working directory.
        :return:
        """
        l = []
        for directory in self._systemMap[self.cwd]:
            l.append(self._systemMapNames[directory])
        return l

    def getFiles(self):
        """
        Get all files in the current directory.
        :return:
        """

        currentDirectory = self.currentDirectory()

        if currentDirectory not in self._cachedFilePaths:

            cfs = []

            for cf in self._systemFiles:
                if cf.serverDirectory() == self.currentDirectory():
                    cfs.append(cf)

            self._cachedFilePaths[currentDirectory] = cfs

        return self._cachedFilePaths[currentDirectory]


sys = CloudFileSystem()
sys.cd('Pipelines')
sys.cd('Generic')
sys.cd('Nuke')
sys.cd('Python')
for fo in sys.getFiles():
    print fo.serverPath()

