from _dependencies.analyze import _make_dependency_spec
from _dependencies.exceptions import DependencyError


class _Graph:
    def __init__(self):
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

    def copy(self):
        graph = _Graph()
        graph.update(self)
        return graph


def _check_dunder_name(name):
    if name.startswith("__") and name.endswith("__"):
        raise DependencyError("Magic methods are not allowed")
