
from zope import component

from zeam.form.base.markers import NO_VALUE
from zeam.form.base.actions import Actions
from zeam.form.base.errors import Error
from zeam.form.base.interfaces import IWidgetExtractor, ActionError
from zeam.form.table import interfaces


class TableActions(Actions):
    """Actions that can be applied on a table.
    """

    def process(self, form, request):
        assert interfaces.ITableFormCanvas.providedBy(form)
        executed = False
        ready = False

        for action in self:
            extractor = component.getMultiAdapter(
                (action, form, request), IWidgetExtractor)
            value, error = extractor.extract()
            if value is not NO_VALUE:
                if not ready:
                    form.updateLines()
                    ready = True
                for line in form.lines:
                    if not line.selected:
                        continue
                    try:
                        if action.validate(line):
                            executed = True
                            content = line.getContentData().getContent()
                            action(form, content, line)
                    except ActionError, e:
                        line.errors.append(Error(e.args[0], line.prefix))
            if executed:
                return True
        return False
