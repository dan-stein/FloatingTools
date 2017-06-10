"""
Element module containing base class for all html objects for python use.
"""


class Element(object):
    """
Base element for all python->html elements. Each Element has a tag, attributes that can be set, and value.

<"tag" "attributes">"value"</"tag">
    """

    def __init__(self, tag, value=None, attributes=None, **kwargs):
        """
        :param tag: str
        :param kwargs: key words are the attributes. Class is an exception that is looked for and then lowered for html
                        syntax since "class" is a python keyword.
        """

        # set tag variable
        self._tag = tag
        self._values = []
        if value:
            self._values.append(value)
        self._flags = []
        self._html = ''
        self._attributes = {}

        # set attributes
        for key in kwargs:
            if key == 'Class':
                self._attributes['class'] = kwargs[key]
                continue
            self._attributes[key] = kwargs[key]
        if attributes:
            self.setAttributes(attributes)

    def setAttributes(self, attributes):
        """
        Set attributes for this element.

        :param attributes: dict
        """
        for key in attributes:
            if key == 'Class':
                self._attributes['class'] = attributes[key]
                continue
            self._attributes[key] = attributes[key]

    def addFlag(self, flag):
        """
        Add a flag to this element. This could be like setting an option to selected.

        :param flag: str
        """
        self._flags.append(flag)

    def addValue(self, value):
        """
        This will be rendered in the value section between the 2 tags.

        :param value: str or Element
        """
        if isinstance(value, list):
            for val in value:
                self._values.append(val)
        else:
            self._values.append(value)
        return value

    def addBreak(self):
        """
        Adds a line break to the element.
        """
        self.addValue(Element('br'))

    def addDivider(self):
        """
        Adds a divider to the element.
        """
        self.addValue(Element('hr'))

    def html(self, indent=''):
        """
        Get the rendered html code for this element.
        """
        # define defaults
        head = self._tag
        tail = head
        attributes = ''
        values = ''
        flags = ''

        # pull value count
        valueCount = len(self._values)

        # if there are no values passed, render a single line with only 1 tag and no closer
        template = "\n%(indent)s<%(head)s%(attributes)s%(flags)s>"

        # if more than 1 value has been, make it a multi line html render.
        if valueCount > 0 or head in ['div', 'iframe']:
            template = "\n%(indent)s<%(head)s%(attributes)s%(flags)s>\n%(indent)s%(values)s\n%(indent)s</%(tail)s>"

        # build attributes
        for attribute in self._attributes:
            attributes += ' %s="%s"' % (attribute, self._attributes[attribute])

        # build flags
        for flag in self._flags:
            flags += ' ' + flag

        # build values
        for value in self._values:
            if isinstance(value, Element):
                value = value.html(indent + '\t')

            # convert to string
            value = str(value)

            # format render
            if len(self._values) > 1:
                values += value
            else:
                values += value

        # clean left over new line
        # values = values.strip('\n')

        return template % locals()
