import types

import pytest
from dependencies import Injector
from dependencies.contrib.pytest import register, require
from dependencies.exceptions import DependencyError


class Foo(object):

    def __init__(self, foo, bar, baz):

        self.foo = foo
        self.bar = bar
        self.baz = baz

    def sum(self):

        return self.foo + self.bar + self.baz


@register
class Container(Injector):
    name = "fixture_name"
    fixture = Foo
    foo = require("fixture_name_1")
    baz = require("fixture_name_2")
    bar = require("fixture_name_3")


@pytest.fixture
def fixture_name_1():

    return 1


@pytest.fixture
def fixture_name_2():

    return 2


@pytest.fixture
def fixture_name_3():

    return 3


def test_register_fixture(fixture_name):
    """
    Register and require Py.test fixtures with `Injector` subclasses.
    """

    assert isinstance(fixture_name, Foo)
    assert fixture_name.sum() == 6


def test_docstrings():
    """
    `register` decorator and `require` marker should have proper
    documentation strings.
    """

    assert (
        register.__doc__
        == "Register Py.test fixture performing injection in it's scope."
    )
    assert require.__doc__ == "Mark fixture as a dependency for injection process."


def test_register_return_value():
    """`register` should return `Injector` subclass unmodified."""

    assert isinstance(Container, types.FunctionType)
    assert issubclass(Container.injector, Injector)


def test_validation():
    """
    `register` decorator should check required `Injector` subclass
    attribute.
    """

    with pytest.raises(DependencyError) as exc_info:

        @register
        class Container1(Injector):
            name = "fixture_name"

    message = str(exc_info.value)
    assert message == "'Container1' can not resolve attribute 'fixture'"

    with pytest.raises(DependencyError) as exc_info:

        @register
        class Container2(Injector):
            fixture = Foo

    message = str(exc_info.value)
    assert message == "'Container2' can not resolve attribute 'name'"


def test_fixture_arguments():
    """
    Allow `register` decorator arguments customization through
    `Injector` subclass attributes.
    """

    @register
    class Container(Injector):
        name = "fixture_name"
        fixture = object
        scope = "session"
        params = ("foo", "bar", "baz")
        autouse = True
        ids = ("one", "two", "three")

    assert Container._pytestfixturefunction.name == "fixture_name"
    assert Container._pytestfixturefunction.scope == "session"
    assert Container._pytestfixturefunction.params == ("foo", "bar", "baz")
    assert Container._pytestfixturefunction.autouse is True
    assert Container._pytestfixturefunction.ids == ("one", "two", "three")
