# Dependencies

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/dependencies/2?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=2&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/dependencies/2?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=2&branchName=master)
[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.python.org/pypi/dependencies/)
[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)

Dependency Injection for Humans.

**[Documentation](https://proofit404.github.io/dependencies/) | [Source Code](https://github.com/proofit404/dependencies) | [Task Tracker](https://github.com/proofit404/dependencies/issues)**

- Provide composition instead of inheritance.
- Solves top-down approach problem.
- Boilerplate-free object hierarchies.
- API entrypoints, admin panels, CLI commands are oneliners.

Dependency Injection (or simply DI) is a great technique. By using it you
can organize responsibilities in you codebase. Define high level
policies and system behavior in one part. Delegate control to low level
mechanisms in another part. Simple and powerful.

With help of DI you can use different parts of your system independently
and combine their behavior really easy.

If you split logic and implementation into different classes, you will
see how pleasant it becomes to change your system.

This tiny library helps you to connect parts of your system, in particular - to
inject low level implementation into high level behavior.

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

## License

Dependencies library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
