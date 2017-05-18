"""
Handles all loading operations
"""
# python imports
import os
import shutil
import urllib
import zipfile

# FT imports
import FloatingTools


def downloadToolbox(repo):
    """
    Download toolbox and unpack
    :param repo: 
    :return: 
    """
    # repo information
    username, repository = repo.full_name.split('/')
    downloadPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, username, repository)
    zipPath = os.path.join(FloatingTools.FLOATING_TOOLS_CACHE, repo.full_name.replace('/', '.'))

    # download data
    zipURL = repo.get_archive_link('zipball')
    urllib.urlretrieve(zipURL, zipPath)

    # set up download path for repo
    if os.path.exists(downloadPath):
        shutil.rmtree(downloadPath)
    os.makedirs(downloadPath)

    # load zip file
    zip_ref = zipfile.ZipFile(zipPath, 'r')

    # begin unpack
    os.chdir(downloadPath)
    root = zip_ref.filelist[0].filename.split('/')[0]
    for i in zip_ref.filelist:
        # create local paths
        cleanPath = i.filename.replace(root + '/', '')
        if cleanPath == '':
            continue

        # extract file contents
        localPath = zip_ref.extract(i)
        targetPath = localPath.replace(root + '/', '')

        # move to proper location
        shutil.move(localPath, targetPath)

    # clear old download path
    shutil.rmtree(os.path.join(downloadPath, root))

    # close the zip
    zip_ref.close()

    # delete zip
    os.unlink(zipPath)