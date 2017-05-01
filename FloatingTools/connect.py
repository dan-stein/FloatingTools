__all__ = [
    'gitHubConnect',
    'verifyLogin'
]

# FloatingTools import
import FloatingTools

# package imports
from github import Github, BadCredentialsException

# globals
HUB = None


def gitHubConnect():
    """
    Get the logged in GitHub connection.
    :return: 
    """
    return HUB


def verifyLogin():
    """
    Verify login information. This will first check if there is data in the local User.json file. If the username and 
    password is None, it will launch the FloatingTools.Dashboard.login() process for the user to login.
    :return: 
    """
    global HUB

    loginInfo = FloatingTools.userData()['Login']
    if loginInfo['username'] is None or loginInfo['password'] is None:
        return False
    try:
        HUB = Github(loginInfo['username'], loginInfo['password'])
        for repo in HUB.get_user().get_repos():
            break
        return True
    except BadCredentialsException:
        return False
