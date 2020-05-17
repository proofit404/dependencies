# -*- coding: utf-8 -*-
from _dependencies.checks.value import _check_class
from _dependencies.checks.value import _check_method
from _dependencies.func import _make_func_spec
from _dependencies.markers import injectable


class Value(object):
    """Evaluate given function during dependency injection.

    Returned value is used as value of the dependency.

    Used as function decorator.

    """

    def __init__(self, function):

        _check_class(function)
        self.__function__ = function


def _make_value_spec(dependency):

    function = dependency.__function__
    args, have_defaults = _make_func_spec(function, function.__name__, "")
    _check_method(args)
    return injectable, function, args, have_defaults
