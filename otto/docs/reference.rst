.. _reference:

Reference
=========

.. automodule:: otto

  .. autoclass:: otto.Router

  .. autoclass:: otto.Publisher

  .. autoclass:: otto.Application


Routes
######

Match dictionary

  Expressions on the form ``:key`` match any string and passes the
  argument by name onto the controller. Examples::

    /search/:term
    /:category/:id

  Match keys must be valid Python variable names.

Asterix

  The asterisk character ("*") matches any path (non-greedy). If it's
  unnamed (not immediately followed by an identifier), the publisher
  calls the resolver function with the path and passes the result to
  the controller as the first argument (before the request
  argument). If it's named, it will be passed as keyword-argument to
  the controller::

    /*
    /*path
    /*/:version
    /documents/*

  Only one asterisk may be used for a single route.

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

    @app.route("/")
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
