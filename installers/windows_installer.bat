if exist C:\Python27\python.exe (set python=C:\Python27\python.exe) else (echo "Python27 is required for install. Download: https://www.python.org/downloads/release/python-2712/")

%python% %~dp0installer.py

PAUSE