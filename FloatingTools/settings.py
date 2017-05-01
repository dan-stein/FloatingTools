"""
Settings API
"""
__all__ = [
    'repositoryData',
    'loadSources',
    'updateLogin',
    'updateSources',
    'userData'
]

# FloatingTools imports
import FloatingTools

# python imports
import os
import json

# globals
USER = os.path.join(FloatingTools.DATA, 'User.json')
SOURCES = os.path.join(FloatingTools.DATA, 'Sources.json')

# make the internal data folder if it doesnt exist.
if not os.path.exists(os.path.dirname(USER)):
    os.mkdir(os.path.dirname(USER))


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
