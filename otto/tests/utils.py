def make_environ(url):
    return {
        'PATH_INFO': url,
        'REQUEST_METHOD': 'GET'
        }

def get_response(app, url):
    env = make_environ(url)
    def start_response(*args):
        pass
    return app(env, start_response)
