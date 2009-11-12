import sys
from StringIO import StringIO
from otto.tests.utils import get_response

class make_server(object):
    def __init__(self, host, port, app):
        self.app = app

    def serve_forever(self):
        pass

def strip(string):
    return string.strip().replace(' ', '').replace('\n', '')

def assert_response(url, app, value):
    response = get_response(app, url.strip('\n '))
    result = strip(''.join(response))
    value = strip(value)
    assert result == value, "Response: %s does not match: %s" % (result, value)

def assert_printed(code, locals, value):
    out = StringIO()
    stdout = sys.stdout
    try:
        sys.stdout = out
        exec code in locals
    finally:
        sys.stdout = stdout
    result = strip(out.getvalue())
    value = strip(value)
    assert result == value, "Printed: %s does not match: %s" % (
        result, value)
