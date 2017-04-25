from distutils.core import setup

setup(
    name='FloatingTools',
    version='0.1',
    packages=['jwt', 'jwt.contrib', 'jwt.contrib.algorithms', 'click', 'flask', 'flask.ext', 'github', 'github.tests',
              'jinja2', 'werkzeug', 'werkzeug.debug', 'werkzeug.contrib', 'markupsafe'],
    package_dir={'': 'FloatingTools/packages'},
    url='https://github.com/aldmbmtl/FloatingTools',
    license='MIT',
    author='Alex Hatfield',
    author_email='alex.e.hatfield@gmail.com',
)
