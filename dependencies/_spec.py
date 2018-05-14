import inspect

from .exceptions import DependencyError


class Marker(object):

    def __bool__(self):

        return False

    __nonzero__ = __bool__


nested_injector = Marker()


def use_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True

        elif "__init__" in base.__dict__:
            return False


try:
    inspect.signature
except AttributeError:

    def make_init_spec(dependency):

        argspec = inspect.getargspec(dependency.__init__)
        args, varargs, kwargs, defaults = argspec
        check_varargs(constructor_name(dependency), varargs, kwargs)
        if defaults is not None:
            check_cls_arguments(args, defaults)
            have_defaults = len(args) - len(defaults)
        else:
            have_defaults = len(args)
        spec = args[1:], have_defaults
        return spec


else:

    def make_init_spec(dependency):

        signature = inspect.signature(dependency.__init__)
        parameters = iter(signature.parameters.items())
        next(parameters)
        args, defaults = [], []
        varargs = kwargs = None
        have_defaults = 1
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
        check_varargs(constructor_name(dependency), varargs, kwargs)
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
