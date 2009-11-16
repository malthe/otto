.. _mapping:

Mapping
=======

The publisher comes with support for object mapping; this is a class
or instance on the form::

  class Mapper(object):
      def resolve(self, path):
          """Return context given the path tuple."""

      def reverse(self, context):
          """Return path or path tuple."""

A mapper may be provided for a particular route (or routes), or set as
the default mapper by passing it to the publisher on instantiation.

It is only used on routes that include an anonymous asterisk, e.g.::

  /static/*

The ``reverse`` method is optional; only if it's implemented is the
``path`` method available on the route.

Traversal
---------

Object mapping can be used to implement traversal. This is a common
operation in object databases where path segments are resolved by
calling transitively calling the ``_getitem__`` method of the
traversed objects to get the next item.
