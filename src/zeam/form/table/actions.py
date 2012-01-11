

from zeam.form.base.markers import NO_VALUE, SUCCESS, FAILURE, NOTHING_DONE
from zeam.form.base.markers import getValue
from zeam.form.base.actions import Actions
from zeam.form.base.errors import Error
from zeam.form.base.interfaces import IWidgetExtractor, ActionError

from zeam.form.table import interfaces

from zope import component
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zeam.form.base')


class TableActions(Actions):
    """Actions that can be applied on a table line.

    Actions are applied for each selected table line.
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
                isPostOnly = getValue(action, 'postOnly', form)
                if isPostOnly and request.method != 'POST':
                    form.errors.append(
                        Error('This form was not submitted properly.',
                              form.prefix))
                    return form, None, FAILURE
                if not ready:
                    form.updateLines(mark_selected=True)
                    ready = True
                for line in form.lines:
                    if not line.selected:
                        continue
                    one_selected = True
                    try:
                        if action.validate(form):
                            content = line.getContentData().getContent()
                            action(form, content, line)
                    except ActionError, e:
                        line.errors.append(Error(e.args[0], line.prefix))
                if not one_selected:
                    form.errors.append(
                        Error(_(u"You didn't select any item!"), None))
                    return form, action, FAILURE
                return form, action, SUCCESS
        return form, None, NOTHING_DONE


class TableSelectionActions(Actions):
    """Actions that manage a selection of table lines.

    Actions are applied only one time with a list of changes regarding
    which lines have been selected and unselected from the original
    content selection.
    """

    def process(self, form, request):
        assert interfaces.ITableFormCanvas.providedBy(form)
        selected_lines = []
        deselected_lines = []
        unchanged_lines = []

        # mark selected by request
        form.updateLines(mark_selected=True)
        for line in form.lines:
            data = line.getContentData()
            content_selected = data.get(line.selectedField.identifier)
            if content_selected:
                if line.selected:
                    unchanged_lines.append(line)
                else:
                    deselected_lines.append(line)
            else:
                if line.selected:
                    selected_lines.append(line)
                else:
                    unchanged_lines.append(line)

        status = NOTHING_DONE
        for action in self:
            extractor = component.getMultiAdapter(
                (action, form, request), IWidgetExtractor)
            value, error = extractor.extract()
            if value is NO_VALUE:
                continue

            isPostOnly = getValue(action, 'postOnly', form)
            if isPostOnly and request.method != 'POST':
                form.errors.append(
                    Error('This form was not submitted properly.',
                          form.prefix))
                return form, None, FAILURE

            try:
                if action.validate(form):
                    return form, action, action(
                        form,
                        selected_lines,
                        deselected_lines,
                        unchanged_lines)
            except ActionError, e:
                form.errors.append(Error(e.args[0], form.prefix))
                return form, action, FAILURE

        return form, None, status


class TableMultiActions(Actions):
    """Actions that manage multiple table lines.

    Actions are applied one time with a list of currently selected and
    unselected lines.
    """

    def process(self, form, request):
        assert interfaces.ITableFormCanvas.providedBy(form)
        selected_lines = []
        unselected_lines = []
        ready = False

        for action in self:
            extractor = component.getMultiAdapter(
                (action, form, request), IWidgetExtractor)
            value, error = extractor.extract()
            if value is not NO_VALUE:
                isPostOnly = getValue(action, 'postOnly', form)
                if isPostOnly and request.method != 'POST':
                    form.errors.append(
                        Error('This form was not submitted properly.',
                              form.prefix))
                    return form, None, FAILURE
                if not ready:
                    form.updateLines(mark_selected=True)
                    for line in form.lines:
                        if line.selected:
                            selected_lines.append(line)
                        else:
                            unselected_lines.append(line)
                    ready = True

                try:
                    if action.validate(form):
                        return form, action, action(
                            form,
                            selected_lines,
                            unselected_lines)
                except ActionError, e:
                    form.errors.append(Error(e.args[0], form.prefix))
                    return form, action, FAILURE

        return form, None, NOTHING_DONE

