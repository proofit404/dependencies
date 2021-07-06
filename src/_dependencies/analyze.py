from _dependencies.objects.attributes import _build_attributes_spec
from _dependencies.objects.attributes import _is_attributes
from _dependencies.objects.classes import _build_class_spec
from _dependencies.objects.classes import _is_class
from _dependencies.objects.data import _build_data_spec
from _dependencies.objects.data import _is_data
from _dependencies.objects.descriptor import _is_descriptor
from _dependencies.objects.enum import _is_enum
from _dependencies.objects.nested import _build_nested_injector_spec
from _dependencies.objects.nested import _is_nested_injector
from _dependencies.objects.package import _build_package_spec
from _dependencies.objects.package import _is_package
from _dependencies.objects.this import _build_this_spec
from _dependencies.objects.this import _is_this
from _dependencies.objects.value import _build_value_spec
from _dependencies.objects.value import _is_value


def _recursive(builder):
    def wrapper(name, dependency):
        state = builder(name, dependency)
        while True:
            try:
                next_dependency = next(state)
                next_spec = _make_dependency_spec(name, next_dependency)
                state.send(next_spec)
            except StopIteration as result:
                return result.value

    return wrapper


conditions = (
    (_is_descriptor, None),
    (_is_enum, None),
    (_is_attributes, _recursive(_build_attributes_spec)),
    (_is_nested_injector, _build_nested_injector_spec),
    (_is_class, _build_class_spec),
    (_is_this, _build_this_spec),
    (_is_package, _recursive(_build_package_spec)),
    (_is_value, _build_value_spec),
    (_is_data, _build_data_spec),
)


def _make_dependency_spec(name, dependency):
    for condition, builder in conditions:  # pragma: no branch
        if condition(name, dependency):
            return builder(name, dependency)
