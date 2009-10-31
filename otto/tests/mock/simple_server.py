from ..utils import make_environ

servers = []

class make_server(object):
    def __init__(self, host, port, app):
        self.app = app

    def serve_forever(self):
        servers.append(self)

def get_response(url):
    app = servers[-1].app
    environ = make_environ(url)
    def start_response(*args):
        pass
    return app(environ, start_response)
