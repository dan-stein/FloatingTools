# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# GitHub imports
from github import Github, BadCredentialsException

# package imports
from utilities import SERVER, stopServer

# globals
VALID_LOGIN = True
LOGGEDIN = False


@SERVER.route('/login', methods=['GET', 'POST'])
def renderLogin():
    """
    Render login page for Floating Tools
    :return: 
    """
    return render_template('Login.html', invalidLogin=VALID_LOGIN, loggedIn=LOGGEDIN)


@SERVER.route('/checkLogin')
def _validateLogin():
    """
    --private--
    :return: 
    """
    FloatingTools.updateLogin(request.values['username'], request.values['password'])

    global VALID_LOGIN
    global LOGGEDIN
    VALID_LOGIN = True

    if FloatingTools.verifyLogin() is True:
        LOGGEDIN = True
        return redirect('/login')
    else:
        VALID_LOGIN = False
        return redirect('/login')


def login():
    """
    Launch login page for Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='login')
