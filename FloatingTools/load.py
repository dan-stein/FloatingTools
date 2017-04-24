"""
Handles all loading operations
"""
# python imports
import os
import json
from functools import partial
import webbrowser

# FloatingTools imports
import FloatingTools

# GitHub imports
from github import Github, BadCredentialsException, GithubException

# globals
USER = os.path.join(FloatingTools.DATA, 'User.json')
SOURCES = os.path.join(FloatingTools.DATA, 'Sources.json')
HUB = None

if not os.path.exists(os.path.dirname(USER)):
    os.mkdir(os.path.dirname(USER))

def gitHubConnect():
    """
    Get the logged in GitHub connection.
    :return: 
    """
    return HUB


def repositoryData():
    """
    Load the repository settings file
    :return: 
    """
    if not os.path.exists(SOURCES):
        defaultData = {'repositories': [
            {
                'name': 'aldmbmtl/toolbox',
                'load': True
            }
        ]}
        json.dump(defaultData, open(SOURCES, 'w'), indent=4, sort_keys=True)

    return json.load(open(SOURCES, 'r'))['repositories']


def loadSources():
    return json.load(open(SOURCES, 'r'))


def updateSources(data):
    json.dump(data, open(SOURCES, 'w'), indent=4, sort_keys=True)


def userData():
    """
    Load the User.json contents.
    :return: 
    """
    if not os.path.exists(USER):
        defaultData = {'Login':
            {
                'username': None,
                'password': None
            }
        }
        json.dump(defaultData, open(USER, 'w'), indent=4, sort_keys=True)

    return json.load(open(USER, 'r'))


def updateLogin(username, password):
    """
    Update the login information.
    :param username: 
    :param password: 
    :return: 
    """
    # load user data
    data = userData()

    data['Login']['username'] = username
    data['Login']['password'] = password

    json.dump(data, open(USER, 'w'), indent=4, sort_keys=True)


def verifyLogin():
    """
    Verify login information. This will first check if there is data in the local User.json file. If the username and 
    password is None, it will launch the FloatingTools.Dashboard.login() process for the user to login.
    :return: 
    """
    global HUB

    loginInfo = userData()['Login']
    if loginInfo['username'] is None or loginInfo['password'] is None:
        return False
    try:
        HUB = Github(loginInfo['username'], loginInfo['password'])
        for repo in HUB.get_user().get_repos():
            break
        return True
    except BadCredentialsException:
        return False


def repoWalk(repo, path, root):
    """
    --private--
    :param repo: 
    :param path: 
    :return: 
    """
    try:
        repoContents = repo.get_dir_contents(path)
    except GithubException:
        FloatingTools.FT_LOOGER.info(path + ' is not a valid path in this toolbox.')
        return

    for fo in repoContents:
        # loop over directories
        if fo.type == 'dir':
            repoWalk(repo, path + '/' + fo.name, root)
            return

        # filter out files that do not pertain to this application
        basename, ext = os.path.splitext(fo.name)
        if ext not in FloatingTools.APP_WRAPPER.fileTypes():
            continue

        # register tool with the application
        FloatingTools.APP_WRAPPER.addMenuEntry(
            (FloatingTools.__name__ + '/%s' % os.path.splitext(repo.name)[0]) + fo.path.replace(root, ''),
            partial(FloatingTools.APP_WRAPPER.loadFile, fo, ext))


def loadTools():
    """
    Main tool loading function.
    :return: 
    """
    # set up dashboard in the application wrapper if there is one loaded.
    if FloatingTools.APP_WRAPPER:
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Dashboard/My Toolbox/Upload',
                                               FloatingTools.Dashboard.upload)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Dashboard/My Toolbox/Organize')
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__ + '/Dashboard')
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Dashboard/Settings',
                                               FloatingTools.Dashboard.settings)
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Network Toolboxes', enabled=False)

    # pull repository data
    repoData = FloatingTools.repositoryData()

    # begin repo loop.
    for repo in repoData:
        if not repo['load']:
            continue

        # connect to the repository
        FloatingTools.FT_LOOGER.info('Loading Repository: ' + repo['name'])
        repo = FloatingTools.gitHubConnect().get_repo(repo['name'])

        # load toolbox data
        toolboxData = json.loads(repo.get_contents('/toolbox.json').decoded_content)

        # loop over the toolbox path
        for path in toolboxData['paths']:
            wildCards = dict(
                Applications=FloatingTools.APP_WRAPPER.name() if FloatingTools.APP_WRAPPER is not None else 'Generic'
            )

            for card in wildCards:
                path = path.replace('{%s}' % card, wildCards[card])

            repoWalk(repo, path, path.strip('/'))

    if FloatingTools.APP_WRAPPER:
        FloatingTools.APP_WRAPPER.addMenuSeparator(FloatingTools.__name__)
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/HatfieldFX',
                                               lambda: webbrowser.open("http://www.hatfieldfx.com/floating-tools"))
        FloatingTools.APP_WRAPPER.addMenuEntry(FloatingTools.__name__ + '/Support/Repository',
                                               lambda: webbrowser.open("https://github.com/aldmbmtl/FloatingTools"))
