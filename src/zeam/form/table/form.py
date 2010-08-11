from megrok import pagetemplate as pt

from zeam.form.base import Fields, Actions, INPUT
from zeam.form.base.form import GrokViewSupport, StandaloneForm, cloneFormData
from zeam.form.base.widgets import Widgets
from zeam.form.composed.form import SubFormBase

from zeam.form.table.actions import TableActions
from zeam.form.table import interfaces

from grokcore import component as grok

pt.templatedir('default_templates')


class TableFormCanvas(GrokViewSupport):
    """A form which is able to edit more than one content as a table.
    """
    grok.baseclass()
    grok.implements(interfaces.ITableFormCanvas)

    label = u''
    description = u''
    prefix = u'form'

    mode = INPUT
    ignoreRequest = False
    ignoreContent = True

    fields = Fields()
    actions = Actions()
    tableActions = TableActions()

    def __init__(self, context, request):
        super(TableFormCanvas, self).__init__(context, request)
        self.actionWidgets = Widgets(form=self, request=self.request)
        self.lines = []
        self.lineWidgets = []

    def updateLines(self):
        self.lines = []
        self.lineWidgets = []

        for position, item in enumerate(self.getItems()):
            prefix = '%s.line-%d' % (self.prefix, position)
            form = cloneFormData(self, content=item, prefix=prefix)

            self.lines.append(form)
            self.lineWidgets.append(Widgets(form=form, request=self.request))

    def updateActions(self):
        self.actions.process(self, self.request)
        self.tableActions.process(self, self.request)

    def updateWidgets(self):
        self.updateLines()
        for widgets in self.lineWidgets:
            widgets.extend(self.fields)
        self.actionWidgets.extend(self.tableActions)
        self.actionWidgets.extend(self.actions)

        for widgets in self.lineWidgets:
            widgets.update()
        self.actionWidgets.update()

    def getItems(self):
        return self.context.values()


class TableForm(TableFormCanvas, StandaloneForm):
    """A full standalone TableForm.
    """
    grok.baseclass()
    grok.implements(interfaces.ITableForm)


class SubTableForm(SubFormBase, TableFormCanvas):
    """A table form which can be used in a composed form.
    """
    grok.baseclass()
    grok.implements(interfaces.ISubTableForm)


class SubTableFormTemplate(pt.PageTemplate):
    """A default template for a SubTableForm
    """
    pt.view(SubTableForm)
