from __future__ import print_function

# ft imports
import FloatingTools

# Python imports
import os
import urllib
import zipfile
import traceback
import importlib

# globals
FT_NET_URL = 'http://floatingtoolsnet.2naxcry8ia.us-west-2.elasticbeanstalk.com/'
if os.environ.get('FT_NET_URL'):
    FT_NET_URL = os.environ.get('FT_NET_URL')

# token
TOKEN = None
TOKEN_FILE = os.path.join(FloatingTools.DATA, 'token')

# client
CLIENT = None
CLIENT_FILE = os.path.join(FloatingTools.DATA, 'client')

# shed
SHED = None


def installToken():
    """
Each install is tied to a unique token tethered to this installs specific ip address tied to the routers public address.
This token is then saved to the token file in the data folder. This token can expire or be blocked from FT.NET
    """
    global TOKEN

    if not TOKEN:
        # validate the token file on disk
        if not os.path.exists(TOKEN_FILE):
            response = urllib.urlopen(FT_NET_URL + 'profile/requestToken').read()

            # handle broken response
            if response == 'None':
                # remove token information
                try:
                    os.unlink(TOKEN_FILE)
                except:
                    pass
                raise Exception('\nInvalid Token. Log into FT.NET and click "Connect client" under the Client dropdown '
                                'section at the top of the profile page. Then relaunch this application.'
                                '\n\tProfile page: http://floatingtoolsnet.2naxcry8ia.us-west-2.elasticbeanstalk.com/profile\n')

            # save data
            with open(TOKEN_FILE, 'w') as tf:
                tf.write(response)

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
            SHED = eval(urllib.urlopen(FT_NET_URL + 'profile/requestShed?token=' + installToken()).read())
        except Exception as e:
            print(e)
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
        request = urllib.urlopen(services[service])

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


def clientInfo():
    """
Get the install information that describes this client.
    """
    global CLIENT

    if not CLIENT:
        # validate the client file on disk
        if not os.path.exists(CLIENT_FILE):

            # save data
            with open(CLIENT_FILE, 'w') as cf:
                cf.write('')

            return None

        # pull client data
        with open(CLIENT_FILE, 'r') as cf:
            CLIENT = cf.read()

    return CLIENT


def updateClient():
    """
Download the client designated from FT.NET for this token.
    """
    if toolShed()['install'] == clientInfo():
        return

    # update the client file with the new target version
    with open(CLIENT_FILE, 'w') as cf:
        cf.write(toolShed()['install'])

    # pull target url for the requested version
    targetVersion = 'https://github.com/aldmbmtl/FloatingTools/archive/%s.zip' % toolShed()['install']

    # download the zip
    updateZip = os.path.join(os.path.dirname(FloatingTools.FLOATING_TOOLS_ROOT), 'update.zip')
    urllib.urlretrieve(targetVersion, updateZip)
    update = zipfile.ZipFile(updateZip, 'r')

    root = update.filelist[0].filename.split('/')[0]

    # clean out old version
    if not os.environ.get('FT_DEV'):
        for i in os.listdir(FloatingTools.FLOATING_TOOLS_ROOT):

            if i in ['cache', 'data', 'packages']:
                continue

            target = os.path.join(FloatingTools.FLOATING_TOOLS_ROOT, i)

            if os.path.isfile(target):
                os.unlink(target)
            if os.path.isdir(target):
                os.rmdir(target)

    # unpack zip
    for i in update.filelist:
        i.filename = i.filename.replace(root + '/', '')
        if not i.filename.startswith("FloatingTools/"):
            continue

        if os.environ.get('FT_DEV'):
            continue

        update.extract(i, os.path.dirname(FloatingTools.FLOATING_TOOLS_ROOT))

    # release the zip
    update.close()

    # clean up
    os.unlink(updateZip)

    try:
        reload(FloatingTools)
    except NameError:
        importlib.reload(FloatingTools)


updateClient()