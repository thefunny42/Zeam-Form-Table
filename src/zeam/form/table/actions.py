
from zeam.form.base import Actions

from zeam.form.table import interfaces


class TableActions(Actions):
    """Actions that can be applied on a table.
    """

    def process(self, form, request):
        assert interfaces.ITableFormCanvas.providedBy(form)
        executed = False

        for action in self:
            extractor = component.getMultiAdapter(
                (action, form, request), interfaces.IWidgetExtractor)
            value, error = extractor.extract()
            if value is not NO_VALUE:
                for line in form.lines:
                    try:
                        if action.validate(line):
                            executed = True
                            action(line)
                    except interfaces.ActionError, e:
                        line.errors.append(Error(e.args[0], line.prefix))
            if executed:
                return True
        return False
