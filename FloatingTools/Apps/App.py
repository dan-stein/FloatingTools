"""
Base App class for FloatingTools Apps that interact with Dashboard by piggy backing on the networking provided by
FloatingTools.
"""
# FT imports
import FloatingTools

# flask imports
from flask import render_template_string, request, redirect, url_for

# python imports
from random import randint


FloatingTools.Dashboard.setDashboardVariable('app_plugins', [])

class App(object):
    """
Apps are written to interact directly with FloatingTools through the Dashboard web interface.

You must register your app by instantiating an instance of it. This instance is the object Dashboard will handle. The
name of your app will be shown in the app list in Dashboard.

.. code-block:: python
    :linenos:

    import FloatingTools

    class MyApp(FloatingTools.App):
        pass

    MyApp('MyApp')

UIs must be built in the App.BuildUI function via redefine. Doing this in the __init__ will not work unless the UI is
static.

.. code-block:: python
    :linenos:

    import FloatingTools

    class MyApp(FloatingTools.App):
        def buildUI(self):
            ui code here...

    """

    # class variables
    APPS = {}
    ICON = None

    # templates
    HOME_PAGE_TEMPLATE = '''
@FloatingTools.Dashboard.SERVER.route('/%(name)s')
def %(name)s_home():
    FloatingTools.App.APPS['%(name)s'].refresh()
    return render_template_string(FloatingTools.App.APPS['%(name)s'].page().render(), **FloatingTools.Dashboard.dashboardEnv())
    '''

    FUNCTION_PAGE_TEMPLATE = '''
@FloatingTools.Dashboard.SERVER.route('/%(name)s/%(function)s')
def %(name)s%(function)s():
    result = FloatingTools.App.APPS['%(name)s'].%(function)s()
    if not result:
        return redirect(request.args['sourcePage'])
    else:
        try:
            return render_template_string(result, **FloatingTools.Dashboard.dashboardEnv())
        except TypeError:
            return result
        '''

    @staticmethod
    def redirect(path, **kwargs):
        """
redirect to a different page

:param path:
:param kwargs: You can pass kwargs to the next page if you'd like.
        """

        if kwargs:
            # grab the flask url map so we can pull the function
            urlMap = FloatingTools.Dashboard.SERVER.url_map.bind(FloatingTools.Dashboard.SERVER.name)

            return redirect(url_for(urlMap.match(path)[0], **kwargs))
        return redirect(path)

    @staticmethod
    def passVariables(**kwargs):
        """
.. warning::
    NOT RECOMMENDED FOR DIRECT USE! Only use this if you know exactly what you are doing with it.

In order to pass variables to a function that gets called through a URL, you must use this function.

:param **kwargs: dict

.. note::
    Requires unpack.

.. code-block:: python
    :linenos:

    strings, elements = self.passVariables(var='foo')

:returns: strings = dict(variableName: variableValue)
:returns: elements = dict(variableName: id of element to grab value from)
        """
        if not kwargs:
            return ''

        elements = {}
        strings = {}

        for var in kwargs:
            val = kwargs[var]
            if isinstance(val, FloatingTools.Dashboard.Element):
                if 'id' not in val._attributes:
                    val._attributes['id'] = randint(0, 99999)
                elements[var] = val._attributes['id']
                continue
            strings[var] = str(kwargs[var])

        return strings, elements

    @staticmethod
    def arguments():
        """
Arguments passed from the website
        """
        try:
            value = {}

            for dic in [request.args, request.form]:
                for val in dic:
                    value[val] = dic[val]

            return value
        except RuntimeError:
            return {}

    def __init__(self, name=None):
        """
:param name: str for the name of your application
        """
        if not name:
            name = self.__class__.__name__

        # instance variables
        self._page = FloatingTools.Dashboard.Page(name)
        self._name = name

        # register the app
        added = FloatingTools.Dashboard.dashboardEnv()['app_plugins']
        added.append(self)
        FloatingTools.Dashboard.setDashboardVariable('app_plugins', added)
        FloatingTools.Dashboard.setDashboardVariable('app_plugin_count', len(added))

        # register page with the Dashboard server.
        exec self.HOME_PAGE_TEMPLATE % locals()

        # register app
        self.APPS[name] = self

    def send(self, data, ip):
        """
Send data across the network to another computer running the same app. This will send the data directly to the receive()
function that you have defined for the App.

:param data: any kind of data that can be sent as a string and rebuilt
:param ip: the peers ip you want to send to
        """
        FloatingTools.Dashboard.send({'type': 'App', 'target': self.name(), 'data': data}, ip)

    def receive(self, data):
        """
Networking handler for receiving data should be set up here. Must sub-class if networking is desired.

:param data: object being sent
        """
        page = FloatingTools.Dashboard.Page('Networking')

        page.add(FloatingTools.Dashboard.Center(FloatingTools.Dashboard.Header('Networking', 3)))
        page.addDivider()
        page.add(FloatingTools.Dashboard.Center('Networking for %s is not set up yet. You need to subclass the receive '
                                                'function in your App. Check the documentation for further '
                                                'information.' % self.name()))
        return page.render()

    def refresh(self):
        """
Refreshing the page will remove the previous Page element and redraw the ui on a fresh page as to eliminate UI
repeating.
        """
        self._page = FloatingTools.Dashboard.Page(self.name())
        self.buildUI()

    def name(self):
        """
Get the name of the app
        """
        return self._name

    def page(self):
        """
Get the page object that represents the Dashboard.Page associated with the application.
        """
        return self._page

    def buildUI(self):
        """
Must subclass in order to build the web front end.
        """
        raise NotImplementedError()

    def registerFunction(self, function):
        """
Register a function as a url

:param function:
        """
        try:
            if hasattr(function, '__name__'):
                function = function.__func__

            exec self.FUNCTION_PAGE_TEMPLATE % {'name': self._name, 'function': function.__name__}
        except AssertionError:
            pass

    def connectToFunction(self, function, **kwargs):
        """
This will create a function with pre-baked arguments in the url. Very useful for passing variables.

.. code-block:: python
    :linenos:

    import FloatingTools

    class MyApp(FloatingTools.App):
        def buildUI(self):
            FloatingTools.Link('print the "var" variable', self.connectToFunction(self.printFunction, var='foo'))

        def printFunction(self):
            print self.arguments()['var']

:param function:
:param kwargs:
        """
        self.registerFunction(function)
        strings, elements = self.passVariables(**kwargs)
        return 'appPassArgs(%s, [%s], [%s]);' % (function.__name__, strings, elements)

    def connectToElement(self, element, function, flag='onclick', **kwargs):
        """
Connect an element through a passed flag to a callable.

:param element: FloatingTools.Dashboard.Element
:param function: callable
:param flag: str this should be a type of signal like 'onclick'
        """
        if not isinstance(element, FloatingTools.Dashboard.Element):
            raise TypeError('Must be an instance of FloatingTools.Dashboard.Element!')

        strings, elements = self.passVariables(**kwargs)

        element.setAttributes(
            {flag: "appPassArgs('%s', '%s', %s, %s);" % (self.name(), function.__name__, strings, elements)}
        )

        self.registerFunction(function)

        return element

