# Nested injectors

Nested injectors supposed to be used as targets for `this` objects.

## Restrictions

You can't resolve nested injectors as main target of dependency injection.

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...     class Nested(Injector):
...         foo = 1

>>> Container.Nested
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: 'Injector' dependencies could only be used to instantiate classes

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
