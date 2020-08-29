class _Replace(Exception):
    def __init__(self, dependency, attrs):
        self.dependency = dependency
        self.attrs = attrs


class _Attributes:
    def __init__(self, spec, attrs):

        self.spec = spec
        self.attrs = attrs

    def __call__(self, **kwargs):
        __tracebackhide__ = True

        result = self.spec(**kwargs)

        for attr in self.attrs:
            result = getattr(result, attr)

        return result

    @property
    def __name__(self):

        return self.spec.__name__

    @property
    def __dependencies__(self):

        return self.spec.__dependencies__
