"""
predefined ui elements for Dashboard development
"""
from element import Element


class Row(Element):

    # predefined column sizes
    SMALL = 'sm'
    MEDIUM = 'md'
    LARGE = 'lg'
    XLARGE = 'xl'

    def __init__(self):
        super(Row, self).__init__('div', Class="row")

    def addColumn(self, width, size='sm'):
        """
        :param size: Row.SIZES (Row.SMALL, Row.MEDIUM, Row.LARGE, Row.XLARGE)
        :param width: int. Keep in mind, this is a Bootstrap row and all rows can add up to no more than 12.
        """
        self._values.append(Element('div', Class='col-%s-%s' % (size, width)))

    def addToColumn(self, value, column):
        """
        Add a value/element to a column owned by the row.
        :param value: str or element
        :param column: index of the column to add the value to
        """
        self._values[column].addValue(value)


class Panel(Element):
    """
    Panels have a header, body, and footer.
    """

    def __init__(self, type='panel-default'):
        super(Panel, self).__init__('div', Class='panel ' + type)

        self.addValue(Element('div', Class='panel-heading'))
        self.addValue(Element('div', Class='panel-body'))
        self.addValue(Element('div', Class='panel-footer'))

    def addToHeader(self, value):
        self._values[0].addValue(value)
        return value

    def addTobody(self, value):
        self._values[1].addValue(value)
        return value

    def addToFooter(self, value):
        self._values[2].addValue(value)
        return value

    def html(self, indent=''):
        for item in self._values:
            if not item._values:
                self._values.remove(item)

        return super(Panel, self).html(indent=indent)


class List(Element):

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


class Link(Element):
    def __init__(self, value, link):
        super(Link, self).__init__('a', href=link)
        self.addValue(value)


class Font(Element):
    def __init__(self, text, **kwargs):
        super(Font, self).__init__('font', **kwargs)
        self.addValue(text)


class Page(object):

    TEMPLATE = ("{% extends \"layout.html\" %}\n"
                "{% block title %}%(self._title)s{% endblock %}\n"
                "{% block body %}\n"
                "%(render)s\n"
                "{% endblock %}\n")

    def __init__(self, title):
        self._title = title
        self._root = Element('body')

    def add(self, element):
        """
        Add an element to this page.
        :param element: str or Element
        """
        self._root.addValue(element)

    def render(self):
        render = self._root.html()
        return self.TEMPLATE.replace('%(self._title)s', self._title).replace('%(render)s', render)