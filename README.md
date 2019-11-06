![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)

[![azure-pipeline](https://dev.azure.com/dry-python/dependencies/_apis/build/status/dry-python.dependencies?branchName=master)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![codecov](https://codecov.io/gh/dry-python/dependencies/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/dependencies)
[![docs](https://readthedocs.org/projects/dependencies/badge/?version=latest)](https://dependencies.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://badges.gitter.im/dry-python/dependencies.svg)](https://gitter.im/dry-python/dependencies)
[![pypi](https://img.shields.io/pypi/v/dependencies.svg)](https://pypi.python.org/pypi/dependencies/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

# Dependency Injection for Humans

- [Source Code](https://github.com/dry-python/dependencies)
- [Issue Tracker](https://github.com/dry-python/dependencies/issues)
- [Documentation](https://dependencies.readthedocs.io/en/latest/)
- [Discussion](https://gitter.im/dry-python/dependencies)

## Installation

All released versions are hosted on the Python Package Index. You can
install this package with following command.

```bash
pip install dependencies
```

## Usage

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

## License

Dependencies library is offered under the two clause BSD license.
