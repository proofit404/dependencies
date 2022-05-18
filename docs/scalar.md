# Scalar types

Scalar types like integer, floats, lists, or dictionaries could be used as
dependencies for classes. But scalar types can't be resolved directly from
attribute access.

```pycon

>>> from dependencies import Injector

>>> class Foo:
...     def __init__(self, bar):
...         self.bar = bar
...
...     def __repr__(self):
...         return f"Foo(bar={self.bar})"

>>> class Container(Injector):
...     foo = Foo
...     bar = 1

>>> Container.foo
Foo(bar=1)

>>> Container.bar
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Scalar dependencies could only be used to instantiate classes

```

<p align="center">&mdash; ⭐ &mdash;</p>
