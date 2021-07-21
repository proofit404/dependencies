# Usage

## Preparations

Before we start to inject dependencies, let's define code which needs these
dependencies. Also, let's add some behavior to your robot.

```pycon

>>> class Robot:
...     def __init__(self, servo, controller, settings):
...         self.servo = servo
...         self.controller = controller
...         self.settings = settings
...
...     def run(self):
...         while True:
...             events = self.accept_events()
...             if not events:
...                 break
...             self.process(events)
...
...     def accept_events(self):
...         # We can inject methods.
...         return self.controller()
...
...     def process(self, events):
...         # We can inject dictionaries.
...         max_point = self.settings["max_point"]
...         for event in events:
...             if event.x > max_point:
...                 # We can inject objects.
...                 self.servo.reverse("x")
...             if event.y > max_point:
...                 self.servo.reverse("y")

```

We use constructor-based dependency injection here: we define necessary
arguments and store them explicitly, for the sake of readability. This will help
us to understand the execution path of your system. Attributes sourced from
nowhere in your code aren't fun. Believe me.

Now, it's time to make this work in the real world.

```pycon

>>> class MechanicalMotor:
...     def reverse(self, coordinate):
...         # Hardware work goes here.
...         pass

>>> def read_sensor():
...     # Another hardware work goes here.
...     return []

>>> production = {'max_point': 0.01}

```

We are close to scream "It's alive!" and, if we're lucky enough, run out of the
building.

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...     robot = Robot
...     servo = MechanicalMotor
...     controller = read_sensor
...     settings = production

>>> robot = Container.robot  # Robots' constructor called here.

>>> robot.run()

```

Congratulations! We've built our robot with dependency injection.

## Injection rules

`Container` above is a dependency scope, and dependencies are defined as its
attributes. When you access one of those attributes, the following happens:

- If attribute value is a `class`, it will be instantiated. To make that
  possible, the library will inspect its constructor's argument list and search
  current dependency scope for dependencies with the same name.
- If attribute value is a `class` but attribute name ends with `_class` - then
  it will be returned as is. (For example, `Container.foo_class` will return the
  class stored in it, not its instance).
- Anything else is returned as is.
- If, during dependency search, we encounter another `class` - it will be
  instantiated along these rules, as well. The process is recursive.

Here is a demonstration of rules above.

```pycon

>>> class Foo:
...     def __init__(self, one, two):
...         self.one = one
...         self.two = two

>>> class Bar:
...     pass

>>> class Baz:
...     def __init__(self, x):
...         self.x = x

>>> from dependencies import Injector

>>> class Scope(Injector):
...     foo = Foo
...     one = Bar
...     two = Baz
...     x = 1

>>> Scope.foo  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>

>>> Scope.foo.one  # doctest: +ELLIPSIS
<__main__.Bar object at 0x...>

>>> Scope.foo.two  # doctest: +ELLIPSIS
<__main__.Baz object at 0x...>

>>> Scope.foo.two.x
1

```

Let's roll down what is happening here:

- `Foo` class requires an argument named `two`;
- In dependency scope, that argument resolves to `Baz` class;
- Which is a class - oh, we need to instantiate it as well;
- But its constructor requires an argument named `x`;
- Which resolves to `1` in the dependency scope, so we do not need to go any
  further.

Having found that out, we effectively construct, execute, and return
`Foo(two=Baz(x=1))`.

### Calculation rules

Each dependency evaluates exactly once during injection process. If during
dependency injection different classes have constructor argument with the same
name, the corresponding dependency will be instantiated once and these two
constructors will receive the same object. But this object only lives during one
injection process; another attribute access means a new object.

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...
...     class Foo:
...
...         def __init__(self, bar, baz):
...             self.bar = bar
...             self.baz = baz
...
...         def check(self):
...             return self.bar.x is self.baz.x
...
...     class Bar:
...
...         def __init__(self, x):
...             self.x = x
...
...     class Baz:
...
...         def __init__(self, x):
...             self.x = x
...
...     class X:
...         pass
...
...     # Names.
...     foo, bar, baz, x = Foo, Bar, Baz, X

>>> Container.foo.check()
True

>>> Container.bar.x is Container.bar.x
False

```

## Scope extension

You can define a dependency scope partially and then extend it; only in
injection moment, meaning at the time of attribute access, you are required to
have the complete scope.

It is possible to extend dependency scopes in two ways:

- inheritance
- call

### Inheritance

You can add additional dependencies or redefine existing ones in a scope
subclass:

```pycon

>>> class Foo:
...     pass

>>> class Scope(Injector):
...     foo = Foo

>>> class ChildScope(Scope):
...     bar = Bar

>>> ChildScope.foo  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>

```

Multiple inheritance is allowed as well.

```pycon

>>> class Scope1(Injector):
...     foo = Foo

>>> class Scope2(Injector):
...     bar = Bar

>>> class ChildScope(Scope1, Scope2):
...     pass

>>> ChildScope.foo  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>

```

We also provide `and` notation for in-place `Injector` composition. Example
below is full equivalent to the previous one, but without intermediate class
needed.

```pycon

>>> class Scope1(Injector):
...     foo = Foo

>>> class Scope2(Injector):
...     bar = Bar

>>> (Scope1 & Scope2).foo  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>

```

!!! note

    Extension scope should not be empty.  You can't inherit from
    `Injector` just to have `pass` keyword as the body of the class.

    ```pycon

    >>> class Container(Injector):
    ...     pass
    Traceback (most recent call last):
      ...
    _dependencies.exceptions.DependencyError: Extension scope can not be empty

    ```

### Call

You can temporary redefine a dependency for only one case. This is extremely
useful for tests. Inject an assertion instead of one or more dependencies, and
you will be able to test your system in all possible cases. It is, for example,
possible to simulate database integrity error on concurrent access.

```pycon

>>> class Scope(Injector):
...     foo = Foo
...     bar = Bar

>>> Scope(bar=Baz).foo  # doctest: +ELLIPSIS
<__main__.Foo object at 0x...>

```

It is possible to build dependency scopes directly from dictionaries using call.

```pycon

>>> settings = {'host': 'localhost', 'port': 1234}

>>> Scope = Injector(foo=Foo, bar=Bar, **settings)

```

## `hasattr` alternative

`hasattr` works by attribute access, so it triggers dependency injection. If
this is unnecessary side effect, `dependencies` provides alternative way.

```pycon

>>> class Container(Injector):
...     foo = 1

>>> 'foo' in Container
True

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
