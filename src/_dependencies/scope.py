from _dependencies.resolve import _Resolver


class _Scope:
    def __init__(self, graph):
        self.graph = graph
        self.cache = {"__self__": self}

    def __getattr__(self, attrname):
        return _Resolver(self.graph, self.cache, attrname).resolve()
