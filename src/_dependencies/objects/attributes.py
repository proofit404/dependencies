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
        _AttributesResolve(origin_spec.factory, dependency.attrs, origin_spec.resolve),
        False,
    )


class _AttributesFactory:
    def __init__(self, factory, attrs):
        self.factory = factory
        self.attrs = attrs

    def __call__(self, **kwargs):
        result, destructor = self.factory(**kwargs)
        for attr in self.attrs:
            result = getattr(result, attr)
        return result, destructor


class _AttributesResolve:
    def __init__(self, factory, attrs, resolve):
        self.factory = factory
        self.attrs = attrs
        self.resolve = resolve

    def __call__(self):
        resolved = self.resolve()
        is_nested = resolved == "'Injector'"
        if is_nested and self.attrs:
            return self.factory.injector.__dependencies__.get(self.attrs[0]).resolve()
        return resolved
