import unittest

class WebObApplicationCase(unittest.TestCase):

    def test_not_found(self):
        from otto.app import WebObApplication
        from otto.tests.utils import get_response
        app = WebObApplication()
        self.assertEqual(get_response(app, '/path'), ['Page not found'])

