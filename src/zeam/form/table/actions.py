
from zeam.form.base.markers import NO_VALUE, SUCCESS, FAILURE, NOTHING_DONE
from zeam.form.base.actions import Actions
from zeam.form.base.errors import Error
from zeam.form.base.interfaces import IWidgetExtractor, ActionError
from zeam.form.table import interfaces

from zope import component
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zeam.form.base')


class TableActions(Actions):
    """Actions that can be applied on a table.
    """

    def process(self, form, request):
        assert interfaces.ITableFormCanvas.providedBy(form)
        one_selected = False
        ready = False

        for action in self:
            extractor = component.getMultiAdapter(
                (action, form, request), IWidgetExtractor)
            value, error = extractor.extract()
            if value is not NO_VALUE:
                if not ready:
                    form.updateLines(mark_selected=True)
                    ready = True
                for line in form.lines:
                    if not line.selected:
                        continue
                    one_selected = True
                    try:
                        if action.validate(line):
                            content = line.getContentData().getContent()
                            action(form, content, line)
                    except ActionError, e:
                        line.errors.append(Error(e.args[0], line.prefix))
                if not one_selected:
                    form.errors.append(
                        Error(_(u"You didn't select any item!"), None))
                    return action, FAILURE
                return action, SUCCESS
        return None, NOTHING_DONE
