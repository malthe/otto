Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. In particular, it
tries to conform to the :term:`Zen Of Python`.

.. code-block:: python

  import otto
  import webob.exc
  import wsgiref.simple_server

  app = otto.Application()

  @app.route("/")
  def frontpage(request):
      raise webob.exc.HTTPForbidden(
          "What? Why did you ask that? What do you "
          "know about my image manipulator?")

  def importer(path):
      name = path.replace('/', '.')
      return __import__(name)

  @app.route("/*/:name", factory=importer)
  def representation(module, request, name=None):
      value = getattr(module, name)
      return webob.Response(repr(value))

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Let's try out this useful application::

  http://localhost:8080/
  http://localhost:8080/math/pi

.. -> input

We're first lead on to have a closer look::

  403 Forbidden

  Access was denied to this resource.

  What? Why did you ask that? What do you know about my image
  manipulator?

.. -> denied_response

And then::

  3.1415926535897931

.. -> pi_response

  >>> from otto.tests.mock.simple_server import assert_response
  >>> paths = [line.split('8080')[1] for line in input.splitlines()]
  >>> assert_response(paths[0], app, denied_response)
  >>> assert_response(paths[1], app, pi_response)

:mod:`Otto` works with Python 2.6 or newer.

License
-------

This software is made available under the BSD license.

