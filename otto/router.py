import re
import operator

from urllib import unquote
from otto.utils import quote_path_segment
from otto.utils import url_quote

try:
    from collections import namedtuple
    Match = namedtuple('Match', 'route dict')
except ImportError: # pragma no cover
    class Match(tuple):
        def __new__(cls, route, dict):
            return tuple.__new__(cls, (route, dict))

        def __repr__(self):
            return '%s(route=%s, dict=%s)' % (
                type(self).__name__, self.route, self.dict)

        route = property(operator.itemgetter(0))
        dict = property(operator.itemgetter(2))

re_segment = re.compile(r':([a-z]+)')
re_stararg = re.compile(r'(?<!\\)\*(?P<name>[A-Za-z_]*)')

def matcher(path):
    """Compile match function for ``path``.

    Return a regular expression match function with match groups as
    defined by the route.

    >>> matchdict = matcher('/a/:b/*/:d/e')('/a/b/c/d/e')
    >>> sorted(matchdict.items())
    [('', (u'c',)), ('b', u'b'), ('d', u'd')]

    >>> matchdict = matcher('/a/:b/*/:e')('/a/b/c/d/e')
    >>> sorted(matchdict.items())
    [('', (u'c', u'd')), ('b', u'b'), ('e', u'e')]

    >>> matcher('/')('/')
    {}

    >>> matcher('')('/')
    {}

    >>> matcher('/:foo')('/')
    {'foo': u''}

    >>> matcher('/*')('/')
    {'': ()}

    >>> matcher('/docs/*')('/docs/math/pi')
    {'': (u'math', u'pi')}

    >>> matchdict = matcher('/docs/*/:name')(u'/docs/math/pi')
    >>> sorted(matchdict.items())
    [('', (u'math',)), ('name', u'pi')]

    >>> matcher('/*path')('/some/path')
    {'path': (u'some', u'path')}

    >>> matcher('*path')('/some/path')
    {'path': (u'some', u'path')}

    >>> matcher('/s/:term')('/s/abc')['term']
    u'abc'

    >>> matcher('/s/(?=[abc]+):term')('/s/abc')['term']
    u'abc'

    >>> matcher(r'/(?=.+\.txt)*')('/test.txt')
    {'': (u'test.txt',)}

    >>> matcher(r'/(?=.\*\.txt)*')('/test.txt')
    {'': (u'test.txt',)}

    >>> matcher('/(?=.+\.txt)*')('/test.rst') is None
    True
    """

    if not path.startswith('/'):
        path = '(?:/)' + path

    # setup star match
    star = re_stararg.search(path)
    if star is not None:
        name = star.group('name')
        path = re_stararg.sub('(?P<_star>.*?)', path)

    # substitute segments into capture groups
    expression = re_segment.sub(r'(?P<\1>[^/]*)', path)

    # unescape star-escape
    expression = re.sub(r'\\\*', '*', expression)
    match = re.compile("^%s$" % expression).match

    if star is None:
        name = None

    def match(path, match=match, name=name, unquote=unquote):
        m = match(path)
        if m is None:
            return
        d = {}
        for k, v in m.groupdict().iteritems():
            v = unquote(v).decode('utf-8')
            if k == '_star':
                k = name
                v = tuple(s for s in v.split('/') if s)
            d[k] = v
        return d

    return match

def generator(path):
    """Compile generate function for ``path``.

    >>> generator('/')({})
    '/'

    >>> generator('/:name/')({'name': 'foo'})
    '/foo/'

    >>> generator('/*')({'': ('some', 'path')})
    '/some/path'

    >>> generator('/*/')({'': ('some', 'path')})
    '/some/path/'

    >>> generator('/*')({'': 'some/path'})
    '/some/path'

    >>> generator('/:foo*bar')({'foo': 'foo', 'bar': ('bar', 'boo')})
    '/foo/bar/boo'

    >>> generator('/docs/*')({'': ('some', 'path')})
    '/docs/some/path'

    >>> generator('/docs/*/:name')({'': ('some',), 'name': 'name'})
    '/docs/some/name'
    """

    expression = re.sub(r':([a-z]+)', '%(\\1)s', path)
    trailing = path.endswith('/')

    star = re_stararg.search(expression)
    if star is not None:
        start = star.start() - 1
        if start > 0 and expression[start] != '/':
            expression = expression[:start + 1] + '/' + expression[start + 1:]

        name = star.group('name') or ''
        expression = re_stararg.sub('%%(%s)s' % name, expression)
    else:
        name = None

    def generate(kw):
        d = {}
        for key, value in kw.items():
            if key == name:
                if isinstance(value, basestring):
                    value = url_quote(value.strip('/'), '/')
                else:
                    quote = quote_path_segment
                    value = "/".join(map(quote_path_segment, value))
            else:
                cls = value.__class__
                if cls is unicode:
                    value = url_quote(value.encode('utf-8'))
                elif cls is str:
                    value = url_quote(value)
            d[key] = value
        path = expression % d
        if trailing is False:
            return path.rstrip('/')
        return path
    return generate

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

    def __init__(self):
        self._routes = []

    def __call__(self, path):
        """Returns an iterator which yields route matches."""

        for route in self._routes:
            m = route.match(path)
            if m is not None:
                yield Match(route, m)

    def connect(self, route):
        """Use this method to add routes."""

        self._routes.append(route)
