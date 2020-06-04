# Dependencies

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/dependencies/2?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=2&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/dependencies/2?style=flat-square)](https://dev.azure.com/proofit404/dependencies/_build/latest?definitionId=2&branchName=master)
[![pypi](https://img.shields.io/pypi/v/dependencies?style=flat-square)](https://pypi.python.org/pypi/dependencies/)
[![conda](https://img.shields.io/conda/vn/conda-forge/dependencies?style=flat-square)](https://anaconda.org/conda-forge/dependencies)

Dependency Injection for Humans.

**[Documentation](https://proofit404.github.io/dependencies/)**

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
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
