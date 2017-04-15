"""
Validate the dependencies are installed.
"""
# python imports
import os
import sys
import urllib
import subprocess

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
