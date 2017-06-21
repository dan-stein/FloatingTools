"""
predefined ui elements for Dashboard development
"""
import FloatingTools
from element import Element


class Img(Element):
    """
Python equivalent to ul/ol lists in html.
    """

    def __init__(self, src, **kwargs):
        super(Img, self).__init__('img', src=src, **kwargs)


class Br(Element):
    def __init__(self):
        super(Br, self).__init__('br')


class Hr(Element):
    def __init__(self):
        super(Hr, self).__init__('hr')


class List(Element):
    """
Python equivalent to ul/ol lists in html.
    """

    def __init__(self, numbered=False, bootstrap=True):
        super(List, self).__init__('ol' if numbered else 'ul')

        if bootstrap:
            self._attributes['Class'] = "list-group"


    def addItem(self, value=None):
        """
Create an item and add it to the list

:param value: the value for the item

:return: The created element item
        """
        item = Element('li', Class="list-group-item")
        if value:
            item.addValue(value)
        self.addValue(item)
        return item


class Table(Element):
    def __init__(self, headers, bootstrap=True):
        super(Table, self).__init__('table')

        if bootstrap:
            self._attributes['Class'] = "list-group"

        # build headers
        tr = Element('tr')
        self.addValue(tr)
        for header in headers:
            tr.addValue(Element('th', Element('center', header)))

    def addRow(self, *values):
        """
Add values to define a row.

:type values: str or Element
        """
        row = Element('tr')
        self.addValue(row)
        for value in values:
            row.addValue(Element('td', value))
        return row


class Link(Element):
    """
Python equivalent to 'a' in html.
    """
    def __init__(self, value, link):
        super(Link, self).__init__('a', href=link)
        self.addValue(value)


class Center(Element):
    def __init__(self, element=None, **kwargs):
        super(Center, self).__init__('center', value=element, **kwargs)


class Header(Element):
    def __init__(self, value, size, **kwargs):
        super(Header, self).__init__('h' + str(size), value=value, **kwargs)


class Font(Element):
    """
Python equivalent to font in html.
    """
    def __init__(self, text, **kwargs):
        super(Font, self).__init__('font', **kwargs)
        self.addValue(text)


class Script(Element):
    def __init__(self, code):
        super(Script, self).__init__('script', value=code)


class Div(Element):
    """
Python equivalent to div in html.
    """
    def __init__(self, value=None, **kwargs):
        super(Div, self).__init__('div', **kwargs)
        if value:
            self.addValue(value)


class Select(Element):
    """
Python equivalent to select in html.
    """
    def __init__(self, name, **kwargs):
        super(Select, self).__init__('select', name=name, Class="form-control", **kwargs)
        
    def addOption(self, value, text=None):
        """
        Add an option to the selection box

        :param value: str
        :return: Option element 
        """
        option = Element('option', attributes={'value': value})
        if text:
            option.addValue(text)
        return self.addValue(option)


class Form(Element):
    """
Python equivalent to form in html.
    """
    def __init__(self, action, **kwargs):
        super(Form, self).__init__('form', action=action, **kwargs)

    @staticmethod
    def password(name):
        return Element('input', Type='password', name=name, attributes={'value': name}, Class='form-control')

    @staticmethod
    def checkbox(name, label):
        return Element('input', value=label, Type='checkbox', name=name, attributes={'value': name})

    @staticmethod
    def email(name):
        return Element('input', Type='email', name=name, attributes={'value': name}, Class='form-control')

    @staticmethod
    def submit(name):
        return Element('input', Type='submit', attributes={'value': name}, Class='btn btn-primary')

    @staticmethod
    def text(name):
        return Element('input', Type='text', name=name, attributes={'value': name}, Class='form-control')


class Collapse(Div):
    """
Python equivalent to collapse in html.
    """
    def __init__(self, id, shown=False, **kwargs):
        """
        :param id: id for this collapse so it can be referenced later.
        """
        super(Collapse, self).__init__(attributes={'id': id}, Class="collapse in" if shown else "collapse", **kwargs)

        # instance variables
        self._id = id

    def linkTo(self, id=None):
        """
        Will return a dict ready to be used in the attributes of any element that will refer to any collapse object via
        the assigned id.

        :param id: id of the collapse element
        """
        return {
            'data-toggle': "collapse",
            'data-target': "#" + id
        } if id else {
            'data-toggle': "collapse",
            'data-target': "#" + self._id
        }


