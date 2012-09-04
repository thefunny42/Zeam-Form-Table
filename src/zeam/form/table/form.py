
from zeam.form.base.fields import Fields
from zeam.form.base.form import FormCanvas
from zeam.form.base.form import StandaloneForm, cloneFormData
from zeam.form.base.widgets import Widgets
from zeam.form.composed.form import SubFormBase

from zeam.form.table.select import SelectField
from zeam.form.table.actions import TableActions
from zeam.form.table import interfaces
from zeam.utils.batch import Batch, IBatching

from zope.component import queryMultiAdapter
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

    batchSize = 0
    batchFactory = Batch
    batchItemFactory = lambda f, x: x
    tableFields = Fields()
    tableActions = TableActions()
    emptyDescription = _(u"There are no items.")

    def __init__(self, context, request):
        super(TableFormCanvas, self).__init__(context, request)
        self.lines = []
        self.lineWidgets = []
        self.batching = None

    def createSelectedField(self, item):
        """Return a field to select the line.
        """
        return SelectField(identifier='select')

    def updateLines(self, mark_selected=False):
        self.lines = []
        self.lineWidgets = []
        self.batching = None
        items = self.getItems()
        if self.batchSize:
            items = self.batchFactory(
                items,
                name=self.prefix,
                factory=self.batchItemFactory,
                count=self.batchSize,
                request=self.request)
            self.batching = queryMultiAdapter(
                (self.getFormForTable(), items, self.request), IBatching)()
        for position, item in enumerate(items):
            prefix = '%s.line-%s' % (self.prefix,
                self.getItemIdentifier(item, position))
            form = cloneFormData(self, content=item, prefix=prefix)
            form.selected = False

            # Checkbox to select the line
            form.selectedField = self.createSelectedField(item)

            if mark_selected:
                # Mark selected lines
                selectedExtractor = form.widgetFactory.extractor(
                    form.selectedField)
                if selectedExtractor is not None:
                    value, error = selectedExtractor.extract()
                    if value:
                        form.selected = True

            lineWidget = Widgets(form=form, request=self.request)
            lineWidget.extend(form.selectedField)
            self.lines.append(form)
            self.lineWidgets.append(lineWidget)

    def updateActions(self):
        form, action, status = self.tableActions.process(self, self.request)
        if action is None:
            form, action, status = self.actions.process(self, self.request)
        return form, action, status

    def updateWidgets(self):
        self.updateLines()
        for widgets in self.lineWidgets:
            widgets.extend(self.tableFields)
        self.fieldWidgets.extend(self.fields)
        self.actionWidgets.extend(self.tableActions)
        self.actionWidgets.extend(self.actions)

        for widgets in self.lineWidgets:
            widgets.update()
        self.fieldWidgets.update()
        self.actionWidgets.update()

    def getItems(self):
        return self.context.values()

    def getItemIdentifier(self, item, position):
        return str(position)


class TableForm(TableFormCanvas, StandaloneForm):
    """A full standalone TableForm.
    """
    grok.baseclass()
    grok.implements(interfaces.ITableForm)

    def getFormForTable(self):
        return self


class SubTableForm(SubFormBase, TableFormCanvas):
    """A table form which can be used in a composed form.
    """
    grok.baseclass()
    grok.implements(interfaces.ISubTableForm)

    def getFormForTable(self):
        return self.getComposedForm()

class SubTableFormTemplate(pt.PageTemplate):
    """A default template for a SubTableForm
    """
    pt.view(SubTableForm)
