Traversal
=========


Events
------

A traversal event is triggered for each step in the traversal
process. This makes it easy to add security checks or logging etc.

.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  from otto import exc
  import wsgiref.simple_server

  root = {'hello': {'world': 'Earth'}}

  app = otto.Application(lambda: root)

  @app.route("/*")
  def hello_world(context, environ, start_response):
      return 'Hello ', context

  my_log = []

  @app.on_traverse
  def handle_traverse(context, environ, name):
      my_log.append(name)

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Let's request the following url.

::

  /hello/world

.. -> url

The log now has entries for each step.

::

  ['hello', 'world']

.. -> output

  >>> from otto.tests.mock.simple_server import get_response
  >>> res = get_response(url.strip())
  >>> repr(my_log) == output.strip()
  True

A common use-case is to filter on type. This is support by the system
directly.

.. code-block:: python

  app = otto.Application(lambda: root)

  class Greeting(object): pass
  class Planet(object): pass

  root = {'hello': Greeting(), 'world': Planet()}

  @app.route("/*")
  def hello_world(context, environ, start_response):
      return 'Hello ', str(context)

  planet_log = []

  @app.on_traverse(type=Planet)
  def planet_traverse(context, environ, name):
      planet_log.append(name)

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

::

  /hello

.. -> url

There is nothing in the log since the type did not match.

::

  []

.. -> output

  >>> from otto.tests.mock.simple_server import get_response
  >>> res = get_response(url.strip())
  >>> repr(planet_log) == output.strip()
  True

Requesting the url that matches a planet will trigger the planet
logger.

::

  /world

.. -> url

::

  ['world']

.. -> output

  >>> from otto.tests.mock.simple_server import get_response
  >>> res = get_response(url.strip())
  >>> repr(planet_log) == output.strip()
  True
