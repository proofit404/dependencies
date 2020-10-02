from _dependencies.checks.value import _check_class
from _dependencies.checks.value import _check_method
from _dependencies.func import _make_func_spec
from _dependencies.markers import injectable


class Value:
    """Evaluate given function during dependency injection.

    Returned value is used as value of the dependency.

    Used as function decorator.

    """

    def __init__(self, function):

        _check_class(function)
        self.__function__ = function


def _make_value_spec(dependency):

    function = dependency.__function__
    name = function.__name__
    owner = f"{name!r} value"
    args, required, optional = _make_func_spec(function, name, owner)
    _check_method(args)
    return injectable, function, args, required, optional
