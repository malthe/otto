.. _usersguide:

User's Guide
============

This section is a guide on how to write web applications using this
library.

Philosophy
----------

In not being a framework, but a library, projects begin with an empty
module and a copy-paste of the *hello world* application. The
objective is to embrace the empty module and avoid the pitfalls
inherent to development outside a framework.

    *I like to create things. As a kid I would spend days building
    with Lego bricks. Programming is like an endless stream of bricks
    of every size, shape and color; that is why I got into it, to play
    and have fun!* - Jeroen Vloothuis

The library was built from the experience of working with various
other libraries and frameworks, or rather, because of it. Many lessons
learned have inspired its design, which adheres to the following
principles:

**Must be fun**

    It means never having to say you're sorry.

**It's your code**

    It's inherent to frameworks to take over control.

    Programming is about solving problems. Frameworks are about
    spelling the solution in the language of the framework and then
    hand over control. Sometimes it's a perfect fit, but often enough
    it's a poor fit or an outright bad fit. Everything's a compromise,
    but it becomes a compromise more quickly when you're using a
    framework that's not an optimal fit.

    Warning signs:

    - Plugins

    - Globals

**Few dependencies**

    Conceptual baggage wears you out.

    Python has enough concepts of its own. It's tempting to introduce
    new playing rules, but in the long term, conceptual baggage incurs
    bitrot.

    An example from :mod:`zope.interface`::

     class Foo(object):
         zope.interface.implements(IFoo)

    What is this code supposed to do? It's not obvious from this
    snippet. Python does not provide a reference to a class while it's
    still being defined.

    We have tried to weed out all dependencies which aren't absolutely
    necessary such that you can decide which code to depend on.

**Use the right abstractions**

    Python is an object-oriented language. With the right abstractions
    in place, this paradigm makes it easy to reuse existing code.

