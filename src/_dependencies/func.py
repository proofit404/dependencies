from inspect import getfullargspec

from _dependencies.checks.func import _check_cls_arguments
from _dependencies.checks.func import _check_varargs


def _make_func_spec(func, funcname, owner_message):

    (
        args,
        varargs,
        varkw,
        defaults,
        kwonlyargs,
        kwonlydefaults,
        annotations,
    ) = getfullargspec(func)
    _check_varargs(funcname, varargs, varkw)
    if defaults is not None:
        _check_cls_arguments(args, defaults, owner_message)
        have_defaults = len(args) - len(defaults)
    else:
        have_defaults = len(args)
    return args, have_defaults
