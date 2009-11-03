.. _syntax:

Reference
=========

Routes
------

Match dictionary

  Expressions on the form ``:key`` match any string and passes the
  argument by name onto the controller. Examples::

    /search/:term
    /:category/:id

  Match keys must be valid Python variable names.

Traversal

  The asterix character ("*") matches any path (non-greedy). The
  publisher calls the route factory with the path and passes the
  result to the controller as the first argument (before the request
  argument).

    /*
    /*/:version
    /documents/*

  Only one asterix may be used for a single route.

Object type

  The ``type`` parameter may be used to define a controller which is
  only available for a particular type. It's only available for routes
  which use the asterix character. Example::

    @index.controller('/', type=Document)
    def view(context, *args):
        ...
