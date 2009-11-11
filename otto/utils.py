import re

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')
_safemaps = {}
_must_quote = {}

def url_quote(s, safe=''):
    """quote('abc def') -> 'abc%20def'

    Faster version of Python stdlib urllib.quote which also quotes
    the '/' character.  

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted.

    RFC 2396 Uniform Resource Identifiers (URI): Generic Syntax lists
    the following reserved characters.

    reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" |
                  "$" | ","

    Each of these characters is reserved in some component of a URL,
    but not necessarily in all of them.

    Unlike the default version of this function in the Python stdlib,
    by default, the quote function is intended for quoting individual
    path segments instead of an already composed path that might have
    '/' characters in it.  Thus, it *will* encode any '/' character it
    finds in a string.
    """
    cachekey = (safe, always_safe)
    try:
        safe_map = _safemaps[cachekey]
        if not _must_quote[cachekey].search(s):
            return s
    except KeyError:
        safe += always_safe
        _must_quote[cachekey] = re.compile(r'[^%s]' % safe)
        safe_map = {}
        for i in range(256):
            c = chr(i)
            safe_map[c] = (c in safe) and c or ('%%%02X' % i)
        _safemaps[cachekey] = safe_map
    res = map(safe_map.__getitem__, s)
    return ''.join(res)

_segment_cache = {}

def quote_path_segment(segment):
    """ Return a quoted representation of a 'path segment' (such as
    the string ``__name__`` attribute of a model) as a string.  If the
    ``segment`` passed in is a unicode object, it is converted to a
    UTF-8 string, then it is URL-quoted using Python's
    ``urllib.quote``.  If the ``segment`` passed in is a string, it is
    URL-quoted using Python's ``urllib.quote``.  If the segment passed
    in is not a string or unicode object, an error will be raised.
    The return value of ``quote_path_segment`` is always a string,
    never Unicode.

    .. note:: The return value for each segment passed to this
              function is cached in a module-scope dictionary for
              speed: the cached version is returned when possible
              rather than recomputing the quoted version.  No cache
              emptying is ever done for the lifetime of an
              application, however.  If you pass arbitrary
              user-supplied strings to this function (as opposed to
              some bounded set of values from a 'working set' known to
              your application), it may become a memory leak.
    """
    # The bit of this code that deals with ``_segment_cache`` is an
    # optimization: we cache all the computation of URL path segments
    # in this module-scope dictionary with the original string (or
    # unicode value) as the key, so we can look it up later without
    # needing to reencode or re-url-quote it
    try:
        return _segment_cache[segment]
    except KeyError:
        if segment.__class__ is unicode: # isinstance slighly slower (~15%)
            result = url_quote(segment.encode('utf-8'))
        else:
            result = url_quote(segment)
        # we don't need a lock to mutate _segment_cache, as the below
        # will generate exactly one Python bytecode (STORE_SUBSCR)
        _segment_cache[segment] = result
        return result

