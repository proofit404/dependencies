import inspect

from ._markers import injectable
from ._spec import make_func_spec
from .exceptions import DependencyError


# FIXME: Huge duplication with `operation` module.


class Value(object):
    # FIXME: Documentation string.

    def __init__(self, function):

        check_class(function)
        self.__function__ = function


def make_value_spec(dependency):

    function = dependency.__function__
    args, have_defaults = make_func_spec(function, function.__name__)
    check_method(args)
    return injectable, function, args, have_defaults


def check_class(function):

    if inspect.isclass(function):
        raise DependencyError("'value' decorator can not be used on classes")


def check_method(arguments):

    if "self" in arguments:
        raise DependencyError("'value' decorator can not be used on methods")
