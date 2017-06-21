"""
Validate the dependencies are installed.
"""

__all__ = [
    'releases',
    'branches'
]

# python imports
import os
import re
import sys
import urllib
import zipfile
import subprocess

# FloatingTools imports
import FloatingTools

# build the packages directory if its not there.
if not os.path.exists(FloatingTools.PACKAGES):
    os.mkdir(FloatingTools.PACKAGES)

# register the FloatingTools/packages directory with sys.path.
sys.path.insert(0, FloatingTools.PACKAGES)

# GLOBALS
RELEASES = {}
BRANCHES = {}
CURRENT_RELEASE = None
VERSION_EXPR = re.compile("/aldmbmtl/FloatingTools/tree/(v[0-9]+.[0-9]+.[0-9]+)")
BRANCH_EXPR = re.compile("/aldmbmtl/FloatingTools/tree/([a-zA-Z]+)")

# begin checking dependency list
# pip
# flask (this brings a bit with it as well)
# PyGithub

# check if pip is installed. This is installed at the Python installs site-packages. Everything else is installed in the
# FloatingTools/packages directory.
ft_packages = os.listdir(FloatingTools.PACKAGES)

try:
    import pip
except ImportError:
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
if 'setuptools' not in ft_packages:
    pip.main(['install', '-U', 'pip', 'setuptools', '-t', FloatingTools.PACKAGES])

def pipInstallPackage(package, pipName=None):
    """
Install packages into FT from pip.

:param package: the name to import the package
:param pipName: in-case the pip install name is different from the module name.
    """
    # due to the nature of the pip install process, we want to set the PYTHONPATH environment variable pointed to the
    # FT/packages directory so that setuptools is in sync with the version of pip installed.
    PYTHONPATH = os.environ["PYTHONPATH"] if "PYTHONPATH" in os.environ else None
    os.environ['PYTHONPATH'] = FloatingTools.PACKAGES

    # Verify the github lib exists
    try:
        __import__(package)
    except ImportError:
        if not pipName:
            pipName = package

        pip.main(['install', pipName, '-t', FloatingTools.PACKAGES])

        # verify install
        __import__(package)

    # flush env
    if PYTHONPATH:
        os.environ['PYTHONPATH'] = PYTHONPATH

for package in [('github', 'PyGithub'), ('flask', 'Flask')]:
    pipInstallPackage(*package)


def downloadBuild(version):
    """
    Download the target FloatingTools build from the version passed.
    :param version:
    :return: 
    """
    # download build
    zipPath = os.path.join(FloatingTools.INSTALL_DIRECTORY, os.path.basename(version))
    urllib.urlretrieve(version, zipPath)
    zipDownload = zipfile.ZipFile(zipPath, 'r')

    # begin unpack
    root = zipDownload.filelist[0].filename.split('/')[0]
    os.chdir(FloatingTools.INSTALL_DIRECTORY)

    for i in zipDownload.filelist:
        # create local paths
        cleanPath = i.filename.replace(root + '/', '')
        if cleanPath == '' or i.filename.startswith('__MACOSX') or os.path.basename(i.filename).startswith('.'):
            continue

        if not i.filename.startswith(root + '/FloatingTools/'):
            continue

        # extract file contents
        # print os.path.join(FloatingTools.INSTALL_DIRECTORY, *i.filename.replace(root, '').split('/'))
        zipDownload.extract(i, path=FloatingTools.INSTALL_DIRECTORY)

    # close the zipfile
    zipDownload.close()

    # remove old zip
    os.unlink(zipPath)


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
    version = None
    message = ""

    if branchData['dev']:
        # find the branch being requested
        version = branches()[branchData['devBranch']]

        message = "Loading in DEV branch: " + branchData['devBranch']

    else:

        if branchData['release'] == 'latest' or branchData['release'] != branchData['installed']:

            # load in the release data from the repository
            if branchData['release'] == 'latest':
                latestVersion = max(releases())

                if branchData['installed'] != version:
                    version = releases()[latestVersion]
                    message = "Downloading FloatingTools " + latestVersion

            elif branchData['release'] != branchData['installed']:
                version = releases()[branchData['release']]
                message = "Downloading FloatingTools " + branchData['release']

            else:
                pass

    # begin download
    if version:
        FloatingTools.FT_LOOGER.info(message)

        downloadBuild(version)

        FloatingTools.FT_LOOGER.info("Download complete.")

        if not branchData['dev']:
            # update the branch data
            branchData['installed'] = version

            # save out data
            FloatingTools.updateBuild(branchData)
    else:
        FloatingTools.FT_LOOGER.info("Install is up-to-date.")


def _update_globals():
    global RELEASES
    global BRANCHES
    global CURRENT_RELEASE

    # update globals
    archive = urllib.urlopen('https://github.com/aldmbmtl/FloatingTools/').read()

    for release in VERSION_EXPR.findall(archive):
        RELEASES[release] = 'https://github.com/aldmbmtl/FloatingTools/archive/' + release + '.zip'
        if release == FloatingTools.buildData()['installed']:
            CURRENT_RELEASE = release

    for branch in BRANCH_EXPR.findall(archive):
        if branch == 'v' or branch in BRANCHES:
            continue
        BRANCHES[branch] = 'https://github.com/aldmbmtl/FloatingTools/archive/' + branch + '.zip'

    sortedReleases = sorted(RELEASES)
    sortedReleases.reverse()

    if CURRENT_RELEASE is None:
        CURRENT_RELEASE = sortedReleases[0]

    FloatingTools.Dashboard.setDashboardVariable('branches', BRANCHES)
    FloatingTools.Dashboard.setDashboardVariable('releases', sortedReleases)
    FloatingTools.Dashboard.setDashboardVariable('current_release', CURRENT_RELEASE)


def releases():
    """
    Get all published released.
    :return: 
    """
    _update_globals()

    return RELEASES


def branches():
    """
    Get all branches.
    :return: 
    """
    _update_globals()

    return BRANCHES
