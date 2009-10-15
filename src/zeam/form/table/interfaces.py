
from zope import interface

from zeam.form.base.interfaces import IFormCanvas


class ITableFormCanvas(IFormCanvas):

    lines = interface.Attribute(u"Widgets lines")

    def getItems():
        """Return the list of contents.
        """
