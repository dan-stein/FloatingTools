"""
Cloud File class
"""
# python imports
import os

# FT imports
import FloatingTools

def GetCloudFile(*args, **kwargs):
    """
    Factory object for creating references to file objects on HFX.com
    :param args: 
    :param kwargs: 
    :return: 
    """
    try:
        return CloudFileObject.ALL_FILES[args[0].id]
    except KeyError:
        return CloudFileObject(*args, **kwargs)


def registerFileHandler(extension, handler):
    """
    Register a handler for a file type.
    :param extension: 
    :param handler: 
    :return: 
    """
    CloudFileObject.HANDLERS[extension] = handler


class CloudFileObject(object):
    """
    Cloud object to interact with HFX.com that represents a file
    """

    ALL_FILES = {}
    HANDLERS = {}

    def __init__(self, wp_obj):

        # instance variables
        self._cloudObj = wp_obj
        self._scratch = None
        self._serverPath = None
        self._fileName = wp_obj.title
        self._ext = os.path.splitext(self._fileName)[1]

        # register with class
        self.ALL_FILES[wp_obj.id] = self

        self.serverPath()

    def _recurse(self, obj):
        """
        --private--
        :param obj: 
        :return: 
        """
        self._scratch.insert(0, obj.name)
        if obj.parent == '0':
            return
        from C_Navigation import CloudFileSystem
        self._recurse(CloudFileSystem._systemObjects[obj.parent])

    def execute(self):
        """
        execute this file based on its extension.
        :return: 
        """
        if self._ext not in self.HANDLERS:
            FloatingTools.FT_LOGGER.debug("There is no handler associated with %(self._ext)s files." % locals())
            return

        return self.HANDLERS[self._ext](self)

    def filename(self):
        """
        Get the name of the file.
        :return: 
        """
        return self._fileName

    def serverPath(self):
        """
        Get the server path of this object.
        :return: 
        """
        self._scratch = []
        self._recurse(self._cloudObj.terms[0])
        self._scratch.append(self._cloudObj.title)
        serverPath = '/'.join(self._scratch)
        self._scratch = None

        return serverPath

    def serverDirectory(self):
        """
        Return the server directory that this file lives in.
        :return: 
        """
        return self.serverPath().rsplit('/', 1)[0]

    def content(self):
        """
        Get the contents of the file
        :return: 
        """
        raw = self._cloudObj.content

        raw = raw.replace('<pre>', '')
        raw = raw.replace('<pre lang="PYTHON">', '')
        raw = raw.replace('</pre>', '')
        raw = raw.replace('&lt;', '<')
        raw = raw.replace('&gt;', '>')

        return raw
