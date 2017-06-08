# FloatingTools imports
import FloatingTools

# flask imports
from flask import render_template_string

# package imports
from ui import *
from utilities import SERVER


class ApplicationsPage(Page):
    """
    Applications page
    """
    def __init__(self):
        super(ApplicationsPage, self).__init__('Applications')

        # build ui
        appList = Table(headers=['App', 'File Types', 'Features'])

        # loop over apps
        for app in FloatingTools.APP_WRAPPERS:

            # app info
            info = Center()
            if app.APP_ICON:
                info.addValue(
                    Img(src=app.APP_ICON, width=50)
                )
            info.addValue(
                Link(value=' ' + app.name(), link="https://www.google.com/search?q=%s+application" % app.name())
            )

            # associated files
            types = Center()
            name = app.name()
            for type in sorted(app.fileTypes()):
                types.addValue(
                    Link(value=type, link="https://www.google.com/search?q=%(name)s+%(type)s+file" % locals())
                )

            # features
            featureList = Table(headers=[])
            featureList.addRow(Center('Multi-Threaded Load Up'), Center('True' if app.MULTI_THREAD else 'False'))
            featureList.addRow(Center('Python arguments'), Center(app.ARGS))

            appList.addRow(info, types, featureList)

        # add to page
        self.add(appList)


@SERVER.route('/applications', methods=['GET', 'POST'])
def renderApplications():
    """
    Render applications page
    :return: 
    """
    return render_template_string(ApplicationsPage().render(), **FloatingTools.Dashboard.dashboardEnv())


def applications():
    """
    Launch applications page
    """
    FloatingTools.Dashboard.startServer(url='applications')
