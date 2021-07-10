from _dependencies.exceptions import DependencyError


class _Spec:
    def __init__(self, factory, args, required, optional, kind, resolvable):
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.kind = kind
        self.resolvable = resolvable

    def resolved(self):
        if not self.resolvable:
            message = (
                f"{self.kind} dependencies could only be used to instantiate classes"
            )
            raise DependencyError(message)
