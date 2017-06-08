"""
Base App class for FloatingTools Apps that interact with Dashboard by piggy backing on the networking provided by
FloatingTools.
"""
# FT imports
import FloatingTools

# flask imports
from flask import render_template_string, request, redirect


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

    # templates
    HOME_PAGE_TEMPLATE = '''
@FloatingTools.Dashboard.SERVER.route('/%(name)s')
def %(name)s_home():
    return render_template_string(FloatingTools.App.APPS['%(name)s'].page().render(), **FloatingTools.Dashboard.dashboardEnv())
    '''

    FUNCTION_PAGE_TEMPLATE = '''
@FloatingTools.Dashboard.SERVER.route('/%(name)s/%(function)s')
def %(name)s%(function)s():
    result = FloatingTools.App.APPS['%(name)s'].%(function)s()
    if not result:
        return render_template_string(FloatingTools.App.APPS['%(name)s'].page().render(), **FloatingTools.Dashboard.dashboardEnv())
    else:
        return render_template_string(result, **FloatingTools.Dashboard.dashboardEnv())
        '''

    def __init__(self, name):
        """
:param name: str for the name of your application
        """

        # instance variables
        self._page = FloatingTools.Dashboard.Page(name)
        self._name = name

        # build ui
        self.buildUI()

        # register the app
        added = FloatingTools.Dashboard.dashboardEnv()['app_plugins']
        added.append(self)
        FloatingTools.Dashboard.setDashboardVariable('app_plugins', added)

        # register page with the Dashboard server.
        exec self.HOME_PAGE_TEMPLATE % locals()

        # register app
        self.APPS[name] = self

    def refresh(self):
        """
Refreshing the page will remove the previous Page element and redraw the ui on a fresh page as to eliminate UI
repeating.
        """
        self._page = FloatingTools.Dashboard.Page(self.name())
        self.buildUI()

    def redirect(self, path):
        """
redirect to a different page

:param path:
        """
        return redirect(path)

    def passVariables(self, **kwargs):
        """
In order to pass variables to a function that gets called through a URL, you must use this function.

.. code-block:: python
    :linenos:

    import FloatingTools

    class MyApp(FloatingTools.App):
        def buildUI(self):
            FloatingTools.Link('print the "var" variable', '/url/printFunction' + self.passVariables(var='foo'))

        def printFunction(self):
            print self.arguments()['var']

:param **kwargs: dict
        """
        args = ['%s=%s' % (var, kwargs[var]) for var in kwargs]
        if not args:
            return ''

        return '?' + '&'.join(args)

    def arguments(self):
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
        return '/%s/%s%s' % (self.name(), function.__name__, self.passVariables(**kwargs))

    def connectToElement(self, element, function, flag='onclick', **kwargs):
        """
Connect an element through a passed flag to a callable.

:param element: FloatingTools.Dashboard.Element
:param function: callable
:param flag: str this should be a type of signal like 'onclick'
        """
        if not isinstance(element, FloatingTools.Dashboard.Element):
            raise TypeError('Must be an instance of FloatingTools.Dashboard.Element!')

        element.setAttributes({flag: "location.href='%s/%s%s'" % (
            self._name, function.__name__, self.passVariables(**kwargs))}
                              )

        self.registerFunction(function)

        return element

