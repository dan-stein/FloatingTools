"""
Authenticate connection to HFX.com
"""
# FT imports
import Utilities
from FloatingTools.Cloud import userLogIn, studioLogIn, updateStudioLogin, updateUserLogin, FT_LOGGER
from FloatingTools.packages.wordpress_xmlrpc import Client, InvalidCredentialsError
from FloatingTools.packages.wordpress_xmlrpc.methods.posts import GetPosts


def login(username, password, updateFunction):
    """
    Performs the actual login validation process. NOT MEANT FOR PUBLIC USE!
    :param username:
    :param password:
    :param updateFunction:
    :return:
    """
    while 1:

        # enter login information
        if username == '':
            username = raw_input('Username: ')
            password = raw_input('Password: ')

        if password == '':
            password = raw_input('Username: %s\nPassword: ' % username)

        # perform validation
        try:
            client = Client('http://www.hatfieldfx.com/xmlrpc.php', username, password)
            client.call(GetPosts())

            # update the associated login file with the new information.
            updateFunction(username, password)
            Utilities.FT_CLIENT = client

            FT_LOGGER.info(' User: %s' % username)

            return True

        except InvalidCredentialsError:

            username = ''
            password = ''

            print 'Invalid login! Try again.'

# authenticate user information and validate with the website
# first check if this install is only using the studio level login information
studioInfo = studioLogIn()
userInfo = userLogIn()

if studioInfo['use_studio_login']:

    username = studioInfo['username']
    password = studioInfo['password']
    updateFunction = updateStudioLogin

else:

    username = userInfo['username']
    password = userInfo['password']
    updateFunction = updateUserLogin

login(username, password, updateFunction)