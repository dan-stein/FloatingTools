"""
AUTO LOADER FOR DETERMINING APPLICATION
"""

# python imports
import os
import sys

# package imports
from AbstractApp import AbstractApplication, setWrapper, wrapper

__all__ = [
    'AbstractApplication',
    'wrapper',
    'setWrapper'
]

exclude = ['__init__.py', 'AbstractApp.py']

sys.path.append(os.path.dirname(__file__))

for wrapperMod in os.listdir(os.path.dirname(__file__)):
    if wrapperMod in exclude or wrapperMod.endswith('.pyc'):
        continue
    try:
        mod = __import__(wrapperMod.replace('.py', ''))
        break
    except ImportError:
        pass
