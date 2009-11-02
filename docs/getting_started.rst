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

  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response("/")).strip() == output.strip()
  True

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

  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response("/otto")).strip() == output.strip()
  True

Routes can use traversal [#]_ to walk an object graph from the path
segments which are then understood as names (or keys). This requires a
dictionary (or dictionary-like) root object (the requirement is to
provide the ``__getitem__`` method). To configure the router for
traversal, a *root factory* must be passed on initialization. This is
a callable which takes no arguments and returns the root object.

The snippet sets up three different kinds of objects for use with
traversal, creates a new application and adds a route which tries to
traverse any URL.

.. code-block:: python

  class Food(object):
      def __init__(self, name):
          self.name = name

  class Fruit(Food): pass
  class Vegetable(Food): pass
  class Meat(Food): pass

  banana = Fruit(u"Banana")
  carrot = Vegetable(u"Carrot")
  monkey = Meat(u"Monkey")

  root = {
     'banana': banana,
     'carrot': carrot,
     'monkey': monkey
     }

  app = otto.Application(lambda: root)

  @app.route("/*")
  def controller(food, request):
      return webob.Response(u"This is a %s." % food.name.lower())

If we visit `http://localhost:8080/banana`, we get::

  This is a banana.

.. -> output

  >>> wsgiref.simple_server.make_server('', 8080, app).serve_forever()
  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response("/banana")).strip() == output.strip()
  True

We can provide different controllers for different kinds of objects.

.. code-block:: python

  app = otto.Application(lambda: root)
  index = app.route("/*")

  @index.controller(type=Fruit)
  @index.controller(type=Vegetable)
  def like(food, request):
      return webob.Response(u"I like to eat %ss." % food.name.lower())

  @index.controller(type=Meat)
  def dislike(food, request):
      return webob.Response(u"I don't like to eat %ss." % food.name.lower())

If we visit `http://localhost:8080/banana` and the other object names,
respectively, we get::

  I like to eat bananas.
  I like to eat carrots.
  I don't like to eat monkeys.

.. -> output

  >>> wsgiref.simple_server.make_server('', 8080, app).serve_forever()
  >>> from otto.tests.mock.simple_server import get_response
  >>> responses = "".join(get_response("/banana")), \
  ...             "".join(get_response("/carrot")), \
  ...             "".join(get_response("/monkey"))
  >>> "\n".join(responses).strip() == output.strip()
  True

Traversal is good for hierarchical data, for instance that of an
object database or a file system.

.. [#] The act of descending “down” a graph of model objects from a root model in order to find a context.
