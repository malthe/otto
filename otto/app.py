import types

from webob import Request
from webob.exc import HTTPError
from webob.exc import HTTPException
from webob.exc import HTTPNotFound
from webob.exc import HTTPMovedPermanently
from otto.publisher import Publisher

class Application(Publisher):
    """WSGI-Application.

    This class adds a WSGI application interface to the HTTP
    publisher. The ``publish`` method can be overriden to intercept
    errors (the HTTP exception classes are provided by :mod:`WebOb`).
    """

    def __call__(self, environ, start_response):
        """WSGI application callable."""

        response = self.publish(environ)
        return response(environ, start_response)

    def __get__(self, inst, cls):
        def wsgi_app(environ, start_response):
            response = self.publish(environ, inst)
            return response(environ, start_response)
        return wsgi_app

    def publish(self, environ, bind=None):
        """Return response for request given by ``environ``."""

        request = Request(environ)
        path = request.path_info
        controller = self.match(path)
        if controller is None:
            if path.endswith('/'):
                path = path.rstrip('/')
            else:
                path = path + '/'
            controller = self.match(path)
            if controller is not None:
                request.path_info = path
                response = HTTPMovedPermanently(location=request.url)
            else:
                response = HTTPNotFound("Page not found.")
        else:
            if bind is not None:
                controller = types.MethodType(controller, bind)
            try:
                response = controller(request)
            except HTTPError as e:
                response = e
            except HTTPException as e:  # pragma no cover
                response = e.wsgi_response

        return response
