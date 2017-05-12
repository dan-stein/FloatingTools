"""
Python rig for importing code directly off the cloud.
"""
__all__ = [
    'virtualPyImport'
]

# python imports
import os
import imp
import sys

# ft imports
import FloatingTools

# caches
CLOUD_CACHE = []


class CloudFinder(object):
    """
    Finder object for determining the loader required to load the module.
    """
    def __init__(self, repo, url):
        """
        Meant for passing the Github url path for later use.
        :param repo: 
        :param url: 
        """
        self.repo = repo
        self.url = url.strip('/')
        self.mapping = {}

        # preload for speed caching
        self.preloadPackageContents()

    def preloadPackageContents(self):
        """
        Preload the packages contents for faster loading
        :return: 
        """
        self.mapping = {}

        # recursion function
        def recurse(self, path):
            for fo in self.repo.get_dir_contents(path):
                if fo.type == 'dir':
                    recurse(self, fo.path)
                else:
                    fileName = os.path.basename(fo.name.replace('.py', ''))
                    moduleName = "%s.%s" % (path.replace(self.url, '').replace('/', '.').strip('.'), fileName)
                    self.mapping[moduleName] = fo

        recurse(self, self.url)

    def find_module(self, fullname, path=None):
        try:
            imp.find_module(fullname)
            return None
        except ImportError:
            packageName = fullname + '.__init__'
            if fullname in self.mapping:
                return CloudLoader(cloudObj=self.mapping[fullname])
            if packageName in self.mapping:
                return CloudLoader(cloudObj=self.mapping[packageName])
            for key in self.mapping:
                if key.endswith(fullname):
                    return CloudLoader(cloudObj=self.mapping[key])
                if key.endswith(packageName):
                    return CloudLoader(cloudObj=self.mapping[key])


class CloudLoader(object):
    def __init__(self, cloudObj):
        """
        :param cloudObj: 
        """
        self.cloudObj = cloudObj

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

        # Set a few properties required by PEP 302
        mod.__file__ = fullname
        mod.__name__ = fullname

        # always looks like a package
        mod.__path__ = [self.cloudObj.path]
        mod.__cloud_object__ = self.cloudObj
        mod.__repository__ = self.cloudObj.repository
        mod.__loader__ = self
        mod.__package__ = '.'.join(fullname.split('.')[:-1])

        # pull code
        code = self.cloudObj.decoded_content

        exec code in mod.__dict__

        return mod


def virtualPyImport(repository, path):
    """
    Import a python package from the cloud. Packages must me loaded in a special manner to handle recursion
    :param repository: (GitHub repository obj) -OR- (str "username/repository")
    :param path: (str) The path to the package itself in the repository
    :return: 
    """
    if isinstance(repository, str):
        repository = FloatingTools.gitHubConnect().get_repo(repository)

    sys.meta_path.append(CloudFinder(repo=repository, url=path))