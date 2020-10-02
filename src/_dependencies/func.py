from inspect import signature

from _dependencies.checks.func import _check_argument_default
from _dependencies.checks.func import _check_varargs


def _make_callable_spec(func, funcname, owner):
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


def _split_argument_spec(arguments):
    args = {}
    required = set()
    optional = set()
    for name, have_default in arguments:
        args[name] = have_default
        target = optional if have_default else required
        target.add(name)
    return args, required, optional


def _make_func_spec(func, funcname, owner):
    arguments = _make_callable_spec(func, funcname, owner)
    return _split_argument_spec(arguments)


def _make_method_spec(func, funcname, owner):
    arguments = _make_callable_spec(func, funcname, owner)
    return _split_argument_spec(arguments[1:])
