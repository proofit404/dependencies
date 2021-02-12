from functools import wraps

from _dependencies.checks.descriptor import _check_descriptor
from _dependencies.kinds.attributes import _build_attributes_spec
from _dependencies.kinds.attributes import _is_attributes
from _dependencies.kinds.classes import _build_class_spec
from _dependencies.kinds.classes import _is_class
from _dependencies.kinds.nested import _build_nested_injector_spec
from _dependencies.kinds.nested import _is_nested_injector
from _dependencies.kinds.package import _build_package_spec
from _dependencies.kinds.package import _is_package
from _dependencies.kinds.raw import _build_raw_spec
from _dependencies.kinds.raw import _is_raw
from _dependencies.kinds.this import _build_this_spec
from _dependencies.kinds.this import _is_this
from _dependencies.kinds.value import _build_value_spec
from _dependencies.kinds.value import _is_value


def _recursive(builder):
    @wraps(builder)
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
    (_check_descriptor, None),
    (_is_attributes, _recursive(_build_attributes_spec)),
    (_is_nested_injector, _build_nested_injector_spec),
    (_is_class, _build_class_spec),
    (_is_this, _build_this_spec),
    (_is_package, _build_package_spec),
    (_is_value, _build_value_spec),
    (_is_raw, _build_raw_spec),
)


def _make_dependency_spec(name, dependency):
    for condition, builder in conditions:  # pragma: no branch
        if condition(name, dependency):
            return builder(name, dependency)
