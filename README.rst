
.. |travis| image:: https://img.shields.io/travis/dry-python/dependencies.svg?style=flat-square
    :target: https://travis-ci.org/dry-python/dependencies
    :alt: Build Status

.. |codecov| image:: https://img.shields.io/codecov/c/github/dry-python/dependencies.svg?style=flat-square
    :target: https://codecov.io/gh/dry-python/dependencies
    :alt: Coverage Status

.. |pyup| image:: https://pyup.io/repos/github/dry-python/dependencies/shield.svg
     :target: https://pyup.io/repos/github/dry-python/dependencies/
     :alt: PyUp Status

.. |codacy| image:: https://img.shields.io/codacy/ac9894ac09cc41028c3eb6fbc27126ad.svg?style=flat-square
    :target: https://www.codacy.com/app/dry-python/dependencies
    :alt: Code Quality Status

.. |pypi| image:: https://img.shields.io/pypi/v/dependencies.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dependencies/
    :alt: Python Package Version

.. image:: https://raw.githubusercontent.com/dry-python/dependencies/master/docs/static/dependencies_logo.png
    :alt: Dependencies

|travis| |codecov| |pyup| |codacy| |pypi|

Dependency Injection for Humans.

- `Source Code`_
- `Issue Tracker`_
- Documentation_

Installation
------------

All released versions are hosted on the Python Package Index.  You can
install this package with following command.

.. code:: bash

    pip install dependencies

Usage
-----

Dependency injection without ``dependencies``

.. code:: python

    robot = Robot(
        servo=Servo(amplifier=Amplifier()),
        controller=Controller(),
        settings=Settings(environment="production"),
    )

    robot.work()

Dependency injection with ``dependencies``

.. code:: python

    class Container(Injector):
        robot = Robot
        servo = Servo
        amplifier = Amplifier
        controller = Controller
        settings = Settings
        environment = "production"

    Container.robot.work()

License
-------

Dependencies library is offered under the two clause BSD license.

.. _source code: https://github.com/dry-python/dependencies
.. _issue tracker: https://github.com/dry-python/dependencies/issues
.. _documentation: http://dependencies.readthedocs.io/en/latest/
