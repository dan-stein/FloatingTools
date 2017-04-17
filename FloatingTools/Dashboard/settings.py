# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# package imports
from utilities import SERVER


@SERVER.route('/settings', methods=['GET', 'POST'])
def renderSettings():
    """
    Render settings page to configure Floating Tools
    :return: 
    """
    repositories = FloatingTools.repositoryData()

    return render_template('Settings.html', repositories=repositories)


@SERVER.route('/addRepo')
def _addRepository():
    """
    --private--
    :return: 
    """
    print request.values
    # for repository in FloatingTools.repositorySettings():
    #     print request.form.get(repository['name'])

    return redirect('/settings')


def settings():
    """
    Launch settings page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='settings')
