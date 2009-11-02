def make_environ(url):
    return {
        'PATH_INFO': url,
        'REQUEST_METHOD': 'GET'
        }

def get_response(app, url):
    environ = make_environ(url.strip())
    def start_response(*args):
        pass
    return app(environ, start_response)
