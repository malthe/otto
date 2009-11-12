Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. We have tried to
incorporate elements of existing publishers to allow diverse and
flexible application patterns while still being in concordance with
the :term:`Zen Of Python`.

Examples of the routing syntax (the asterisk character matches any path)::

  /*
  /*/edit
  /users/:id
  /users/:id/*subpath

The anonymous asterisk character denotes traversal; this facilitates
an integration between the routing system and application data which
can be expressed as a model graph, e.g. an object database like
:mod:`ZODB`. To learn more about routes, see the reference on :ref:`routing
<routing>`.

Why?
----

This package exists for three reasons: simplicity, flexibility and
scalability. An extensive survey of the existing packages that provide
similar functionality showed that you can choose between the first two
and never the third [#]_.

In general, a routing engine is tasked with mapping a request to view
code. Most engines provide this as library functionality. The
*publisher* is an abstraction which instead maps the request to an
object and then to view code which applies to that particular
object. This abstraction is usually implemented as framework
functionality. While it is often valid to phrase problems using a
framework, it opens a pandora's box of complexity and there are good
reasons to keep it closed.

With that in mind, all examples in this documentation are written
imperatively. There is no declarative configuration or other
indirection. This means you can copy and paste the code right into
your editor and start from there. There is also no inversion of
control. The code does exactly what you expect from it -- and no more.

.. [#] Some examples to back up this claim: `Bobo <http://bobo.digicool.com>`_ and `Bottle <http://bottle.paws.de/>`_ are simple, but not flexible. `Routes <http://routes.groovie.org/>`_ is flexible, but not simple. These are used by many other libraries and frameworks and cover most of the ground (conceptually, if not in terms of implementation). None of these scale -- requests are matched against routes one by one until a match is found. The engine used by the router in this package instead finds all matching routes in a single operation; it then extracts match information in a second operation. As a sidenote, the `Zope <http://www.zope.org/>`_ publisher is very flexible and very complex. It does not support the routes syntax.

How it works
------------

The publisher is given an HTTP environment and returns an HTTP
response. It always returns a response.

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

Example
-------

This example application exposes all module globals over the open
wire. It returns the Python string representation of the global which
is provided on the path, e.g. ``http://localhost:8080/math/pi``.

.. code-block:: python

  #!/usr/bin/env python2.6

  import sys
  import otto
  import webob.exc
  import wsgiref.simple_server

  class traverser:
      @staticmethod
      def resolve(segments):
          name = '.'.join(segments)
          __import__(name)
          return sys.modules[name]

      # not used in this example, but included for coherence
      @staticmethod
      def reverse(module):
          return module.__name__.split('.')

  app = otto.Application(traverser)

  # access to the home page is forbidden by this controller
  @app.connect("/")
  def frontpage(request):
      return webob.exc.HTTPForbidden(
          "What? Why did you ask that? What do you "
          "know about my image manipulator?")

  # the asterisk matches any path; the last path segment is mapped to
  # the ``name`` keyword-argument
  @app.connect("/*/:name")
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

The ``math`` library contains the ``pi`` symbol::

  http://localhost:8080/math/pi

.. -> pi_input

The response body to this request is the Python string representation::

  3.1415926535897931

.. -> pi_response

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response(root_input.split('8080')[1], app, denied_response)
  >>> assert_response(pi_input.split('8080')[1], app, pi_response)

If you are new to the library, the :ref:`getting started <tutorial>`
section begins with the *hello world* application and ends with the
present example.

License
-------

This software is made available under the BSD license.

