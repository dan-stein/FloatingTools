# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, render_template, redirect

# package imports
from utilities import SERVER


@SERVER.route('/settings', methods=['GET', 'POST'])
def renderSettings():
    """
    Render settings page to configure Floating Tools
    :return: 
    """
    data = {
        'build': FloatingTools.buildData,
        'sources': FloatingTools.sourceData
    }

    # update dashboards env with the latest data.
    for entry in data:
        FloatingTools.Dashboard.setDashboardVariable(entry, data[entry]())

    FloatingTools.branches()
    FloatingTools.releases()

    return render_template('Settings.html', **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/_save')
def saveSettings():
    """
    Handles setting saving.
    :return: 
    """

    print request.form

    return redirect('/settings')

def settings():
    """
    Launch settings page to configure Floating Tools
    :return: 
    """
    FloatingTools.Dashboard.startServer(url='settings')
