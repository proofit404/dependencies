from weakref import ref

from _dependencies.markers import injectable
from _dependencies.markers import nested_injector


def _make_nested_injector_spec(dependency):

    return (
        nested_injector,
        _NestedInjectorSpec(dependency),
        {"__self__": False},
        {"__self__"},
        set(),
    )


class _NestedInjectorSpec:
    def __init__(self, injector):

        self.injector = injector

    def __call__(self, __self__):

        subclass = type(self.injector.__name__, (self.injector,), _NonEmptyNamespace())
        parent = injectable, ref(__self__), {}, set(), set()
        subclass.__dependencies__["__parent__"] = parent
        return subclass

    @property
    def __dependencies__(self):

        return self.injector.__dependencies__


class _NonEmptyNamespace(dict):
    def __bool__(self):
        return True
