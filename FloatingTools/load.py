"""
Handles all loading operations
"""
# python imports
import os
import json

# FloatingTools imports
import FloatingTools


def repositorySettings():
    """
    Load the repository settings file
    :return: 
    """
    sourcesFile = os.path.join(FloatingTools.DATA, 'sources.json')

    if not os.path.exists(sourcesFile):
        defaultData = {'repositories': [{'aldmbmtl/FloatingTools': ['Tools/{application}/']}]}
        json.dump(defaultData, open(sourcesFile, 'w'), indent=4, sort_keys=True)
