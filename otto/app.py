from functools import partial
from webob import Request
from webob import Response
from webob.exc import HTTPError
from .router import Router

class Application(object):
    """WSGI-application.

    The application matches a route from the routing table and calls
    the route controller. The request object is passed; controllers
    must return a response object.

    If traversal is used, the result is passed on to the controller as
    the first argument.
    """

    def __init__(self, traverser=None):
        self._router = Router()
        self._traverser = traverser
        self._resolvers = {}

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
            resolver = self._resolvers[route]
            context = resolver(match.path)
            controller = route.bind(type(context))
            return partial(controller, context, **match.dict)
        else:
            controller = route.bind()
            return partial(controller, **match.dict)

    def route(self, path, traverser=None):
        if traverser is None:
            traverser = self._traverser
        route = self._router.new(path, traverser=traverser)
        if traverser is not None:
            self._resolvers[route] = traverser.resolve
        return route

    def not_found(self, request):
        return Response(u"Page not found.", status="404 Not Found")

