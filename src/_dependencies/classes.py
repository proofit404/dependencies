from _dependencies.func import _make_method_spec
from _dependencies.markers import injectable


def _make_init_spec(dependency):

    if _using_object_init(dependency):
        return injectable, dependency, {}, set(), set()
    else:
        name = dependency.__name__ + "." + "__init__"
        owner = f"{dependency.__name__!r} class"
        args, required, optional = _make_method_spec(dependency.__init__, name, owner)
        return injectable, dependency, args, required, optional


def _using_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False
