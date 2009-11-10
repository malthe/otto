Security
========

There is no security model built into the publisher as such;
applications should make assertions using the exception classes from
the :mod:`WebOb` library, e.g.:

.. invisible-code-block: python

  >>> import otto
  >>> import webob.exc
  >>> import wsgiref.simple_server
  >>> app = otto.Application()

.. code-block:: python

  @app.route("/")
  def controller(request):
      if 'REMOTE_USER' not in request.environ:
          raise webob.exc.HTTPForbidden("Server not accessible.")
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

