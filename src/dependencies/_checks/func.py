import inspect

from ..exceptions import DependencyError


def check_cls_arguments(argnames, defaults):

    for name, value in zip(reversed(argnames), reversed(defaults)):
        expect_class = name.endswith("_class")
        is_class = inspect.isclass(value)
        if expect_class and not is_class:
            message = "{0!r} default value should be a class"
            raise DependencyError(message.format(name))
        if not expect_class and is_class:
            message = "{0!r} argument can not have class as its default value"
            raise DependencyError(message.format(name))


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
