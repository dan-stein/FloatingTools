"""
FloatingTools is protected under the MIT license and is owned and maintained by Hatfield FX, LLC. 

Copyright (c) 2017 Hatfield FX, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# namespace
__all__ = [
    'FLOATING_TOOLS_ROOT',
    'INSTALL_DIRECTORY',
    'PACKAGES',
    'PYTHON_EXECUTABLE',
    'DATA',
]

# python imports
import os
import sys
import logging

logging.basicConfig(level=logging.ERROR)

# Global variables
FT_LOOGER = logging.getLogger('FloatingTools')
FLOATING_TOOLS_ROOT = os.path.dirname(os.path.realpath(__file__))
FLOATING_TOOLS_CACHE = os.path.join(FLOATING_TOOLS_ROOT, 'cache')
INSTALL_DIRECTORY = os.path.dirname(FLOATING_TOOLS_ROOT)
PACKAGES = os.path.join(FLOATING_TOOLS_ROOT, 'packages')
DATA = os.path.join(FLOATING_TOOLS_ROOT, 'data')
PYTHON_EXECUTABLE = sys.executable

# create cache directory
if not os.path.exists(FLOATING_TOOLS_CACHE):
    os.makedirs(FLOATING_TOOLS_CACHE)

# create packages directory
if not os.path.exists(PACKAGES):
    os.makedirs(PACKAGES)

# create data directory
if not os.path.exists(DATA):
    os.makedirs(DATA)


DEV = True

# initial ft imports
from utilities import *
from ftnet import *

# standard lib imports
from AbstractService import Service, loadedServices, createToolbox, toolboxes, getToolbox, getService
