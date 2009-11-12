import mock.simple_server

try:
    import wsgiref.simple_server
    wsgiref.simple_server = mock.simple_server
except ImportError: # pragma no cover
    import sys
    sys.modules['wsgiref'] = mock
