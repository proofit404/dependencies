import pytest
from dependencies import Injector, value
from dependencies.exceptions import DependencyError


def test_define_value():
    class Container(Injector):

        foo = 1
        bar = 2
        baz = 3

        @value
        def result(foo, bar, baz):
            return foo + bar + baz

    assert Container.result == 6


def test_keyword_arguments():
    class Container(Injector):

        foo = 1
        bar = 2

        @value
        def result(foo, bar, baz=3):
            return foo + bar + baz

    assert Container.result == 6


def test_protect_against_self():

    with pytest.raises(DependencyError) as exc_info:

        @value
        def method(self, foo, bar):
            pass

    assert str(exc_info.value) == "'value' decorator can not be used on methods"


def test_protect_against_classes():

    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo(object):
            pass

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


def test_protect_against_args_kwargs():

    with pytest.raises(DependencyError) as exc_info:

        @value
        def func(*args):
            pass

    assert str(exc_info.value) == "func have arbitrary argument list"

    with pytest.raises(DependencyError) as exc_info:

        @value
        def func(**kwargs):
            pass

    assert str(exc_info.value) == "func have arbitrary keyword arguments"

    with pytest.raises(DependencyError) as exc_info:

        @value
        def func(*args, **kwargs):
            pass

    assert (
        str(exc_info.value) == "func have arbitrary argument list and keyword arguments"
    )
