from functools import partial
from .router import Router

class Publisher(object):
    """HTTP publisher.

    The ``traverser`` argument is optional; if provided, it will be
    used as the default traverser.

    Route definitions are added using the ``route`` method. It takes
    an optional ``traverser`` argument which is then used in place of
    the default value.
    """

    def __init__(self, traverser=None):
        self._router = Router(traverser)

    def match(self, path):
        try:
            match = self._router(path).next()
        except StopIteration:
            return
        route = match.route
        if match.path is not None:
            context = route.resolve(match.path)
            controller = route.bind(type(context))
            return partial(controller, context, **match.dict)
        else:
            controller = route.bind()
            return partial(controller, **match.dict)

    def route(self, path, **kw):
        return self._router.connect(path, **kw)

