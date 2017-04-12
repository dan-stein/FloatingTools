"""
Floating Tools utils
"""
# python imports
import os
import json
import logging

# FloatingTools import
import FloatingTools


# set up logger
logging.basicConfig(level=logging.INFO)


# globals
FT_DIRECTORY = FloatingTools.__path__[0]
FT_STUDIO_LOGIN = os.path.join(FT_DIRECTORY, 'FloatingStudio.json')
FT_USER_LOGIN = os.path.join(os.path.expanduser('~'), 'FloatingUser.json')
FT_LOGGER = logging.getLogger('Floating Tools')
FT_CLIENT = None


def floatingToolsDirectory():
    """
    Get the path where the floating tools module lives. Mirrors calling FloatingTools.__package__
    :return:
    """
    return FT_DIRECTORY


def studioLogInPath():
    """
    Get the path where the floating tools studio level login information lives.
    :return:
    """

    # check if the studio login path exists
    if not os.path.exists(FT_STUDIO_LOGIN):

        # create the login file and populate with the default information
        loginFile = open(FT_STUDIO_LOGIN, 'w')
        loginInfo = {'use_studio_login': True, 'username': '', 'password': ''}
        json.dump(loginInfo, loginFile)

        # close the file
        loginFile.close()

    return FT_STUDIO_LOGIN


def userLogInPath():
    """
    Get the path where the floating tools user level login information lives.
    :return:
    """

    # check if the user login path exists
    if not os.path.exists(FT_USER_LOGIN):

        # create the login file and populate with the default information
        loginFile = open(FT_USER_LOGIN, 'w')
        loginInfo = {'username': '', 'password': ''}
        json.dump(loginInfo, loginFile)

        # close the file
        loginFile.close()

    return FT_USER_LOGIN


def studioLogIn():
    """
    Get the login information from the studio level.
    :return:
    """
    return json.load(open(studioLogInPath(), 'r'))


def userLogIn():
    """
    Get the login information from the user level.
    :return:
    """
    return json.load(open(userLogInPath(), 'r'))


def updateUserLogin(username, password):
    """
    Update the user login file
    :param username:
    :param password:
    :return:
    """
    information = userLogIn()
    information['username'] = username
    information['password'] = password

    json.dump(information, open(FT_USER_LOGIN, 'w'))


def updateStudioLogin(username, password):
    """
    Update the studio login file
    :param username:
    :param password:
    :return:
    """
    information = studioLogIn()
    information['username'] = username
    information['password'] = password

    json.dump(information, open(FT_STUDIO_LOGIN, 'w'))


def connection():
    """
    The connection to HFX.com
    :return:
    """
    return FT_CLIENT