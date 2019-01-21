import functools
import inspect

from ._markers import injectable
from ._spec import make_func_spec
from .exceptions import DependencyError


class Operation(object):
    """
    Create callable class appropriated for dependency injection.

    Used as function decorator.
    """

    def __init__(self, function):

        check_class(function)
        self.__function__ = function


def make_operation_spec(dependency):

    function = dependency.__function__
    args, have_defaults = make_func_spec(function, function.__name__)
    check_method(args)
    return injectable, OperationSpec(function), args, have_defaults


class OperationSpec(object):
    def __init__(self, func):

        self.func = func

    def __call__(self, **kwargs):

        return functools.partial(self.func, **kwargs)

    @property
    def __name__(self):

        return self.func.__name__


def check_class(function):

    if inspect.isclass(function):
        raise DependencyError("'operation' decorator can not be used on classes")


def check_method(arguments):

    if "self" in arguments:
        raise DependencyError("'operation' decorator can not be used on methods")
