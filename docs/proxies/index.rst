=========
 Proxies
=========

Dependencies provides some utilities to make working with injector
structure more pleasant and more declarative.

.. toctree::
    :maxdepth: 2

    this

``this`` gives you declarative access to neighbor dependencies,
attribute and item access.  ``this`` also has access to nested and
parent injectors.  Expressions defined with ``this`` are **lazy** and
will be evaluated during injection process.

For example, if there is a dependency ``foo`` which contains class
``Foo``, then dependency ``bar`` which contains ``this.foo.bar`` will
be resolved to the **bound** method ``bar`` of the ``Foo``
**instance**.

.. toctree::
    :maxdepth: 2

    operation
    package
