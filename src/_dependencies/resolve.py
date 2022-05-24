from _dependencies.exceptions import DependencyError
from _dependencies.state import _State
from _dependencies.trace import _Trace


class _Resolver:
    def __init__(self, graph, cache, attrname, remember):
        self.graph = graph
        self.state = _State(cache, attrname)
        self.attrname = attrname
        self.remember = remember

    def resolve(self):
        try:
            return self.find()
        except RecursionError:
            message = _Trace(self.state)
            message.add("Circle error found in definition of the dependency graph")
            raise DependencyError(message) from None

    def find(self):
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
        message = _Trace(self.state)
        message.add(f"Can not resolve attribute {self.state.current!r}")
        raise DependencyError(message)

    def create(self, factory, args):
        try:
            result, destructor = factory(**self.state.kwargs(args))
            self.state.store(result)
            self.remember(destructor)
        except DependencyError as error:
            message = _Trace(self.state)
            message.add(error)
            raise DependencyError(message) from None

    def match(self, args):
        for arg, have_default in args.items():  # pragma: no branch
            if self.state.should(arg, have_default):
                self.state.add(arg, have_default)
                break
