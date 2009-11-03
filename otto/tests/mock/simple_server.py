from ..utils import get_response

class make_server(object):
    def __init__(self, host, port, app):
        self.app = app

    def serve_forever(self):
        pass

def assert_response(url, app, value):
    response = get_response(app, url)
    result = ''.join(response).strip().replace(' ', '')
    value = value.strip().replace(' ', '')
    assert result == value, "Response: %s does not match: %s" % (result, value)
