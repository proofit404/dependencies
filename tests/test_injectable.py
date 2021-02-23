"""Tests related to injectable objects."""
import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


deny_varargs = CodeCollector()
varargs_defs = CodeCollector("foo")


@deny_varargs.parametrize
@varargs_defs.parametrize
def test_deny_arbitrary_argument_list(code, foo):
    """Raise `DependencyError` if constructor have *args argument."""
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    message = str(exc_info.value)
    assert message in {
        "'Foo.__init__' have variable-length positional arguments",
        "'func' have variable-length positional arguments",
    }


@deny_varargs
def _dfe1c22c641e(Foo):
    class Container(Injector):
        foo = Foo
        args = (1, 2, 3)


@deny_varargs
def _f7ef2aa82c18(Foo):
    Injector(foo=Foo, args=(1, 2, 3))


@varargs_defs
def _xkebooxhls7f():
    class Foo:
        def __init__(self, *args):
            pass  # pragma: no cover

    return Foo


@varargs_defs
def _eapfhkr8z0mg():
    @value
    def func(*args):
        pass  # pragma: no cover

    return func


deny_kwargs = CodeCollector()
kwargs_defs = CodeCollector("foo")


@deny_kwargs.parametrize
@kwargs_defs.parametrize
def test_deny_arbitrary_keyword_arguments(code, foo):
    """Raise `DependencyError` if constructor have **kwargs argument."""
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    message = str(exc_info.value)
    assert message in {
        "'Foo.__init__' have variable-length keyword arguments",
        "'func' have variable-length keyword arguments",
    }


@deny_kwargs
def _e281099be65d(Foo):
    class Container(Injector):
        foo = Foo
        kwargs = {"start": 5}


@deny_kwargs
def _bcf7c5881b2c(Foo):
    Injector(foo=Foo, kwargs={"start": 5})


@kwargs_defs
def _gvhotc3zgfuq():
    class Foo:
        def __init__(self, **kwargs):
            pass  # pragma: no cover

    return Foo


@kwargs_defs
def _hmshyccwnhsw():
    @value
    def func(**kwargs):
        pass  # pragma: no cover

    return func


cls_named_arguments = CodeCollector()
arguments_defs = CodeCollector("bar")


@cls_named_arguments.parametrize
@arguments_defs.parametrize
def test_deny_classes_as_default_values(code, bar):
    """Verify constructor default arguments against naming conventions.

    If argument name doesn't ends with `_class`, its default value can't be a class.

    """

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(bar(Foo))

    message = str(exc_info.value)

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

    assert message in {expected_class, expected_value}


@cls_named_arguments
def _dad79637580d(Bar):
    class Container(Injector):
        bar = Bar


@cls_named_arguments
def _bccb4f621e70(Bar):
    Injector(bar=Bar)


@arguments_defs
def _sxd25ppy5ypj(Foo):
    class Bar:
        def __init__(self, foo=Foo):
            pass  # pragma: no cover

    return Bar


@arguments_defs
def _oafemes7wcku(Foo):
    @value
    def func(foo=Foo):
        pass  # pragma: no cover

    return func


cls_named_defaults = CodeCollector()
defaults_defs = CodeCollector("bar")


@cls_named_defaults.parametrize
@defaults_defs.parametrize
def test_deny_non_classes_in_class_named_arguments(code, bar):
    """If argument name ends with `_class`, it must have a class as it default value."""
    with pytest.raises(DependencyError) as exc_info:
        code(bar())

    message = str(exc_info.value)

    assert message == "'foo_class' default value should be a class"


@cls_named_defaults
def _a8cd70341d3d(Bar):
    class Container(Injector):
        bar = Bar


@cls_named_defaults
def _b859e98f2913(Bar):
    Injector(bar=Bar)


@defaults_defs
def _x53iiy9oyx4i():
    class Bar:
        def __init__(self, foo_class=1):
            pass  # pragma: no cover

    return Bar


@defaults_defs
def _zkh2hnjhe149():
    @value
    def func(foo_class=1):
        pass  # pragma: no cover

    return func
