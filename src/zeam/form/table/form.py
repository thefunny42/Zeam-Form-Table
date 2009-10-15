
from zeam.form.base import Fields, Actions
from zeam.form.base.form import GrokViewSupport, StandaloneForm, FormSubmission

from zeam.form.table.actions import TableActions
from zeam.form.table import interfaces

from grokcore import component as grok


class TableFormCanvas(GrokViewSupport):
    """A form which is able to edit more than one content as a table.
    """
    grok.baseclass()
    grok.implements(interfaces.ITableFormCanvas)

    label = u''
    description = u''
    prefix = u'form'

    fields = Fields()
    actions = Actions()
    tableActions = TableActions()

    def __init__(self, context, request):
        super(TableFormCanvas, self).__init__(context, request)
        self.actionWidgets = Widgets(form=self, request=self.request)

        self.lines = []
        self.lineWidgets = []
        count = 1

        for item in self.getItems():
            submission = FormSubmission(item, request)

            submission.ignoreContent = self.ignoreContent
            submission.ignoreRequest = self.ignoreRequest
            submission.mode = self.mode
            submission.prefix = '%s.line-%d' % (self.prefix, count)

            self.lines.append(submission)
            self.lineWidgets.append(Widgets(form=submission, request=request))
            count +=1

    def updateActions(self):
        self.actions.process(self, self.request)
        self.tableActions.process(self, self.request)

    def updateWidgets(self):
        for widgets in self.lineWidgets:
            widgets.extend(self.fields)
        self.actionWidgets.extend(self.tableActions)
        self.actionWidgets.extend(self.actions)

        for widgets in self.lineWidgets:
            widgets.update()
        self.actionWidgets.update()

    def getItems(self):
        raise NotImplementedError


class TableForm(TableFormCanvas, StandaloneForm):
    """A full standalone TableForm.
    """
    grok.baseclass()

