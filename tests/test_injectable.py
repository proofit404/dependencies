"""Tests related to injectable objects."""
import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError


def test_deny_variable_length_positional_arguments(d):
    """Raise `DependencyError` if constructor have *args argument."""

    class Baz:
        pass

    class Container(Injector):
        foo = d
        args = (1, 2, 3)
        baz = Baz

    with pytest.raises(DependencyError) as exc_info:
        Container.baz

    assert str(exc_info.value) in {
        "'Foo.__init__' have variable-length positional arguments",
        "'func' have variable-length positional arguments",
    }


def _varargs():
    class Foo:
        def __init__(self, *args):
            raise RuntimeError

    @value
    def func(*args):
        raise RuntimeError

    yield Foo
    yield func


@pytest.fixture(params=_varargs())
def d(request):
    """All possible variable-length positional argument definitions."""
    return request.param


def test_deny_variable_length_keyword_arguments(e):
    """Raise `DependencyError` if constructor have **kwargs argument."""

    class Baz:
        pass

    class Container(Injector):
        foo = e
        kwargs = {"start": 5}
        baz = Baz

    with pytest.raises(DependencyError) as exc_info:
        Container.baz

    assert str(exc_info.value) in {
        "'Foo.__init__' have variable-length keyword arguments",
        "'func' have variable-length keyword arguments",
    }


def _kwargs():
    class Foo:
        def __init__(self, **kwargs):
            raise RuntimeError

    @value
    def func(**kwargs):
        raise RuntimeError

    yield Foo
    yield func


@pytest.fixture(params=_kwargs())
def e(request):
    """All possible variable-length keyword argument definitions."""
    return request.param


def test_deny_positional_only_arguments(f):
    """We can not inject positional-only arguments."""

    class Container(Injector):
        foo = f

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    assert str(exc_info.value) in {
        "'Foo.__init__' have positional-only arguments",
        "'foo' have positional-only arguments",
    }


def _positional_only():
    class Foo:
        def __init__(self, a, /, b):
            raise RuntimeError

    @value
    def foo(a, /, b):
        raise RuntimeError

    yield Foo
    yield foo


@pytest.fixture(params=_positional_only())
def f(request):
    """All possible positional-only argument definitions."""
    return request.param


def test_deny_classes_as_default_values(q):
    """Verify constructor default arguments against naming conventions.

    If argument name doesn't ends with `_class`, its default value can't be a class.

    """

    class Baz:
        pass

    class Container(Injector):
        bar = q
        baz = Baz

    with pytest.raises(DependencyError) as exc_info:
        Container.baz

    expected_class = """
'Bar' class has a default value of 'foo' argument set to 'Foo' class.

You should either change the name of the argument into 'foo_class'
or set the default value to an instance of that class.
""".strip()

    expected_value = """
'func' value has a default value of 'foo' argument set to 'Foo' class.

You should either change the name of the argument into 'foo_class'
or set the default value to an instance of that class.
""".strip()

    assert str(exc_info.value) in {expected_class, expected_value}


def _default_class():
    class Foo:
        pass

    class Bar:
        def __init__(self, foo=Foo):
            raise RuntimeError

    @value
    def func(foo=Foo):
        raise RuntimeError

    yield Bar
    yield func


@pytest.fixture(params=_default_class())
def q(request):
    """All default argument definitions."""
    return request.param


def test_deny_non_classes_in_class_named_arguments(t):
    """If argument name ends with `_class`, it must have a class as it default value."""

    class Baz:
        pass

    class Container(Injector):
        bar = t
        baz = Baz

    with pytest.raises(DependencyError) as exc_info:
        Container.baz

    message = str(exc_info.value)

    assert message == "'foo_class' default value should be a class"


def _class_named():
    class Bar:
        def __init__(self, foo_class=1):
            raise RuntimeError

    @value
    def func(foo_class=1):
        raise RuntimeError

    yield Bar
    yield func


@pytest.fixture(params=_class_named())
def t(request):
    """All class-named argument definitions."""
    return request.param
