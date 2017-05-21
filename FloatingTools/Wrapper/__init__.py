"""
AUTO LOADER FOR DETERMINING APPLICATION
"""
# floating tools imports
import FloatingTools

# python imports
import os
import sys

# package imports
from AbstractApp import AbstractApplication, setWrapper, wrapper

__all__ = [
    'AbstractApplication',
    'wrapper',
    'setWrapper',
    'APP_WRAPPER',
    'APP_WRAPPERS'
]

# globals
APP_WRAPPER = None
APP_WRAPPERS = []


exclude = ['__init__.py', 'AbstractApp.py']
sys.path.append(os.path.dirname(__file__))

for wrapperMod in os.listdir(os.path.dirname(__file__)):
    if wrapperMod in exclude or wrapperMod.endswith('.pyc'):
        continue
    try:
        mod = __import__(wrapperMod.replace('.py', ''))

        for i in dir(mod):
            obj = mod.__getattribute__(i)
            if 'appTest' in dir(obj):
                try:
                    if obj.name() is not None:
                        if obj.EXECUTABLE:
                            obj.EXECUTABLE_ORDER = sorted(obj.EXECUTABLE)
                        APP_WRAPPERS.append(obj)
                        wrap = obj()
                        APP_WRAPPER = obj
                except:
                    pass
    except:
        pass

FloatingTools.Dashboard.setDashboardVariable('wrappers', APP_WRAPPERS)
FloatingTools.Dashboard.setDashboardVariable('active_wrapper', APP_WRAPPER)
