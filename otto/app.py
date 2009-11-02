from functools import partial

from webob.exc import HTTPMovedPermanently

from .router import Router
from .exc import Forbidden

class Event(object):

    def __init__(self):
        self._reg = {}

    def register(self, key, value):
        self._reg[key] = value

    def lookup(self, obj):
        for key in self._get_variations(obj):
            if key in self._reg:
                yield self._reg[key]

    def _get_variations(self, obj):
        return type(obj).__mro__

    def __call__(self, obj, *args, **kwargs):
        for handler in self.lookup(obj):
            handler(obj, *args, **kwargs)


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
        self._traverse_event = Event()

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        try:
            controller = self.match(path, environ)
            return controller(environ, start_response)
        except Forbidden:
            return self.forbidden(environ, start_response)

    def match(self, path, environ):
        match = self._router(path)
        if match is None:
            if path.endswith('/'):
                path = path[:-1]
            else:
                path = path + '/'
            if self._router(path):
                if self._router(path) is not None:
                    def redirect(request):
                        return HTTPMovedPermanently(location=path)
                    return redirect
            return self.not_found
        route = match.route
        if match.path is not None:
            root_factory = self._root_factories[route]
            root = root_factory()
            context = self.traverse(root, match.path, environ)
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

    def traverse(self, root, path, environ):
        segments = path.split('/')
        context = root
        for segment in segments:
            context = context[segment]
            self.traverse_event(context, environ, segment)
        return context

    def traverse_event(self, context, environ, segment):
        self._traverse_event(context, environ, segment)

    def on_traverse(self, func=None, **kwargs):
        if 'type' in kwargs:
            def register(func):
                self._traverse_event.register(kwargs['type'], func)
                return func
            return register
        self._traverse_event.register(object, func)
        return func

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
        request = self._request_factory(environ)
        controller = self.match(path, request)
        response = controller(request)
        return response(environ, start_response)

    def not_found(self, request):
        return self._response_factory(status=404, body='Page not found')
