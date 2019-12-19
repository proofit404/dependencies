![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)

[![azure-pipeline](https://dev.azure.com/dry-python/dependencies/_apis/build/status/dry-python.dependencies?branchName=master)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![codecov](https://codecov.io/gh/dry-python/dependencies/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/dependencies)
[![docs](https://readthedocs.org/projects/dependencies/badge/?version=latest)](http://dependencies.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://badges.gitter.im/dry-python/dependencies.svg)](https://gitter.im/dry-python/dependencies)
[![pypi](https://img.shields.io/pypi/v/dependencies.svg)](https://pypi.python.org/pypi/dependencies/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

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

>>> from examples import Robot, Servo, Amplifier, Controller, Settings

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
