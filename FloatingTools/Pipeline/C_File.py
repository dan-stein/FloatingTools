"""
Cloud File class
"""

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


class CloudFileObject(object):
    """
    Cloud object to interact with HFX.com that represents a file
    """

    ALL_FILES = {}

    def __init__(self, wp_obj):

        # instance variables
        self._cloudObj = wp_obj
        self._scratch = None
        self._serverPath = None

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
