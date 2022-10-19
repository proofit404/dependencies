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
from _dependencies.objects.shield import _build_shield_spec
from _dependencies.objects.shield import _is_shield
from _dependencies.objects.this import _build_this_spec
from _dependencies.objects.this import _is_this
from _dependencies.objects.value import _build_value_spec
from _dependencies.objects.value import _is_value


def _recursive(builder):
    def wrapper(name, dependency):
        state = builder(name, dependency)
        return _iterate(name, state)

    return wrapper


def _iterate(name, state):
    try:
        dependency = next(state)
        while True:
            spec = _make_dependency_spec(name, dependency)
            dependency = state.send(spec)
    except StopIteration as result:
        return result.value


def _make_dependency_spec(name, dependency):
    for condition, builder in (  # pragma: no branch
        (_is_descriptor, None),
        (_is_enum, None),
        (_is_attributes, _recursive(_build_attributes_spec)),
        (_is_nested_injector, _build_nested_injector_spec),
        (_is_class, _build_class_spec),
        (_is_this, _build_this_spec),
        (_is_package, _recursive(_build_package_spec)),
        (_is_value, _build_value_spec),
        (_is_shield, _recursive(_build_shield_spec)),
        (_is_data, _build_data_spec),
    ):
        if condition(name, dependency):
            return builder(name, dependency)
