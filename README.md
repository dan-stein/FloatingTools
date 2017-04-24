# Floating Tools

Maintained by [HatfieldFX LLC](http://www.hatfieldfx.com/)

## Installation

Installing FloatingTools is intended to be very simple as to allow for less technical people to it set up.

### System requirements:
 - python 2.7 or 2.6
 - [GitHub account](https://github.com/) with at least 1 repository. This is your digital toolbox now!

### Required packages that will be installed:
We do this all for you so no reason to worry! This is just information about what we are installing for you.
If you already have these installed in your site-packages, we wont install ours. If you don't know if you have them or 
not, no worries, we will figure it out for you!

 - [pip](https://pip.pypa.io/en/stable/)
    - pip is an awesome library for easily installing libraries. We use it to install the other packages we have listed.
 - [PyGithub](http://pygithub.readthedocs.io/en/latest/introduction.html)
    - FloatingTools interacts with github repositories through this library. Repository browsing/uploading/downloading 
    and authentication is all handled here. 
 - [Flask](http://flask.pocoo.org/docs/0.12/)
    - FloatingTools uses an internal web service for the settings interaction. This was chosen because the easiest
    way to make cross platform UI design consistently was utilizing a web front end with html powered by flask.
    
We install these libraries into the actual FloatingTools package. This is usually pretty unconventional, but the reason
we do is so that we don't go spraying these libraries all over your python site-packages! If you uninstall FloatingTools 
(just delete the folder), it will remove everything including the other packages mentioned above. With the exception of pip. 
Pip requires being installed in the python site-packages.

### Install instructions:
1. Download the release you would like to use from [here](https://github.com/aldmbmtl/FloatingTools/releases). 
Usually the latest is fine. If you are on Linux, download the .tar. The .zip will be fine for all other operating systems. 

2. After downloading and unpacking the .zip or .tar, open the directory and copy the FloatingTools folder 
(this is the python package) and put it on your python sys.path. If you are in Nuke for example, your .nuke directory is
 fine. This package is set up for individual use and studio use. For studio installs, you can store this in a server
 location and it will work the same.
   
3. Simply import FloatingTools and it will make you log in to your github account.
```python
import sys
sys.path.append("path/to/floatingtools")

# this will install everything you need!
import FloatingTools
```
You're done!

Getting Started
-
After installation is complete, open any of the following applications that are supported by FloatingTools and has 
FloatingTools installed on the sys.path.
 + Nuke
 + Maya

If the application has a valid ApplicationWrapper, there should be a menu in the applications UI for FloatingTools. 
Click FloatingTools/Dashboard/Settings from the menu and your web browser should open up with the FloatingTools settings
page. Here you will see information about the toolboxes that are being loaded from github and also install information 
and settings.

## Technical Information

### Basic API calls
FloatingTools comes with a very simple api. The intention is once again to make this system very user friendly. So most
everything you'd need to do can be done from the Dashboard pages. But if you'd like to make calls from the shell or 
something like that, here are some basic examples for opening those pages. 
```python
import FloatingTools

# For launching the settings/uploading/login server

# log in page
FloatingTools.Dashboard.login()

# upload page
FloatingTools.Dashboard.upload()

# settings page
FloatingTools.Dashboard.settings()
```

#### Application Wrappers
FloatingTools runs on an abstraction system. If you want to extend FloatingTools to a new application, like Houdini, 
simply subclass the AbstractApplication class and add the path to your abstraction to FloatingTools. 
 
```python
import FloatingTools

class HoudiniWrapper(FloatingTools.AbstractApplication):
    FILE_TYPES = ['.hip']
    NAME = 'Houdini'
    APP_ICON = 'http://whatever/icon.jpg' # url to the application icon.
    
    @staticmethod
    def addMenuSeparator(menuPath):
        """
        Code for houdini menu sep.
        """
        
    @staticmethod
    def appTest():
        """
        This function is run to test if we are in houdini
        
        try to do something that if it fails you can return 
        False meaning you aren't in houdini. Return True if we are in houdini 
        """
        if in houdini:
            return True
        else:
            return False
        
    @staticmethod
    def addMenuEntry(menuPath, command=None, icon=None, enabled=True):
        """
        Run the houdini equivalent for adding a menu item to the ui.
        """
        
    @staticmethod
    def loadFile(gitHubFileObject, fileType):
        """
        This is what houdini will do when a tool from github is passed to it. So if the file is a python script in the
        toolbox (repository), you would write the houdini handler here. 
        """

# here you would there set wrapper. This is required so FloatingTools know which wrapper it needs to use.
FloatingTools.setWrapper(HoudiniWrapper)
```



