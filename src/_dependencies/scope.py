from _dependencies.exceptions import DependencyError
from _dependencies.resolve import _Resolver


def _setattr_method(cls, attrname, value):
    raise DependencyError("'Injector' modification is not allowed")


def _delattr_method(cls, attrname):
    raise DependencyError("'Injector' modification is not allowed")


class _Scope:
    def __new__(cls, name, graph, initialize):
        def _getattr_method(self, attrname):
            return _Resolver(graph, cache, attrname, lambda descriptor: None).resolve()

        instance = type(
            name,
            (),
            {
                "__getattr__": _getattr_method,
                "__setattr__": _setattr_method,
                "__delattr__": _delattr_method,
            },
        )()
        cache = {"__self__": instance}
        initialize(graph, cache)
        return instance
