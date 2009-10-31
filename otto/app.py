from functools import partial
from .router import Router
from .exc import Forbidden

class Application(object):
    """WSGI-application.

    :param root_factory: callable which returns a root object

    The application passes ``environ`` and ``start_response`` to the
    controller and expects an iterable as return value (or generator).

    If traversal is used, the result is passed on to the controller as
    the first argument.
    """

    def __init__(self, root_factory=None):
        self._router = Router()
        self._root_factories = {}
        self._root_factory = root_factory

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        controller = self.match(path)
        try:
            return controller(environ, start_response)
        except Forbidden:
            return self.forbidden(environ, start_response)

    def match(self, path):
        match = self._router(path)
        if match is None:
            return self.not_found
        route = match.route
        if match.path is not None:
            root_factory = self._root_factories[route]
            root = root_factory()
            context = self.traverse(root, match.path)
            controller = route.get(type(context))
            return partial(controller, context, **match.dict)
        else:
            controller = route.get()
            return partial(controller, **match.dict)

    def _handle_error(self, start_response, status, message):
        start_response("404 Not Found", [('Content-type', 'text/plain')])
        return message,

    def not_found(self, environ, start_response):
        return self._handle_error(
            start_response, "404 Not Found", "Page not found")

    def forbidden(self, environ, start_response):
        return self._handle_error(
            start_response, "403 Forbidden", "Access was denied.")

    def route(self, path, root_factory=None):
        if root_factory is None:
            root_factory = self._root_factory
        route = self._router.new(path)
        self._root_factories[route] = root_factory
        return route

    def traverse(self, root, path):
        segments = path.split('/')
        context = root
        for segment in segments:
            context = context[segment]
        return context

class WebObApplication(Application):
    """WSGI-application which passed a ``webob.Request`` object to the
    controller instead of ``environ`` and ``start_response``. The
    controller must return a ``webob.Response`` object.
    """

    def __init__(self):
        from webob import Request, Response
        self._request_factory = Request
        self._response_factory = Response
        super(WebObApplication, self).__init__()

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        controller = self.match(path)
        request = self._request_factory(environ)
        response = controller(request)
        return response(environ, start_response)

    def not_found(self, request):
        return self._response_factory(status=404, body='Page not found')
