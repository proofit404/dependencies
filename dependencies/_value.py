import inspect
import itertools

from ._spec import check_varargs
from ._this import random_string
from .exceptions import DependencyError


def value(function):

    if inspect.isclass(function):
        raise DependencyError("'value' decorator can not be used on classes")

    __new__ = make_new(function)
    __init__ = make_init(function)

    return type("Value", (object,), {"__new__": __new__, "__init__": __init__})


def make_new(function):

    argument_names, arguments, scope = make_new_scope(function)
    code = new_template.format(arguments=arguments, argument_names=argument_names)
    exec(code, scope)
    __new__ = scope["__new__"]
    return __new__


def make_init(function):

    argument_names, arguments, scope = make_new_scope(function)
    code = init_template.format(arguments=arguments)
    exec(code, scope)
    __init__ = scope["__init__"]
    return __init__


new_template = """def __new__(self, {arguments}):
    return function({argument_names})
"""


init_template = """def __init__(self, {arguments}):
    pass
"""


def make_new_scope(function):

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


def get_arguments(function):

    names, varargs, kwargs, defaults = get_argument_names(function)
    check_varargs(function.__name__, varargs, kwargs)
    if "self" in names:
        raise DependencyError("'value' decorator can not be used on methods")
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
