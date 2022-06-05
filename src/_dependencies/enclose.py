from _dependencies.resolve import _Resolver


class _Enclose:
    def __init__(self):
        self.callbacks = []

    def add(self, function):
        if function is not None:
            self.callbacks.insert(0, function)

    def before(self, graph, cache):
        for context in graph.contexts:
            _Resolver(graph, cache, context, self.add).resolve()

    def after(self):
        for callback in self.callbacks:
            callback()
