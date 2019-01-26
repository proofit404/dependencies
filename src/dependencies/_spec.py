import inspect

from ._checks.spec import check_cls_arguments, check_varargs
from ._markers import injectable


def make_init_spec(dependency):

    if use_object_init(dependency):
        return injectable, dependency, [], 0
    else:
        name = dependency.__name__ + "." + "__init__"
        args, have_defaults = make_func_spec(dependency.__init__, name)
        return injectable, dependency, args[1:], have_defaults


def use_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False


try:
    inspect.signature
except AttributeError:

    def make_func_spec(func, funcname):

        args, varargs, kwargs, defaults = inspect.getargspec(func)
        check_varargs(funcname, varargs, kwargs)
        if defaults is not None:
            check_cls_arguments(args, defaults)
            have_defaults = len(args) - len(defaults)
        else:
            have_defaults = len(args)
        return args, have_defaults


else:

    def make_func_spec(func, funcname):

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
            check_cls_arguments(args, defaults)
        return args, have_defaults