class Row(Div):

    # predefined column sizes
    SMALL = 'sm'
    MEDIUM = 'md'
    LARGE = 'lg'
    XLARGE = 'xl'

    def __init__(self):
        super(Row, self).__init__(Class="row")

    def addColumn(self, width, size='sm'):
        """
        :param size: Row.SIZES (Row.SMALL, Row.MEDIUM, Row.LARGE, Row.XLARGE)
        :param width: int. Keep in mind, this is a Bootstrap row and all rows can add up to no more than 12.
        """
        self._values.append(Div(Class='col-%s-%s' % (size, width)))

    def addToColumn(self, value, column):
        """
Add a value/element to a column owned by the row.

:param value: str or element
:param column: index of the column to add the value to
        """
        self._values[column].addValue(value)


class Panel(Div):
    """
Panels have a header, body, and footer. Python equivalent to bootstrap panels.
    """
    COLLAPSE_ID_SEED = 0

    # TYPES
    DEFAULT = 'panel-default'
    PRIMARY = 'panel-primary'
    SUCCESS = 'panel-success'
    INFO = 'panel-info'
    WARNING = 'panel-warning'
    DANGER = 'panel-danger'

    def __init__(self, type=DEFAULT, collapsible=False, collapseShown=False):
        """
        :param type: the panel class you want to use. https://www.w3schools.com/bootstrap/bootstrap_panels.asp
        :param collapsible: bool if you want to panel to be collapsible
        :param collapseShown: bool if you want the panel open by default or not
        """
        super(Panel, self).__init__(Class='panel ' + type)

        # instance vars
        self._collapseID = None
        self._header = Div(Class='panel-heading')
        self._body = Div(Class='panel-body')
        self._footer = Div(Class='panel-footer')

        self.addValue(self._header)

        if collapsible:
            col = Collapse('panel-collapse-' + str(self.COLLAPSE_ID_SEED), shown=True if collapseShown else False)
            self.COLLAPSE_ID_SEED += 1

            col.addValue(self._body)
            col.addValue(self._footer)

            self.addValue(col)

            self._collapseID = col.linkTo()
        else:
            self.addValue(self._body)
            self.addValue(self._footer)

    def collapseLink(self):
        """
Get the link to the collapse
        """
        return self._collapseID

    def addToHeader(self, value):
        """
        Add an element to the header portion of the panel

        :param value: Element or str
        :return: value
        """
        self._header.addValue(value)
        return value

    def addTobody(self, value):
        """
        Add an element to the body portion of the panel

        :param value: Element or str
        :return: value
        """
        self._body.addValue(value)
        return value

    def addToFooter(self, value):
        """
        Add an element to the footer portion of the panel

        :param value: Element or str
        :return: value
        """
        self._footer.addValue(value)
        return value

    def html(self, indent=''):
        for item in self._values:
            if not item._values:
                self._values.remove(item)

        return super(Panel, self).html(indent=indent)


class PanelGroup(Div):
    def __init__(self, **kwargs):
        super(PanelGroup, self).__init__('div', Class='panel-group', **kwargs)


class Page(object):
    """
Pages are where you build your content. Add your root element(s) to the page and they will be automatically rendered for
you.
    """


    TEMPLATE = ("{% extends \"layout.html\" %}\n"
                "{% block title %}%(title)s{% endblock %}\n"
                "{% block body %}\n"
                "%(render)s\n"
                "{% endblock %}\n"
                "{% block help_video %}\n"
                "%(help_video)s\n"
                "{% endblock %}\n"
                "{% block app_sidebar %}\n"
                "%(app_sidebar)s\n"
                "{% endblock %}\n")

    def __init__(self, title):
        self._title = title
        self._root = Element('body')
        self._sideBar = Element('body')
        self._helpCenter = Element('body')

    def add(self, element):
        """
Add an element to this page.

:param element: str or Element
        """
        self._root.addValue(element)

    def addToSideBar(self, element):
        """
Add an element as a side bar

:param element:
        """
        self._sideBar.addValue(element)

    def addToHelp(self, element):
        """
Add an element to the help center

:param element:
        """
        self._helpCenter.addValue(element)

    def addDivider(self):
        """
Add a divider on the page
        """
        self.add(Hr())

    def addBreak(self):
        """
Add a break on the page
        """
        self.add(Br())

    def render(self):

        render = self._root.html()
        app_sidebar = self._sideBar.html()
        help_video = self._helpCenter.html()
        title = self._title

        renderSTR = self.TEMPLATE
        substitution = locals()
        for var in substitution:
            try:
                renderSTR = renderSTR.replace('%(' + var + ')s', substitution[var])
            except TypeError:
                pass

        return renderSTR


class Style(Element):
    def __init__(self, code):
        super(Style, self).__init__('style', value=code)