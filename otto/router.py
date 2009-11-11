import collections
import re

Match = collections.namedtuple('Match', 'route path dict')

def compile_path(path):
    """Path compile.

    Return a regular expression match function with match groups as
    defined by the route.

    >>> compile_path('/')('/').groupdict()
    {}

    >>> compile_path('/*')('/').groupdict()
    {'_star': ''}

    >>> compile_path('/docs/*')('/docs/math/pi').groupdict()
    {'_star': 'math/pi'}

    >>> match = compile_path('/docs/*/:name')('/docs/math/pi')
    >>> sorted(match.groupdict().items())
    [('_star', 'math'), ('name', 'pi')]

    >>> compile_path('/*path')('/some/path').groupdict()
    {'path': 'some/path'}

    >>> compile_path('*path')('/some/path').groupdict()
    {'path': '/some/path'}

    >>> compile_path('/s/:term')('/s/abc').groupdict()['term']
    'abc'

    >>> compile_path('/s/(?=[abc]+):term')('/s/abc').groupdict()['term']
    'abc'

    >>> compile_path(r'/(?=.\*\.txt)*')('/test.txt').groupdict()
    {'_star': 'test.txt'}

    >>> compile_path('/(?=.+\.txt)*')('/test.txt').groupdict()
    {'_star': 'test.txt'}

    >>> compile_path('/(?=.+\.txt)*')('/test.rst') is None
    True
    """

    expression = re.sub(r':([a-z]+)', r'(?P<\1>[^/]+)', path)
    expression = re.sub(r'(?<!\\)\*(?![A-Za-z_])', '(?P<_star>.*)', expression)
    expression = re.sub(r'(?<!\\)\*([A-Za-z_]+)', '(?P<\\1>.*)', expression)
    expression = re.sub(r'\\\*', '*', expression)
    return re.compile(expression).match

def compile_reverse(path):
    """Reverse path compile.

    >>> compile_reverse('/')({})
    '/'

    >>> compile_reverse('/*')(dict(_star='some/path'))
    '/some/path'

    >>> compile_reverse('/docs/*')(dict(_star='some/path'))
    '/docs/some/path'

    >>> compile_reverse('/docs/*/:name')(dict(_star='some', name='name'))
    '/docs/some/name'
    """

    expression = re.sub(r':([a-z]+)', '%(\\1)s', path)
    expression = re.sub(r'\*(?![A-Za-z_])', '%(_star)s', expression)
    expression = re.sub(r'\*([A-Za-z_]+)', '%(\\1)s', expression)
    return expression.__mod__

def compile_routes(routes):
    """Routes compiler.

    This method compiles zero or more routes into a single regular
    expression, the result of which determines a route match; a second
    match is then performed to return the match dictionary.

    The following routes are complete matches.

    >>> index = Route('/')
    >>> search = Route('/search/:term')
    >>> rest = Route('/rest/:kind/:id')

    This route is open-ended from the start and must match to the
    end of the expression.

    >>> manage = Route('/*/manage')

    This route will match all paths.

    >>> traverse = Route('/*')

    We compile all of these into a mapper. Note that the order is
    important. Matches are greedy.

    >>> mapper = compile_routes(
    ...    (index, manage, search, rest, traverse))

    The root matches and returns an empty match dict.

    >>> mapper('/').next()
    Match(route=<Route path="/">, path=None, dict={})

    The search route only matches if a term is provided; this is
    illustrate in this example which matches the traverser route.

    >>> mapper('/front-page').next()
    Match(route=<Route path="/*">, path='front-page', dict={})

    When the term is provided, it's available in the match dict:

    >>> mapper('/search/abc').next()
    Match(route=<Route path="/search/:term">, path=None, dict={'term': 'abc'})

    This URL demonstrates how routes can match towards the end:

    >>> mapper('/front-page/manage').next()
    Match(route=<Route path="/*/manage">, path='front-page', dict={})

    >>> mapper('/rest/doc/123').next().dict
    {'kind': 'doc', 'id': '123'}
    """

    count = len(routes)
    paths = [route._path for route in routes]
    extractors = [compile_path(path) for path in paths]

    expressions = []
    for path in paths:
        expression = re.sub(r':([a-z]+)', r'(?:[^/]+)', path)
        expression = re.sub(r'\*', r'(?:.*?)', expression)
        expressions.append(expression)

    matchers = []
    for i in range(count):
        expression = "|".join(
            "(^%s$)" % expression for expression in expressions[i:])
        matcher = re.compile("(?:.*)(?:%s)" % expression).match
        matchers.append(matcher)

    del paths
    del expressions

    routes = tuple(routes)

    def matcher(path):
        i = 0
        while i < count:
            matcher = matchers[i]
            m = matcher(path)
            if m is None:
                return
            groups = m.groups()

            try:
                i += groups.index(path)
            except ValueError:
                if routes and i == 0: raise
                return

            matchdict = extractors[i](path).groupdict()
            yield Match(routes[i], matchdict.pop('_star', None), matchdict)

            i += 1

    return matcher

class Route(object):
    def __init__(self, path, controller=None, traverser=None):
        self._path = path
        self._controllers = {object: controller}
        self._reverse = compile_reverse(path)
        self._traverser = traverser

    def __call__(self, controller):
        self._controllers[object] = controller
        return self

    def __repr__(self):
        return '<%s path="%s">' % (self.__class__.__name__, self._path)

    def bind(self, cls=object):
        get = self._controllers.get
        for base in cls.__mro__:
            controller = get(base)
            if controller is not None:
                return controller

    def controller(self, type=object):
        def handler(func):
            for cls in type.__mro__:
                self._controllers[cls] = func
            return func
        return handler

    def path(self, context=None, **kw):
        if context is not None:
            try:
                reverse = self._traverser.reverse
            except AttributeError:
                raise NotImplementedError(
                    "Unable to reverse resolve %s using %s." % (
                        repr(context), repr(self._traverser)))

            path = reverse(context)
            kw['_star'] = path

        return self._reverse(kw)

    def resolve(self, path):
        try:
            resolve = self._traverser.resolve
        except AttributeError:
            raise NotImplementedError(
                "Unable to resolve %s using %s." % (
                    repr(path), repr(self._traverser)))
        return resolve(path)

class Router(object):
    """Router.

    Use the ``connect`` method to add routes. It takes a path and
    optionally keyword-arguments ``traverser`` and ``controller``.
    """

    _mapper = None

    def __init__(self, traverser=None):
        self._routes = []
        self._traverser = traverser

    def __call__(self, path):
        mapper = self._mapper
        if mapper is None:
            mapper = self._mapper = compile_routes(self._routes)
        return mapper(path)

    def connect(self, *args, **kwargs):
        kwargs.setdefault('traverser', self._traverser)
        route = Route(*args, **kwargs)
        self._routes.append(route)
        self._mapper = None
        return route
