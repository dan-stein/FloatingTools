"""
Validate the dependencies are installed.
"""
# python imports
import os
import sys
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

# GLOBALS
RELEASES = {}
BRANCHES = {}
CURRENT_RELEASE = None

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
            # determine executable from the application wrapper
            executable = sys.executable
            args = []
            if FloatingTools.WRAPPER and FloatingTools.WRAPPER.ARGS:
                args = FloatingTools.WRAPPER.ARGS

            FloatingTools.FT_LOOGER.info("Python executable (+args) for pip install: " + executable)

            # install pip
            downloadPath = os.path.join(FloatingTools.PACKAGES, 'get-pip.py')
            urllib.urlretrieve("https://bootstrap.pypa.io/get-pip.py", downloadPath)

            pipDL = open(downloadPath, 'r')
            code = pipDL.read()
            code = code.replace('sys.exit(pip.main(["install", "--upgrade"] + args))',
                                'sys.exit(pip.main(["install", "pip", "-t", "%s"]))' % FloatingTools.PACKAGES)
            pipDL.close()
            open(downloadPath, 'w').write(code)

            command = [os.path.abspath(executable)] + args + [downloadPath]

            # execute the python pip install call
            subprocess.call(command)

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
            break

# upgrade pip if needed
pip.main(['install', '--upgrade', 'pip'])

try:
    import setuptools
except:
    pip.main(['install', '-U', 'pip', 'setuptools', '-t', FloatingTools.PACKAGES])

    # verify install
    import github

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
            continue

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

    branchData = FloatingTools.buildData()

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
            FloatingTools.updateBuild(branchData)
    else:
        FloatingTools.FT_LOOGER.info("Install is up-to-date.")


def _update_gloabls():
    global RELEASES
    global BRANCHES
    global CURRENT_RELEASE

    # update globals
    if not RELEASES or not BRANCHES:
        ftRepo = FloatingTools.gitHubConnect().get_repo('aldmbmtl/FloatingTools')

        # get branches
        for branch in ftRepo.get_branches():
            BRANCHES[branch.name] = branch

        # get releases
        for release in ftRepo.get_tags():
            RELEASES[release.name] = release
            if release.name == FloatingTools.buildData()['installed']:
                CURRENT_RELEASE = release.name

        # default to latest release if there was none matched.
        if CURRENT_RELEASE is None:
            sortedReleases = sorted(RELEASES)
            sortedReleases.reverse()
            CURRENT_RELEASE = sortedReleases[0]

    FloatingTools.Dashboard.setDashboardVariable('branches', BRANCHES)
    FloatingTools.Dashboard.setDashboardVariable('releases', sorted(RELEASES))
    FloatingTools.Dashboard.setDashboardVariable('current_release', CURRENT_RELEASE)


def releases():
    """
    Get all published released.
    :return: 
    """
    _update_gloabls()

    return RELEASES


def branches():
    """
    Get all branches.
    :return: 
    """
    _update_gloabls()

    return BRANCHES
