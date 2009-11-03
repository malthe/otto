Security
========

There is no security model built into the publisher; applications
should make assertions using the exception classes from the
:mod:`WebOb` library.

An example:

  >>> import otto
  >>> import webob.exc
  >>> import wsgiref.simple_server
  >>> app = otto.Application()

.. code-block:: python

  @app.route("/")
  def controller(request):
      raise webob.exc.HTTPForbidden("Server not accessible.")

  >>> wsgiref.simple_server.make_server('', 8080, app).serve_forever()

If we browse to ``http://localhost:8080/`` we get::

  403 Forbidden

  Access was denied to this resource.

   Server not accessible.

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)

