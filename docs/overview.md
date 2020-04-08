# Overview

`dependencies` library provides a nice DSL for specifying relations of
your classes and make instantiation as simple as attribute access.

```pycon

>>> from dependencies import Injector
>>> from app.robot import Robot, Servo, Amplifier, Controller, Settings

>>> class Container(Injector):
...     robot = Robot # Constructor of this class needs `servo`, `controller`, and `settings` arguments.
...     servo = Servo # Constructor of this class needs `amplifier` argument.
...     amplifier = Amplifier
...     controller = Controller
...     settings = Settings # Constructor of this class needs `environment` argument.
...     environment = "production"

>>> Container.robot.work()
>>> #         `---> This attribute access creates instances of `Controller`,
>>> #               `Amplifier`, `Settings`, `Servo`, and `Robot` classes
>>> #               in the proper order and calls each constructor with
>>> #               proper arguments.

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
