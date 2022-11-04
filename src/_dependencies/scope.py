from _dependencies.resolve import _Resolver


class _Scope:
    def __new__(cls, name, graph, initialize):
        def getattr_method(self, attrname):
            return _Resolver(graph, cache, attrname, lambda descriptor: None).resolve()

        instance = type(name, (), {"__getattr__": getattr_method})()
        cache = {"__self__": instance}
        initialize(graph, cache)
        return instance
