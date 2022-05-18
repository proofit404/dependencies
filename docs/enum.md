# Enums

Since `Enum` definition keep enumeration itself a class we need to instantiate
it somehow. Even taking into consideration that enumeration classes are used as
constants most of the times, we can't make an exclusion in the rule that classes
should be instantiated. Members of enumeration are instancies of the enumeration
class itself. That's why we allow to use `Enum` members only in the dependency
injection scope.

```pycon

>>> from enum import Enum, auto, unique
>>> from dependencies import Injector

>>> @unique
... class Status(Enum):
...     new = auto()
...     accepted = auto()
...     processed = auto()
...     rejected = auto()
...     done = auto()

>>> class Order:
...     def __init__(self, status):
...         self.status = status
...
...     def __repr__(self):
...         return f"Order({self.status!r})"

>>> class Container(Injector):
...     order = Order
...     status = Status.new

>>> Container.order
Order(<Status.new: 1>)

```

In the mean time, we are strongly forbid usage `Enum` class itself inside
injection scope. `Injector` will raise an error if you try to define an
attribute with enumeration class in it.

```pycon

>>> class Container(Injector):
...     order = Order
...     status = Status

>>> Container.order
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Attribute 'status' contains Enum.
<BLANKLINE>
Do not inject enumeration classes.
<BLANKLINE>
It will be unable to instantiate this class.
<BLANKLINE>
Inject its members instead.

```

Using enumeration classes in class-named attributes are still allowed.

```pycon

>>> class Price:
...     def __init__(self, status_class):
...         self.status_class = status_class
...
...     def __repr__(self):
...         return f"Price({self.status_class!r})"

>>> class Container(Injector):
...     price = Price
...     status_class = Status

>>> Container.price
Price(<enum 'Status'>)

```

As you can see, no exception was raised above.

<p align="center">&mdash; ⭐ &mdash;</p>
