=========
 Proxies
=========

Dependencies provides some utilities to make working with injector
structure more pleasant and more declarative.

this
====

`this`_ gives you declarative access to neighbor dependencies,
attribute and item access.  `this`_ also has access to nested and
parent injectors.  Expressions defined with `this`_ are **lazy** and
will be evaluated during injection process.

For example, if there is a dependency ``foo`` which contains class
``Foo``, then dependency ``bar`` which contains ``this.foo.bar`` will
be resolved to the **bound** method ``bar`` of the ``Foo``
**instance**.

Contents
========

.. toctree::
    :maxdepth: 2

    this
    operation
    package

.. _this: this.html
