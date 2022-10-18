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
    callback = dependency.callback
    factory = _ShieldFactory(callback)
    return _Spec(factory, {}, set(), set(), lambda: None, False)


class _ShieldFactory:
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, **kwargs):
        return self.callback(**kwargs), None
