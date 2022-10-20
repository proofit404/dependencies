# shield

Sometimes you need to instantiate classes that were not designed to be used in
dependency injection context. For example, it has variable length positional or
keyword arguments. Commonly known as `*args` and `**kwargs`. Our dependency
injection implementation highly coupled with constructor signature of the class.
We have to know ahead what arguments we need to pass to the class by names.

For specific cases like this we introduced `shield` object. It allows you to
specify necessary signature manually. In that case dependency injection engine
would know what arguments to pass.

## Principles

- [Variable-length positional arguments could be specified](#variable-length-positional-arguments-could-be-specified)
- [`this` object could be used in arguments](#this-object-could-be-used-in-arguments)

### Variable-length positional arguments could be specified

If you specify positional arguments next to the class you want to build inside
`shield` object signature, they would be injected based on on the semantic
commonly used for such dependency type.

For example, scalar types would be passed as is. The same way they would be
passed from `Injector` attributes.

```pycon

>>> from dependencies import Injector, shield

>>> class Sum:
...     def __init__(self, *args):
...         self.args = args
...
...     def do(self):
...         return sum(self.args)

>>> class Wrong(Injector):
...     sum = Sum

>>> Wrong.sum.do()
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: 'Sum.__init__' have variable-length positional arguments

>>> class Container(Injector):
...     sum = shield(Sum, 1, 2)

>>> Container.sum.do()
3

```

### `this` object could be used in arguments

You could pass `this` objects to variable-length positional or keyword
arguments. It would be resolved in the same scope where `shield` object was
defined.

```pycon

>>> from dependencies import Injector, shield, this

>>> class Sum:
...     def __init__(self, *args):
...         self.args = args
...
...     def do(self):
...         return sum(self.args)

>>> class Container(Injector):
...     sum = shield(Sum, this.a, this.b)
...     a = 1
...     b = 2

>>> Container.sum.do()
3

```

<p align="center">&mdash; ⭐ &mdash;</p>
