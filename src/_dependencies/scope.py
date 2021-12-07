from _dependencies.resolve import _Resolver


class _IsScope:
    pass


class _Scope:
    def __new__(cls, name, graph):
        def getattr_method(self, attrname):
            return _Resolver(graph, cache, attrname).resolve()

        instance = type(name, (_IsScope,), {"__getattr__": getattr_method})()
        cache = {"__self__": instance}
        return instance
