import inspect

from _dependencies.checks.func import check_cls_arguments
from _dependencies.checks.func import check_varargs


if getattr(inspect, "signature", None):

    def make_func_spec(func, funcname, owner_message):

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
        check_varargs(funcname, varargs, kwargs)
        if defaults:
            check_cls_arguments(args, defaults, owner_message)
        return args, have_defaults


else:

    def make_func_spec(func, funcname, owner_message):

        args, varargs, kwargs, defaults = inspect.getargspec(func)
        check_varargs(funcname, varargs, kwargs)
        if defaults is not None:
            check_cls_arguments(args, defaults, owner_message)
            have_defaults = len(args) - len(defaults)
        else:
            have_defaults = len(args)
        return args, have_defaults
