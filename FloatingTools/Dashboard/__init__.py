"""
Dashboard handles the web interface
"""
# website environment
SITE_ENV = {}

# dashboard imports
from utilities import startServer, setDashboardVariable, dashboardEnv, SERVER, ErrorPage, HOST, PORT
from ui import *
from network import *
from settings import settings
from applications import applications
from toolshed import toolShed
from services import services
import news
