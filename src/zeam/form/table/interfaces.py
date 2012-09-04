
from zope import interface

from zeam.form.base.interfaces import IFormCanvas, IForm
from zeam.form.base.interfaces import IZeamFormBaseAPI
from zeam.form.composed.interfaces import ISubForm


class ITableFormCanvas(IFormCanvas):
    """Base form behavior for forms working on more than one content
    at a time.
    """

    lines = interface.Attribute(u"Widgets lines")

    def updateLines():
        """Prepare widgets and forms for each lines.
        """

    def getItems():
        """Return the list of contents.
        """

    def getItemIdentifier(item, position):
        """A factory with parameters
           item (the item from getItems),
           and position (the index in getItems)
        """

class ITableForm(IForm, ITableFormCanvas):
    """A form which is able to work on more than one item at a time.
    """


class ISubTableForm(ISubForm, ITableFormCanvas):
    """A table form that can be used in a composed form.
    """


class IZeamFormTableAPI(IZeamFormBaseAPI):
    """Public API of zeam.form.table
    """

    TableForm = interface.Attribute(
        u"A form able to work on more on more than one item at a time")
    SubTableForm = interface.Attribute(
        u"A table form that can be used in a composed form")
    TableActions = interface.Attribute(
        u"Action being executed on more than one content at a time")
    TableSelectionActions = interface.Attribute(
        u"Action executed on the selection of content")
    TableMultiActions = interface.Attribute(
        u"Action excted one time for multiple content")
