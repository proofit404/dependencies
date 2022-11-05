from inspect import isclass

from _dependencies.injectable import _method_args
from _dependencies.spec import _Spec


def _is_class(name, dependency):
    return isclass(dependency) and not name.endswith("_class")


def _build_class_spec(name, dependency):
    if _using_object_init(dependency):
        return _Spec(_ClassFactory(dependency), {}, set(), set(), False)
    else:
        name = dependency.__name__ + "." + "__init__"
        owner = f"{dependency.__name__!r} class"
        args, required, optional = _method_args(dependency.__init__, name, owner)
        return _Spec(_ClassFactory(dependency), args, required, optional, False)


def _using_object_init(cls):
    for base in cls.__mro__:  # pragma: no branch
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False


class _ClassFactory:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, **kwargs):
        return self.cls(**kwargs), None
