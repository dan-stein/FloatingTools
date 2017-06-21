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
        appList = Table(headers=['App', 'File Types', 'Features', 'Setting'])

        # load time dict
        loadTimes = {}

        # loop over apps
        for app in FloatingTools.APP_WRAPPERS:

            # pull load time
            loadTimes[app.name()] = 0.0
            for toolBox in FloatingTools.sourceData():
                if app.name() in toolBox['loadTimes']:
                    loadTimes[app.name()] = loadTimes[app.name()] + eval(toolBox['loadTimes'][app.name()])

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

            # features and settings
            featureList = Div()
            featureList.addValue('Multi-Threaded Load Up')
            featureList.addBreak()
            featureList.addValue('Python arguments')

            settingList = Div()
            settingList.addValue('True' if app.MULTI_THREAD else 'False')
            settingList.addBreak()
            settingList.addValue(app.ARGS)

            appList.addRow(info, types, featureList, settingList)

        # add to page
        self.add(Center(appList))
        self.add(FloatingTools.Dashboard.BarGraph('FloatingTools Application Load', loadTimes, 100, 500))


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
