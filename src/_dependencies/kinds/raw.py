from _dependencies.spec import _Spec


def _is_raw(name, dependency):
    return True


def _build_raw_spec(name, dependency):
    return _Spec(lambda: dependency, {}, set(), set())
