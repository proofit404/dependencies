from inspect import isclass

from _dependencies.classes import _make_init_spec
from _dependencies.nested import _make_nested_injector_spec
from _dependencies.operation import _make_operation_spec
from _dependencies.operation import Operation
from _dependencies.package import _make_package_spec
from _dependencies.package import Package
from _dependencies.raw import _make_raw_spec
from _dependencies.this import _make_this_spec
from _dependencies.this import This
from _dependencies.value import _make_value_spec
from _dependencies.value import Value


class _InjectorTypeType(type):
    pass


def _make_dependency_spec(name, dependency):

    if isinstance(dependency, _InjectorTypeType):
        return _make_nested_injector_spec(dependency)
    elif isclass(dependency) and not name.endswith("_class"):
        return _make_init_spec(dependency)
    elif isinstance(dependency, This):
        return _make_this_spec(dependency)
    elif isinstance(dependency, Package):
        return _make_package_spec(dependency)
    elif isinstance(dependency, Operation):
        return _make_operation_spec(dependency)
    elif isinstance(dependency, Value):
        return _make_value_spec(dependency)
    else:
        return _make_raw_spec(dependency)
