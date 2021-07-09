from weakref import ref

from _dependencies.pointer import _Pointer
from _dependencies.resolve import _Resolver
from _dependencies.spec import _Spec


class _InjectorTypeType(type):
    pass


def _is_nested_injector(name, dependency):
    return isinstance(dependency, _InjectorTypeType)


def _build_nested_injector_spec(name, dependency):
    return _Spec(
        _NestedInjectorFactory(dependency), {"__self__": False}, {"__self__"}, set()
    )


class _NestedInjectorFactory:
    def __init__(self, injector):
        self.injector = injector

    def __call__(self, __self__):
        parent = _Spec(ref(__self__), {}, set(), set())
        graph = self.injector.__dependencies__
        graph.specs["__parent__"] = parent
        pointer = _Pointer()
        cache = {"__self__": pointer}
        pointer.resolver = _Resolver(graph, cache, None)
        return pointer
