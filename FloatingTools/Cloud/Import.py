"""
Defines the Cloud loading capabilities for FloatingTools
"""
# python imports
import imp, sys

# FT imports
import FloatingTools


def ImportCloudModule(C_File):
    """
    Import a module from url path in HFX.
    :param C_File: FloatingTools.Pipeline.C_File.CloudFileObject
    :return: 
    """

    # check type passed.
    if not isinstance(C_File, FloatingTools.Pipeline.C_File.CloudFileObject):
        FloatingTools.FT_LOGGER.error('Failed to import %(C_File)s. Must be '
                                      'FloatingTools.Pipeline.C_File.CloudFileObject. Use FloatingTools.GetCloudFile '
                                      'and then pass to this function.' % locals())

        raise TypeError('Failed to import cloud module. Check logger.')
