Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. We have tried to
incorporate elements of existing publishers to allow diverse and
flexible application patterns while still being in corcordance with
the :term:`Zen Of Python`.

Examples of the routing syntax (the asterisk character matches any path)::

  /*
  /*/edit
  /users/:id
  /users/:id/*subpath

When a request comes in, the publisher matches the ``PATH_INFO``
variable with the routing table to find exactly one route and extracts
the :term:`match dict`. In case no route matches, a ``404 Not Found``
response is returned. If the route contains a lone asterisk, a
:term:`context` object is resolved from the path represented by the
asterisk using a route traverser -- see :ref:`traversal
<traversal>`. In any case, the publisher invokes the first valid
controller, passing the match dict as keyword arguments.

  request ⇾ *routing table* ⇾ route ⇾ *controllers* ⇾ controller

There can be several controllers defined for a single route; each will
then specify one or more :ref:`predicates <reference>`. Like routes,
controllers are looked up in order of definition. The first valid
controller is used.

An example application which exposes all module globals over the open
wire:

.. code-block:: python

  #!/usr/bin/env python2.6

  import sys
  import otto
  import webob.exc
  import wsgiref.simple_server

  # we resolve request paths by defining a traverser; for now, we only
  # implement the ``resolve`` method -- for reverse lookups we'd also
  # have to define the ``reverse`` method (which takes an object).
  class traverser:
    @staticmethod
    def resolve(path):
        name = path.replace('/', '.')
        __import__(name)
        return sys.modules[name]

  app = otto.Application(traverser)

  # access to the home page is forbidden by this controller
  @app.route("/")
  def frontpage(request):
      raise webob.exc.HTTPForbidden(
          "What? Why did you ask that? What do you "
          "know about my image manipulator?")

  # the asterisk matches any path; the last path segment is mapped to
  # the ``name`` keyword-argument
  @app.route("/*/:name")
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

