from _dependencies.resolve import _Resolver


class _IsScope:
    pass


class _Scope:
    def __new__(cls, graph):
        def getattr_method(self, attrname):
            return _Resolver(graph, cache, attrname).resolve()

        instance = type(cls.__name__, (_IsScope,), {"__getattr__": getattr_method})()
        cache = {"__self__": instance}
        return instance
