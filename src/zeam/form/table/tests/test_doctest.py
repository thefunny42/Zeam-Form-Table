import doctest
import unittest
from zeam.form.table.testing import FunctionalLayer


def test_suite():
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    globs= {}

    suite = unittest.TestSuite()
    for filename in ['forms.txt',]:
        test = doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs=globs)
        test.layer = FunctionalLayer
        suite.addTest(test)

    return suite
