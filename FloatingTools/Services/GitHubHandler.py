"""
Github handler class 
"""
# python imports
import os
import json
import shutil
import webbrowser
from functools import partial

# FT imports
import FloatingTools
from AbstractService import Handler


class GitHubHandler(Handler):
    LOGIN_FIELDS = [
        FloatingTools.Dashboard.Form.email('username', ''),
        FloatingTools.Dashboard.Form.password('password', '')
    ]

    ICON = 'https://assets-cdn.github.com/images/modules/logos_page/Octocat.png'
    CONNECTION = None

    @classmethod
    def initialize(cls):
        # install the git hub lib through pip
        FloatingTools.installPackage('github', 'PyGithub')

        import github

        if not cls.userData():
            return

        cls.CONNECTION = github.Github(cls.userData()['username'], cls.userData()['password'])

        try:
            for repo in cls.CONNECTION.get_user().get_repos():
                break
            cls.WEBPAGE = 'https://github.com/' + cls.CONNECTION.get_user().login
        except github.BadCredentialsException:
            FloatingTools.FT_LOOGER.error('Github log in information is invalid! Correct them in the services page.')
            cls.CONNECTION = github.Github()

    def install(self):
        """
        Handle install
        :return: 
        """
        # extract data to build download path
        username, toolbox = self.sourcePath().full_name.split('/')
        toolboxPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, username, toolbox)
        zipPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, '.'.join([username, toolbox]))

        # download data
        zipURL = self.sourcePath().get_archive_link('zipball')
        if not self.downloadSource(zipURL, zipPath):
            return

        # set up download path for repo
        if os.path.exists(toolboxPath):
            shutil.rmtree(toolboxPath)
        os.makedirs(toolboxPath)

        # install zip ball
        self.installZip(zipPath)

    def loadSource(self, source):
        """
Load GitHub source with the validated git connection.
The source should be "{username}/{repository}". If there is no "/", the current user is assumed.

:param source:
        """
        source = source['Username'] + '/' + source['Repository']

        # pull repository
        repository = self.CONNECTION.get_repo(source)

        # set required variables for this toolbox handler
        try:
            toolboxData = json.loads(repository.get_contents('/toolbox.json').decoded_content)
            self.setToolboxPaths(toolboxData['paths'])
        except Exception, e:
            FloatingTools.FT_LOOGER.debug(e)

        self.setName(repository.full_name)
        self.setSourcePath(repository)

        # build git repo link
        githubUrl = 'https://github.com/' + self.name()
        lic = githubUrl + '/blob/master/LICENSE'
        about = githubUrl + '/blob/master/README.md'

        # build menu items
        self.addMenuItem('/Open on GitHub', partial(webbrowser.open, githubUrl), html=githubUrl)
        self.addMenuItem('/License', partial(webbrowser.open, lic), html=lic)
        self.addMenuItem('/About', partial(webbrowser.open, about), html=about)


# add fields
GitHubHandler.addSourceField('Username')
GitHubHandler.addSourceField('Repository')

# register handler
GitHubHandler.registerHandler('GitHub')