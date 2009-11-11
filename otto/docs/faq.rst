.. _faq:

FAQ
===

**How do I set up virtual hosting?**

  The publisher does not come with built-in support for virtual
  hosting setups. You can use :mod:`paste.urlmap` to host your
  application at some subpath. This will set the ``SCRIPT_NAME``
  variable to the subpath and pass on the remaining path as the
  ``PATH_INFO``.

  For URL generation, you need to establish your application URL
  manually; the paths obtained using the ``path`` method of a route
  come after the application URL, e.g.::

    absolute_url = application_url + route.path(...)

  The ``application_url`` attribute of the :mod:`WebOb` request object
  returns the host including the script name. It never ends in a
  trailing slash.

**How do I control what the routes match?**

  It is not advertised, but the routes syntax allows for regular
  expression usage. Some examples:

  To traverse all URLs which ends in ``.txt`` we use positive
  look-ahead::

     /some/path/(?=.+\.txt)*

  Instead of ``+``, we can use ``\*``; the asterisk character must be
  escaped in this context (else it will be interpreted by the route
  compiler).

  We can use look-ahead assertions (both positive or negative) on the
  match dict segments too. The following matches only keys consisting
  of lowercase characters::

     /keys/(?=[a-z]+):key

  In general, these assertions are discouraged. It's usually better to
  inform the user that something was unexpected than return a ``404
  Not Found`` (which will be the response if no route matches).
