import inspect

from _dependencies.classes import make_init_spec
from _dependencies.nested import make_nested_injector_spec
from _dependencies.operation import Operation, make_operation_spec
from _dependencies.package import Package, make_package_spec
from _dependencies.raw import make_raw_spec
from _dependencies.this import This, make_this_spec
from _dependencies.value import Value, make_value_spec


class InjectorTypeType(type):
    pass


def make_dependency_spec(name, dependency):

    # FIXME: Protect `Injector` from `_class` named attributes.
    if isinstance(dependency, InjectorTypeType):
        return make_nested_injector_spec(dependency)
    elif inspect.isclass(dependency) and not name.endswith("_class"):
        return make_init_spec(dependency)
    elif isinstance(dependency, This):
        return make_this_spec(dependency)
    elif isinstance(dependency, Package):
        return make_package_spec(dependency)
    elif isinstance(dependency, Operation):
        return make_operation_spec(dependency)
    elif isinstance(dependency, Value):
        return make_value_spec(dependency)
    else:
        return make_raw_spec(dependency)
