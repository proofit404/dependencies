from inspect import isclass
from inspect import isgeneratorfunction

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


def _is_context(function):
    return isgeneratorfunction(function)


def _build_value_spec(name, dependency):
    function = dependency.__function__
    name = function.__name__
    owner = f"{name!r} value"
    args, required, optional = _function_args(function, name, owner)
    _check_method(args)
    if _is_context(function):
        factory = _ContextFactory(function)
        is_context = True
    else:
        factory = _ValueFactory(function)
        is_context = False
    return _Spec(factory, args, required, optional, lambda: "'value'", is_context)


class _ValueFactory:
    def __init__(self, function):
        self.function = function

    def __call__(self, **kwargs):
        return self.function(**kwargs), None


class _ContextFactory:
    def __init__(self, function):
        self.function = function

    def __call__(self, **kwargs):
        generator = self.function(**kwargs)
        return next(generator), _Finalizer(generator)


class _Finalizer:
    def __init__(self, generator):
        self.generator = generator

    def __call__(self):
        try:
            next(self.generator)
        except StopIteration:
            pass


def _check_class(function):
    if isclass(function):
        raise DependencyError("'value' decorator can not be used on classes")


def _check_method(arguments):
    if "self" in arguments:
        raise DependencyError("'value' decorator can not be used on methods")
