# ft imports
import FloatingTools

# Python imports
import os
import urllib2
import traceback
import webbrowser

# globals
FT_NET_URL = 'http://floatingtoolsnet.2naxcry8ia.us-west-2.elasticbeanstalk.com/'

# token
TOKEN = None
TOKEN_FILE = os.path.join(FloatingTools.DATA, 'token')

# user
USER = None
USER_FILE = os.path.join(FloatingTools.DATA, 'user')

# shed
SHED = None


def user():
    """
    Pull the username saved on disk.
    """
    global USER

    # grab cache
    if not USER:
        # validate the user file on disk
        if not os.path.exists(USER_FILE):
            username = raw_input('FloatingTools.NET username: ')

            # save data
            with open(USER_FILE, 'w') as uf:
                uf.write(username)

        # pull username
        with open(USER_FILE, 'r') as uf:
            USER = uf.read()

    return USER


def installToken():
    """
Each install is tied to a unique token tethered to this installs specific ip address tied to the routers public address.
This token is then saved to the token file in the data folder. This token can expire or be blocked from FT.NET
    """
    global TOKEN

    if not TOKEN:
        # validate the token file on disk
        if not os.path.exists(TOKEN_FILE):

            # save data
            with open(TOKEN_FILE, 'w') as tf:
                tf.write(urllib2.urlopen(FT_NET_URL + 'profile/requestToken?user=' + user()).read())

        # pull token
        with open(TOKEN_FILE, 'r') as tf:
            TOKEN = tf.read()

    return TOKEN


def refreshToken():
    """
Request a new token for this install.
    """
    # remove token information
    os.unlink(TOKEN_FILE)

    # pull new token
    return installToken()


def toolShed():
    """
Request the latest tool shed data.
    """
    global SHED

    if not SHED:
        try:
            # request the tool shed tied to the token on disk
            SHED = eval(urllib2.urlopen(FT_NET_URL + 'profile/requestShed?token=' + installToken()).read())
        except urllib2.HTTPError:
            raise Exception('Invalid token. Token passed is either blocked, sent from an ip address not tethered to '
                            'this user, or you have never logged into the site from this computer on the FT.NET site.')

    return SHED


def requiredServices():
    """
Get all required services for the tool shed.
    """
    return toolShed()['services']


def requestedTools():
    """
Get all tools in the requested tool shed.
    """
    return toolShed()['tools']


def downloadServices():
    """
Download the required services into memory for use.
    """
    # pull the required services
    services = requiredServices()

    # loop over only required services
    for service in services:
        request = urllib2.urlopen(services[service])

        # pull the raw code before execution
        code = request.read()

        # execute the code but if it fails print the error and continue
        try:
            exec code
        except Exception:
            traceback.print_exc()


def downloadTools():
    """
Pull the list of tools requested and download them.
    """
    # first download the latest services that are required for all tools.
    downloadServices()

    # pull down the requested tools and begin loop over each tool.
    tools = requestedTools()
    for tool in tools:
        try:
            FloatingTools.createToolbox(tools[tool]['service'], tools[tool]['fields'])
        except:
            traceback.print_exc()