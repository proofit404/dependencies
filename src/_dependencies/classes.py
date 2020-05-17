# -*- coding: utf-8 -*-
from _dependencies.func import _make_func_spec
from _dependencies.markers import injectable


def _make_init_spec(dependency):

    if _using_object_init(dependency):
        return injectable, dependency, [], 0
    else:
        name = dependency.__name__ + "." + "__init__"
        owner_message = "{cls!r} class".format(cls=dependency.__name__)
        args, have_defaults = _make_func_spec(dependency.__init__, name, owner_message)
        return injectable, dependency, args[1:], have_defaults


def _using_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False
