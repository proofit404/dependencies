from _dependencies.exceptions import DependencyError


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
        if not self.graph.get(attrname).resolvable:
            message = "Scalar dependencies could only be used to instantiate classes"
            raise DependencyError(message)
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
        self.state.store(factory(**self.state.kwargs(args)))

    def match(self, args):
        for arg, default in args.items():  # pragma: no branch
            if self.state.should(arg, default):
                self.state.add(arg, default)
                break
