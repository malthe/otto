Security
========

Most non-trivial applications require some form of security
system. Otto uses the concept of security assertions.


.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  from otto import exc
  import wsgiref.simple_server

  app = otto.Application()

  @app.route("/")
  def hello_world(environ, start_response):
      raise exc.Forbidden

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Blah blah

::

  Access was denied.

.. -> output

  >>> from otto.tests.mock.simple_server import assert_response
  >>> assert_response("/", app, output)


Checking during traversal
-------------------------

.. code-block:: python

  class Resource(object):
      def __init__(self, name):
          self.name = name

      def __getitem__(self, key):
          return Resource(key)

  root = Resource('root')

  app = otto.Application(lambda: root)

  @app.route("/*")
  def hello_world(context, environ, start_response):
      return context.name

  @app.on_traverse
  def check_not_world(context, environ, name):
      if name == 'world':
          raise exc.Forbidden

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

Let's request the following url.

::

  /hello

.. -> url

This just renders the controller.

::

  hello

.. -> output

  >>> assert_response(url, app, output)

Requesting a protected url will give a different result.

:: -> url

  /hello/world

.. -> url

This will output an error message.

::

  Access was denied.

.. -> output

  >>> assert_response(url, app, output)

