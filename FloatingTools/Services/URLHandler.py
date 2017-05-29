"""
Direct url handler class 
"""
# python imports
import os
import shutil
import webbrowser
from functools import partial

# FT imports
from AbstractService import Handler


class URLHandler(Handler):

    def install(self):
        """
        Handle install
        :return: 
        """
        # pull install path
        basename = os.path.basename(self.sourcePath())
        repository, ext = os.path.splitext(basename)

        # set up download path for repo
        if os.path.exists(self.installDirectory()):
            shutil.rmtree(self.installDirectory())
        os.makedirs(self.installDirectory())

        # download data
        local = os.path.join(self.installDirectory(), basename)
        if not self.downloadSource(self.sourcePath(), local):
            return

        # determine how to handle source.
        if ext == '.zip':
            self.installZip(local)

    def loadSource(self, source):
        """
        Load a zip or code directly from url
        
        :param source: 
        :return: 
        """
        # pull data
        header, sitePath = source['URL'].split('//', 1)
        name = sitePath.split('/', 1)[0]
        website = header + '//' + name
        toolLink = os.path.dirname(source['URL']).rstrip('/')

        # set handler variables
        self.setSourcePath(source['URL'])
        repository, ext = os.path.splitext(os.path.basename(self.sourcePath()))
        self.setName(name + '/' + repository)

        # menu items
        self.addMenuItem('/Open Home', partial(webbrowser.open, website), html=website)
        self.addMenuItem('/Open Tool Page', partial(webbrowser.open, toolLink), html=toolLink)

# add fields
URLHandler.addSourceField('URL')

# register handler
URLHandler.registerHandler('URL')