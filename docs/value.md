# `value` proxy

Value proxy is a way to execute code **during** dependency injection process.
Result of the function will be provided as a dependency for other attributes in
the `Injector` subclass.

## Example

```pycon

>>> from dependencies import Injector, value

>>> class Container(Injector):
...     foo = 1
...     bar = 2
...     baz = 3
...
...     @value
...     def quiz(foo, bar, baz):
...         return foo + bar + baz

>>> Container.quiz
6

```

## Depending on result of the proxy

```pycon

>>> class Foo:
...     def __init__(self, quiz):
...         self.quiz = quiz

>>> class Bar:
...     def __init__(self, quiz):
...         self.quiz = quiz

>>> class Baz:
...     def __init__(self, foo, bar):
...         self.foo = foo
...         self.bar = bar

>>> class Container(Injector):
...     foo = Foo
...     bar = Bar
...     baz = Baz
...
...     @value
...     def quiz():
...         print('value executed')
...         return 3

>>> baz = Container.baz
value executed

>>> baz.foo.quiz
3

>>> baz.bar.quiz
3

```

As you can see `@value` decorated function was called only once even two objects
depends on it.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
