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

This serves up the application on `http://localhost:8080`.

::

  Hello world!

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)

We can extract values from the path using ``:key`` notation. This
works on any path segment and returns a unicode string value which is
passed as keyword argument to the controller function.

To continue our example application, we'll add a route which will
return a personal greeting.

.. code-block:: python

  @app.route("/:name")
  def hello_name(request, name=None):
      return webob.Response(u"Hello %s!" % name.capitalize())

If we visit `http://localhost:8080/otto`, we get::

  Hello Otto!


.. -> output

  >>> assert_response("/otto", app, output)

Routes can include the asterix character to match any number of path
segments in a non-greedy way. The path is passed to the *route
factory* callable [#]_ and the result is passed to the controller as
the first argument.

.. code-block:: python

  import sys

  def importer(path):
      name = path.replace('/', '.')
      __import__(name)
      return sys.modules[name]

  app = otto.Application(importer)

  @app.route("/repr/*/:name")
  def controller(module, request, name=None):
      obj = getattr(module, name)
      return webob.Response(repr(obj))

If we visit `http://localhost:8080/repr/math/pi`, we get::

  3.1415926535897931

.. -> output

  >>> assert_response("/repr/math/pi", app, output)

We can define controllers by the type of the object returned by the
factory.

.. code-block:: python

  index = app.route("/docs/*")

  @index.controller(type=str)
  def doc(module, request):
      return webob.Response(unicode(module.__doc__))

If we visit `http://localhost:8080/docs/hotshot/stats` we get::

  Statistics analyzer for HotShot.

.. -> output

  >>> assert_response("/docs/hotshot/stats", app, output)

.. [#] An example of such a factory is a traverser which descends
.. “down” a graph of model objects in order to find a
.. context. Traversal is good for hierarchical data, for instance that
.. of an object database or a file system.

