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

  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response("/")).strip() == output.strip()
  True


