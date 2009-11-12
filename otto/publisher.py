from otto.utils import partial
from otto.router import Router
from otto.router import Route

class Publisher(object):
    """HTTP publisher.

    The ``traverser`` argument is optional; if provided, it will be
    used as the default traverser.

    Route definitions are added using the ``route`` method. It takes
    an optional ``traverser`` argument which is then used in place of
    the default value.
    """

    def __init__(self, traverser=None):
        """The optional ``traverser`` argument specifies the default
        route traverser."""

        self._router = Router()
        self._traverser = traverser

    def match(self, path):
        """Match ``path`` with routing table and return route controller."""

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

    def connect(self, path, controller=None, traverser=None):
        """Use this method to add routes."""

        if traverser is None:
            traverser = self._traverser
        route = Dispatcher(path, controller=controller, traverser=traverser)
        self._router.connect(route)
        return route

class Dispatcher(Route):
    """Route which integrates with publisher."""

    def __init__(self, path, controller=None, traverser=None):
        super(Dispatcher, self).__init__(path)
        self._traverser = traverser
        self._controllers = {object: controller}

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

    def path(self, context=None, **matchdict):
        """Generate route path. When traversal is used, ``context``
        must be provided (usually as first positional argument)."""

        if context is not None:
            try:
                reverse = self._traverser.reverse
            except AttributeError: # pragma no cover
                raise NotImplementedError(
                    "Unable to generate resolve %s using %s." % (
                        repr(context), repr(self._traverser)))

            path = reverse(context)
            matchdict['*'] = path

        return super(Dispatcher, self).path(**matchdict)

    def resolve(self, path):
        try:
            resolve = self._traverser.resolve
        except AttributeError: # pragma no cover
            raise NotImplementedError(
                "Unable to resolve %s using %s." % (
                    repr(path), repr(self._traverser)))
        return resolve(path)

