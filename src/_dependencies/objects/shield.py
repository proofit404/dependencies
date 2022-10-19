from _dependencies.spec import _Spec


class Shield:
    """Pass positional and keyword arguments based on spec."""

    def __init__(self, callback, *args):
        self.callback = callback
        self.args = args


shield = Shield


def _is_shield(name, dependency):
    return isinstance(dependency, Shield)


def _build_shield_spec(name, dependency):
    varargs_factories = []
    spec_args = {}
    spec_required = set()
    spec_optional = set()
    for vararg in dependency.args:
        vararg_spec = yield vararg
        varargs_factories.append(vararg_spec.factory)
        spec_args.update(vararg_spec.args)
        spec_required |= vararg_spec.required
        spec_optional |= vararg_spec.optional
    factory = _ShieldFactory(dependency.callback, varargs_factories)
    return _Spec(factory, spec_args, spec_required, spec_optional, lambda: None, False)


class _ShieldFactory:
    def __init__(self, callback, args_factories):
        self.callback = callback
        self.args_factories = args_factories

    def __call__(self, **kwargs):
        args = []
        for factory in self.args_factories:
            arg, destructor = factory(**kwargs)
            args.append(arg)
        return self.callback(*args), None
