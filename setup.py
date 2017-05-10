from setuptools import find_packages, setup

setup(
    name='FloatingTools',
    packages=find_packages(),
    package_data={
        '': ['templates/*.html']
    },
    install_requires=['Flask', 'PyGithub'],
    url='https://github.com/aldmbmtl/FloatingTools',
    license='MIT',
    author='Alex Hatfield',
    author_email='alex.e.hatfield@gmail.com',
)
