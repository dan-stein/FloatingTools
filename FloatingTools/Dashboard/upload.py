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


@SERVER.route('/upload', methods=['GET', 'POST'])
def renderUpload():
    """
    Render upload page to upload tools to your repository.
    :return:
    """
    myRepositories = FloatingTools.gitHubConnect().get_user().get_repos()

    toolBoxes = {}

    for repo in myRepositories:
        try:
            toolboxPaths = json.loads(repo.get_contents('/toolbox.json').decoded_content)['paths']
        except UnknownObjectException:
            continue

        toolBoxes[repo.name] = toolboxPaths

    target = request.args.get('toolBox')
    if not target:
        target = toolBoxes.keys()[0]

    return render_template(
        'Upload.html',
        toolboxes=toolBoxes,
        toolbox=target,
        app_wrapper=FloatingTools.APP_WRAPPER,
        app_file_types=', '.join(FloatingTools.APP_WRAPPER.fileTypes())
    )


def upload():
    """
    Launch upload page to upload tools to your floating toolbox.
    :return: 
    """
    if FloatingTools.APP_WRAPPER is not None:
        FloatingTools.Dashboard.startServer(url='upload')
