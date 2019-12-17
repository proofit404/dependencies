# Py.Test contrib

[Py.test](https://docs.pytest.org/) is a state of art testing framework
for Python.

If you business objects have to do with a lot of third-party services,
it might be difficult to build a reliable test suite.

Many of us do not want to make third-party API calls or send emails each
time their test suite runs.

If you wrap your business objects in pytest fixture, you can easily
substitute external interactions with well-defined stubs.

## Define a fixture

To define pytest fixture directly from the injector subclass you should
do the following

```pycon

>>> # tests/order_creation_test.py

>>> from dependencies import Injector
>>> from dependencies.contrib.pytest import register
>>> from examples.order.commands import CreateOrder
>>> from examples.stubs import send_email_stub

>>> @register
... class CreateOrderFixture(Injector):
...     name = 'create_order'
...     fixture = CreateOrder
...     send_email = send_email_stub

>>> def test_create_order(create_order):
...     create_order.create()
...     assert create_order.send_email.called

```

Dependency injection will take place during the test preparation process
while building a tree of fixtures. Your test will get already configured
object so you can take away setup boiler place from your tests and check
an actual business logic behind it.

### Customizable arguments

As with pytest own `fixture` decorator arguments, you can set some
attributes to the injector subclass to tweak fixture behavior.

- `fixture` attribute resolved to the fixture value. The result of the
  DI process will be available in tests as test argument value.
- `name` of the fixture. You should add an argument with this name to
  your test to access fixture value.
- `scope` of the fixture. The `session`, `module`, `class` and
  `function` scopes are available and work exactly the same way
  regular fixture scopes do.
- `params` create parametrized fixture.
- `autouse` attaches this fixture to every test in the suite.
- `ids` getter for parametrized tests in the report.

### Available scope

Before test run injector scope will be executed with this attributes.
You can use them as dependencies for your classes.

- `request` instance of the pytest `FixtureRequest`.

## Depend on a fixture

Let's imagine your stubs are defined in other fixtures, not in modules.

```pycon

>>> # tests/smtp_fixtures.py

>>> import pytest
>>> from examples.stubs import send_email_stub

>>> @pytest.fixture
... def send_email():
...     return send_email_stub

```

Your business objects can depend on values of another fixture.

```pycon

# tests/order_creation_test.py

>>> from dependencies import Injector
>>> from dependencies.contrib.pytest import register, require

>>> @register
... class CreateOrderFixture(Injector):
...     name = 'create_order'
...     fixture = CreateOrder
...     send_email = require('send_email')

>>> def test_create_order(create_order, send_email):
...     create_order.create()
...     assert send_email.called

```

The value of the `send_email` fixture will be injected into
`CreateOrder` constructor before each test.

## Parametrized fixture

It is possible to define parametrized fixture with `params` attribute
set on the injector subclass.

```pycon

>>> # tests/app_test.py

>>> from dependencies import Injector, this

>>> class CreateOrder(object):
...     def __init__(self, discount):
...         pass

>>> @register
... class CreateOrderFixture(Injector):
...     name = 'create_order'
...     fixture = CreateOrder
...     discount = this.request.param
...     params = [20, 30, 50]

```

In this example we create parametrized fixture and use this param in
actual object as a dependency.
