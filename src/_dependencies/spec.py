class _Spec:
    def __init__(self, factory, args, required, optional, resolvable=True):
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.resolvable = resolvable
