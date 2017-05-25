"""
Direct url handler class 
"""
# python imports
import os
import shutil
import urllib
import zipfile
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
        urllib.urlretrieve(self.sourcePath(), local)

        # determine how to handle source.
        if ext == '.zip':
            # load zip file
            zipRef = zipfile.ZipFile(local, 'r')

            # begin unpack
            os.chdir(self.installDirectory())
            root = zipRef.filelist[0].filename.split('/')[0]
            for i in zipRef.filelist:
                # create local paths
                cleanPath = i.filename.replace(root + '/', '')
                if cleanPath == '' or i.filename.startswith('__MACOSX') or os.path.basename(i.filename).startswith('.'):
                    continue

                # extract file contents
                initialInstall = zipRef.extract(i)
                reinstallPath = os.path.join(self.installDirectory(), *i.filename.replace(root, '').split('/'))

                # move
                shutil.move(initialInstall, reinstallPath)

            # delete directory
            shutil.rmtree(os.path.join(self.installDirectory(), root))

            # remove old zip
            os.unlink(local)

    def loadSource(self, source):
        """
        Load a zip or code directly from url
        
        :param source: 
        :return: 
        """
        # pull data
        website = source['URL'].split('.com')[0] + '.com'
        toolLink = os.path.dirname(source['URL']).rstrip('/')

        # set handler variables
        self.setSourcePath(source['URL'])
        repository, ext = os.path.splitext(os.path.basename(self.sourcePath()))
        self.setName(('www.' + website.split('www.')[1]) + '/' + repository)

        # menu items
        self.addMenuItem('/Open Home', partial(webbrowser.open, website), html=website)
        self.addMenuItem('/Open Tool Page', partial(webbrowser.open, toolLink), html=toolLink)

# add fields
URLHandler.addSourceField('URL')

# register handler
URLHandler.registerHandler('URL')