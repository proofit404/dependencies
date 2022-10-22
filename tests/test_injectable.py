"""Tests related to injectable objects."""
import pytest

from dependencies import Injector
from dependencies import value


def _varargs():
    class Foo:
        def __init__(self, *args):
            raise RuntimeError

    @value
    def func(*args):
        raise RuntimeError

    yield Foo, "'Foo.__init__' have variable-length positional arguments"
    yield func, "'func' have variable-length positional arguments"


@pytest.mark.parametrize(("arg", "message"), _varargs())
def test_deny_variable_length_positional_arguments(expect, catch, arg, message):
    """Raise `DependencyError` if constructor have *args argument."""

    class Container(Injector):
        foo = arg

    @expect(Container)
    @catch(message)
    def case(it):
        it.bar


def _kwargs():
    class Foo:
        def __init__(self, **kwargs):
            raise RuntimeError

    @value
    def func(**kwargs):
        raise RuntimeError

    yield Foo, "'Foo.__init__' have variable-length keyword arguments"
    yield func, "'func' have variable-length keyword arguments"


@pytest.mark.parametrize(("arg", "message"), _kwargs())
def test_deny_variable_length_keyword_arguments(expect, catch, arg, message):
    """Raise `DependencyError` if constructor have **kwargs argument."""

    class Container(Injector):
        foo = arg

    @expect(Container)
    @catch(message)
    def case(it):
        it.bar


def _positional_only():
    class Foo:
        def __init__(self, a, /, b):
            raise RuntimeError

    @value
    def foo(a, /, b):
        raise RuntimeError

    yield Foo, "'Foo.__init__' have positional-only arguments"
    yield foo, "'foo' have positional-only arguments"


@pytest.mark.parametrize(("arg", "message"), _positional_only())
def test_deny_positional_only_arguments(expect, catch, arg, message):
    """We can not inject positional-only arguments."""

    class Container(Injector):
        foo = arg

    @expect(Container)
    @catch(message)
    def case(it):
        it.bar
