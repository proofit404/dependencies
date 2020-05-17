# -*- coding: utf-8 -*-
import inspect

from _dependencies.checks.func import _check_cls_arguments
from _dependencies.checks.func import _check_varargs


if getattr(inspect, "signature", None):

    def _make_func_spec(func, funcname, owner_message):

        signature = inspect.signature(func)
        parameters = iter(signature.parameters.items())
        args, defaults = [], []
        varargs = kwargs = None
        have_defaults = 0
        for name, param in parameters:
            args.append(name)
            if param.default is not param.empty:
                defaults.append(param.default)
            else:
                have_defaults += 1
            if param.kind is param.VAR_POSITIONAL:
                varargs = True
            if param.kind is param.VAR_KEYWORD:
                kwargs = True
        _check_varargs(funcname, varargs, kwargs)
        if defaults:
            _check_cls_arguments(args, defaults, owner_message)
        return args, have_defaults


else:

    def _make_func_spec(func, funcname, owner_message):

        args, varargs, kwargs, defaults = inspect.getargspec(func)
        _check_varargs(funcname, varargs, kwargs)
        if defaults is not None:
            _check_cls_arguments(args, defaults, owner_message)
            have_defaults = len(args) - len(defaults)
        else:
            have_defaults = len(args)
        return args, have_defaults
