from functools import partial

from _dependencies.checks.operation import _check_class
from _dependencies.checks.operation import _check_method
from _dependencies.injectable import _function_args
from _dependencies.spec import _Spec


class Operation:
    """Create callable class appropriated for dependency injection.

    Used as function decorator.

    """

    def __init__(self, function):
        _check_class(function)
        self.__function__ = function


def _is_operation(name, dependency):
    return isinstance(dependency, Operation)


def _build_operation_spec(name, dependency):
    function = dependency.__function__
    name = function.__name__
    owner = f"{name!r} operation"
    args, required, optional = _function_args(function, name, owner)
    _check_method(args)
    return _Spec(_OperationFactory(function), args, required, optional)


class _OperationFactory:
    def __init__(self, func):
        self.func = func

    def __call__(self, **kwargs):
        return partial(self.func, **kwargs)
