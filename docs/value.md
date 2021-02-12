# `value` object

Value object gives you the way to execute code **during** dependency injection
process.

If dependency injection process needs to resolve value object, a decorated
function will be called. Result of it's execution will be used as resolved
dependency under value object name. Returned value treated as is without further
processing. Classes returned by `@value` decorated function would be be used as
classes. It will not be treated as something we need instantiate.

Value object will be stored in the injection scope under the same name as
decorated function.

Arguments of the decorated function will be treated as direct dependencies of
the `@value` object. Each argument will be resolved from the same injection
scope where value object was defined.

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

As you can see, `foo`, `bar`, and `baz` were resolved from the `Container`
injection scope. After that `quiz` function was called with resolved
dependencies passed to its arguments. Result of the function was stored in the
injection scope under the same `quiz` name. We received value from `quiz` name
from the injection scope.

## Depending on the value

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

You may depend on the `@value` object value the same way you depend on regular
instances of the class.

In the example above `Foo` and `Bar` depends on `quiz` name. Value object would
be resolved to `3` (result returned by decorated function) and this value would
be injected in corresponding argument of `Foo` and `Bar` constructors.

As you can see `@value` decorated function was called only once even two objects
depends on it.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
