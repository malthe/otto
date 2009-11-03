from functools import partial
from webob import Request
from webob import Response

from webob.exc import HTTPError
from webob.exc import HTTPForbidden

from .router import Router

class Application(object):
    """WSGI-application.

    The application matches a route from the routing table and calls
    the route controller. The request object is passed; controllers
    must return a response object.

    If traversal is used, the result is passed on to the controller as
    the first argument.
    """

    def __init__(self, factory=None):
        self._router = Router()
        self._factory = factory
        self._factories = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        match = self._router(path)
        request = Request(environ)
        if match is None:
            controller = self.not_found
        else:
            controller = self.bind(match)
        try:
            response = controller(request)
        except HTTPError, response:
            pass
        return response(environ, start_response)

    def bind(self, match):
        route = match.route
        if match.path is not None:
            factory = self._factories[route]
            context = factory(match.path)
            controller = route.get(type(context))
            return partial(controller, context, **match.dict)
        else:
            controller = route.get()
            return partial(controller, **match.dict)

    def route(self, path, factory=None):
        if factory is None:
            factory = self._factory
        route = self._router.new(path)
        self._factories[route] = factory
        return route

    def not_found(self, request):
        return Response(u"Page not found.", status="404 Not Found")

