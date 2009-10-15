
from zope import interface

from zeam.form.base.interfaces import IFormCanvas, IForm
from zeam.form.base.interfaces import IZeamFormBaseAPI


class ITableFormCanvas(IFormCanvas):
    """Base form behavior for forms working on more than one content
    at a time.
    """

    lines = interface.Attribute(u"Widgets lines")

    def getItems():
        """Return the list of contents.
        """


class ITableForm(IForm):
    """A form which is able to work on more than one item at a time.
    """



class IZeamFormTableAPI(IZeamFormBaseAPI):
    """Public API of zeam.form.table
    """

    TableForm = interface.Attribute(
        u"A form able to work on more on more than one item at a time")
    TableActions = interface.Attribute(
        u"Action being executed on more than one content at a time")
