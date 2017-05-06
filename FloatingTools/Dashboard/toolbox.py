# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# github imports
from github import UnknownObjectException

# package imports
from utilities import SERVER

# python imports
import json


@SERVER.route('/toolbox', methods=['GET', 'POST'])
def renderToolbox():
    """
    Render tool shed page to configure Floating Tools
    :return: 
    """

    localRepos = {}
    for repo in FloatingTools.gitHubConnect().get_user().get_repos():
        localRepos[repo.name] = repo

    # get the user repositories and add to the dashboard env
    FloatingTools.Dashboard.setDashboardVariable('user_repos', sorted(localRepos.keys()))

    # handle local toolbox
    localToolbox = request.args.get("toolbox")
    if not localToolbox:
        localToolbox = localRepos.keys()[0]
    FloatingTools.Dashboard.setDashboardVariable('toolbox', localToolbox)
    FloatingTools.Dashboard.setDashboardVariable('toolbox_data', None)

    # validate the local toolbox
    data = None
    try:
        data = json.loads(localRepos[localToolbox].get_file_contents('/toolbox.json').decoded_content)
    except UnknownObjectException:
        pass

    finally:
        FloatingTools.Dashboard.setDashboardVariable('toolbox_data', data)

    return render_template('Toolbox.html', **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/toolbox/_save')
def saveToolbox():
    return redirect('/toolbox')


def toolbox():
    """
    Launch tool shed page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='toolbox')
