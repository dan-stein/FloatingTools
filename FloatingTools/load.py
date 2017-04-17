"""
Handles all loading operations
"""
# python imports
import os
import json

# FloatingTools imports
import FloatingTools

# GitHub imports
from github import Github, BadCredentialsException

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


def loadPipeline():
    """
    Main pipeline loading function.
    :return: 
    """
    # pull repository data
    repoData = FloatingTools.repositoryData()

    # begin repo loop.
    for repo in repoData:
        if not repo['load']:
            continue

        # load the repository
        loadRepository(repo['name'])


def loadRepository(repository):
    """
    Load a repository based on a template path.
    :param repository: 
    :return: 
    """
    # load repository
    FloatingTools.FT_LOOGER.info('Loading Repository: ' + repository)
    repo = FloatingTools.gitHubConnect().get_repo(repository)

    # # apply template wildcard and formatting
    # path = path.replace('{application}', FloatingTools.wrapper().name()).rstrip('/')
    # if not path.startswith('/'):
    #     path = '/' + path
    # path = repository.split('/')[1] + path
    # FloatingTools.FT_LOOGER.info('Template Path: ' + path)

    # # loop over all the files in the build.
    # for fo in repo.get_dir_contents(path):
    #     base, ext = os.path.splitext(fo.name)
    #     if ext not in FloatingTools.wrapper().fileTypes():
    #         continue
    #     print fo.name
    #     print fo.path
