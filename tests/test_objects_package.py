"""Tests related to the Package object."""
import inspect

import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


def test_provide_module():
    """Package instance itself should refer to the module."""
    from _ import examples as _examples
    import examples

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = _examples

    assert inspect.ismodule(Container.root.result)
    assert examples is Container.root.result


def test_provide_submodule():
    """Package instance itself should refer to the module."""
    from _ import examples as _examples
    import examples.submodule

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = _examples.submodule

    assert inspect.ismodule(Container.root.result)
    assert examples.submodule is Container.root.result


def test_provide_a_variable():
    """Package instance attribute access should provide regular variable."""
    from _ import examples

    class Root:
        def __init__(self, result):
            self.result = result

    class Container1(Injector):
        root = Root
        result = examples.submodule.variable

    class Container2(Injector):
        root = Root
        result = examples.init_variable

    # NOTE: Use @expect with multiple injectors.
    assert Container1.root.result == 1
    assert Container2.root.result == 1


def test_provide_a_function():
    """Package instance attribute access should provide regular function."""
    from _ import examples

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = examples.submodule.function

    assert inspect.isfunction(Container.root.result)
    assert Container.root.result() == 1


def test_provide_an_instance():
    """Package attribute access should provide an instance when refer to a class.

    We explicitly does not create an intermediate Root class to have access to the
    package declaration. Package could provide access to the class defined in another
    module.

    """
    from examples.submodule import Foo

    from _ import examples

    class Container(Injector):
        result = examples.submodule.Foo

    assert isinstance(Container.result, Foo)
    assert Container.result.do() == 1


def test_provide_instance_method():
    """Package instance attribute access should provide instance method.

    Access bound method should not be allowed to be resolved directly. That's why we
    need an intermediate Root class.

    """
    from examples.submodule import Bar

    from _ import examples

    class Root:
        def __init__(self, result):
            self.result = result

    class Container(Injector):
        root = Root
        result = examples.submodule.Bar.do
        a = 7
        b = 5

    assert inspect.ismethod(Container.root.result)
    assert isinstance(Container.root.result.__self__, Bar)
    assert Container.root.result() == 12


def test_provide_a_class():
    """Package class-named attributes should provide classes.

    Package attribute should provide a class when it stored in the attribute with
    `_class` in its name.

    """
    from examples.submodule import Foo

    from _ import examples

    class Root:
        def __init__(self, result_class):
            self.result_class = result_class

    class Container(Injector):
        root = Root
        result_class = examples.submodule.Foo

    assert inspect.isclass(Container.root.result_class)
    assert Container.root.result_class is Foo


def test_point_to_injector():
    """Package attribute access should provide Injector classes as is.

    Package pointer should be able to point to `Injector` subclass attribute defined in
    another module.

    """
    from _ import examples

    class Root:
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    class Container(Injector):
        root = Root
        foo = examples.injected.Container.foo
        bar = examples.injected.Container.bar
        baz = 2

    assert Container.root.foo == 1
    assert Container.root.bar == 2


def test_package_provides_lazy_loading():
    """We can point `Package` to the same module.

    If `Injector` subclass tries to point to another `Injector` subclass defined *below*
    in the same module, we should handle it as usual.

    """
    from _ import examples

    class Container(Injector):
        foo = examples.self_pointer.Container.foo

    assert Container.foo.bar == "baz"


def test_handle_import_error():
    """Import time errors should be propagated.

    Import error raised by poorly written project module should not be hidden by Package
    implementation.

    """
    from _ import examples

    class Root:
        def __init__(self, result):
            raise RuntimeError

    class Container(Injector):
        root = Root
        result = this.Nested.foo

        class Nested(Injector):
            foo = examples.import_error.Vision

    with pytest.raises(ModuleNotFoundError) as exc_info:
        Container.root

    assert str(exc_info.value) == "No module named 'astral'"


@pytest.mark.parametrize("relative", [".", "..", ".example", "..example"])
def test_protect_against_relative_import(relative):
    """Deny to use relative import path in Package declaration."""
    from dependencies import Package

    with pytest.raises(DependencyError) as exc_info:
        Package(relative)

    expected = "Do not use relative import path in Package declaration"

    assert str(exc_info.value) == expected
