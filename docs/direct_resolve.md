# Direct resolve

## Why

Primary goal of `dependencies` library is making objects composition easier.
That's why we focus primary on object instantiation. We suppose you not gonna
use `Injector` as constant storage for example. This assumption leads us to the
conclusion that only attributes containing classes are useful to be resolved by
attribute access. This architectural limitation gives us ability to implement
interesting features like [Sticky scopes](./sticky.md).

## Principles

- [Classes are resolved by attribute access](#classes-are-resolved-by-attribute-access)
- [Scalar types could not be resolved directly](#scalar-types-could-not-be-resolved-directly)
- [Nested injectors could not be resolved directly](#nested-injectors-could-not-be-resolved-directly)
- [`@value` object could not be resolved directly](#value-object-could-not-be-resolved-directly)

### Classes are resolved by attribute access

When we speak about resolving dependencies that mean client code (interactive
python console in our case) would use attribute access on `Injector` subclass.
In some sense you could think of this as access of external code.

```pycon

>>> from dependencies import Injector

>>> class User:
...     def __init__(self, name):
...         self.name = name
...
...     def __repr__(self):
...         return f"User({self.name=!r})"

>>> class Container(Injector):
...     user = User
...     name = "Jeff"

>>> Container.user
User(self.name='Jeff')

```

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

### Nested injectors could not be resolved directly

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

### `@value` object could not be resolved directly

You can't resolve value objects as main target of dependency injection. The main
goal of `value` objects is to be evaluated dependencies for classes.

```pycon

>>> from dependencies import Injector, value

>>> class Container(Injector):
...     @value
...     def foo():
...         return 1

>>> Container.foo
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: 'value' dependencies could only be used to instantiate classes

```

<p align="center">&mdash; ⭐ &mdash;</p>
