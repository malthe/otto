Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object mapping and traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. We have tried to
incorporate elements of existing publishers to allow diverse and
flexible application patterns while still being in concordance with
the :term:`Zen Of Python`.

Examples of the routing syntax (the asterisk character matches any
path)::

  /*
  /*/edit
  /users/:id
  /users/:id/*
  /static/*static

The anonymous asterisk character denotes object mapping; this
facilitates an integration between the routing system and application
data which can be expressed as a model graph, e.g. an object database
like :mod:`ZODB`. To learn more about routes, see the reference on
:ref:`routing <routing>`.

Why?
----

To put it plainly, there is nothing new under the sun here. However,
this package exists for two reasons: simplicity and flexibility. The
existing packages in this problem space give you one without the
other.

**Simple**

  The routing syntax is clear and not cluttered with features. You
  can't capture variables with regular expressions. To illustrate this
  we take an example from the :mod:`Routes` package::

    # this is academic:
    connect(r'/blog/{year:\d+}/{month:\d+}/{id:\d+}')

  We opt for the simple version::

    # this is usually what you want:
    connect('/blog/:year/:month/:name')

  Type checking and conversion is done in the controller::

    def view_entry(request, year=None, month=None, name=None):
        try:
            year, month = int(year), int(month)
        except TypeError:
            return webob.Response(
                u"This request had errors: %s." % request.url)
        ...

  Not all problems can be aptly spelled using the routes
  syntax. Here's an example from the :mod:`bobo` framework which comes
  with its own routes-like syntax::

    @bobo.query(method='GET')
    def get(who='world'):
        ...

    @bobo.query(method='POST')
    def post(who='world'):
        ...

  It looks useful, but what's wrong with this::

    def both(request, who='world'):
        if request.method == 'POST':
          ...
        ...

  Most of the time you want to handle the ``POST`` data and then
  continue with the logic of the ``GET`` method. This needn't be
  managed using routes.

  And many properties of the HTTP environment require more than just
  an equality match.

**Flexible**

  There are essentially two kinds routes: fixed length and variable
  length. When you wire up the variable part with an *object mapper*,
  it's called the :term:`hybrid model`. This is an optional
  abstraction which maps path segments to an object -- often used for
  hierarchical data like that in a file system or object database.

  To illustrate, the following could be a route for a user's private
  files which are served over :term:`WebDAV`::

    /users/:id/*/edit

  Example: ``/users/john/private/darknet.txt``

  The asterisk matches any number of path segments, then invokes the
  object mapper. Because the ``id`` match comes before it, this value
  will be passed as keyword argument to the constructor::

    class Mapper(object):
        def __init__(self, id=None):
            ...

        def resolve(self, path):
            return PlainText(os.path.join(path))

  The ``resolve`` method gets a path tuple and returns any object; we
  use the term ``context``. Route controllers can decide to respond
  only to context objects of a certain type::

    @route.controller(type=PlainText)
    def edit(context, request)
        ...

  The ``type`` parameter is only valid for routes which use
  mapping. The controller does not get the ``id`` parameter since it
  was passed to the object mapper.

  Complex systems can use the object mapper abstraction to integrate
  security and other framework into the URL dispatch routine.

How it works
------------

The publisher is given an HTTP environment and returns an HTTP
response. It always returns a response.

When a request comes in, the publisher matches the ``PATH_INFO``
variable with the routing table to find exactly one route and extracts
the :term:`match dict`. In case no route matches, a ``404 Not Found``
response is returned. If the route contains an anonymous asterisk, a
:term:`context` object is resolved from the path represented by the
asterisk using an object mapper -- see :ref:`mapping <mapping>`. In
any case, the publisher invokes the first valid controller, passing
the match dict as keyword arguments.

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

  class Modules(object):
      """Maps paths to Python modules."""

      def resolve(self, path):
          name = '.'.join(path)
          __import__(name)
          return sys.modules[name]

      def reverse(self, module):
          return module.__name__.split('.')

  app = otto.Application(Modules)

  @app.connect("/")
  def frontpage(request):
      return webob.exc.HTTPForbidden(
          "What? Why did you ask that? What do you "
          "know about my image manipulator?")

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

