from webob import Request
from webob.exc import HTTPError
from webob.exc import HTTPNotFound
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
        path = environ['PATH_INFO']
        controller = self.match(path)
        if controller is None:
            response = HTTPNotFound("Page not found.")
        else:
            request = Request(environ)
            try:
                response = controller(request)
            except HTTPError, response:
                pass
        return response
