.. _traversal:

Traversal
=========

The publisher comes with support for traversal; this is a class or
instance on the form::

  class Traverser(object):
      @staticmethod
      def resolve(segments):
          """Return context."""

      @staticmethod
      def reverse(context):
          """Return path or path segments."""

A traverser may be provided for a particular route (or routes), or set
as the default traverser by passing it to the publisher on
instantiation.

It is only used on routes that include an unnamed asterisk, e.g.::

  /static/*

The ``reverse`` method is optional; only if it's implemented is the
``path`` method available on the route.
