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

>>> class Calc:
...     def __init__(self, result):
...         self.result = result

>>> class Container(Injector):
...     calc = Calc
...     foo = 1
...     bar = 2
...     baz = 3
...
...     @value
...     def result(foo, bar, baz):
...         return foo + bar + baz

>>> Container.calc.result
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

## Singletons

The singleton pattern is considered a bad practice in general. But in some cases
you would actually need to use them. For example, if you instantiate connection
pool for you database, message queue, or cache.

In that case you could use `functools.lru_cache` together with `@value`
decorator.

Let assume you would like to instantiate your view class each time you need to
handle a separate HTTP request. If your view class would depend on connection
pool, it would not be recreated each time you want to process the request.

Nice thing about this approach - you don't need to make connection pool a
singleton itself. This logic would kept inside `Injector` subclass, which would
make pool class a little bit more testable.

```pycon

>>> from functools import lru_cache

>>> class Connections:
...     """Connection pool."""
...     def __init__(self, host, port):
...         ...
...
...     def connect(self):
...         ...

>>> class Request:
...     def __init__(self, connections):
...         self.connections = connections

>>> class Container(Injector):
...     request = Request
...     host = "localhost"
...     port = 1234
...
...     @value
...     @lru_cache
...     def connections(host, port):
...         pool = Connections(host, port)
...         pool.connect()
...         return port

>>> request1 = Container.request

>>> request2 = Container.request

>>> request1 is request2
False

>>> request1.connections is request2.connections
True

```

<p align="center">&mdash; ⭐ &mdash;</p>
