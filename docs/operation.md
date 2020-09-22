# `operation` proxy

Operation is a way to define injectable functions easily. This functions can
only call other dependencies and take no additional value arguments.

```pycon

>>> from dependencies import Injector, operation

```

## Call

Dependencies injected based on the arguments names.

```pycon

>>> class Container(Injector):
...     foo = 1
...     bar = 2
...     baz = 3
...
...     @operation
...     def func(foo, bar, baz):
...         return foo + bar + baz

>>> Container.func() == 6
True

```

If you want to pass additional value parameter to the function, add it to the
injector with the call.

```pycon

>>> class Foo:
...     def do(self, arg):
...         return arg + 3

>>> class Bar:
...     def do(self, arg):
...         return arg + 2

>>> class Container(Injector):
...     foo = Foo
...     bar = Bar
...
...     @operation
...     def func(foo, bar, arg):
...         return foo.do(bar.do(arg))

>>> Container(arg=1).func()
6

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
