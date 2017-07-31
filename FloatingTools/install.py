"""
Validate the dependencies are installed.
"""

__all__ = [
    'installPackage'
]

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
sys.path.insert(0, FloatingTools.PACKAGES)

# begin checking dependency list
# pip

# check if pip is installed. This is installed at the Python installs site-packages. Everything else is installed in the
# FloatingTools/packages directory.
ft_packages = os.listdir(FloatingTools.PACKAGES)

try:
    import pip
except ImportError:
    # determine executable from the application wrapper
    executable = sys.executable
    args = []
    if FloatingTools.WRAPPER and FloatingTools.WRAPPER.ARGS:
        args = FloatingTools.WRAPPER.ARGS

    FloatingTools.FT_LOOGER.info("Python executable (+args) for pip install: " + executable)

    # install pip
    downloadPath = os.path.join(FloatingTools.PACKAGES, 'get-pip.py')
    urllib.urlretrieve("https://bootstrap.pypa.io/get-pip.py", downloadPath)

    pipDL = open(downloadPath, 'r')
    code = pipDL.read()
    code = code.replace('sys.exit(pip.main(["install", "--upgrade"] + args))',
                        'sys.exit(pip.main(["install", "pip", "-t", "%s"]))' % FloatingTools.PACKAGES)
    pipDL.close()
    open(downloadPath, 'w').write(code)

    command = [os.path.abspath(executable)] + args + [downloadPath]

    # execute the python pip install call
    subprocess.call(command)

    # delete get-pip.py
    os.unlink(downloadPath)

    try:
        import pip
    except ImportError:
        raise Exception('Pip is required for install. Launch FloatingTools on its own by opening the python '
                        'interpreter and running:\n\nimport sys\nsys.path.append("%s")\nimport FloatingTools\n'
                        '\nThis will allow the packages required to be installed into the FloatingTools package'
                        '. Once complete, relaunch this application.' %
                        os.path.abspath(FloatingTools.__file__ + '/../../'))

# upgrade pip if needed
pip.main(['install', '--upgrade', 'pip'])
if 'setuptools' not in ft_packages:
    pip.main(['install', '-U', 'pip', 'setuptools', '-t', FloatingTools.PACKAGES])

def installPackage(package, pipName=None):
    """
Install packages into FT from pip.
:param package: the name to import the package
:param pipName: in-case the pip install name is different from the module name.
    """
    # due to the nature of the pip install process, we want to set the PYTHONPATH environment variable pointed to the
    # FT/packages directory so that setuptools is in sync with the version of pip installed.
    PYTHONPATH = os.environ["PYTHONPATH"] if "PYTHONPATH" in os.environ else None
    os.environ['PYTHONPATH'] = FloatingTools.PACKAGES

    # Verify the github lib exists
    try:
        __import__(package)
    except ImportError:
        if not pipName:
            pipName = package

        pip.main(['install', pipName, '-t', FloatingTools.PACKAGES])

        # verify install
        __import__(package)

    FloatingTools.FT_LOOGER.info(package + ' pip installed and ready for use.')

    # flush env
    if PYTHONPATH:
        os.environ['PYTHONPATH'] = PYTHONPATH