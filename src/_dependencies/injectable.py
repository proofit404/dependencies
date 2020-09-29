from inspect import signature

from _dependencies.checks.func import _check_argument_default
from _dependencies.checks.func import _check_varargs


def _function_args(func, funcname, owner):
    arguments = _args(func, funcname, owner)
    return _separate(arguments)


def _method_args(func, funcname, owner):
    arguments = _args(func, funcname, owner)
    return _separate(arguments[1:])


def _args(func, funcname, owner):
    args = []
    varargs = kwargs = None
    for name, param in signature(func).parameters.items():
        have_default = param.default is not param.empty
        args.append((name, have_default))
        if have_default:
            _check_argument_default(name, param.default, owner)
        if param.kind is param.VAR_POSITIONAL:
            varargs = True
        if param.kind is param.VAR_KEYWORD:
            kwargs = True
    _check_varargs(funcname, varargs, kwargs)
    return args


def _separate(arguments):
    args = {}
    required = set()
    optional = set()
    for name, have_default in arguments:
        args[name] = have_default
        target = optional if have_default else required
        target.add(name)
    return args, required, optional
