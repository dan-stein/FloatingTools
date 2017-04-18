# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# package imports
from utilities import SERVER

# python imports
import json


@SERVER.route('/settings', methods=['GET', 'POST'])
def renderSettings():
    """
    Render settings page to configure Floating Tools
    :return: 
    """
    repositories = FloatingTools.repositoryData()
    myRepositories = FloatingTools.gitHubConnect().get_user().get_repos()

    myToolbox = myRepositories[0].name

    for repo in myRepositories:
        if (FloatingTools.gitHubConnect().get_user().login + '/' + repo.name) in \
                [source['name'] for source in FloatingTools.loadSources()['repositories']]:
            myToolbox = repo.name

    for arg in request.args:
        if arg == 'myToolbox':
            myToolbox = request.args[arg]

    map = False
    try:
        map = json.loads(
            FloatingTools.gitHubConnect().get_user().get_repo(myToolbox).get_contents('/toolbox.json').decoded_content)
    except:
        pass

    return render_template('Settings.html',
                           myRepositories=myRepositories,
                           myToolbox=myToolbox,
                           myToolboxMap=map,
                           repositories=repositories
                           )


@SERVER.route('/saveSettings')
def _save():
    """
    --private--
    :return: 
    """

    sources = FloatingTools.loadSources()
    localRepoName = FloatingTools.gitHubConnect().get_user().login + '/' + request.args.get('myToolbox')
    localRepo = None

    added = False
    for item in sources['repositories']:
        if item['name'] in request.args:
            item['load'] = True
        elif item['name'] == localRepoName:
            localRepo = item
            added = True
        else:
            item['load'] = False

    if not added:
        localRepo = dict(name=localRepoName, load=True)
        sources['repositories'].append(localRepo)

    localRepo['load'] = (localRepoName + '/') in request.args

    FloatingTools.updateSources(sources)

    return redirect('/settings?myToolbox=' + request.args.get('myToolbox'))


@SERVER.route('/setupToolbox')
def _setUpToolbox():
    """
    --private--
    :return: 
    """

    repo = FloatingTools.gitHubConnect().get_user().get_repo(request.args.get('toolbox'))
    repo.create_file('/toolbox.json',
                     'Floating Tools Toolbox set up file created @ /toolbox.json.',
                     json.dumps({'paths': ['/tools/{Applications}']}, indent=4, sort_keys=True)
                     )

    return redirect('/settings?myToolbox=' + request.args.get('toolbox'))


@SERVER.route('/addToolboxPath')
def _addPath():
    """
    --private--
    :return: 
    """
    path = request.args.get('path').rstrip('/')
    toolBox = request.args.get('toolbox')
    repo = FloatingTools.gitHubConnect().get_user().get_repo(toolBox)
    f = repo.get_contents('/toolbox.json')
    publishedPaths = json.loads(f.decoded_content)

    if 'remove' in request.args:
        for index, i in enumerate(publishedPaths['paths']):
            if i == str(path):
                publishedPaths['paths'].pop(index)
        message = 'Floating Tools adding new path to toolbox.json: ' + path
    else:
        if path not in publishedPaths['paths']:
            publishedPaths['paths'].append(path)
            message = 'Floating Tools adding new path to toolbox.json: ' + path
        else:
            return redirect('/settings?myToolbox=' + toolBox)

    repo.update_file('/toolbox.json', message, json.dumps(publishedPaths, indent=4, sort_keys=True), f.sha)

    return redirect('/settings?myToolbox=' + toolBox)


@SERVER.route('/addToolbox')
def _addToolBox():
    """
    --private--
    :return: 
    """
    repoData = FloatingTools.loadSources()
    newToolBox = request.args.get('newToolbox').rstrip('/')

    add = True

    # loop over repo
    for index, repo in enumerate(repoData['repositories']):
        if repo['name'] == newToolBox:
            if 'remove' in request.args:
                del repoData['repositories'][index]
            add = False
            break
    if add:
        repoData['repositories'].append(dict(name=newToolBox, load=True))

    # update the local data
    FloatingTools.updateSources(repoData)

    return redirect('/settings?myToolbox=' + request.args.get('toolbox'))


def settings():
    """
    Launch settings page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='settings')
