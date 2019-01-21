import inspect

from ._markers import injectable, nested_injector
from .exceptions import DependencyError


def make_init_spec(dependency):

    if use_object_init(dependency):
        return injectable, dependency, [], 0
    else:
        name = constructor_name(dependency)
        args, have_defaults = make_func_spec(dependency.__init__, name)
        return injectable, dependency, args[1:], have_defaults


def make_nested_injector_spec(dependency):

    return nested_injector, dependency, None, None


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


def check_cls_arguments(argnames, defaults):

    for name, value in zip(reversed(argnames), reversed(defaults)):
        expect_class = name.endswith("_class")
        is_class = inspect.isclass(value)
        if expect_class and not is_class:
            raise DependencyError("{0!r} default value should be a class".format(name))
        if not expect_class and is_class:
            raise DependencyError(
                "{0!r} argument can not have class as its default value".format(name)
            )


def check_varargs(name, varargs, kwargs):

    if varargs and kwargs:
        message = "{0} have arbitrary argument list and keyword arguments"
        raise DependencyError(message.format(name))
    elif varargs:
        message = "{0} have arbitrary argument list"
        raise DependencyError(message.format(name))
    elif kwargs:
        message = "{0} have arbitrary keyword arguments"
        raise DependencyError(message.format(name))


def constructor_name(dependency):

    return dependency.__name__ + ".__init__"
