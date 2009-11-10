.. _traversal:

Traversal
=========

The publisher comes with support for traversal; this is a class or
instance on the form::

  class Traverser(object):
      @staticmethod
      def resolve(path):
          """Return context."""

      @staticmethod
      def reverse(context):
          """Return path."""

A traverser may be provided for a particular route (or routes), or set
as the default traverser by passing it to the publisher on
instantiation.

The ``reverse`` method is optional; only if it's implemented is the
``path`` method available on the route (which returns a path for that
route given data that matches the match dict).
