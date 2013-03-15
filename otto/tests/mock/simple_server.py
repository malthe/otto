import re
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from otto.tests.utils import get_response


class make_server(object):
    def __init__(self, host, port, app):
        self.app = app

    def serve_forever(self):
        pass


def compare(result, value):
    regex = re.compile(re.escape(value).replace(re.escape('...'), '(.+)?'))
    if regex.match(result) is None:
        raise AssertionError(
            "Printed: %s does not match: %s" % (
                result, value
            )
        )


def strip(string):
    return string.strip().replace(' ', '').replace('\n', '')


def assert_response(url, app, value):
    response = get_response(app, url.strip('\n '))
    try:
        result = ''.join(response)
    except TypeError:
        result = ''.join([part.decode('utf-8') for part in response])

    result = strip(result)
    value = strip(value)
    compare(result, value)


def assert_printed(code, locals, value):
    out = StringIO()
    stdout = sys.stdout
    try:
        sys.stdout = out
        exec(code, locals)
    finally:
        sys.stdout = stdout
    result = strip(out.getvalue())
    value = strip(value)
    compare(result, value)
