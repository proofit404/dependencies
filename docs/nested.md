# Nested injectors

Nested injectors supposed to be used as targets for `this` objects.

## Restrictions

Your classes can't depend on nested `Injector` as it's arguments. Nested
injectors are supposed to be accessed only by `this` objects.

```pycon

>>> from dependencies import Injector

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
