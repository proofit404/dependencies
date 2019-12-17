# Overview

`dependencies` library provides a nice DSL for specifying relations of
your classes and make instantiation as simple as attribute access.

```pycon

>>> from dependencies import Injector
>>> from examples.overview import Logger, Servo, Robot

>>> class Container(Injector):
...     logger = Logger
...     servo = Servo # Constructor of this class needs `logger` argument.
...     robot = Robot # Constructor of this class needs `servo` argument.

>>> Container.robot.run()
>>> #         `---> This attribute access creates instances of `Logger`,
>>> #               `Servo`, and `Robot` classes in the proper order and
>>> #               calls each constructor with proper arguments.

```
