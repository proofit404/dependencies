from _dependencies.markers import injectable


def make_raw_spec(dependency):

    return injectable, RawSpec(dependency), [], 0


class RawSpec(object):
    def __init__(self, dependency):

        self.dependency = dependency

    def __call__(self):

        return self.dependency
