from weakref import ref

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
        subclass = type(self.injector.__name__, (self.injector,), _NonEmptyNamespace())
        subclass.__dependencies__.specs["__parent__"] = parent
        return subclass


class _NonEmptyNamespace(dict):
    def __bool__(self):
        return True
