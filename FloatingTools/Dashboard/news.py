import FloatingTools

# flask imports
from flask import render_template_string

# package imports
from ui import Element, Page
from utilities import SERVER

__all__ = []


@SERVER.route('/home', methods=['GET', 'POST'])
def renderHome():
    """
    Render home page
    :return: 
    """
    p = Page('Home')
    p.add(Element('iframe', src="http://www.hatfieldfx.com/hfx-news", width="100%", height=1000))
    return render_template_string(p.render(), **FloatingTools.Dashboard.dashboardEnv())
