import inspect

from _dependencies.exceptions import DependencyError


def check_class(function):

    if inspect.isclass(function):
        raise DependencyError("'operation' decorator can not be used on classes")


def check_method(arguments):

    if "self" in arguments:
        raise DependencyError("'operation' decorator can not be used on methods")
