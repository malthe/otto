import os
import unittest
import doctest
from functools import partial

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
        join = partial(os.path.join, '..', '..', 'docs')
        docs = ('getting_started.rst', 'security.rst', 'traversal.rst')
        return manuel.testing.TestSuite(m, *map(join, docs))
