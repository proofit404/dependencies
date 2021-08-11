# Dependencies

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/dependencies/15?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=15&branchName=release)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/dependencies/15?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=15&branchName=release)
[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.org/project/dependencies)
[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)
[![python](https://img.shields.io/pypi/pyversions/dependencies?style=flat-square)](https://pypi.org/project/dependencies)

Constructor injection designed with OOP in mind.

**[Documentation](https://proofit404.github.io/dependencies) |
[Source Code](https://github.com/proofit404/dependencies) |
[Task Tracker](https://github.com/proofit404/dependencies/issues)**

Dependency Injection (or simply DI) is a great technique. By using it you can
organize responsibilities in you codebase. Define high level policies and system
behavior in one part. Delegate control to low level mechanisms in another part.
Simple and powerful.

With help of DI you can use different parts of your system independently and
combine their behavior really easy.

If you split logic and implementation into different classes, you will see how
pleasant it becomes to change your system.

This tiny library helps you to connect parts of your system, in particular - to
inject low level implementation into high level behavior.

## Pros

- Provide composition instead of inheritance.
- Solves top-down architecture problems.
- Boilerplate-free object hierarchies.
- API entrypoints, admin panels, CLI commands are oneliners.

## Example

Dependency injection without `dependencies`

```pycon

>>> from app.robot import Robot, Servo, Amplifier, Controller, Settings

>>> robot = Robot(
...     servo=Servo(amplifier=Amplifier()),
...     controller=Controller(),
...     settings=Settings(environment="production"),
... )

>>> robot.work()

```

Dependency injection with `dependencies`

```pycon

>>> from dependencies import Injector

>>> class Container(Injector):
...     robot = Robot
...     servo = Servo
...     amplifier = Amplifier
...     controller = Controller
...     settings = Settings
...     environment = "production"

>>> Container.robot.work()

```

## Questions

If you have any questions, feel free to create an issue in our
[Task Tracker](https://github.com/proofit404/dependencies/issues). We have the
[question label](https://github.com/proofit404/dependencies/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)
exactly for this purpose.

## Enterprise support

If you have an issue with any version of the library, you can apply for a paid
enterprise support contract. This will guarantee you that no breaking changes
will happen to you. No matter how old version you're using at the moment. All
necessary features and bug fixes will be backported in a way that serves your
needs.

Please contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you're
interested in it.

## License

`dependencies` library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
