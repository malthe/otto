import re

from otto.utils import partial
from otto.router import Router
from otto.router import Route

re_prefetch = re.compile(r'(?:(?::([a-z]+))[^:]+)+(?<!\\)\*(?![A-Za-z])')

class Publisher(object):
    """HTTP publisher.

    The ``mapper`` argument is optional; if provided, it will be
    used as the default mapper.

    Route definitions are added using the ``route`` method. It takes
    an optional ``mapper`` argument which is then used in place of
    the default value.
    """

    def __init__(self, mapper=None):
        """The optional ``mapper`` argument specifies the default
        route mapper."""

        self._router = Router()
        self._mapper = mapper

    def match(self, path):
        """Match ``path`` with routing table and return route controller."""

        try:
            match = self._router(path).next()
        except StopIteration:
            return

        route = match.route
        return route.dispatch(match.dict)

    def connect(self, path, controller=None, mapper=None):
        """Use this method to add routes."""

        if mapper is None:
            mapper = self._mapper
        route = Dispatcher(path, controller=controller, mapper=mapper)
        self._router.connect(route)
        return route

class Dispatcher(Route):
    """Route which integrates with publisher."""

    _prefetch = ()

    def __init__(self, path, controller=None, mapper=None):
        super(Dispatcher, self).__init__(path)
        self._mapper = mapper
        self._controllers = {object: controller}

        m = re_prefetch.search(path)
        if m is not None:
            self._prefetch = m.groups()

    def __call__(self, controller):
        self._controllers[object] = controller
        return self

    def bind(self, type=None):
        """Return controller; if ``type`` is specified, use adaptation
        on the type hierarchy."""

        if type is None:
            type = object
        get = self._controllers.get
        for base in type.__mro__:
            controller = get(base)
            if controller is not None:
                return controller

    def controller(self, controller=None, type=None):
        """Register ``controller`` for this route; if ``type`` is
        provided, the controller is used only for objects that contain
        this type in its class hierarchy."""

        if type is None:
            type = object
        if controller is not None:
            return self(controller)
        def handler(func):
            for cls in type.__mro__:
                self._controllers[cls] = func
            return func
        return handler

    def dispatch(self, matchdict):
        path = matchdict.pop('', None)
        if path is not None:
            d = {}
            for arg in self._prefetch:
                d[arg] = matchdict.pop(arg)
            context = self.resolve(path, **d)
            controller = self.bind(type(context))
            return partial(controller, context, **matchdict)
        else:
            controller = self.bind()
            return partial(controller, **matchdict)

    def path(self, context=None, **matchdict):
        """Generate route path. When traversal is used, ``context``
        must be provided (usually as first positional argument)."""

        if context is not None:
            try:
                reverse = self._mapper().reverse
            except AttributeError: # pragma no cover
                raise NotImplementedError(
                    "Unable to generate resolve %s using %s." % (
                        repr(context), repr(self._mapper)))

            path = reverse(context)
            matchdict[''] = path

        return super(Dispatcher, self).path(**matchdict)

    def resolve(self, path, **matchdict):
        try:
            resolve = self._mapper(**matchdict).resolve
        except AttributeError: # pragma no cover
            raise NotImplementedError(
                "Unable to resolve %s using %s." % (
                    repr(path), repr(self._mapper)))
        return resolve(path)

