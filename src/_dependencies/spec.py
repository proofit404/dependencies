from _dependencies.exceptions import DependencyError


class _Spec:
    def __init__(self, factory, args, required, optional, resolve, is_context):
        _validate_factory(factory)
        _validate_args(args, required, optional)
        _validate_resolve(resolve)
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.resolve = resolve
        self.is_context = is_context

    def resolved(self):
        kind = self.resolve()
        if kind is not None:
            message = f"{kind} dependencies could only be used to instantiate classes"
            raise DependencyError(message)


def _validate_factory(factory):
    if not callable(factory):
        raise RuntimeError


def _validate_args(args, required, optional):
    if not (args.keys() == required ^ optional and not required & optional):
        raise RuntimeError


def _validate_resolve(resolve):
    if not callable(resolve):
        raise RuntimeError
