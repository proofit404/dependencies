from _dependencies.exceptions import DependencyError
from _dependencies.replace import _Replace


class _Resolver:
    def __init__(self, injector, state):
        self.injector = injector
        self.graph = injector.__dependencies__
        self.state = state

    def resolve(self, attrname):
        while attrname not in self.state.cache:
            spec = self.graph.get(self.state.current)
            if self.is_optional(spec):
                continue
            if self.state.resolved(spec.required, spec.optional):
                self.create(spec.factory, spec.args)
            else:
                self.match(spec.args)
        return self.state.cache[attrname]

    def is_optional(self, spec):
        if spec is not None:
            return False
        if self.state.have_default:
            self.state.pop()
            return True
        if self.state.full():
            message = "{!r} can not resolve attribute {!r} while building {!r}".format(
                self.injector.__name__, self.state.current, self.state.stack.pop()[0]
            )
        else:
            message = "{!r} can not resolve attribute {!r}".format(
                self.injector.__name__, self.state.current
            )
        raise DependencyError(message)

    def create(self, factory, args):
        try:
            self.state.store(factory(**self.state.kwargs(args)))
        except _Replace as replace:
            self.replace(replace.dependency)

    def match(self, args):
        for arg, default in args.items():  # pragma: no branch
            if self.state.should(arg, default):
                self.state.add(arg, default)
                break

    def replace(self, dependency):
        for injector in self.injector.__mro__:  # pragma: no branch
            if injector.__dependencies__.has(self.state.current):
                injector.__dependencies__.assign(self.state.current, dependency)
            else:
                break
