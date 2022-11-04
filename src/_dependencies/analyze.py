from _dependencies.objects.classes import _build_class_spec
from _dependencies.objects.classes import _is_class
from _dependencies.objects.data import _build_data_spec
from _dependencies.objects.data import _is_data
from _dependencies.objects.descriptor import _is_descriptor
from _dependencies.objects.enum import _is_enum
from _dependencies.objects.nested import _is_nested_injector
from _dependencies.objects.shield import _build_shield_spec
from _dependencies.objects.shield import _is_shield
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
        (_is_nested_injector, None),
        (_is_class, _build_class_spec),
        (_is_value, _build_value_spec),
        (_is_shield, _recursive(_build_shield_spec)),
        (_is_data, _build_data_spec),
    ):
        if condition(name, dependency):
            return builder(name, dependency)
