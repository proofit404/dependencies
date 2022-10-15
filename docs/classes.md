# Classes

## Principles

- [Positional-only constructor arguments are forbidden](#positional-only-constructor-arguments-are-forbidden)

### Positional-only constructor arguments are forbidden

At the moment `dependencies` library use `**kwargs` expansion to pass arguments
into class constructor.
[Positional-only parameters](#https://peps.python.org/pep-0570/) introduced in
python 3.8 broke this pattern. We have no plan to support this corner case in
`dependencies` core `Injector` algorithm.

```pycon

>>> from dependencies import Injector

>>> class User:
...     def __init__(self, /, name):
...         self.name = name
...
...     def __repr__(self):
...         return f"User({self.name=!r})"

>>> User("Jeff")
User(self.name='Jeff')

>>> class Container(Injector):
...     user = User
...     name = "Jeff"

>>> Container.user
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: 'User.__init__' have positional-only arguments

```

<p align="center">&mdash; ⭐ &mdash;</p>
