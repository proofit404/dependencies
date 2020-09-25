"""Tests related to the function checks."""
import pytest

from dependencies import Injector
from dependencies import operation
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
        "Foo.__init__ have arbitrary argument list",
        "func have arbitrary argument list",
    }


@deny_varargs
def _dfe1c22c641e(Foo):
    class Summator(Injector):
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
def _u69ddou3olnl():
    @operation
    def func(*args):
        pass  # pragma: no cover

    return func


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
        "Foo.__init__ have arbitrary keyword arguments",
        "func have arbitrary keyword arguments",
    }


@deny_kwargs
def _e281099be65d(Foo):
    class Summator(Injector):
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
def _d0li35b2qiaw():
    @operation
    def func(**kwargs):
        pass  # pragma: no cover

    return func


@kwargs_defs
def _hmshyccwnhsw():
    @value
    def func(**kwargs):
        pass  # pragma: no cover

    return func


deny_varargs_kwargs = CodeCollector()
varargs_kwargs_defs = CodeCollector("foo")


@deny_varargs_kwargs.parametrize
@varargs_kwargs_defs.parametrize
def test_deny_arbitrary_positional_and_keyword_arguments_together(code, foo):
    """Raise `DependencyError` if constructor have *args and **kwargs argument."""
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    message = str(exc_info.value)
    assert message in {
        "Foo.__init__ have arbitrary argument list and keyword arguments",
        "func have arbitrary argument list and keyword arguments",
    }


@deny_varargs_kwargs
def _efbf07f8deb6(Foo):
    class Summator(Injector):
        foo = Foo
        args = (1, 2, 3)
        kwargs = {"start": 5}


@deny_varargs_kwargs
def _c4362558f312(Foo):
    Injector(foo=Foo, args=(1, 2, 3), kwargs={"start": 5})


@varargs_kwargs_defs
def _qyy5p4ah11qj():
    class Foo:
        def __init__(self, *args, **kwargs):
            pass  # pragma: no cover

    return Foo


@varargs_kwargs_defs
def _q3o6g5va9wtj():
    @operation
    def func(*args, **kwargs):
        pass  # pragma: no cover

    return func


@varargs_kwargs_defs
def _btt8ue2wjjra():
    @value
    def func(*args, **kwargs):
        pass  # pragma: no cover

    return func


cls_named_arguments = CodeCollector()


@cls_named_arguments.parametrize
def test_deny_classes_as_default_values(code):
    """Verify constructor default arguments against naming conventions.

    If argument name doesn't ends with `_class`, its default value can't be a class.

    """

    class Foo:
        pass

    class Bar:
        def __init__(self, foo=Foo):
            pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, Bar)

    message = str(exc_info.value)
    expected_message = """
'Bar' class has a default value of 'foo' argument set to 'Foo' class.

You should either change the name of the argument into 'foo_class'
or set the default value to an instance of that class.
""".strip()
    assert message == expected_message


@cls_named_arguments
def _dad79637580d(Foo, Bar):
    class Container(Injector):
        bar = Bar


@cls_named_arguments
def _bccb4f621e70(Foo, Bar):
    Injector(bar=Bar)


cls_named_defaults = CodeCollector()


@cls_named_defaults.parametrize
def test_deny_non_classes_in_class_named_arguments(code):
    """If argument name ends with `_class`, it must have a class as it default value."""

    class Bar:
        def __init__(self, foo_class=1):
            self.foo_class = foo_class

    with pytest.raises(DependencyError) as exc_info:
        code(Bar)

    message = str(exc_info.value)
    assert message == "'foo_class' default value should be a class"


@cls_named_defaults
def _a8cd70341d3d(Bar):
    class Container(Injector):
        bar = Bar


@cls_named_defaults
def _b859e98f2913(Bar):
    Injector(bar=Bar)
