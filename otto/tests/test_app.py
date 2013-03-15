import unittest

class ApplicationCase(unittest.TestCase):
    def test_not_found(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        response = get_response(app, '/path')
        strings = map(str, response)
        self.assertTrue('404 Not Found' in "".join(strings))

    def test_forbidden(self):
        from otto import Application
        from otto.tests.utils import get_response
        app = Application()
        import webob.exc
        @app.connect('/')
        def controller(request):
            raise webob.exc.HTTPForbidden("No access.")
        response = get_response(app, '/')
        strings = map(str, response)
        self.assertTrue('403 Forbidden' in "".join(strings))
