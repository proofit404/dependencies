import functools

from ._checks.operation import check_class, check_method
from ._func import make_func_spec
from ._markers import injectable


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
