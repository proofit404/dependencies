class _Spec:
    def __init__(self, factory, args, required, optional, is_context):
        _validate_factory(factory)
        _validate_args(args, required, optional)
        _validate_context(is_context)
        self.factory = factory
        self.args = args
        self.required = required
        self.optional = optional
        self.is_context = is_context


def _validate_factory(factory):
    if not callable(factory):
        raise RuntimeError


def _validate_args(args, required, optional):
    if not (args.keys() == required ^ optional and not required & optional):
        raise RuntimeError


def _validate_context(is_context):
    if not isinstance(is_context, bool):
        raise RuntimeError
