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
For step by step videos for installing, go [here](http://www.hatfieldfx.com/floating-tools).

1. Download the release you would like to use from [here](https://github.com/aldmbmtl/FloatingTools/releases). 
Usually the latest is fine. If you are on Linux, download the .tar. The .zip will be fine for all other operating systems. 

2. After downloading and unpacking the .zip or .tar, there should be a "FloatingTools" folder and an "installers". Open 
the installers folder and double click the installer file for your OS. If you are running Linux or OSX, you may need to
execute it through the command line. Just drag and drop the file into the terminal and hit enter.

3. After the install is complete, you can move the FloatingTools folder wherever you want to use it! 
<span style="color:red"> YOU MUST COPY THE FLOATINGTOOLS DIRECTORY OUT OF THE ZIP FOLDER!</span>. This means if you 
download and unpack the zip, you want to get FloatingTools-0.5.2/-->*FloatingTools*<--. Not the zip! In order to use it, 
just copy it where you want it and import it! 
```python
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

[API documentation](https://aldmbmtl.github.io/FloatingTools/index.html)


