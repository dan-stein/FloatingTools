"""
Validate the dependencies are installed.
"""
# python imports
import os
import sys
import json
import urllib
import base64
import datetime
import subprocess
from time import strptime

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
    # install pip
    downloadPath = os.path.join(FloatingTools.PACKAGES, 'get-pip.py')
    urllib.urlretrieve("https://bootstrap.pypa.io/get-pip.py", downloadPath)

    # execute the python pip install call
    subprocess.call([sys.executable, downloadPath])

    # verify pip install worked
    import pip

    # delete get-pip.py
    os.unlink(downloadPath)

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


def githubDate2Datetime(githubDate):
    """
    --private--
    :param githubDate: 
    :return: 
    """
    splitGHTime = githubDate.split(' ')
    splitGHSmallTime = splitGHTime[4].split(':')
    converted = datetime.datetime(
        day=int(splitGHTime[1]),
        month=strptime(splitGHTime[2], '%b').tm_mon,
        year=int(splitGHTime[3]),
        hour=int(splitGHSmallTime[0]),
        minute=int(splitGHSmallTime[1]),
        second=int(splitGHSmallTime[2])
    )
    return converted


def downloadBuild(repository, sha):
    """
    Download the latest FloatingTools build from the passed sha.
    :param repository: 
    :param sha: 
    :return: 
    """
    for fo in repository.get_dir_contents('/FloatingTools/'):
        if fo.type == 'dir':
            continue

        # pull server data
        serverPath = fo.path
        try:
            fileContent = repository.get_contents(serverPath, ref=sha)
            fileData = base64.b64decode(fileContent.content)
            fileOut = open(os.path.join(FloatingTools.INSTALL_DIRECTORY, serverPath), "w")
            fileOut.write(fileData)
            fileOut.close()
        except (github.GithubException, IOError):
            print 'Failed to update ' + serverPath


def loadBranch():
    """
    Load the branch information from the Branch.json file.
    :return: 
    """
    if not os.path.exists(FloatingTools.DATA):
        os.mkdir(FloatingTools.DATA)

    branchFile = os.path.join(FloatingTools.DATA, 'Branch.json')
    # create the file if it doesnt exists.
    if not os.path.exists(branchFile):
        # build the default release data
        branchData = {'branch': 'master', 'build-date': None, 'build-time': None}
        # dump the data
        json.dump(branchData, open(branchFile, 'w'), indent=4, sort_keys=True)
    # load the branch data
    branchData = json.load(open(branchFile, 'r'))

    # connect to github and pull the FloatingTools repository.
    hub = github.Github()
    repository = hub.get_repo('aldmbmtl/FloatingTools')
    commit = None

    # find the branch being requested
    for branch in repository.get_branches():
        if branch.name == branchData['branch']:
            commit = branch.commit
            break

    # grab the sha tag for loading from the branch.
    sha = commit.sha
    latestBuildData = githubDate2Datetime(commit.stats.last_modified)

    # begin download
    if branchData['build-date'] is None:
        downloadBuild(repository, sha)

        # update the branch data
        branchData['build-date'] = latestBuildData.date().isoformat()
        branchData['build-time'] = latestBuildData.time().isoformat()

        # save out data
        json.dump(branchData, open(branchFile, 'w'), indent=4, sort_keys=True)

    elif datetime.datetime(year=int(branchData['build-date'].split('-')[0]),
                           month=int(branchData['build-date'].split('-')[1]),
                           day=int(branchData['build-date'].split('-')[2]),
                           hour=int(branchData['build-time'].split(':')[0]),
                           minute=int(branchData['build-time'].split(':')[1]),
                           second=int(branchData['build-time'].split(':')[2])) < latestBuildData:
        downloadBuild(repository, sha)

        # update the branch data
        branchData['build-date'] = latestBuildData.date().isoformat()
        branchData['build-time'] = latestBuildData.time().isoformat()

        # save out data
        json.dump(branchData, open(branchFile, 'w'), indent=4, sort_keys=True)

    else:
        pass


loadBranch()
