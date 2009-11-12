Security
========

There is no security model built into the publisher as such;
applications should return instances of the exception response classes
from the :mod:`WebOb` library (on Python 2.5+ ``raise`` may be used):

.. invisible-code-block: python

  >>> import otto
  >>> import webob.exc
  >>> import wsgiref.simple_server
  >>> app = otto.Application()

.. code-block:: python

  @app.connect("/")
  def controller(request):
      if 'REMOTE_USER' not in request.environ:
          return webob.exc.HTTPForbidden("Server not accessible.")
      return webob.Response(u"Welcome, %s!" % request.environ['REMOTE_USER'])

.. invisible-code-block: python

  >>> wsgiref.simple_server.make_server('', 8080, app).serve_forever()

If we browse to ``http://localhost:8080/`` we get::

  403 Forbidden

  Access was denied to this resource.

  Server not accessible.

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)

