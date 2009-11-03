Overview
========

Otto uses a routes-like syntax to map URLs to code and supports
object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. The documentation
includes a tutorial and examples which show how to solve common
problems.

.. code-block:: python

  import otto
  import webob
  import wsgiref.simple_server

  app = otto.Application()

  @app.route("/")
  def hello_world(request):
      return webob.Response(u"Hello world!")

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

This starts an application server which serves the *hello world*
application on ``http://localhost:8080``.

::

  Hello world!

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)

:mod:`Otto` works with Python 2.6 or newer.

License
-------

This software is made available under the BSD license.

