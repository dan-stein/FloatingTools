"""
Dashboard handles the web interface
"""
# dashboard imports
from utilities import startServer, setDashboardVariable, dashboardEnv
from settings import settings
from login import login
from applications import applications
from toolshed import toolShed
from toolbox import toolbox

# website environment
SITE_ENV = {}
