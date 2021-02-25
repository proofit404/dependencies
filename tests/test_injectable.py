"""Tests related to injectable objects."""
import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies import Package
from dependencies import value
from dependencies.exceptions import DependencyError


deny_varargs = CodeCollector()
varargs_defs = CodeCollector("foo")


@deny_varargs.parametrize
@varargs_defs.parametrize
def test_deny_variable_length_positional_arguments(code, foo):
    """Raise `DependencyError` if constructor have *args argument."""

    class Baz:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(foo(), Baz)

    message = str(exc_info.value)
    assert message in {
        "'Foo.__init__' have variable-length positional arguments",
        "'func' have variable-length positional arguments",
    }


@deny_varargs
def _dfe1c22c641e(Foo, Baz):
    class Container(Injector):
        foo = Foo
        args = (1, 2, 3)
        baz = Baz

    Container.baz


@deny_varargs
def _f7ef2aa82c18(Foo, Baz):
    Injector(foo=Foo, args=(1, 2, 3), baz=Baz).baz


@varargs_defs
def _xkebooxhls7f():
    class Foo:
        def __init__(self, *args):
            raise RuntimeError

    return Foo


@varargs_defs
def _eapfhkr8z0mg():
    @value
    def func(*args):
        raise RuntimeError

    return func


deny_kwargs = CodeCollector()
kwargs_defs = CodeCollector("foo")


@deny_kwargs.parametrize
@kwargs_defs.parametrize
def test_deny_variable_length_keyword_arguments(code, foo):
    """Raise `DependencyError` if constructor have **kwargs argument."""

    class Baz:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(foo(), Baz)

    message = str(exc_info.value)
    assert message in {
        "'Foo.__init__' have variable-length keyword arguments",
        "'func' have variable-length keyword arguments",
    }


@deny_kwargs
def _e281099be65d(Foo, Baz):
    class Container(Injector):
        foo = Foo
        kwargs = {"start": 5}
        baz = Baz

    Container.baz


@deny_kwargs
def _bcf7c5881b2c(Foo, Baz):
    Injector(foo=Foo, kwargs={"start": 5}, baz=Baz).baz


@kwargs_defs
def _gvhotc3zgfuq():
    class Foo:
        def __init__(self, **kwargs):
            raise RuntimeError

    return Foo


@kwargs_defs
def _hmshyccwnhsw():
    @value
    def func(**kwargs):
        raise RuntimeError

    return func


deny_positional_only_arguments = CodeCollector()
positional_only_arguments_defs = CodeCollector("foo")


@deny_positional_only_arguments.parametrize
@positional_only_arguments_defs.parametrize
def test_deny_positional_only_arguments(code, foo):
    """We can not inject positional-only arguments."""
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    message = str(exc_info.value)
    assert message in {
        "'Foo.__init__' have positional-only arguments",
        "'foo' have positional-only arguments",
    }


@deny_positional_only_arguments
def _b81wVbPL16QR(Foo):
    class Container(Injector):
        foo = Foo

    Container.foo


@deny_positional_only_arguments
def _bF3JriFujPqf(Foo):
    Injector(foo=Foo).foo


@positional_only_arguments_defs
def _rPiy4i9XVvzb():
    class Foo:
        def __init__(self, a, /, b):
            raise RuntimeError

    return Foo


@positional_only_arguments_defs
def _hw5TnOooZVOG():
    @value
    def foo(a, /, b):
        raise RuntimeError

    return foo


@positional_only_arguments_defs
def _dQ7tFVMvSYmF():
    examples = Package("examples")
    return examples.positional_only.Foo


@positional_only_arguments_defs
def _h79dcovVgStH():
    examples = Package("examples")
    return examples.positional_only.foo


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

    class Baz:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(bar(Foo), Baz)

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
def _dad79637580d(Bar, Baz):
    class Container(Injector):
        bar = Bar
        baz = Baz

    Container.baz


@cls_named_arguments
def _bccb4f621e70(Bar, Baz):
    Injector(bar=Bar, baz=Baz).baz


@arguments_defs
def _sxd25ppy5ypj(Foo):
    class Bar:
        def __init__(self, foo=Foo):
            raise RuntimeError

    return Bar


@arguments_defs
def _oafemes7wcku(Foo):
    @value
    def func(foo=Foo):
        raise RuntimeError

    return func


cls_named_defaults = CodeCollector()
defaults_defs = CodeCollector("bar")


@cls_named_defaults.parametrize
@defaults_defs.parametrize
def test_deny_non_classes_in_class_named_arguments(code, bar):
    """If argument name ends with `_class`, it must have a class as it default value."""

    class Baz:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(bar(), Baz)

    message = str(exc_info.value)

    assert message == "'foo_class' default value should be a class"


@cls_named_defaults
def _a8cd70341d3d(Bar, Baz):
    class Container(Injector):
        bar = Bar
        baz = Baz

    Container.baz


@cls_named_defaults
def _b859e98f2913(Bar, Baz):
    Injector(bar=Bar, baz=Baz).baz


@defaults_defs
def _x53iiy9oyx4i():
    class Bar:
        def __init__(self, foo_class=1):
            raise RuntimeError

    return Bar


@defaults_defs
def _zkh2hnjhe149():
    @value
    def func(foo_class=1):
        raise RuntimeError

    return func
