# FloatingTools imports
import FloatingTools

# flask imports
from flask import request, redirect, render_template_string

# package imports
from ui import *
from utilities import SERVER


class SettingsPage(Page):
    def __init__(self):
        super(SettingsPage, self).__init__('Settings')

        data = {
            'build': FloatingTools.buildData,
            'sources': FloatingTools.sourceData
        }

        # update dashboards env with the latest data.
        for entry in data:
            FloatingTools.Dashboard.setDashboardVariable(entry, data[entry]())

        FloatingTools.branches()
        FloatingTools.releases()

        # build UI
        header = Header(size=4, value=Element('label', 'Current Install'))
        header.addValue(': ' + FloatingTools.Dashboard.dashboardEnv()['current_release'])

        self.add(header)
        self.add(Link(
            value='Release Information',
            link="https://github.com/aldmbmtl/FloatingTools/releases/tag/" + FloatingTools.Dashboard.dashboardEnv()['current_release']
        ))
        self.add(Br())
        self.add(Br())
        self.add(Element('label', 'Install Location'))
        self.add(Br())
        self.add(FloatingTools.Dashboard.dashboardEnv()['python_location'])
        self.add(Hr())

        # build form information
        form = Form(action='/settings/_save')

        # release section
        releaseSection = Element('label', 'Change Release: (requires relaunch)')
        selector = Select('release')
        selector.addOption('latest', text='Latest').addFlag('selected')

        for release in FloatingTools.Dashboard.dashboardEnv()['releases']:
            option = selector.addOption(release, text=release)
            if release == FloatingTools.buildData()['release']:
                option.addFlag('selected')

        releaseSection.addValue(selector)

        row = Row()
        row.addColumn(11)
        row.addToColumn(releaseSection, 0)
        row.addToColumn(Br(), 0)
        row.addToColumn(
            Element(
                'span',
                value='"Freeze" your install to a specific version or set it to "Latest" to auto-download latest release.'
            ),
            0
        )
        row.addColumn(1)
        row.addToColumn(Element('input', attributes={'value': 'Save', 'type': 'submit'}, Class='form-control'), 1)

        form.addValue(row)
        form.addValue(Br())
        form.addValue(Br())

        # dev tools section
        devPanel = Panel()
        form.addValue(devPanel)

        devPanel.addToHeader(Header(value='Development Tools', size=5))
        label = devPanel.addTobody(Element('label', 'Branch: '))

        branchSelect = Select(name='dev-branch')
        branchSelect.addOption('disable', text='Disable').addFlag('selected')

        for branch in FloatingTools.Dashboard.dashboardEnv()['branches']:
            opt = branchSelect.addOption(branch, text=branch)
            if branch == FloatingTools.buildData()['devBranch']:
                opt.addFlag('selected')


        label.addValue(branchSelect)
        devPanel.addTobody(Br())
        devPanel.addTobody(
            Element(
                'span',
                value='Selecting a branch from the FloatingTools repository will pull the build from the development '
                      'branch you select. <strong>This will disable the Release System and overwrite the local '
                      'FloatingTools build.</strong> You can disable this and it will revert to the release system.',
                Class="help-block"
            )
        )
        devPanel.addTobody(Hr())
        label = devPanel.addTobody(Element('label', 'Collaborator: '))

        branchSelect = Select(name='collaborator')
        off = branchSelect.addOption('false', text='Disable')
        on = branchSelect.addOption('true', text='Enable')

        off.addFlag('selected')
        if FloatingTools.buildData()['collaborator']:
            on.addFlag('selected')

        label.addValue(branchSelect)
        devPanel.addTobody(Br())

        devPanel.addTobody(
            Element(
                'span',
                value='This allows you to modify your local FloatingTools install.<strong>This overrides the Branch and'
                      ' Release Systems.</strong>',
                Class="help-block"
            )
        )

        self.add(form)

@SERVER.route('/settings', methods=['GET', 'POST'])
def renderSettings():
    """
    Render settings page to configure Floating Tools
    :return: 
    """
    return render_template_string(SettingsPage().render(), **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/settings/_save')
def saveSettings():
    """
    Handles setting saving.
    :return: 
    """

    buildData = FloatingTools.buildData()
    buildData['release'] = request.args.get('release')
    buildData['collaborator'] = False
    if request.args.get('collaborator') == "true":
        buildData['collaborator'] = True
    branch = request.args.get('dev-branch')

    buildData['dev'] = True
    if branch == 'disable':
        buildData['dev'] = False
    buildData['devBranch'] = branch

    FloatingTools.updateBuild(buildData)

    return redirect('/settings')

def settings():
    """
    Launch settings page to configure Floating Tools
    """
    FloatingTools.Dashboard.startServer(url='settings')
