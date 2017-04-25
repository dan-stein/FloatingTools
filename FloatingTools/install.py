"""
Validate the dependencies are installed.
"""
# python imports
import os
import sys
import imp
import json
import urllib
import base64
import subprocess

# FloatingTools imports
import FloatingTools

# build the packages directory if its not there.
if not os.path.exists(FloatingTools.PACKAGES):
    os.mkdir(FloatingTools.PACKAGES)

# register the FloatingTools/packages directory with sys.path.
sys.path.append(FloatingTools.PACKAGES)

# begin checking dependency list
# pip
# flask (this brings a bit with it as well)
# PyGithub

# check if pip is installed. This is installed at the Python installs site-packages. Everything else is installed in the
# FloatingTools/packages directory.
try:
    import pip
except ImportError:
    ft_packages = os.listdir(FloatingTools.PACKAGES)
    for pack in ['github', 'flask']:
        if pack not in ft_packages:
            # install pip
            downloadPath = os.path.join(FloatingTools.PACKAGES, 'get-pip.py')
            urllib.urlretrieve("https://bootstrap.pypa.io/get-pip.py", downloadPath)

            # execute the python pip install call
            subprocess.call([FloatingTools.PYTHON_EXECUTABLE, downloadPath])

            # delete get-pip.py
            os.unlink(downloadPath)

            try:
                import pip
            except ImportError:
                raise Exception('Pip is required for install. Launch FloatingTools on its own by opening the python '
                                'interpreter and running:\n\nimport sys\nsys.path.append("%s")\nimport FloatingTools\n'
                                '\nThis will allow the packages required to be installed into the FloatingTools package'
                                '. Once complete, relaunch this application.' %
                                os.path.abspath(FloatingTools.__file__ + '/../../'))

# Verify the github lib exists
try:
    import github
except ImportError:
    pip.main(['install', 'PyGithub', '-t', FloatingTools.PACKAGES])

    # verify install
    import github

# Verify the flask lib exists
try:
    import flask
except ImportError:
    pip.main(['install', 'Flask', '-t', FloatingTools.PACKAGES])

    # verify install
    import flask


def downloadBuild(repository, sha, path=None):
    """
    Download the latest FloatingTools build from the passed sha.
    :param path: 
    :param repository: 
    :param sha: 
    :return: 
    """
    if path is None:
        path = '/FloatingTools/'

    for fo in repository.get_dir_contents(path):
        if fo.type == 'dir':
            downloadBuild(repository, sha, path + fo.name + '/')
            return

        # pull server data
        serverPath = fo.path
        localPath = os.path.join(FloatingTools.INSTALL_DIRECTORY, serverPath)
        try:
            fileContent = repository.get_contents(serverPath, ref=sha)
            fileData = base64.b64decode(fileContent.content)
            fileOut = open(localPath, "w")
            fileOut.write(fileData)
            fileOut.close()
            FloatingTools.FT_LOOGER.info('Updated: ' + localPath)
        except (github.GithubException, IOError):
            FloatingTools.FT_LOOGER.error('Failed updating: ' + localPath)


def loadVersion():
    """
    Load the build information from the Branch.json file for the FloatingTools version.
    :return: 
    """
    if not os.path.exists(FloatingTools.DATA):
        os.mkdir(FloatingTools.DATA)

    branchFile = os.path.join(FloatingTools.DATA, 'Branch.json')
    # create the file if it doesnt exists.
    if not os.path.exists(branchFile):
        # build the default release data
        branchData = {'dev': False,
                      'devBranch': 'master',
                      'release': 'latest',
                      'installed': None,
                      'collaborator': False
                      }
        # dump the data
        json.dump(branchData, open(branchFile, 'w'), indent=4, sort_keys=True)
    # load the branch data
    branchData = json.load(open(branchFile, 'r'))

    if branchData['collaborator']:
        FloatingTools.FT_LOOGER.info("Launched in Collaborator mode. You are responsible for VCS control and syncing "
                                     "with HatfieldFX, LLC repository for FloatingTools. Repository public address "
                                     "aldmbmtl/FloatingTools. Thank you for helping us make FT better!")
        return

    # connect to github and pull the FloatingTools repository.
    hub = FloatingTools.gitHubConnect()
    repository = hub.get_repo('aldmbmtl/FloatingTools')

    version = None
    message = ""

    if branchData['dev']:
        # find the branch being requested
        commit = repository.get_branch(branchData['devBranch']).commit
        version = commit.sha

        message = "Loading in DEV branch: " + branchData['devBranch']

    else:
        # load in the release data from the repository
        if branchData['release'] != branchData['installed']:

            # load all releases
            releases = {}
            for release in repository.get_tags():
                releases[release.name] = release.commit.sha

            if branchData['release'] == 'latest':
                # find the latest version
                version = releases[max(releases)]
                message = "Downloading FloatingTools " + max(releases)
            else:
                version = releases[branchData['release']]
                message = "Downloading FloatingTools " + branchData['release']

    # begin download
    if version:
        FloatingTools.FT_LOOGER.info(message)

        downloadBuild(repository, version)

        FloatingTools.FT_LOOGER.info("Download complete.")

        if not branchData['dev']:
            # update the branch data
            branchData['installed'] = branchData['release']

            # save out data
            json.dump(branchData, open(branchFile, 'w'), indent=4, sort_keys=True)
    else:
        FloatingTools.FT_LOOGER.info("Install is up-to-date.")
