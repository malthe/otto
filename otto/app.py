from webob import Request
from webob.exc import HTTPError
from webob.exc import HTTPNotFound
from webob.exc import HTTPMovedPermanently
from .publisher import Publisher

class Application(Publisher):
    """WSGI-Application.

    This class adds a WSGI application interface to the HTTP
    publisher. The ``publish`` method can be overriden to intercept
    errors (the HTTP exception classes are provided by :mod:`WebOb`).
    """

    def __call__(self, environ, start_response):
        response = self.publish(environ)
        return response(environ, start_response)

    def publish(self, environ):
        request = Request(environ)
        path = request.path_info
        controller = self.match(path)
        if controller is None:
            # try adding or removing a trailing slash
            path = path.rstrip('/') if path.endswith('/') else path + '/'
            controller = self.match(path)
            if controller is not None:
                request.path_info = path
                response = HTTPMovedPermanently(location=request.url)
            else:
                response = HTTPNotFound("Page not found.")
        else:
            try:
                response = controller(request)
            except HTTPError, response:
                pass
        return response
