Overview
========

Otto is an HTTP publisher which uses a routes-like syntax to map URLs
to code. It supports object traversal.

You can use the publisher to write web applications. It was designed
with both small and large applications in mind. We have tried to
incorporate elements of existing publishers to allow diverse and
flexible application patterns while still being in concordance with
the :term:`Zen Of Python`.

Here's a variation of a familiar theme::

  import otto
  import webob
  import wsgiref.simple_server

  app = otto.Application()

  @app.connect("/*path/:name")
  def hello_world(request, path=None, name=u'world'):
      return webob.Response(u"An %d-deep hello %s!" % (len(path), name))

  wsgiref.simple_server.make_server('', 8080, app).serve_forever()

This release is compatible with Python 2.4+.

See the `documentation <http://www.ottohttp.org/docs/1.1/>`_ for this release.

