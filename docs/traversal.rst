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
  >>> res = get_response(url, app)
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
  >>> res = get_response(url, app)
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

  >>> res = get_response(url, app)
  >>> repr(planet_log) == output.strip()
  True

Overriding
----------

It is possible to override the default behaviour by creating a custom
application. During traversal the `traverse_event` is called.


.. code-block:: python

  root = {'hello': {'world': 'Earth'}}

  class MyApp(otto.Application):
      my_events = []
      def traverse_event(self, context, environ, segment):
          self.my_events.append('Event: %s' % segment)

  app = MyApp(lambda: root)

  @app.route("/*")
  def hello_world(context, environ, start_response):
      return 'Hello World'

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

::

  /hello/world

.. -> url

This creates the events directly. Since we do not call the super we
will not activate any handlers.

::

  ['Event: hello', 'Event: world']

.. -> output

  >>> res = get_response(url, app)
  >>> repr(app.my_events) == output.strip()
  True
