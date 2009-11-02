import unittest

class WebObApplicationCase(unittest.TestCase):

    def test_not_found(self):
        from otto.app import WebObApplication
        from otto.tests.utils import get_response
        app = WebObApplication()
        self.assertEqual(get_response(app, '/path'), ['Page not found'])

    def test_url_slash_handling(self):
        from otto.app import WebObApplication
        from webob import Request
        app = WebObApplication()
        @app.route('/url/with/')
        def controller_with(request):
            return 'With'
        @app.route('/url/without')
        def controller_without(request):
            return 'Without'

        r = Request.blank('/url/with').get_response(app)
        self.assertEqual(r.status, '301 Moved Permanently')
        self.assertEqual(r.headers['location'], 'http://localhost/url/with/')

        r = Request.blank('/url/without/').get_response(app)
        self.assertEqual(r.status, '301 Moved Permanently')
        self.assertEqual(r.headers['location'], 'http://localhost/url/without')



