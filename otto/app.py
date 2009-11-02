from functools import partial
from webob import Request
from webob import Response

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
        match = self._router(path)
        request = Request(environ)
        try:
            controller = self.bind(match)
        except Forbidden:
            controller = self.forbidden
        response = controller(request)
        return response(environ, start_response)

    def bind(self, match):
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

    def not_found(self, request):
        return Response(u"Page not found.", status="404 Not Found")

    def forbidden(self, request):
        return Response(u"Access was denied.", status="403 Forbidden")

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

