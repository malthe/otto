Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. In particular, it
tries to conform to the :term:`Zen Of Python`.

An example application which exposes all module globals over the open
wire:

.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  import webob.exc
  import wsgiref.simple_server

  app = otto.Application()

  # access to the home page is forbidden by this controller
  @app.route("/")
  def frontpage(request):
      raise webob.exc.HTTPForbidden(
          "What? Why did you ask that? What do you "
          "know about my image manipulator?")

  # for the next route we'll need a function which takes a path and
  # returns a Python-module; this is a route factory.
  def importer(path):
      name = path.replace('/', '.')
      return __import__(name)

  # the asterix matches any path; the last path segment is mapped to
  # the ``name`` keyword-argument
  @app.route("/*/:name", factory=importer)
  def representation(module, request, name=None):
      value = getattr(module, name)
      return webob.Response(repr(value))

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Let's try out this useful application::

  http://localhost:8080/

.. -> root_input

The route that matches this URL is connected to a controller which
raises an HTTP exception (the :mod:`WebOb` library provides exception
classes for standard response status codes) to signal that the request
is *forbidden*::

  403 Forbidden

  Access was denied to this resource.

  What? Why did you ask that? What do you know about my image
  manipulator?

.. -> denied_response

The ``math`` library contains a symbol ``pi``::

  http://localhost:8080/math/pi

.. -> pi_input

The controller simply computes the string representation and returns
it as the HTTP response body::

  3.1415926535897931

.. -> pi_response

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response(root_input.split('8080')[1], app, denied_response)
  >>> assert_response(pi_input.split('8080')[1], app, pi_response)

License
-------

This software is made available under the BSD license.

