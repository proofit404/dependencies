"""Tests related to class-named attributes."""
from inspect import isclass

import pytest

from dependencies import Injector
from dependencies import value
from signature import Signature


def _no_instantiate():
    class Bar:
        def __init__(self, foo_class):
            self.foo_class = foo_class

    @value
    def bar(foo_class):
        return Signature(foo_class=foo_class)

    yield Bar
    yield bar


@pytest.mark.parametrize("arg", _no_instantiate())
def test_class_named_do_not_instantiate(e, expect, arg):
    """Do not call class constructor, if it stored with name ended `_class`."""

    class Container(Injector):
        result = e.Take["bar"]
        bar = arg
        foo_class = e.Null

    @expect(Container)
    def case(it):
        assert isclass(it.result.foo_class)
        assert it.result.foo_class is e.Null


def _default_value():
    class Foo:
        pass

    class Bar:
        def __init__(self, foo_class=Foo):
            self.foo_class = foo_class

    @value
    def bar(foo_class=Foo):
        return Signature(foo_class=foo_class)

    yield Foo, Bar
    yield Foo, bar


@pytest.mark.parametrize(("default", "arg"), _default_value())
def test_class_named_default_value(e, expect, default, arg):
    """Allow classes as default argument values if argument name ends with `_class`."""

    class Container(Injector):
        baz = e.Take["bar"]
        bar = arg

    @expect(Container)
    def case(it):
        assert isclass(it.baz.foo_class)
        assert it.baz.foo_class is default


def _default_class():
    class Foo:
        pass

    class Bar:
        def __init__(self, foo=Foo):
            raise RuntimeError

    @value
    def func(foo=Foo):
        raise RuntimeError

    yield Bar, """
'Bar' class has a default value of 'foo' argument set to 'Foo' class.

You should either change the name of the argument into 'foo_class'
or set the default value to an instance of that class.
    """
    yield func, """
'func' value has a default value of 'foo' argument set to 'Foo' class.

You should either change the name of the argument into 'foo_class'
or set the default value to an instance of that class.
    """


@pytest.mark.parametrize(("arg", "message"), _default_class())
def test_non_class_named_default_value_is_class(expect, catch, arg, message):
    """If argument does not end with `_class`, its default value can't be a class."""

    class Container(Injector):
        bar = arg

    @expect(Container)
    @catch(message)
    def case(it):
        it.baz


def _class_named():
    class Bar:
        def __init__(self, foo_class=1):
            raise RuntimeError

    @value
    def func(foo_class=1):
        raise RuntimeError

    yield Bar
    yield func


@pytest.mark.parametrize("arg", _class_named())
def test_class_named_default_value_not_class(expect, catch, arg):
    """If argument ends with `_class`, it must have a class as it default value."""

    class Container(Injector):
        bar = arg

    @expect(Container)
    @catch("'foo_class' default value should be a class")
    def case(it):
        it.baz
