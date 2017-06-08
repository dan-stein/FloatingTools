# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template_string, redirect

# package imports
from ui import *
from utilities import SERVER

# globals
VALID_LOGIN = True
LOGGEDIN = False


@SERVER.route('/login', methods=['GET', 'POST'])
def renderLogin():
    """
    Render login page for Floating Tools
    :return: 
    """
    container = Div(Class='container')
    well = Div(Class='well well-sm')
    header = Center(
        Header('Floating Tools', 2)
    )
    subHeader = Center(
        Element('span', 'Login with your GitHub account information', Class='help-block')
    )

    form = Form(action='/shutdown' if LOGGEDIN else '/checkLogin')
    formRow = Div(Class='form-group row')
    formRow.addValue(Div(Class='col-xs-4'))
    messageArea = formRow.addValue(Div(Class='col-xs-4'))

    form.addValue(formRow)

    if LOGGEDIN:
        alert = messageArea.addValue(Div(Class='alert alert-success'))
        alert.addValue(Center('<strong>Logged in!</strong> Click the continue button and close this tab.'))
        messageArea.addValue(Center(Element('input', type='submit', attributes={'value': 'Continue'}, Class='btn btn-success')))
    else:
        if not VALID_LOGIN:
            col = Collapse(id='login_info', value='This should be the login for your GitHub account.')
            link = Element('a', attributes=col.linkTo(), value='Invalid Log In')

            messageArea.addValue(Center(link))
            messageArea.addValue(Center(col))

        # fields
        userRow = Div(Class='form-group row')
        userRow.addValue(Div(Class='col-xs-4'))
        userRow.addValue(Div(Class='col-xs-4', value=Element('input', type='text', Class='form-control', name='username', placeholder='Username')))
        userRow.addValue(Div(Class='col-xs-4'))

        # fields
        passwordRow = Div(Class='form-group row')
        passwordRow.addValue(Div(Class='col-xs-4'))
        passwordRow.addValue(Div(Class='col-xs-4', value=Element('input', type='password', Class='form-control', name='password', placeholder='Password')))
        passwordRow.addValue(Div(Class='col-xs-4'))

        form.addValue(userRow)
        form.addValue(passwordRow)

        form.addValue(Center(Element('input', type='submit', attributes={'value': 'Login'}, Class='btn btn-success')))

    form.addValue(Div(Class='col-xs-4'))

    well.addValue(header)
    well.addValue(subHeader)
    well.addValue(form)
    container.addValue(well)

    page = Page('Login')
    page.add(container)

    return render_template_string(page.render())
    # return render_template('Login.html', invalidLogin=VALID_LOGIN, loggedIn=LOGGEDIN)


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
