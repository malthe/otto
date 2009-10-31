import os
import unittest
import doctest

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class DoctestCase(unittest.TestCase):
    def __new__(self, test):
        return getattr(self, test)()

    @classmethod
    def test_router(cls):
        import otto.router
        return doctest.DocTestSuite(otto.router, optionflags=OPTIONFLAGS)

    @classmethod
    def test_tutorial(cls):
        import manuel.testing
        import manuel.codeblock
        import manuel.doctest
        import manuel.capture
        m = manuel.doctest.Manuel()
        m += manuel.codeblock.Manuel()
        m += manuel.capture.Manuel()
        return manuel.testing.TestSuite(
            m, os.path.join('..', 'docs', 'getting_started.rst'))
