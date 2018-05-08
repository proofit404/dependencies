import inspect
import itertools

from ._spec import check_varargs
from ._this import random_string
from .exceptions import DependencyError


def operation(function):
    """
    Create callable class appropriated for dependency injection.

    Used as function decorator.
    """

    if inspect.isclass(function):
        raise DependencyError("'operation' decorator can not be used on classes")

    class OperationType(type):

        def __repr__(cls):
            return "<class Operation[" + function.__name__ + "]>"

    __init__ = make_init(function)

    return OperationType(
        "Operation",
        (object,),
        {"__init__": __init__, "__call__": __call__, "__repr__": __repr__},
    )


def make_init(function):

    argument_names, arguments, scope = make_init_scope(function)
    code = init_template.format(arguments=arguments, argument_names=argument_names)
    exec(code, scope)
    __init__ = scope["__init__"]
    return __init__


init_template = """def __init__(self, {arguments}):
    self.__function__ = function
    self.__arguments__ = [{argument_names}]
"""


def make_init_scope(function):

    names, defaults = get_arguments(function)
    stubs = itertools.repeat(None, len(names) - len(defaults))
    keys = [random_string() for each in defaults]

    argument_names = ", ".join(names)

    arguments = ", ".join(
        arg + "=" + key if key is not None else arg
        for arg, key in zip(names, itertools.chain(stubs, keys))
    )

    scope = {"function": function}
    scope.update(zip(keys, defaults))
    return argument_names, arguments, scope


def __call__(self):

    return self.__function__(*self.__arguments__)


def __repr__(self):

    return "<Operation[" + self.__function__.__name__ + "] object>"


def get_arguments(function):

    names, varargs, kwargs, defaults = get_argument_names(function)
    check_varargs(function.__name__, varargs, kwargs)
    if "self" in names:
        raise DependencyError("'operation' decorator can not be used on methods")
    defaults = defaults or []
    return names, defaults


try:
    inspect.signature
except AttributeError:

    get_argument_names = inspect.getargspec

else:

    def get_argument_names(function):

        signature = inspect.signature(function)
        args = [name for name, param in signature.parameters.items()]
        varargs = any(
            param.kind is param.VAR_POSITIONAL
            for name, param in signature.parameters.items()
        )
        kwargs = any(
            param.kind is param.VAR_KEYWORD
            for name, param in signature.parameters.items()
        )
        defaults = [
            param.default
            for name, param in signature.parameters.items()
            if param.default is not param.empty
        ]
        return args, varargs, kwargs, defaults
