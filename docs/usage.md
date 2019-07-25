# Usage

## Preparations

Before we start to inject dependencies lets define code which needs this
dependencies.

```python
>>> class Robot:
...     def __init__(self, servo, controller, settings)
...         self.servo = servo
...         self.controller = controller
...         self.settings = settings
...
```

We use constructor based dependency injection. We define necessary
arguments and store it explicitly. We do this for readability. This will
helps us to understand the path things go in your system. Attributes
taken from nowhere in your code aren't fun. Believe me.

## Behavior

So lets add some behavior to your robot.

```python
>>> def run(self):
...     while True:
...         events = self.accept_events()
...         self.process(events)
...
>>> def accept_events(self):
...     return self.controller()  # We can inject methods.
...
>>> def process(self, events):
...     max_point = self.settings['max_point']  # Dictionaries.
...     for event in events:
...         if event.x > max_point:
...             self.servo.reverse('x')  # And objects.
...         if event.y > max_point:
...             self.servo.reverse('y')
```

Now its time to make it work in real world

```python
>>> class MechanicalMotor:
...     def reverse(self, coordinate):
...         # Hardware work goes here.
...
>>> def read_sensor():
...     # Another hardware work goes here.
...
>>> production = {'max_point': 0.01}
```

So we are close to scream "It's alive!" and run out of the building.

```python
>>> from dependencies import Injector
>>> class Container(Injector):
...     robot = Robot
...     servo = MechanicalMotor
...     controller = read_sensor
...     settings = production
...
>>> robot = Container.robot  # Robots' constructor called here.
>>> robot.run()
```

Congratulations! We build our robot with dependency injection.

## Injection rules

`Container` above is a dependency scope. You can take any of them from
his attribute. Following things happens when you access an argument:

* If `class` stored in attributes it will be instantiated. We will see
  what arguments it takes and search for each in the same dependency
  scope.
* If it a `class` stored in the attribute named with `_class` at the
  end - then it return as is. (For example `Container.foo_class` will
  give you class stored in it. Not an instance).
* Anything else returned as is.
* If we found a class during dependency search we will instantiate it
  as well.

Here is a demonstration of rules above.

```python
>>> class Foo:
...     def __init__(self, one, two):
...         self.one = one
...         self.two = two
...
>>> class Bar:
...     pass
...
>>> class Baz:
...     def __init__(self, x):
...         self.x = x
...
>>> from dependencies import Injector
>>> class Scope(Injector):
...     foo = Foo
...     one = Bar
...     two = Baz
...     x = 1
...
>>> Scope.foo
<__main__.Foo object at 0x7f99f4f5f080>
>>> Scope.foo.one
<__main__.Bar object at 0x7f99f47fd278>
>>> Scope.foo.two
<__main__.Baz object at 0x7f99f4f5f0b8>
>>> Scope.foo.two.x
1
```

As you can see `Foo` class needs argument named `two`. We find `Baz`
class as a dependency satisfied this name. We see that this is a class -
so we need to instantiate it too. We search for dependency named `x` and
find `1`. We build `Baz` instance then use it to build `Foo` instance.

### Calculation rules

Each dependency evaluates once during injection process. If during
dependency injection different classes have constructor argument with
same name, it will be one object. But this objects lives only during one
injection process. New attribute access - new object.

```python
>>> from dependencies import Injector
>>> class Container(Injector):
...     class Foo:
...         def __init__(self, bar, baz):
...             self.bar = bar
...             self.baz = baz
...         def check(self):
...             return self.bar.x is self.baz.x
...     class Bar:
...         def __init__(self, x):
...             self.x = x
...     class Baz:
...         def __init__(self, x):
...             self.x = x
...     class X:
...         pass
...     # Names.
...     foo, bar, baz, x = Foo, Bar, Baz, X
...
>>> Container.foo.check()
True
>>> Container.bar.x is Container.bar.x
False
```

### Nested `Injectors`

It is possible to inject `Injector` it self. `Injector` subclasses
provided as is and calculate its attributes on first use.

```python
>>> from dependencies import Injector
>>> class Container(Injector):
...     class Foo:
...         def __init__(self, bar):
...             self.bar = bar
...         def __call__(self):
...             return self.bar.baz()
...     class Bar(Injector):
...         class Baz:
...             def __init__(self, func):
...                 self.func = func
...             def __call__(self):
...                 return self.func()
...         def func():
...             return 1
...         # Names.
...         baz = Baz
...     # Names.
...     foo, bar = Foo, Bar
...
>>> Container.foo()
1
>>> Container.foo.bar
<class '__main__.Container.Bar'>
>>> Container.foo.bar.baz
<__main__.Container.Bar.Baz object at 0x7ffff610c390>
>>> Container.foo.bar.baz.func
<function Container.Bar.func at 0x7ffff61129d8>
>>> Container.foo.bar.baz.func()
1
```

## Scope extension

You need to have whole collection of dependencies only in injection
moment i.e. on scope attribute access. You can define scope partially
and then extend it. There are two ways to do that:

* inheritance
* `let` notation

### Inheritance

You can add additional dependencies or redefine already provided in the
scope subclasses:

```python
>>> class Scope(Injector):
...     foo = Foo
...
>>> class ChildScope(Scope):
...     bar = Bar
...
>>> ChildScope.foo
```

Multiple inheritance is allowed as well.

```python
>>> class Scope1(Injector):
...     foo = Foo
...
>>> class Scope2(Injector):
...     bar = Bar
...
>>> class ChildScope(Scope1, Scope2):
...     pass
...
>>> ChildScope.foo
```

Also we provide `and` notation for inplace `Injector` composition.
Example below is full equivalent to the previous one without
intermediate class needed.

```python
>>> class Scope1(Injector):
...     foo = Foo
...
>>> class Scope2(Injector):
...     bar = Bar
...
>>> (Scope1 & Scope2).foo
```

### `let` notation

You can temporary redefine dependency for only one case. This is
extremely useful for tests. Inject asserts instead of some dependency an
you will be able to test your system in all possible cases. It even
possible to simulate database integrity error on concurrent access.

```python
>>> class Scope(Injector):
...     foo = Foo
...     bar = Bar
...
>>> Scope.let(bar=Baz).foo
```

It is possible to build dependency scopes directly from dictionaries
using `let` notation.

```python
>>> Scope = Injector.let(foo=Foo, bar=Bar, **settings)
```

## `hasattr` alternative

`hasattr` works by attribute access, so it triggers dependency
injection. If this is unnecessary side effect, `dependencies` provides
alternative way.

```python
>>> class Container(Injector):
...     foo = 1
...
>>> 'foo' in Container
True
>>>
```
