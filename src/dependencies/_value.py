from ._checks.value import check_class, check_method
from ._func import make_func_spec
from ._markers import injectable


class Value(object):
    """
    Evaluate given function during dependency injection.

    Returned value is used as value of the dependency.

    Used as function decorator.
    """

    def __init__(self, function):

        check_class(function)
        self.__function__ = function


def make_value_spec(dependency):

    function = dependency.__function__
    args, have_defaults = make_func_spec(function, function.__name__)
    check_method(args)
    return injectable, function, args, have_defaults
