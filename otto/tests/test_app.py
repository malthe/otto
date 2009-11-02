import unittest

class ApplicationCase(unittest.TestCase):
    def test_not_found(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        self.assertEqual(get_response(app, '/path'), ['Page not found.'])

