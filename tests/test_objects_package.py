"""Tests related to the Package object."""
import inspect

import pytest

from dependencies import Injector
from dependencies import Package
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


provide_module = CodeCollector()


@provide_module.parametrize
def test_provide_module(code):
    """Package instance itself should refer to the module."""
    import examples

    class Root:
        def __init__(self, result):
            self.result = result

    Container = code(Root)
    assert inspect.ismodule(Container.root.result)
    assert examples is Container.root.result


@provide_module
def _vlg36qA6yZyS(Root):
    examples = Package("examples")

    class Container(Injector):
        root = Root
        result = examples

    return Container


@provide_module
def _vNORYQu36ygs(Root):
    examples = Package("examples")
    return Injector(root=Root, result=examples)


provide_submodule = CodeCollector()
submodule_variant = CodeCollector("sub")


@provide_submodule.parametrize
@submodule_variant.parametrize
def test_provide_submodule(code, sub):
    """Package instance itself should refer to the module."""
    import examples.submodule

    class Root:
        def __init__(self, result):
            self.result = result

    Container = code(Root, sub())
    assert inspect.ismodule(Container.root.result)
    assert examples.submodule is Container.root.result


@provide_submodule
def _maXQQRr7Q7HH(Root, sub):
    class Container(Injector):
        root = Root
        result = sub

    return Container


@provide_submodule
def _cjMUDUzwLP6j(Root, sub):
    return Injector(root=Root, result=sub)


@submodule_variant
def _kFnqTphEQoHc():
    return Package("examples.submodule")


@submodule_variant
def _c50eltRQOS2a():
    examples = Package("examples")
    return examples.submodule


provide_variable = CodeCollector()
variable_variant = CodeCollector("variable")


@provide_variable.parametrize
@variable_variant.parametrize
def test_provide_a_variable(code, variable):
    """Package instance attribute access should provide regular variable."""

    class Root:
        def __init__(self, result):
            self.result = result

    Container = code(Root, variable())
    assert Container.root.result == 1


@provide_variable
def _fpOfsFByaQOc(Root, variable):
    class Container(Injector):
        root = Root
        result = variable

    return Container


@provide_variable
def _qICvFa5gphmY(Root, variable):
    return Injector(root=Root, result=variable)


@variable_variant
def _xqImNk0p0kun():
    examples = Package("examples")
    return examples.submodule.variable


@variable_variant
def _d1H5hbDhnoVL():
    submodule = Package("examples.submodule")
    return submodule.variable


@variable_variant
def _ocFk5G1OWGty():
    examples = Package("examples")
    return examples.init_variable


provide_function = CodeCollector()
function_variant = CodeCollector("function")


@provide_function.parametrize
@function_variant.parametrize
def test_provide_a_function(code, function):
    """Package instance attribute access should provide regular function."""

    class Root:
        def __init__(self, result):
            self.result = result

    Container = code(Root, function())
    assert inspect.isfunction(Container.root.result)
    assert Container.root.result() == 1


@provide_function
def _qy2e8eIhQ7k4(Root, function):
    class Container(Injector):
        root = Root
        result = function

    return Container


@provide_function
def _lCNl7nzCX0KO(Root, function):
    return Injector(root=Root, result=function)


@function_variant
def _xIMIuAFAZ5iR():
    examples = Package("examples")
    return examples.submodule.function


@function_variant
def _l3PIIW8qeapm():
    submodule = Package("examples.submodule")
    return submodule.function


provide_instance = CodeCollector()
instance_variant = CodeCollector("instance")


@provide_instance.parametrize
@instance_variant.parametrize
def test_provide_an_instance(code, instance):
    """Package attribute access should provide an instance when refer to a class.

    We explicitly does not create an intermediate Root class to have access to the
    package declaration. Package could provide access to the class defined in another
    module.

    """
    from examples.submodule import Foo

    Container = code(instance())
    assert isinstance(Container.result, Foo)
    assert Container.result.do() == 1


@provide_instance
def _s9nywIe9xRPm(instance):
    class Container(Injector):
        result = instance

    return Container


@provide_instance
def _qviB3dir35aM(instance):
    return Injector(result=instance)


@instance_variant
def _t6nazic2SZeH():
    examples = Package("examples")
    return examples.submodule.Foo


@instance_variant
def _j9swuGAFg3Ss():
    submodule = Package("examples.submodule")
    return submodule.Foo


provide_instance_method = CodeCollector()
instance_method_variant = CodeCollector("method")


@provide_instance_method.parametrize
@instance_method_variant.parametrize
def test_provide_instance_method(code, method):
    """Package instance attribute access should provide instance method.

    Access bound method should not be allowed to be resolved directly. That's why we
    need an intermediate Root class.

    """
    from examples.submodule import Bar

    class Root:
        def __init__(self, result):
            self.result = result

    Container = code(Root, method())
    assert inspect.ismethod(Container.root.result)
    assert isinstance(Container.root.result.__self__, Bar)
    assert Container.root.result() == 12


