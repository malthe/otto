==================
Guiding principals
==================

Fun is important
================

I like creating things. Ever since I was a little kid I would spend
days on end building with Legos. For me programming is like having
an endless stream of Lego bricks in any size, shape and color I can
think of. That is why I got into it, I just wanted to play and have
fun!

You might have a different story. But I bet that, like I, you didn't
start coding for the money. Let's face it, there are probably more
effective ways of doing that. My guess would be that for some reason
or other you got to have fun when programming.

Fun, or lack thereof, is the main driver behind Otto. We wanted
to have a system which made web-development an enjoyable experience
again. Something which puts us in control instead of being
controlled.

Having fun gives energy, makes you more productive, happy and even
more healthy. So when faced with the choice of doing something, why
not pick the option that's more fun?

No conceptual baggage
=====================

Baggage is junk which you have to haul with you wherever you go. It
slows you down when traveling, makes your back hurt and exhausts you
faster. This is also true for conceptual baggage, which is baggage
you have to lug around in your mind.

That is why systems should try to avoid introducing radically new
concepts. A Python developer should not have to re-learn the
language because someone other than Guido introduced something new.

An example of conceptual baggage from the zope.interface
package. Can you guess what the `implements` call is going to do?::

class Foo(object):
    interface.implement(IFoo) # <-- What is this supposed to do?

Python just does not have a concept like a function call which
modifies something outside of it's normal scoping
rules. "Directives" like these just do not make sense and introduce
new conceptual baggage.

Frameworks suck, try to avoid them
==================================

Coding is about solving problems your way. Frameworks are about
requiring you to structure your code in their way. At one point your
way and the frameworks way will collide. What makes perfect sense to
you will be made impossible by the framework.

You then have to rethink your problem in terms the framework might
support, probably going as far as forgoing the optimal solution. The
force and restrictions a framework imposes on you, telling what you
can and cannot do, just sucks. It drains energy and creativity. It's
just not fun.

A way to handle this problem is by take note of a few possible (this
list is not exhaustive) guidelines:

- A framework is anything where you plug your code into

- Frameworks usually have globals, don't use them.

- Globals are only to be introduced by the developer of an
  application, not by a library or framework.

- Make it easy to alter behavior by using the object-oriented paradigms:

  - Sub-classing and overriding methods is a fine way to let people
    customize your code.

  - Favor delegation over sub-classing.

  - Put code in control by giving it all you can. This means that
    plug-ins should receive as much state as you can reasonably give
    them. Err on the side of giving to much, it's easier to ignore
    state then to make it magically appear when you need it.

 tip::

      Extend and replace before plugging in place. That which is
      passed around does not have to be globally bound.
