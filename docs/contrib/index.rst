=========
 Contrib
=========

This section of the documentation describes ``dependencies``
integration with third-party tools.  This allows to reduce boilerplate
you need to setup each time you want to connect your business logic to
the framework of your choice.

attrs
=====

`attrs`_ is an excellent python library and does not need any
integration code to work together with dependencies.  But usage of
this library is way more convenient than writing ``__init__`` methods
by hand.  So we decide decided to devote a whole documentation page to
describe best practices of `using attrs`_ together with dependencies.

Django
======

The most common place for Injector occurrence in the django project is
a view.  `Django`_ contrib allows you to add injector subclasses
directly to the url config.  Class-based and form handling views are
supported.

REST Framework
==============

`REST Framework`_ contrib works similarly to the django integration.
It allows you to define model view sets directly from your injectors,
add injector subclasses to the DRF routers and define low-lever API
views from your injectors.

Celery
======

When working with Celery distributed task queue it is a common
practice to access injector subclasses from your tasks.  `Celery`_
contrib allows you to define tasks directly from your injectors,
without the need to write intermediate task functions.  Regular and
shared tasks are supported.

Py.test
=======

Py.test is a state of art testing tool for Python.  `pytest`_ contrib
gives you an ability to define fixtures from injector subclasses.
Injection runs during test setup so you can inject results of other
fixtures as regular dependencies.

Contents
========

.. toctree::
    :maxdepth: 2

    attrs
    django
    rest_framework
    celery
    pytest

.. _attrs: http://www.attrs.org
.. _using attrs: attrs.html
.. _django: django.html
.. _rest framework: rest_framework.html
.. _celery: celery.html
.. _pytest: pytest.html
