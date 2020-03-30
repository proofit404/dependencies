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

>>> from examples.users.utils import create_user
>>> # A lot of import statements here...

>>> class Container(Injector):
...     persist_user = create_user
...     # A lot of assignment statements here...

```

To save some typing I tend to write this code like this

```pycon

>>> class Container(Injector):
...     from examples.users.utils import create_user as persist_user
...     # A lot of import statements here...

```

`Package` can help to deal with this inconsistency

```pycon

>>> examples = Package("examples")

>>> class Container(Injector):
...     persist_user = examples.users.utils.create_user
...     # A lot of assignment statements here...

```

If a lot of dependencies defined in the utils module, you can set
`Package` source to the utils module itself.

```pycon

>>> utils = Package("examples.users.utils")

>>> class Container(Injector):
...     persist_user = utils.create_user
...     # A lot of assignment statements here...

```

## Classes

If an attribute of the `Package` object point to the attribute of the
class defined in some module, this class will be instantiated before
attribute access is actually happen. You can inject bound methods with
exactly one line.

```pycon

# examples/utils.py

>>> class Foo:
...
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...
...     def do(self):
...         return self.a + self.b

# examples/base.py

>>> utils = Package("examples.utils")

>>> class Container(Injector):
...     foo = utils.Foo.do
...     a = 1
...     b = 2

>>> assert Container.foo() == 3

```

The injector definition above is equivalent to the longuer version:

```pycon

>>> from dependencies import this
>>> from examples.utils import Foo

>>> class Container(Injector):
...     foo = this.tmp.do
...     tmp = Foo
...     a = 1
...     b = 2

>>> assert Container.foo() == 3

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
