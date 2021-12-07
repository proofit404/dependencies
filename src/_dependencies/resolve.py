from _dependencies.exceptions import DependencyError
from _dependencies.state import _State


class _Resolver:
    def __init__(self, graph, cache, attrname):
        self.graph = graph
        self.state = _State(cache, attrname)
        self.attrname = attrname

    def resolve(self):
        while self.attrname not in self.state.cache:
            spec = self.graph.get(self.state.current)
            if self.is_optional(spec):
                continue
            if self.state.resolved(spec.required, spec.optional):
                self.create(spec.factory, spec.args)
            else:
                self.match(spec.args)
        return self.state.cache[self.attrname]

    def is_optional(self, spec):
        if spec is not None:
            return False
        if self.state.have_default:
            self.state.pop()
            return True
        message = f"Can not resolve attribute {self.state.current!r}:\n\n{self.state!r}"
        raise DependencyError(message)

    def create(self, factory, args):
        self.state.store(factory(**self.state.kwargs(args)))

    def match(self, args):
        for arg, have_default in args.items():  # pragma: no branch
            if self.state.should(arg, have_default):
                self.state.add(arg, have_default)
                break
