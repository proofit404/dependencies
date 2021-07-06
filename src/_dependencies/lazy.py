from _dependencies.graph import _Graph


class _LazyGraph:
    def __init__(self, attrname, namespace):
        self.attrname = attrname
        self.namespace = namespace

    def __get__(self, instance, owner):
        graph = _Graph()
        for base in reversed(owner.__bases__):
            graph.update(base.__dependencies__)
        for name, dependency in self.namespace.items():
            graph.assign(name, dependency)
        type.__setattr__(owner, self.attrname, graph)
        return graph
