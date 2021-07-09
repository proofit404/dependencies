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
        if self.state.full():
            message = "Can not resolve attribute {!r} while building {!r}".format(
                self.state.current, self.state.stack.pop()[0]
            )
        else:
            message = f"Can not resolve attribute {self.state.current!r}"
        raise DependencyError(message)

    def create(self, factory, args):
        self.state.store(factory(**self.state.kwargs(args)))

    def match(self, args):
        for arg, default in args.items():  # pragma: no branch
            if self.state.should(arg, default):
                self.state.add(arg, default)
                break
