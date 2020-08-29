# Using attrs

[attrs](http://www.attrs.org/) is the Python package that will bring back the
joy of writing classes by relieving you from the drudgery of implementing object
protocols (aka [dunder](https://nedbatchelder.com/blog/200605/dunder.html)
methods).

It's an excellent library. Personally, I use it heavily in all projects.

## Inject classes

Here is an example of how to use it together with `dependencies`.

```pycon

>>> from attr import attrs, attrib
>>> from dependencies import Injector

>>> @attrs
... class Order:
...     price = attrib()
...     items = attrib()

>>> class Container(Injector):
...     order = Order
...     price = (799, 99)
...     items = ["amplifier", "servo"]

>>> Container.order
Order(price=(799, 99), items=['amplifier', 'servo'])

```

As you can see, instances of a class defined with `attrs` are built completely
the same way we build handwritten classes. But there is no need to write all
this boilerplate by hand.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
