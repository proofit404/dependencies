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
        message = _Trace(self.state)
        message.add(f"Can not resolve attribute {self.state.current!r}")
        raise DependencyError(message)

    def create(self, factory, args):
        try:
            self.state.store(factory(**self.state.kwargs(args)))
        except DependencyError as error:
            message = _Trace(self.state)
            message.add(error)
            raise DependencyError(message)

    def match(self, args):
        for arg, have_default in args.items():  # pragma: no branch
            if self.state.should(arg, have_default):
                self.state.add(arg, have_default)
                break


class _Trace:
    def __init__(self, state):
        name = state.cache["__self__"].__class__.__name__
        self.attributes = [
            f"{name}.{attrname}" for attrname, have_default in state.stack
        ]
        self.attributes.append(f"{name}.{state.current}")

    def __str__(self):
        indentation = _Indentation()
        return self.error + ":\n\n" + "\n".join(map(indentation, self.attributes))

    def add(self, error):
        if isinstance(error, DependencyError):
            message = error.args[0]
            if isinstance(message, _Trace):
                self.error = message.error
                self.attributes.extend(message.attributes)
            else:
                self.error = message
        else:
            self.error = error


class _Indentation:
    def __init__(self):
        self.index = 0

    def __call__(self, arg):
        result = "  " * self.index + arg
        self.index += 1
        return result
