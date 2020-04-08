![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/dependencies.png)

[![azure-devops-builds](https://img.shields.io/azure-devops/build/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/dry-python/dependencies/2?style=flat-square)](https://dev.azure.com/dry-python/dependencies/_build/latest?definitionId=2&branchName=master)
[![readthedocs](https://img.shields.io/readthedocs/dependencies?style=flat-square)](https://dependencies.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://img.shields.io/gitter/room/dry-python/dependencies?style=flat-square)](https://gitter.im/dry-python/dependencies)
[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.python.org/pypi/dependencies/)
[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)

---

# Dependency Injection for Humans

- [Source Code](https://github.com/dry-python/dependencies)
- [Issue Tracker](https://github.com/dry-python/dependencies/issues)
- [Documentation](https://dependencies.readthedocs.io/en/latest/)
- [Newsletter](https://twitter.com/dry_py)
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
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
