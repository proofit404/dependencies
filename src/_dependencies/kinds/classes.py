from inspect import isclass

from _dependencies.injectable import _method_args
from _dependencies.spec import _Spec


def _is_class(name, dependency):
    return isclass(dependency) and not name.endswith("_class")


def _build_class_spec(name, dependency):
    if _using_object_init(dependency):
        return _Spec(dependency, {}, set(), set())
    else:
        name = dependency.__name__ + "." + "__init__"
        owner = f"{dependency.__name__!r} class"
        args, required, optional = _method_args(dependency.__init__, name, owner)
        return _Spec(dependency, args, required, optional)


def _using_object_init(cls):
    for base in cls.__mro__:  # pragma: no branch
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False
