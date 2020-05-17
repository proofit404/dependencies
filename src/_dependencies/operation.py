# -*- coding: utf-8 -*-
import functools

from _dependencies.checks.operation import _check_class
from _dependencies.checks.operation import _check_method
from _dependencies.func import _make_func_spec
from _dependencies.markers import injectable


class Operation(object):
    """Create callable class appropriated for dependency injection.

    Used as function decorator.

    """

    def __init__(self, function):

        _check_class(function)
        self.__function__ = function


def _make_operation_spec(dependency):

    function = dependency.__function__
    args, have_defaults = _make_func_spec(function, function.__name__, "")
    _check_method(args)
    return injectable, _OperationSpec(function), args, have_defaults


class _OperationSpec(object):
    def __init__(self, func):

        self.func = func

    def __call__(self, **kwargs):

        return functools.partial(self.func, **kwargs)

    @property
    def __name__(self):

        return self.func.__name__
