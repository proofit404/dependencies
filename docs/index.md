![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)

[![azure-devops-builds](https://img.shields.io/azure-devops/build/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![readthedocs](https://img.shields.io/readthedocs/dependencies?style=flat-square)](https://dependencies.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://img.shields.io/gitter/room/dry-python/dependencies?style=flat-square)](https://gitter.im/dry-python/dependencies)
[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.python.org/pypi/dependencies/)
[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)

---

# Dependency Injection for Humans

Dependency Injection (or simply DI) is a great technique. By using it you
can organize responsibilities in you codebase. Define high level
policies and system behavior in one part. Delegate control to low level
mechanisms in anotherpart. Simple and powerful.

With help of DI you can use different parts of your system independently
and combine their behavior really easy.

If you split logic and implementation into different classes, you will
see how pleasant it becomes to change your system.

This tiny library helps you to connect parts of your system, in particular - to
inject low level implementation into high level behavior.

# Example

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

# Installation

## Release version

Dependencies is available on PyPI - to install it, just run:

```bash
pip install -U dependencies
```

That's it! Once installed, `dependencies` library is available for use. Import
it and have fun.

## Development version

You can always install last development version directly from source
control:

```bash
pip install -U git+https://github.com/dry-python/dependencies.git
```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
