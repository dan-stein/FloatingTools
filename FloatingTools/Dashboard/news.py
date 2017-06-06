import FloatingTools

# flask imports
from flask import render_template

# package imports
from utilities import SERVER


@SERVER.route('/home', methods=['GET', 'POST'])
def renderHome():
    """
    Render home page
    :return: 
    """
    return render_template('Home.html', **FloatingTools.Dashboard.dashboardEnv())
