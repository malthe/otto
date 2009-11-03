Traversal
=========

Traversal is the act of descending “down” a graph of model objects
from a root model in order to find a context.

Event
-----

After each traversal step, the ``on_traverse`` event is
triggered. Example applications include logging and security
assertions.

This example logs all traversal steps.

.. code-block:: python

  #!/usr/bin/env python2.6

  import otto
  import webob.exc
  import wsgiref.simple_server

  # content hierarchy
  root = {
    "some": {
       "path": u"Hello world!"
       }
    }

  app = otto.Application(lambda: root)

  @app.route("/*")
  def hello_world(context, request):
      return webob.Response(context)

  log = []

  @app.on_traverse
  def log_any(context, name):
      log.append(name)

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

If we request the URL ``http://localhost:8080/some/path``, the
traversed path have been logged to the list.

::

  ['some', 'path']

.. -> output

  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response(app, "/some/path"))
  'Hello world!'
  >>> repr(log) == output.strip()
  True

The ``on_traverse`` decorator accepts a ``type`` parameter; the event
handler is only called if the type matches the traversal context.

.. invisible-code-block: python

  >>> del log[:]

.. code-block:: python

  @app.on_traverse(type=unicode)
  def log_unicode(context, name):
      log.append(context)

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

The ``log_unicode`` handler is called before the general handler since
it's more specialized.

::

  ['some', u'Hello world!', 'path']

.. -> output

  >>> from otto.tests.mock.simple_server import get_response
  >>> "".join(get_response(app, "/some/path"))
  'Hello world!'
  >>> repr(log) == output.strip()
  True

