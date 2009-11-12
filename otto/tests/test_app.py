import unittest

class ApplicationCase(unittest.TestCase):
    def test_not_found(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        response = get_response(app, '/path')
        self.assertTrue('404 Not Found' in "".join(response))

    def test_forbidden(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        import webob.exc
        @app.connect('/')
        def controller(request):
            raise webob.exc.HTTPForbidden("No access.").exception
        response = get_response(app, '/')
        self.assertTrue('403 Forbidden' in "".join(response))
