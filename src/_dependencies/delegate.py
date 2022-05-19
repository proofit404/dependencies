from _dependencies.exceptions import DependencyError


def _setattr_method(cls, attrname, value):
    raise DependencyError("'Injector' modification is not allowed")


def _delattr_method(cls, attrname):
    raise DependencyError("'Injector' modification is not allowed")


class _Delegate:
    def __new__(cls, name, graph, scope):
        def _getattr_method(self, attrname):
            resolved = getattr(scope, attrname)
            graph.get(attrname).resolved()
            return resolved

        methods = {
            "__getattr__": _getattr_method,
            "__setattr__": _setattr_method,
            "__delattr__": _delattr_method,
        }
        return type(name, (), methods)()
