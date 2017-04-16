# python imports
import os

# Global variables
FLOATING_TOOLS_ROOT = os.path.dirname(__file__)
INSTALL_DIRECTORY = os.path.dirname(FLOATING_TOOLS_ROOT)
PACKAGES = os.path.join(FLOATING_TOOLS_ROOT, 'packages')

# validate the install
import install
