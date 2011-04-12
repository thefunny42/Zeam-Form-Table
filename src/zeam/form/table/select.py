
from zeam.form.base.fields import Field
from zeam.form.base.widgets import FieldWidget, WidgetExtractor

from grokcore import component as grok


class SelectField(Field):
    # This field is always in input and have a different prefix
    mode = 'input'
    prefix = 'select'
    ignoreContent = True
    ignoreRequest = False
    defaultValue = False


class SelectFieldWidget(FieldWidget):
    grok.adapts(SelectField, None, None)

    def htmlClass(self):
        cls = ['field', '-'.join([self.form.parent.htmlId(), 'select'])]
        return ' '.join(cls)

    def prepareContentValue(self, value):
        return {self.identifier: bool(value)}


class SelectFieldExtractor(WidgetExtractor):
    grok.adapts(SelectField, None, None)

    def extract(self):
        value, error = WidgetExtractor.extract(self)
        if value == 'selected':
            return True, None
        return False, None
