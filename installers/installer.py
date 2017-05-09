"""
Installer file for FloatingTools
"""
import sys
import shutil
import traceback
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))

try:
    import FloatingTools

    print "Floating Tools installed and ready. Cleaning up..."
    shutil.rmtree(dirname(__file__))
except ImportError:
    traceback.print_exc()