@provide_instance_method
def _s6NFdEBsCnNy(Root, method):
    class Container(Injector):
        root = Root
        result = method
        a = 7
        b = 5

    return Container


@provide_instance_method
def _o2BJhyCPZKft(Root, method):
    return Injector(root=Root, result=method, a=7, b=5)


@instance_method_variant
def _nsYIrniBcXRO():
    examples = Package("examples")
    return examples.submodule.Bar.do


@instance_method_variant
def _jz76zoiIhe0f():
    submodule = Package("examples.submodule")
    return submodule.Bar.do


provide_class = CodeCollector()
class_variant = CodeCollector("klass")


@provide_class.parametrize
@class_variant.parametrize
def test_provide_a_class(code, klass):
    """Package class-named attributes should provide classes.

    Package attribute should provide a class when it stored in the attribute with
    `_class` in its name.

    """
    from examples.submodule import Foo

    class Root:
        def __init__(self, result_class):
            self.result_class = result_class

    Container = code(Root, klass())
    assert inspect.isclass(Container.root.result_class)
    assert Container.root.result_class is Foo


@provide_class
def _rpx7XSPKVFaV(Root, klass):
    class Container(Injector):
        root = Root
        result_class = klass

    return Container


@provide_class
def _aTLBa5GAkLkV(Root, klass):
    return Injector(root=Root, result_class=klass)


@class_variant
def _qtSV6ssFFmT0():
    examples = Package("examples")
    return examples.submodule.Foo


@class_variant
def _fmreItIa9y2J():
    submodule = Package("examples.submodule")
    return submodule.Foo


deny_direct_resolve = CodeCollector()


@deny_direct_resolve.parametrize
def test_direct_data_resolve(code):
    """Attempt to resolve scalar types directly should raise exception."""
    with pytest.raises(DependencyError) as exc_info:
        code()
    expected = "Scalar dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_direct_resolve
def _so9SmIf2QZ5l():
    examples = Package("examples")

    class Container(Injector):
        a = examples.submodule.variable

    Container.a


@deny_direct_resolve
def _gMiVaHHt4rJG():
    examples = Package("examples")
    Injector(a=examples.submodule.variable).a


injector_pointer = CodeCollector()


@injector_pointer.parametrize
def test_point_to_injector(code):
    """Package attribute access should provide Injector classes as is.

    Package pointer should be able to point to `Injector` subclass attribute defined in
    another module.

    """

    class Root:
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    Container = code(Root)
    assert Container.root.foo == 1
    assert Container.root.bar == 2


@injector_pointer
def _zprTYSyMkLEC(Root):
    examples = Package("examples")

    class Container(Injector):
        root = Root
        foo = examples.injected.Container.foo
        bar = examples.injected.Container.bar
        baz = 2

    return Container


@injector_pointer
def _dqXJgFoftQja(Root):
    injected = Package("examples.injected")

    class Container(Injector):
        root = Root
        foo = injected.Container.foo
        bar = injected.Container.bar
        baz = 2

    return Container


self_pointer = CodeCollector()


@self_pointer.parametrize
def test_package_provides_lazy_loading(code):
    """We can point `Package` to the same module.

    If `Injector` subclass tries to point to another `Injector` subclass defined *below*
    in the same module, we should handle it as usual.

    """
    Container = code()
    assert Container.foo.bar == "baz"


@self_pointer
def _dmldmoXCFIBG():
    self_pointer = Package("examples.self_pointer")

    class Container(Injector):
        foo = self_pointer.Container.foo

    return Container


@self_pointer
def _pRX4SSAbG8iO():
    examples = Package("examples")
    return Injector(foo=examples.self_pointer.Container.foo)


import_error = CodeCollector()
nested_variant = CodeCollector("nested")
error_variant = CodeCollector("error")


@import_error.parametrize
@nested_variant.parametrize
@error_variant.parametrize
def test_handle_import_error(code, nested, error):
    """Import time errors should be propagated.

    Import error raised by poorly written project module should not be hidden by Package
    implementation.

    """

    class Root:
        def __init__(self, result):
            raise RuntimeError

    Container = code(Root, nested(error()))

    with pytest.raises(ModuleNotFoundError) as exc_info:
        Container.root

    assert str(exc_info.value) == "No module named 'astral'"


@import_error
def _yjihTbbUJ3rS(Root, Nested):
    class Container(Injector):
        root = Root
        result = this.nested.foo
        nested = Nested

    return Container


@import_error
def _xtLbizL0vuJr(Root, Nested):
    return Injector(root=Root, result=this.nested.foo, nested=Nested)


@nested_variant
def _cdYU3Mxu5W0R(error):
    class Nested(Injector):
        foo = error

    return Nested


@nested_variant
def _q8vFClchGiWW(error):
    return Injector(foo=error)


@error_variant
def _cXjECOua1K75():
    examples = Package("examples")
    return examples.import_error.Vision


@error_variant
def _jNELGA2KFLA7():
    submodule = Package("examples.import_error")
    return submodule.Vision
