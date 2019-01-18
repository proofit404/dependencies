import inspect

from ._spec import make_func_spec
from .exceptions import DependencyError


# FIXME: Duplication with `operation` module.


class Value(object):
    # FIXME: Documentation string.

    def __init__(self, function):

        check_class(function)
        arguments, have_defaults = make_func_spec(function, function.__name__)
        check_method(arguments)

        self.__function__ = function
        self.__arguments__ = arguments
        self.__have_defaults__ = have_defaults


def resolve_value_mark(value, injector):

    # FIXME: Reuse `Injector` cache.  Don't build arguments them self.
    arguments = {}
    for num, arg in enumerate(value.__arguments__):
        if arg not in injector and num >= value.__have_defaults__:
            continue
        arguments[arg] = getattr(injector, arg)
    return value.__function__(**arguments)


def check_class(function):

    if inspect.isclass(function):
        raise DependencyError("'value' decorator can not be used on classes")


def check_method(arguments):

    if "self" in arguments:
        raise DependencyError("'value' decorator can not be used on methods")
