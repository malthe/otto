Changes
=======

1.2 (2009-11-16)
----------------

Features
########

- Route matches that come before object mapping are passed on to the
  mapper on instantiation; these matches are then not passed to the
  controller.

Backwards incompatibilities
###########################

- The object mapper takes the place of the *traverser*; on
  instantiation it gets the part of the match dictionary that comes
  before the asterisk.

- The empty asterisk is now mapped to the empty string. This does not
  change the high-level interface.

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
