# Descriptors

Descriptors is a powerful feature of the python language. It allows an object to
know in attribute of what other object it is stored. Python will know an object
is a descriptor if it implements descriptor protocol. In other words, if it
defines `__get__`, `__set__`, and `__delete__` methods.

```pycon

>>> class Descriptor:
...     def __get__(self, instance, klass):
...         print("=>", instance)
...         print("=>", klass)
...         return 1

>>> class Holder:
...     attribute = Descriptor()

>>> Holder().attribute  # doctest: +ELLIPSIS
=> <__main__.Holder object at 0x...>
=> <class '__main__.Holder'>
1

>>> Holder.attribute
=> None
=> <class '__main__.Holder'>
1

```

Probably, you don't write code like that frequently. But a lot of your code uses
descriptors already. For example, `@property` decorator and fields of Django
models are implemented as descriptors.

```pycon

>>> @property
... def attribute(self):
...     return 1

>>> hasattr(attribute, '__get__')
True

>>> hasattr(attribute, '__set__')
True

```

## Inconsistency with `dependencies`

As you already noticed descriptors could be assigned only at class definition
time. Descriptor protocol will not be used in case you assign descriptor object
to the object attribute.

```pycon

>>> class Wrong:
...
...     def __init__(self, attribute):
...
...         self.attribute = attribute

>>> Wrong(Descriptor()).attribute  # doctest: +ELLIPSIS
<__main__.Descriptor object at 0x...>

```

The code above does not execute `__get__` method. It returns descriptor object
as is.

Most of the times `dependencies` library used to build instances of objects.
That's why specifying descriptor as a dependency of some object would be a
suspicious operation to do.

1. **You will not have access to the `Injector` class it self.**
2. **You will not have access to the object descriptor was passed to.**

That's why descriptor found in the injection scope will be treated as an error.

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...
...     wrong = Wrong
...     attribute = Descriptor()

>>> Container.wrong
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Attribute 'attribute' contains descriptor.
<BLANKLINE>
Descriptors usage will be confusing inside Injector subclasses.
<BLANKLINE>
Use @value decorator instead, if you really need inject descriptor instance somewhere.

>>> class Container(Injector):
...
...     wrong = Wrong
...
...     @property
...     def attribute(self):
...         return 1

>>> Container.wrong
Traceback (most recent call last):
  ...
_dependencies.exceptions.DependencyError: Attribute 'attribute' contains descriptor.
<BLANKLINE>
Descriptors usage will be confusing inside Injector subclasses.
<BLANKLINE>
Use @value decorator instead, if you really need inject descriptor instance somewhere.

```

## Inject descriptors anyway

As we explain earlier, using descriptors in the injection scope is a user error
is most cases. You **don't** need a workaround until you're doing something
really strange like defining classes during dependency injection process or
accessing `Injector` attributes during class definition process.

If you decided to bypass this restriction, you can use a nested class to hide
the nature of an object.

```pycon

>>> class Container(Injector):
...
...     class attribute:
...         def __new__(cls):
...             return Descriptor()

>>> class Strange:
...
...     attribute = Container.attribute

>>> Strange().attribute  # doctest: +ELLIPSIS
=> <__main__.Strange object at 0x...>
=> <class '__main__.Strange'>
1

>>> Strange.attribute
=> None
=> <class '__main__.Strange'>
1

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
