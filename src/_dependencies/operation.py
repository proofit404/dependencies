from functools import partial

from _dependencies.checks.operation import _check_class
from _dependencies.checks.operation import _check_method
from _dependencies.func import _make_func_spec
from _dependencies.markers import injectable


class Operation:
    """Create callable class appropriated for dependency injection.

    Used as function decorator.

    """

    def __init__(self, function):

        _check_class(function)
        self.__function__ = function


def _make_operation_spec(dependency):

    function = dependency.__function__
    name = function.__name__
    owner = f"{name!r} operation"
    args, required, optional = _make_func_spec(function, name, owner)
    _check_method(args)
    return injectable, _OperationSpec(function), args, required, optional


class _OperationSpec:
    def __init__(self, func):

        self.func = func

    def __call__(self, **kwargs):

        return partial(self.func, **kwargs)

    @property
    def __name__(self):

        return self.func.__name__
