Changes
=======

1.1 (2009-11-12)
----------------

Features
########

- The leading slash is now optional in a route path definition.

- The ``Route`` class now provides the ``match`` method.

Backwards incompatibilities
###########################

- The ``Publisher.route`` method was renamed to ``connect``. This
  method now takes a route object. This change was also applied for
  the ``Router`` class.

1.0 (2009-11-12)
----------------

- Initial public release.
