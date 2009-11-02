from functools import partial
from webob import Request
from webob import Response

from webob.exc import HTTPError
from webob.exc import HTTPForbidden

from .router import Router

class Event(object):
    """Application event."""

    def __init__(self):
        self._registry = {}

    def __call__(self, obj, *args):
        registry = self._registry
        for base in type(obj).__mro__:
            handler = registry.get(base)
            if handler is not None:
                handler(obj, *args)

    def register(self, key, value):
        self._registry[key] = value

class Application(object):
    """WSGI-application.

    :param root_factory: callable which returns a root object

    The application matches a route from the routing table and calls
    the route controller. The request object is passed; controllers
    must return a response object.

    If traversal is used, the result is passed on to the controller as
    the first argument.
    """

    _traverse_event = None

    def __init__(self, root_factory=None):
        self._router = Router()
        self._root_factories = {}
        self._root_factory = root_factory

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        match = self._router(path)
        request = Request(environ)
        if match is None:
            controller = self.not_found
        else:
            try:
                controller = self.bind(match)
            except HTTPForbidden:
                controller = self.forbidden
        try:
            response = controller(request)
        except HTTPError, response:
            pass
        return response(environ, start_response)

    def bind(self, match):
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

    def route(self, path, root_factory=None):
        if root_factory is None:
            root_factory = self._root_factory
        route = self._router.new(path)
        self._root_factories[route] = root_factory
        return route

    def traverse(self, root, path):
        segments = path.split('/')
        context = root
        event = self._traverse_event
        for segment in segments:
            context = context[segment]
            if event is not None:
                event(context, segment)
        return context

    def on_traverse(self, func=None, type=None, **kwargs):
        event = self.__dict__.setdefault('_traverse_event', Event())
        if type is not None:
            def register(func):
                event.register(type, func)
                return func
            return register
        event.register(object, func)
        return func

    def forbidden(self, request):
        return Response(u"Access was denied.", status="403 Forbidden")

    def not_found(self, request):
        return Response(u"Page not found.", status="404 Not Found")

