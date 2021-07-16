from _dependencies.exceptions import DependencyError


class _Spec:
    def __init__(self, factory, args, required, optional, resolve):
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.resolve = resolve

    def resolved(self):
        kind = self.resolve()
        if kind is not None:
            message = f"{kind} dependencies could only be used to instantiate classes"
            raise DependencyError(message)
