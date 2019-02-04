from ._func import make_func_spec
from ._markers import injectable


def make_init_spec(dependency):

    if using_object_init(dependency):
        return injectable, dependency, [], 0
    else:
        name = dependency.__name__ + "." + "__init__"
        args, have_defaults = make_func_spec(dependency.__init__, name)
        return injectable, dependency, args[1:], have_defaults


def using_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False
