.. _tutorial:

Getting started
===============

An application can be as simple as a Python script. This example will
serve up the *hello world* application.

.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  import webob
  import wsgiref.simple_server

  app = otto.Application()

  @app.route("/")
  def hello_world(request):
      return webob.Response(u"Hello world!")

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Start the application server by running the script from your shell::

$ chmod +x hello_world.py
$ ./hello_world.py

This serves up the application on ``http://localhost:8080``.

::

  Hello world!

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)

We can extract values from the path using ``:key`` notation. This
works on any path segment and returns a unicode string value which is
passed as keyword argument to the controller function.

To continue our example application, we'll add a route which will
return a personal greeting:

.. code-block:: python

  @app.route("/:name")
  def hello_name(request, name=None):
      return webob.Response(u"Hello %s!" % name.capitalize())

If we visit ``http://localhost:8080/otto``, we get::

  Hello Otto!

.. -> output

  >>> assert_response("/otto", app, output)

The ``hello_name`` variable now refers to the route (since the
function was decorated using ``app.route``). We can get to the
controller by using its ``bind`` method:

.. code-block:: python

  controller = hello_name.bind()
  print controller(None, name=u"Otto")

.. -> code

As expected, this calls the controller and prints the greeting::

  200 OK
  Content-Type: text/html; charset=UTF-8
  Content-Length: 11

  Hello Otto!

.. -> output

  >>> from otto.tests.mock.simple_server import assert_printed
  >>> assert_printed(code, locals(), output)

Given a route, we can ask for a path. If the route keyword matching,
those keywords must be passed in as well:

.. code-block:: python

  print hello_name.path(name=u"Otto")

.. -> code

  /Otto

.. -> output

  >>> assert_printed(code, locals(), output)

Routes can include the asterisk character to match any number of path
segments in a non-greedy way. The path is passed to the traverser's
``resolve`` method [#]_ and the result is passed to the controller as
the first argument.

The following example exposes the module globals of the Python process
on the open wire (responses are given by the representation string of
the object):

.. code-block:: python

  import sys

  class traverser:
      @staticmethod
      def resolve(segments):
          name = '.'.join(segments)
          __import__(name)
          return sys.modules[name]

      @staticmethod
      def reverse(module):
          return module.__name__.split('.')

  app = otto.Application(traverser)

  @app.route("/repr/*/:name")
  def expose(module, request, name=None):
      obj = getattr(module, name)
      return webob.Response(repr(obj))

If we visit ``http://localhost:8080/repr/math/pi``, we get::

  3.1415926535897931

.. -> output

  >>> assert_response("/repr/math/pi", app, output)

We can ask the route to generate a path given a dictionary which
matches the route's match dict expectations, and in this case, a
context for the traverser.

To separate out route paths from library code (such that library
needn't be explicitly aware of routing configuration):

.. code-block:: python

  import math
  print expose.path(math, name=u"pi")

.. -> code

  /repr/math/pi

.. -> output

  >>> assert_printed(code, locals(), output)

We can define controllers by the type of the object returned by the
resolver.

.. code-block:: python

  index = app.route("/docs/*")

  @index.controller(type=str)
  def doc(module, request):
      return webob.Response(unicode(module.__doc__))

If we visit ``http://localhost:8080/docs/hotshot/stats`` we get::

  Statistics analyzer for HotShot.

.. -> output

  >>> assert_response("/docs/hotshot/stats", app, output)

.. [#] An example of such a resolver is a function which descends “down” a graph of model objects in order to find a context, using e.g. ``__getitem__``. Traversal is good for hierarchical data, for instance that of an object database or a file system.

This concludes the introduction. See :ref:`frequently asked questions
<frequently_asked_questions>` for solutions to common problems.

