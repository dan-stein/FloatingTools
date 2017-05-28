"""
Github handler class 
"""
# python imports
import os
import json
import shutil
import zipfile
import webbrowser
from functools import partial

# FT imports
import FloatingTools
from AbstractService import Handler


class GitHubHandler(Handler):

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
        :return: 
        """
        source = source['Username'] + '/' + source['Repository']

        # pull repository
        if '/' not in source:
            repository = FloatingTools.gitHubConnect().get_user().get_repo(source)
        else:
            repository = FloatingTools.gitHubConnect().get_repo(source)

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