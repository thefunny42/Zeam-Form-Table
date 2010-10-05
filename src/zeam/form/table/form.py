
from zeam.form.base.fields import Fields
from zeam.form.base.form import FormCanvas
from zeam.form.base.form import StandaloneForm, cloneFormData
from zeam.form.base.widgets import Widgets, getWidgetExtractor
from zeam.form.composed.form import SubFormBase

from zeam.form.table.select import SelectField
from zeam.form.table.actions import TableActions
from zeam.form.table import interfaces

from grokcore import component as grok
from megrok import pagetemplate as pt
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zeam.form.base')


pt.templatedir('default_templates')


class TableFormCanvas(FormCanvas):
    """A form which is able to edit more than one content as a table.
    """
    grok.baseclass()
    grok.implements(interfaces.ITableFormCanvas)

    tableFields = Fields()
    tableActions = TableActions()
    emptyDescription = _(u"There are no items.")

    def __init__(self, context, request):
        super(TableFormCanvas, self).__init__(context, request)
        self.lines = []
        self.lineWidgets = []

    def updateLines(self, mark_selected=False):
        self.lines = []
        self.lineWidgets = []

        for position, item in enumerate(self.getItems()):
            prefix = '%s.line-%d' % (self.prefix, position)
            form = cloneFormData(self, content=item, prefix=prefix)
            form.selected = False

            # Checkbox to select the line
            selectedField = SelectField(identifier=position)

            if mark_selected:
                # Mark selected lines
                selectedExtractor = getWidgetExtractor(
                    selectedField, form, self.request)
                if selectedExtractor is not None:
                    value, error = selectedExtractor.extract()
                    if value:
                        form.selected = True

            lineWidget = Widgets(form=form, request=self.request)
            lineWidget.extend(selectedField)
            self.lines.append(form)
            self.lineWidgets.append(lineWidget)

    def updateActions(self):
        action, status = self.tableActions.process(self, self.request)
        if action is None:
            action, status = self.actions.process(self, self.request)
        return action, status

    def updateWidgets(self):
        self.updateLines()
        for widgets in self.lineWidgets:
            widgets.extend(self.tableFields)
        self.fieldWidgets.extend(self.fields)
        self.actionWidgets.extend(self.actions)
        self.actionWidgets.extend(self.tableActions)

        for widgets in self.lineWidgets:
            widgets.update()
        self.fieldWidgets.update()
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
