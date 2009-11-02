class Event(object):
    """Subscriber based event registry.

    Event instances can be used to create have a subscriber based event
    model. Each instance contains it own registry.

    >>> from otto.event import Event
    >>> my_event = Event()

    Handlers can be can registered with the event. A key must be given when
    registering. This key must be a class, it can be `object` to handle
    everything.

    >>> from pprint import pprint
    >>> def handle_event(obj, *args, **kwargs):
    ...     pprint((args, kwargs))
    >>> my_event.register(object, handle_event)

    All handlers are executed when the event is called. The call needs at least
    one argument on which it determines the handlers it needs to trigger.

    >>> class A(object):
    ...     pass

    >>> my_event(A(), 1, 2, hello='world')
    ((1, 2), {'hello': 'world'})

    The system dispatches all handlers for matching type or their subclasses.

    >>> class B(A):
    ...     pass

    >>> class C(B):
    ...     pass

    >>> another_event = Event()
    >>> another_event.register(B, handle_event)

    Objects of type `C` will trigger the event since it is a super class of
    `B`.

    >>> another_event(C(), 'hello')
    (('hello',), {})

    An `A` object will not trigger the event handler since it is not a subtype
    of B.

    >>> another_event(A(), 'hello')

    """

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


