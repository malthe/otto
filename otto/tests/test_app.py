import unittest

class ApplicationCase(unittest.TestCase):
    def test_not_found(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        self.assertEqual(get_response(app, '/path'), ['Page not found.'])

    def test_forbidden(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        import webob.exc
        @app.route('/')
        def controller(request):
            raise webob.exc.HTTPForbidden("Forbidden.")
        response = get_response(app, '/')
        self.assertTrue('Forbidden' in "".join(response))
