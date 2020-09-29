from _dependencies.analyze import _make_dependency_spec
from _dependencies.checks.injector import _check_dunder_name


class _Graph:
    def __init__(self, in_class):
        self.in_class = in_class
        self.specs = {}

    def get(self, name):
        return self.specs.get(name)

    def assign(self, name, dependency):
        _check_dunder_name(name)
        self.specs[name] = _make_dependency_spec(name, dependency)

    def has(self, name):
        return name in self.specs

    def update(self, graph):
        self.specs.update(graph.specs)
