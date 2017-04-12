"""
Default handlers
"""
# package imports
from C_File import registerFileHandler

# python imports
import sys, imp


def pyHandler(C_File):
    """
    Handler for python objects on HFX.com. This will import them by default.
    :param C_File: 
    :return: 
    """
    moduleName = C_File.filename().split('.')[0]
    mod = imp.new_module(moduleName)
    exec C_File.content() in mod.__dict__
    sys.modules[moduleName] = mod


registerFileHandler('.py', pyHandler)
