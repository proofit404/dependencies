Dependencies
============

Dependency Injection for Humans.

Dependency Injection (or simply DI) is great technique.  By using it
you can organize responsibilities in you code base.  Define high level
policies and system behavior in one part.  Delegate control to low
level mechanisms from different part.  Simple and powerful.

With help of DI you can use different parts of you system
independently and combine their behavior really easy.

If you split logic and implementation into different classes, you will
see how pleasant it became to change your system.

This tiny library helps you to connect parts of your system i.e. to
inject low level implementation into high level behavior.

Example
-------

Dependency injection without ``dependencies``

.. code:: python

    robot = Robot(
        servo=Servo(amplifier=Amplifier()),
        controller=Controller(),
        settings=Settings(environment="production"),
    )

Dependency injection with ``dependencies``

.. code:: python

    class Container(Injector):
        robot = Robot
        servo = Servo
        amplifier = Amplifier
        controller = Controller
        settings = Settings
        environment = "production"

    robot = Container.robot

Contents
--------

.. toctree::
    :maxdepth: 2

    installation
    why
    usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
