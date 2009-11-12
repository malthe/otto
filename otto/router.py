import collections
import re

from urllib import unquote
from .utils import quote_path_segment
from .utils import url_quote

Match = collections.namedtuple('Match', 'route path dict')

re_segment = re.compile(r':([a-z]+)')
re_stararg = re.compile(r'(?<!\\)\*(?P<name>[A-Za-z_]*)')

def matcher(path):
    """Path compile.

    Return a regular expression match function with match groups as
    defined by the route.

    >>> matchdict = matcher('/a/:b/*/:d/e')('/a/b/c/d/e')
    >>> sorted(matchdict.items())
    [('*', (u'c',)), ('b', 'b'), ('d', 'd')]

    >>> matchdict = matcher('/a/:b/*/:e')('/a/b/c/d/e')
    >>> sorted(matchdict.items())
    [('*', (u'c', u'd')), ('b', 'b'), ('e', 'e')]

    >>> matcher('/')('/')
    {}

    >>> matcher('/:foo')('/')
    {'foo': u''}

    >>> matcher('/*')('/')
    {'*': ()}

    >>> matcher('/docs/*')('/docs/math/pi')
    {'*': (u'math', u'pi')}

    >>> matchdict = matcher('/docs/*/:name')(u'/docs/math/pi')
    >>> sorted(matchdict.items())
    [('*', (u'math',)), ('name', u'pi')]

    >>> matcher('/*path')('/some/path')
    {'path': (u'some', u'path')}

    >>> matcher('*path')('/some/path')
    {'path': (u'some', u'path')}

    >>> matcher('/s/:term')('/s/abc')['term']
    u'abc'

    >>> matcher('/s/(?=[abc]+):term')('/s/abc')['term']
    u'abc'

    >>> matcher(r'/(?=.\*\.txt)*')('/test.txt')
    {'*': (u'test.txt',)}

    >>> matcher('/(?=.+\.txt)*')('/test.txt')
    {'*': (u'test.txt',)}

    >>> matcher('/(?=.+\.txt)*')('/test.rst') is None
    True
    """

    # setup star match
    star = re_stararg.search(path)
    if star is not None:
        name = star.group('name') or '*'
        path = re_stararg.sub('(?P<_star>.*?)', path)

    # substitute segments into capture groups
    expression = re_segment.sub(r'(?P<\1>[^/]*)', path)

    # unescape star-escape
    expression = re.sub(r'\\\*', '*', expression)
    match = re.compile("^%s$" % expression).match

    if star is None:
        def groupdict(path, match=match):
            m = match(path)
            if m is not None:
                matchdict = m.groupdict()
                for key, value in matchdict.items():
                    matchdict[key] = unquote(value).decode('utf-8')
                return matchdict
        return groupdict

    def stargroupdict(path, match=match, name=name):
        m = match(path)
        if m is None:
            return
        matchdict = m.groupdict()
        star = unquote(matchdict.pop('_star')).decode('utf-8')
        matchdict[name] = tuple(filter(None, star.split('/')))
        return matchdict

    return stargroupdict

def generator(path):
    """Generate path compile.

    >>> generator('/')({})
    '/'

    >>> generator('/:name/')({'name': 'foo'})
    '/foo/'

    >>> generator('/*')({'*': ('some', 'path')})
    '/some/path'

    >>> generator('/*/')({'*': ('some', 'path')})
    '/some/path/'

    >>> generator('/*')({'*': 'some/path'})
    '/some/path'

    >>> generator('/:foo*bar')({'foo': 'foo', 'bar': ('bar', 'boo')})
    '/foo/bar/boo'

    >>> generator('/docs/*')({'*': ('some', 'path')})
    '/docs/some/path'

    >>> generator('/docs/*/:name')({'*': ('some',), 'name': 'name'})
    '/docs/some/name'
    """

    expression = re.sub(r':([a-z]+)', '%(\\1)s', path)

    star = re_stararg.search(expression)
    if star is None:
        def generate(kw, expression=expression):
            for key, value in kw.items():
                kw[key] = quote_path_segment(unicode(value))
            return expression % kw
        return generate

    start = star.start() - 1
    if start > 0 and expression[start] != '/':
        expression = expression[:start + 1] + '/' + expression[start + 1:]

    name = star.group('name') or '*'
    expression = re_stararg.sub('%%(%s)s' % name, expression)
    trailing = path.endswith('/')

    def generate(kw, name=name, expression=expression, trailing=trailing):
        star = kw.pop(name)
        for key, value in kw.items():
            kw[key] = quote_path_segment(unicode(value))
        if isinstance(star, basestring):
            star = url_quote(star.strip('/'), '/')
        else:
            quote = quote_path_segment
            star = "/".join(map(quote_path_segment, star))
        kw[name] = star
        path = expression % kw
        if trailing is False:
            return path.rstrip('/')
        return path

    return generate

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
    Match(route=<Route path="/*">, path=(u'front-page',), dict={})

    When the term is provided, it's available in the match dict:

    >>> mapper('/search/abc').next()
    Match(route=<Route path="/search/:term">, path=None, dict={'term': u'abc'})

    This URL demonstrates how routes can match towards the end:

    >>> mapper('/front-page/manage').next()
    Match(route=<Route path="/*/manage">, path=(u'front-page',), dict={})

    >>> mapper('/rest/doc/123').next().dict
    {'kind': u'doc', 'id': u'123'}
    """

    count = len(routes)
    paths = [route._path for route in routes]

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
            i += groups.index(path)
            route = routes[i]
            matchdict = route.match(path)
            yield Match(routes[i], matchdict.pop('*', None), matchdict)

            i += 1

    return matcher

class Route(object):
    def __init__(self, path):
        """Create route given by ``path``."""

        self._path = path
        self._generate = generator(path)
        self.match = matcher(path)

    def __repr__(self):
        return '<%s path="%s">' % (self.__class__.__name__, self._path)

    def path(self, **matchdict):
        """Generate path given ``**matchdict``."""

        return self._generate(matchdict)

class Router(object):
    """Interface to the routing engine."""

    _mapper = None

    def __init__(self):
        self._routes = []

    def __call__(self, path):
        """Returns an iterator which yields route matches."""

        mapper = self._mapper
        if mapper is None:
            mapper = self._mapper = compile_routes(self._routes)
        return mapper(path)

    def connect(self, route):
        """Use this method to add routes."""

        self._routes.append(route)
        self._mapper = None
        return route
