import weakref

from _dependencies.markers import injectable
from _dependencies.markers import nested_injector


def make_nested_injector_spec(dependency):

    return nested_injector, NestedInjectorSpec(dependency), ["__self__"], 0


class NestedInjectorSpec(object):
    def __init__(self, injector):

        self.injector = injector

    def __call__(self, __self__):

        subclass = type(self.injector.__name__, (self.injector,), {})
        parent = injectable, weakref.ref(__self__), [], 0
        subclass.__dependencies__["__parent__"] = parent
        return subclass

    @property
    def __dependencies__(self):

        return self.injector.__dependencies__
