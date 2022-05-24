from _dependencies.spec import _Spec


def _is_data(name, dependency):
    return True


def _build_data_spec(name, dependency):
    return _Spec(lambda: (dependency, None), {}, set(), set(), lambda: "Scalar", False)
