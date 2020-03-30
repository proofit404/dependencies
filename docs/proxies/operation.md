# `operation` proxy

Operation is a way to define injectable functions easily. This functions
can only call other dependencies and take no additional value arguments.

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

>>> assert Container.func() == 6

```

If you want to pass additional value parameter to the function, add it
to the injector with the `let` notation.

```pycon

>>> from examples.operation import Foo, Bar

>>> class Container(Injector):
...     foo = Foo
...     bar = Bar
...
...     @operation
...     def func(foo, bar, arg):
...         return foo.do(bar.do(arg))

>>> Container.let(arg=1).func()

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
