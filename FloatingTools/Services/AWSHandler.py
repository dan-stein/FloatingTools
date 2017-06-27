"""
Github handler class
"""
# python imports
import os

# FT imports
import FloatingTools
from AbstractService import Handler


class AWSHandler(Handler):
    LOGIN_FIELDS = [
        FloatingTools.Dashboard.Form.password('access key', ''),
        FloatingTools.Dashboard.Form.password('secret key', '')
    ]

    ICON = 'https://uploads.toptal.io/blog/category/logo/106/C.png'
    CONNECTION = None

    @classmethod
    def initialize(cls):
        # install the drive api lib through pip
        FloatingTools.installPackage('boto3', 'boto')

        import boto3
        from botocore.client import Config

        os.environ['AWS_ACCESS_KEY_ID'] = cls.userData()['access key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = cls.userData()['secret key']

        cls.CONNECTION = boto3.resource('s3', config=Config(signature_version='s3v4'))

    def loadSource(self, source):
        """
Load S3 bucket source.

:param source:
        """
        self.setSourcePath(source)
        self.setName(source['Bucket'])
        if source['Tool Path']:
            self.setName(self.name() + '>' + source['Tool Path'].replace('/', '-'))

    def install(self):
        """
Handle install
        """
        targetBucket = self.CONNECTION.Bucket(self.sourcePath()['Bucket'])

        prefix = self.sourcePath()['Tool Path'].strip('/')

        for obj in targetBucket.objects.filter(Prefix=prefix):
            print obj.key

# source fields
AWSHandler.addSourceField('Bucket')
AWSHandler.addSourceField('Tool Path')

# register handler
AWSHandler.registerHandler('AWS')