from setuptools import find_packages, setup

setup(
    name='FloatingTools',
    version='v0.1',
    packages=find_packages(),
    package_data={
        '': ['*.html']
    },
    install_requires=['Flask', 'PyGithub'],
    url='https://github.com/aldmbmtl/FloatingTools',
    license='MIT',
    author='Alex Hatfield',
    author_email='alex.e.hatfield@gmail.com',
)
