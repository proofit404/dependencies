from _dependencies.scope import _Scope
from _dependencies.spec import _Spec


class _InjectorTypeType(type):
    pass


def _is_nested_injector(name, dependency):
    return isinstance(dependency, _InjectorTypeType)


def _build_nested_injector_spec(name, dependency):
    return _Spec(
        _NestedInjectorFactory(dependency),
        {"__self__": False},
        {"__self__"},
        set(),
        "'Injector'",
        False,
    )


class _NestedInjectorFactory:
    def __init__(self, injector):
        self.injector = injector

    def __call__(self, __self__):
        parent = _Spec(lambda: __self__, {}, set(), set(), "'Injector'", False)
        graph = self.injector.__dependencies__
        graph.specs["__parent__"] = parent
        return _Scope(graph)
