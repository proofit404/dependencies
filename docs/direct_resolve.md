# Direct resolve

## Why

## Principles

- [Scalar types could not be resolved directly](#scalar-types-could-not-be-resolved-directly)

### Scalar types could not be resolved directly

Scalar types like integer, floats, lists, or dictionaries could be used as
dependencies for classes. But scalar types can't be resolved directly from
attribute access.

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...     integer = 1

>>> Container.integer
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Scalar dependencies could only be used to instantiate classes

```

<p align="center">&mdash; ⭐ &mdash;</p>
