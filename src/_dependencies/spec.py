class _Spec:
    def __init__(self, factory, args, required, optional, kind=None, resolvable=True):
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.kind = kind
        self.resolvable = resolvable
