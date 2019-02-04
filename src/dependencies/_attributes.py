class Replace(Exception):
    def __init__(self, dependency, attrs):
        self.dependency = dependency
        self.attrs = attrs


class Attributes(object):
    def __init__(self, spec, attrs):

        self.spec = spec
        self.attrs = attrs

    def __call__(self, **kwargs):

        result = self.spec(**kwargs)

        for attr in self.attrs:
            result = getattr(result, attr)

        return result
