.. _reference:

Reference
=========

.. _routing:

Routes
######

Match dictionary

  Expressions on the form ``:key`` match any string and passes the
  argument by name onto the controller. Examples::

    /search/:term
    /:category/:id

  Match keys must be valid Python variable names.

  Note that all values are returned as unquoted unicode strings.

Asterix

  The asterisk character ("*") matches any number of path segments
  (non-greedy).

  If it's named (e.g. ``*foo``), it will be passed by keyword argument
  to the controller.

  An unnamed asterisk (not immediately followed by an identifier) will
  invoke the the traverser. The publisher calls the traverser's
  ``resolve`` method with the path segments (a tuple) and passes the
  result to the controller as the first positional argument (before
  the request argument).

  Examples of routes which use the asterisk::

    /*
    /*path
    /*/:version
    /documents/*

  It is invalid to use more than one asterisk in a route path. Note
  that the asterisk may be escaped using the backslash character,
  e.g. ``\*``.

Trailing slash

  These URLs often indicate a container-like object. Although the two
  spellings are fungible in the eyes of a web browser, applications
  should not allow two same documents be returned from different URLs
  (for both caching and SEO reasons). One variant should redirect to
  the other -- ``301 Redirect``.

  The router comes with support for such redirection. We can
  demonstrate it with a trivial example:

  .. invisible-code-block:: python

    >>> from otto import Application
    >>> app = Application()

  .. code-block:: python

    @app.connect("/")
    def controler(request):
        return webob.Response(u"Hello world!")

  .. -> code

    >>> exec(code)

  If we visit the application without a trailing slash,
  e.g. ``http://localhost``, we should get redirected to the URL that
  does end in a trailing slash::

    301 Moved Permanently
    Content-Type: text/html; charset=UTF-8
    Content-Length: 0
    location: http://localhost/

  .. -> output

    >>> import webob
    >>> request = webob.Request.blank("")
    >>> response = app.publish(request.environ)
    >>> str(response).strip() == output.strip()
    True
    >>> request = webob.Request.blank("/not-exists")
    >>> response = app.publish(request.environ)
    >>> '404' in response.status
    True

  The browser will follow the redirect to ``http://localhost/``::

    200 OK
    Content-Type: text/html; charset=UTF-8
    Content-Length: 12

    Hello world!

  .. -> output

    >>> request = webob.Request.blank("/")
    >>> response = app.publish(request.environ)
    >>> str(response).strip() == output.strip()
    True

Path generation

  The ``path`` method of the route object returns a path given keyword
  arguments. If traversal is used on the route, the path segment
  tuple should be provided either as the first positional argument
  (for an unnamed asterisk), or by keyword argument.

  Note that for asterisk arguments, either a path segment tuple or
  string may be provided.

  All values should be unicode. The result of the ``path`` method is
  always a quoted string.

Controllers
###########

.. _predicates:

Type

  The ``type`` parameter may be used to define a controller which is
  only available for a particular type. It's only available for routes
  which use the asterisk character. Example::

    @index.controller('/', type=Document)
    def view(context, request):
        ...

API
###

.. automodule:: otto

  .. autoclass:: otto.Application
     :show-inheritance:

     .. automethod:: __call__

     .. automethod:: publish

  .. autoclass:: otto.Publisher

     .. automethod:: __init__

     .. automethod:: connect

     .. automethod:: match

  .. autoclass:: otto.Router

     .. automethod:: __call__

     .. automethod:: connect

  .. autoclass:: otto.Route

     .. automethod:: __init__

     .. method:: match(path)

        Match the ``path`` against the route. Returns a match
        dictionary or ``None``.

     .. automethod:: path

.. automodule:: otto.publisher

  .. autoclass:: otto.publisher.Dispatcher
     :show-inheritance:

     .. automethod:: __init__

     .. automethod:: bind

     .. automethod:: controller

     .. automethod:: path
