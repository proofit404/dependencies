# `Package` proxy

`Package` object is a way to define injector scope with dependencies
defined in other places (like modules and packages). You can point
package object to the module, a variable defined in the module, a
function defined in the module, a class defined in the module, any
attribute of the class which was defined in this module.

```pycon

>>> from dependencies import Injector, Package

```

## Attributes

A usual use case for the `Package` object is to replace havy import
statements with attribute access.

If you have complex project structure, you will see a lot of code like
this in your injectors.

```pycon

>>> from app.repositories import create_user
>>> # A lot of import statements here...

>>> class Container(Injector):
...     persist_user = create_user
...     # A lot of assignment statements here...

```

To save some typing I tend to write this code like this

```pycon

>>> class Container(Injector):
...     from app.repositories import create_user as persist_user
...     # A lot of import statements here...

```

`Package` can help to deal with this inconsistency

```pycon

>>> app = Package("app")

>>> class Container(Injector):
...     persist_user = app.repositories.create_user
...     # A lot of assignment statements here...

```

If a lot of dependencies defined in the repositories module, you can
set `Package` source to the repositories module itself.

```pycon

>>> repositories = Package("app.repositories")

>>> class Container(Injector):
...     persist_user = repositories.create_user
...     # A lot of assignment statements here...

```

## Classes

If an attribute of the `Package` object point to the attribute of the
class defined in some module, this class will be instantiated before
attribute access is actually happen. You can inject bound methods with
exactly one line.

```pycon

# app/calc.py

>>> class Calc:
...
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...
...     def do(self):
...         return self.a + self.b

# app/base.py

>>> calc = Package("app.calc")

>>> class Container(Injector):
...     foo = calc.Calc.do
...     a = 1
...     b = 2

>>> assert Container.foo() == 3

```

The injector definition above is equivalent to the longuer version:

```pycon

>>> from dependencies import this
>>> from app.calc import Calc

>>> class Container(Injector):
...     foo = this.tmp.do
...     tmp = Calc
...     a = 1
...     b = 2

>>> assert Container.foo() == 3

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
