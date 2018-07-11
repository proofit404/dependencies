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

operation
=========

Sometimes you defined a class with two methods: ``__init__`` and
``__call__`` just to invoke its dependencies in a certain way.  If
this callable object doesn't accept any arguments, you can reduce this
class to the simple function with `operation`_ decorator.

Package
=======

`package`_ gives you an ability to point injector to the classes,
methods, functions and variables defined in the different places in
your code base without import statements.

Contents
========

.. toctree::
    :maxdepth: 2

    this
    operation
    package

.. _this: this.html
.. _operation: operation.html
.. _package: package.html
