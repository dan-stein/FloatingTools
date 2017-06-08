"""
Plug in for FloatingTools that allows for dynamic redefinition of running python code without needing relaunch
"""
# FT
from FloatingTools import Dashboard
from App import App

# python imports
import gc
import inspect
import traceback


class Blur(App):
    # class vars
    redefined = {}

    def __init__(self):
        super(Blur, self).__init__('Blur')

        # instance variables
        self._instances = []

    def buildUI(self):
        # create layout
        row = Dashboard.Row()
        row.addColumn(3)
        row.addColumn(9)

        # build panels
        pythonStructure = Dashboard.Panel()

        # headers
        pythonStructure.addToHeader(Dashboard.Element('center', value=Dashboard.Element('h4', value='Structure')))

        # add body sections
        pythonStructure.addTobody(self.structureUI())

        row.addToColumn(pythonStructure, 0)

        if self.arguments() and 'target' in self.arguments():
            codePanel = Dashboard.Panel()
            codePanel.addToHeader(Dashboard.Element('center', Dashboard.Element('h4', value='Code')))
            codePanel.addTobody(self.codeUI())

            row.addToColumn(codePanel, 1)

            self.page().add(row)
        else:
            self.page().add(pythonStructure)

    def codeUI(self):
        # build ui form
        codeForm = Dashboard.Element('form', action='/Blur/redefine')

        instance = getattr(__import__(self.arguments()['search']), self.arguments()['target'])

        self._instances = []

        for obj in gc.get_objects():
            try:
                if isinstance(obj, instance) or issubclass(obj, instance):
                    if not inspect.isclass(obj):
                        self._instances.append(obj)
            except (TypeError, ImportError):
                pass

        try:
            code = inspect.getsource(instance)
        except (TypeError, IOError):
            return ''

        replacementCode = Dashboard.Element('textarea', Class="form-control", rows=100,
                                            placeholder="Replacement code...", name="replace"
                                            )

        replacementCode.addValue('\n' + code + '\n')
        replacementCode.addFlag('required')
        codeForm.addValue(
            Dashboard.Element('input', attributes={'value': self.arguments()['search']}, Class="form-control",
                              name='search')
        )
        codeForm.addValue(
            Dashboard.Element('input', attributes={'value': self.arguments()['target']}, Class="form-control",
                              name='target')
        )
        codeForm.addValue(Dashboard.Element('hr'))
        codeForm.addValue(replacementCode)
        codeForm.addValue(Dashboard.Element('hr'))
        codeForm.addValue(Dashboard.Element('input', Class="form-control", type="submit"))

        self.registerFunction(self.redefine)

        return codeForm

    def structureUI(self):
        # build search form
        searchForm = Dashboard.Element('form', action='/Blur/search')
        searchBar = Dashboard.Element(
            'input', input='text', placeholder='module', Class='form-control', name='search', id='search'
        )
        label = Dashboard.Element('label', value='Search', attributes={'for': 'search'})

        # add all elements and connect
        searchForm.addValue(label)
        searchForm.addValue(searchBar)

        # load args
        if self.arguments() and 'search' in self.arguments():
            searchWord = self.arguments()['search']

            searchForm.addValue(Dashboard.Element('hr'))

            try:
                mod = __import__(searchWord)

                ul = Dashboard.List()

                for var in sorted(dir(mod)):
                    ul.addItem(Dashboard.Link(var, self.connectToFunction(self.search, search=searchWord, target=var)))

                searchForm.addValue(ul)

            except ImportError:
                searchForm.addValue(Dashboard.Element('label', value='Couldn\'t find module'))

        self.registerFunction(self.search)

        return searchForm

    def search(self):
        self.refresh()

    def redefine(self):

        self.redefined[self.arguments()['search']] = self.arguments()['replace']

        try:
            print 'Redefining %s...' % str(self.arguments()['search'])
            mod = __import__(self.arguments()['search']).__dict__
            exec self.arguments()['replace'] in mod
            print 'Redefining complete...'
        except:
            traceback.print_exc()

        self.redirect('/Blur')

Blur()