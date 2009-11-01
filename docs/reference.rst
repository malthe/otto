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
  publisher traverses this path by obtaining a root object from the
  root factory and processing each path segment by calling the
  ``__getitem__`` method on each object. Examples::

    /*
    /*/:version
    /documents/*

  When an asterix is used in a route path, the traversed object is
  passed on to the controller as the first argument.

  Only one asterix may be used for a single route.

Object type

  The ``type`` parameter may be used on controllers in combination
  with traversal. When a class is passed as the value, the controller
  is only used if the required type is present in its class hierarchy
  (including the class itself). Example::

    @index.controller('/', type=Document)
    def view(context, *args):
        ...
