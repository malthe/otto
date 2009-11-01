from ..utils import make_environ

class make_server(object):
    def __init__(self, host, port, app):
        self.app = app

    def serve_forever(self):
        pass

def get_response(url, app):
    environ = make_environ(url.strip())
    def start_response(*args):
        pass
    return app(environ, start_response)

def assert_response(url, app, value):
    response = ''.join(get_response(url, app)).strip()
    value = value.strip()
    if response != value:
        raise Exception('Response: %s does not match: %s' % (response, value))
