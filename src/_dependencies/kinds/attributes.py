from _dependencies.spec import _Spec


class _Attributes:
    def __init__(self, origin, attrs):
        self.origin = origin
        self.attrs = attrs


def _is_attributes(name, dependency):
    return isinstance(dependency, _Attributes)


def _build_attributes_spec(name, dependency):
    origin_spec = yield dependency.origin
    return _Spec(
        _AttributesFactory(origin_spec.factory, dependency.attrs),
        origin_spec.args,
        origin_spec.required,
        origin_spec.optional,
    )


class _AttributesFactory:
    def __init__(self, factory, attrs):
        self.factory = factory
        self.attrs = attrs

    def __call__(self, **kwargs):
        __tracebackhide__ = True
        result = self.factory(**kwargs)
        for attr in self.attrs:
            result = getattr(result, attr)
        return result
