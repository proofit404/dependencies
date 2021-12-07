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

Your classes can't depend on nested `Injector` as it's arguments. Nested
injectors are supposed to be accessed only by `this` objects.

```pycon

>>> class Foo:
...     def __init__(self, Bar):
...         self.baz = Bar.baz

>>> class Container(Injector):
...     foo = Foo
...
...     class Bar(Injector):
...         baz = 1

>>> Container.foo
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Do not depend on nested injectors directly.
<BLANKLINE>
Use this object to access inner attributes of nested injector:
<BLANKLINE>
Container.foo

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
