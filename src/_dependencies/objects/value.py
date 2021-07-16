from inspect import isclass

from _dependencies.exceptions import DependencyError
from _dependencies.injectable import _function_args
from _dependencies.spec import _Spec


class Value:
    """Evaluate given function during dependency injection.

    Returned value is used as value of the dependency.

    Used as function decorator.

    """

    def __init__(self, function):
        _check_class(function)
        self.__function__ = function


value = Value


def _is_value(name, dependency):
    return isinstance(dependency, Value)


def _build_value_spec(name, dependency):
    function = dependency.__function__
    name = function.__name__
    owner = f"{name!r} value"
    args, required, optional = _function_args(function, name, owner)
    _check_method(args)
    return _Spec(function, args, required, optional, lambda: "'value'")


def _check_class(function):
    if isclass(function):
        raise DependencyError("'value' decorator can not be used on classes")


def _check_method(arguments):
    if "self" in arguments:
        raise DependencyError("'value' decorator can not be used on methods")
