# flask imports
from flask import render_template_string, redirect, request

# package imports
from ui import *
from utilities import SERVER


class Services(Page):
    def __init__(self):
        super(Services, self).__init__('Services')

        # build ui
        serviceTable = Table(['Service', 'Credentials'])

        for service in FloatingTools.services():
            service = FloatingTools.getHandler(service)

            if not service.LOGIN_FIELDS:
                continue

            serviceInfo = Div()
            if service.ICON:
                serviceInfo.addValue(Center(Img(service.ICON, width=100)))
                serviceInfo.addDivider()
            serviceInfo.addValue(Center(service.handlerName()))

            if service.WEBPAGE:
                serviceInfo.addValue(Center(Link('Home Page', service.WEBPAGE)))

            serviceFields = Div()
            if service.LOGIN_FIELDS:
                for field in service.LOGIN_FIELDS:

                    attrs = field._attributes.copy()

                    attrs['name'] = service.handlerName() + '-' + field._attributes['name']
                    if service.userData():
                        if field.name() in service.userData():
                            attrs['value'] = service.userData()[field.name()]

                    attrs['size'] = 50

                    field.setAttributes(attrs)

                    serviceFields.addValue(field)
                    serviceFields.addBreak()
            else:
                serviceFields.addValue(Center(Header('None required', 3)))

            serviceTable.addRow(serviceInfo, serviceFields)

        form = Form(action='/_saveServices')
        form.addValue(Center(serviceTable))
        form.addValue(Center(Form.submit('Save')))

        self.add(form)


@SERVER.route('/services')
def renderServices():
    """
    Render services page
    :return:
    """
    return render_template_string(Services().render(), **FloatingTools.Dashboard.dashboardEnv())


@SERVER.route('/_saveServices')
def _saveServices():
    """
    Save services
    :return:
    """
    data = FloatingTools.userData()

    for arg in request.args:
        service, key = arg.split('-', 1)
        if service not in data:
            data[service] = {}
        data[service][key] = request.args[arg]

    FloatingTools.updateUserData(data)

    return redirect('/services')


def services():
    """
    Launch services page
    """
    FloatingTools.Dashboard.startServer(url='services')